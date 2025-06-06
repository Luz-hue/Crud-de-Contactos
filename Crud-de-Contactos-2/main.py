import re  # Importa el módulo de expresiones regulares para validar entradas.
import flet as ft  # Importa Flet para construir la interfaz de usuario.
from contact_manager import ContactManager  # Importa el manejador de contactos.
from fpdf import FPDF  # Importa FPDF para la generación de PDFs.
import pandas as pd  # Importa pandas para la manipulación de datos.
import datetime  # Importa datetime para manejar fechas y horas.

# Clase que define el encabezado y pie de página de un PDF.
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)  # Establece la fuente para el encabezado.
        self.cell(0, 10, 'Tabla de Datos', 0, 1, 'C')  # Añade el título en el centro.

    def footer(self):
        self.set_y(-15)  # Posiciona el pie de página.
        self.set_font('Arial', 'I', 8)  # Establece la fuente para el pie de página.
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')  # Añade el número de página.

# Clase que define la interfaz de usuario del formulario.
class FormUi(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)  # Llama al constructor de la clase base.
        self.page = page  # Guarda la referencia a la página.
        self.data = ContactManager()  # Inicializa el manejador de contactos.
        self.selected_row = None  # Almacena la fila seleccionada.

        # Campos de entrada para los datos del contacto.
        self.name = ft.TextField(label="Nombre", border_color="pink")
        self.age = ft.TextField(label="Edad", border_color="pink", 
                                input_filter=ft.NumbersOnlyInputFilter(),
                                max_length=2)
        self.email = ft.TextField(label="Correo", border_color="pink")
        self.phone = ft.TextField(label="Teléfono", border_color="pink",
                                  input_filter=ft.NumbersOnlyInputFilter(),
                                  max_length=10)
        self.ci = ft.TextField(label="Cédula de identidad", border_color="pink",
                                  input_filter=ft.NumbersOnlyInputFilter(),
                                  max_length=10)

        # Campo de búsqueda para encontrar contactos por nombre.
        self.search_field = ft.TextField(  
                            suffix_icon=ft.icons.SEARCH,
                            label="Buscar por el nombre",
                            border=ft.InputBorder.UNDERLINE,
                            border_color="white",
                            label_style=ft.TextStyle(color="white"),
                            on_change=self.search_data,  
                        )

        # Tabla para mostrar los datos de los contactos.
        self.data_table = ft.DataTable(
                            expand=True,
                            border=ft.border.all(2, "pink"),
                            data_row_color={ft.MaterialState.SELECTED: "pink", ft.MaterialState.PRESSED: "black"},
                            border_radius=10,
                            show_checkbox_column=True,
                            columns=[  # Columnas de la tabla.
                                ft.DataColumn(ft.Text("Nombre", color="pink", weight="bold")),
                                ft.DataColumn(ft.Text("Edad", color="pink", weight="bold")),
                                ft.DataColumn(ft.Text("Cédula de identidad", color="pink", weight="bold"), numeric=True),
                                ft.DataColumn(ft.Text("Correo", color="pink", weight="bold"), numeric=True),
                                ft.DataColumn(ft.Text("Teléfono", color="pink", weight="bold"), numeric=True),
                            ],
                        )        

        self.show_data()  # Muestra los datos existentes en la tabla.

        # Contenedor principal del formulario.
        self.form = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            col=4,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Ingrese sus datos",
                            size=40,
                            text_align="center",
                            font_family="arial",),
                    self.name,
                    self.age,
                    self.ci,
                    self.email,
                    self.phone,

                    # Contenedor de botones Guardar, Actualizar, Borrar y Limpiar
                    ft.Container(
                        content=ft.Column(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.TextButton(
                                            text="Guardar",
                                            icon=ft.icons.SAVE,
                                            icon_color="white",
                                            style=ft.ButtonStyle(color="white", bgcolor="pink"),
                                            on_click=self.add_data,  # Acción de guardar datos.
                                        ),
                                        ft.TextButton(
                                            text="Actualizar",
                                            icon=ft.icons.UPDATE,
                                            icon_color="white",
                                            style=ft.ButtonStyle(color="white", bgcolor="pink"),
                                            on_click=self.update_data,  # Acción de actualizar datos.
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.TextButton(
                                            text="Borrar",
                                            icon=ft.icons.DELETE,
                                            icon_color="white",
                                            style=ft.ButtonStyle(color="white", bgcolor="pink"),
                                            on_click=self.delete_data,  # Acción de borrar datos.
                                        ),
                                        ft.TextButton(
                                            text="Limpiar",
                                            icon=ft.icons.CLEAR,
                                            icon_color="white",
                                            style=ft.ButtonStyle(color="white", bgcolor="pink"),
                                            on_click=self.clean_fields,  # Acción para limpiar campos.
                                        ),
                                    ]
                                ),
                            ]
                        )
                    )
                ]
            )
        )

        # Contenedor para la tabla de datos y las acciones adicionales.
        self.table = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            padding=10,
            col=8,
            content=ft.Column(   
                expand=True,           
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                self.search_field,  
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=self.edit_field_text,  
                                    icon_color="white",
                                ),
                                ft.IconButton(tooltip="Descargar en PDF",
                                            icon=ft.icons.PICTURE_AS_PDF,
                                            icon_color="white",
                                            on_click=self.save_pdf,  # Acción para descargar en PDF.
                                            ),     
                                ft.IconButton(tooltip="Descargar en EXCEL",
                                        icon=ft.icons.SAVE_ALT,
                                        icon_color="white",
                                        on_click=self.save_excel,  # Acción para descargar en Excel.
                                        ),  
                            ]
                        ),
                    ),
                    ft.Column(
                        expand=True, 
                        scroll="auto",
                        controls=[
                        ft.ResponsiveRow([self.data_table]),  # Muestra la tabla de datos.
                        ]
                    )
                ]
            )
        )
        
        # Estructura final del contenido que combina el formulario y la tabla.
        self.content = ft.ResponsiveRow(  
            controls=[self.form, self.table]
        )
    
    # Método para mostrar los datos en la tabla.
    def show_data(self):
        self.data_table.rows = []  # Limpia las filas actuales.
        for x in self.data.get_contacts():  # Obtiene todos los contactos.
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,  # Llama a get_index al seleccionar una fila.
                    cells=[
                        ft.DataCell(ft.Text(x[1])),  # Nombre.
                        ft.DataCell(ft.Text(str(x[2]))),  # Edad.
                        ft.DataCell(ft.Text(str(x[5]))),  # Ci
                        ft.DataCell(ft.Text(x[3])),  # Correo.
                        ft.DataCell(ft.Text(str(x[4]))),  # Teléfono.
                    ]
                )
            )
        self.update()  # Actualiza la interfaz.

# MANEJO DE ERRORES
    def add_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        ci = str(self.ci.value)
        email = self.email.value
        phone = str(self.phone.value)

        # Validar campos vacíos  
        if not name or not age or not ci or not email or not phone:
            self.show_error_modal("Falta rellenar campos.")
            return
        
        # Validar el nombre (solo letras y espacios).
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ\\s]+$", name):

            self.show_error_modal("El nombre solo debe contener letras y espacios.")
            return

        # Validar el correo (simple validación).
        if not "@" in email or not "." in email:
            self.show_error_modal("El correo no es válido.")
            return
        
        # Comprobar si el contacto ya existe.
        contact_exists = False
        for row in self.data.get_contacts():
            if row[1] == name:
                contact_exists = True
                break

        if not contact_exists:
            self.clean_fields()  # Limpia los campos tras agregar.
            self.data.add_contact(name, age, ci, email, phone)  # Añade el nuevo contacto.
            self.show_data()  # Muestra los datos actualizados.
        else:
            self.show_error_modal("El contacto ya existe en la base de datos.")  # Muestra error si el contacto existe.

    # Método para mostrar un modal de error.
    def show_error_modal(self, message):
        modal = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.close_modal(modal))  # Botón para cerrar el modal.
            ]
        )
        self.page.dialog = modal
        modal.open = True  # Abre el modal.
        self.page.update()

    def close_modal(self, modal):
        modal.open = False  # Cierra el modal.
        self.page.update()

    def get_index(self, e):
        if e.control.selected:  # Cambia el estado de selección de la fila.
           e.control.selected = False
        else: 
            e.control.selected = True
        name = e.control.cells[0].content.value  # Obtiene el nombre de la fila seleccionada.
        for row in self.data.get_contacts():
            if row[1] == name:
                self.selected_row = row  # Guarda la fila seleccionada.
                break
        self.update()

    def edit_field_text(self, e):  
        try: 
            # Rellena los campos con los datos de la fila seleccionada.
            self.name.value = self.selected_row[1]
            self.age.value = self.selected_row[2]
            self.ci.value = self.selected_row[5]
            self.email.value = self.selected_row[3]
            self.phone.value = self.selected_row[4]   
            self.update()
        except TypeError:
            print("Error")  # Manejo de error si no se seleccionó ninguna fila.

# ACTUALIZAR DATOS
    def update_data(self, e):
        if not self.selected_row:
            self.show_error_modal("No ha seleccionado ningún registro.")  # Error si no hay fila seleccionada.
            return

        name = self.name.value
        age = str(self.age.value)
        ci = str(self.ci.value)
        email = self.email.value
        phone = str(self.phone.value)

        # Verifica que los campos no estén vacíos.
        if len(name) > 0 and len(age) > 0 and len(ci) > 0 and len(email) > 0 and len(phone) > 0:
            self.clean_fields()  # Limpia los campos tras actualizar.
            self.data.update_contact(self.selected_row[0], name, age, ci, email, phone)  # Actualiza el contacto.
            self.show_data()  # Muestra los datos actualizados.

# BORRAR DATOS
    def delete_data(self, e):
        if not self.selected_row:
            self.show_error_modal("No ha seleccionado ningún registro.")  # Error si no hay fila seleccionada.
            return

        self.data.delete_contact(self.selected_row[1])  # Elimina el contacto seleccionado.
        self.show_data()  # Muestra los datos actualizados.

# BÚSQUEDA
    def search_data(self, e):  
        search = self.search_field.value.lower()  # Obtiene el término de búsqueda.
        name = list(filter(lambda x: search in x[1].lower(), self.data.get_contacts()))  # Filtra contactos.
        self.data_table.rows = []  # Limpia la tabla.
        if not self.search_field.value == "": 
            if len(name) > 0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,  # Llama a get_index al seleccionar una fila.
                            cells=[
                                ft.DataCell(ft.Text(x[1])),  # Nombre.
                                ft.DataCell(ft.Text(str(x[2]))),  # Edad.
                                ft.DataCell(ft.Text(str(x[5]))),  # CI.
                                ft.DataCell(ft.Text(x[3])),  # Correo.
                                ft.DataCell(ft.Text(str(x[4]))),  # Teléfono.
                            ]
                        )
                    )
                    self.update()
        else:
            self.show_data()  # Si no hay búsqueda, muestra todos los datos.

# LIMPIAR CAMPOS
    def clean_fields(self, e=None):
        self.name.value = ""  # Limpia el campo de nombre.
        self.age.value = ""  # Limpia el campo de edad.
        self.ci.value = ""  # Limpia el campo de ci.
        self.email.value = ""  # Limpia el campo de correo.
        self.phone.value = ""  # Limpia el campo de teléfono.      
        self.update()  # Actualiza la interfaz.

# APARTADO DE DESCARGA PARA PDF 
    def save_pdf(self, e):
        pdf = PDF()  # Crea una nueva instancia de PDF.
        pdf.add_page()  # Añade una página al PDF.
        column_widths = [10, 40, 20, 40, 80, 40]  # Define el ancho de las columnas.
        # Agrega filas a la tabla.
        data = self.data.get_contacts()  # Obtiene todos los contactos.
        header = ("ID", "NOMBRE", "EDAD", "CORREO", "TELÉFONO", "CÉDULA")  # Define el encabezado.
        data.insert(0, header)  # Inserta el encabezado en los datos.
        for row in data:  # Añade cada fila al PDF.
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)  # Escribe cada celda.
            pdf.ln()  # Salto de línea para la siguiente fila.
        file_name = datetime.datetime.now()  # Crea un nombre de archivo basado en la fecha y hora.
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"  # Formato del nombre.
        pdf.output(file_name)  # Guarda el PDF.

# APARTADO DE DESCARGA PARA EXCEL
    def save_excel(self, e):
        file_name = datetime.datetime.now()  # Crea un nombre de archivo basado en la fecha y hora.
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"  # Formato del nombre.
        contacts = self.data.get_contacts()  # Obtiene todos los contactos.
        df = pd.DataFrame(contacts, columns=["ID", "Nombre", "Edad", "Correo", "Teléfono", "Cédula"])  # Crea un DataFrame.
        df.to_excel(file_name, index=False)  # Guarda el DataFrame como archivo Excel.

    def build(self):
        return self.content

# Función principal que inicializa la aplicación.
def main(page: ft.Page):
    page.bgcolor = "black"  # Establece el color de fondo de la página.
    page.title = "CRUD SQLite"  # Título de la ventana.
    page.window_min_width = 1100  # Ancho mínimo de la ventana.
    page.window_min_height = 500  # Altura mínima de la ventana.
    form_ui = FormUi(page)  # Crea una instancia de la interfaz de usuario.
    form_ui.data.close_connection()  # Cierra la conexión a la base de datos.
    page.add(FormUi(page))  # Agrega la interfaz a la página.

ft.app(main)  # Ejecuta la aplicación.
