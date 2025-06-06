import sqlite3  # Importa el módulo sqlite3 para trabajar con bases de datos SQLite.

# Clase que maneja las operaciones CRUD para contactos.
class ContactManager:
    def __init__(self):
        # Inicializa la conexión a la base de datos 'data.db'.
        self.connection = sqlite3.connect("data.db", check_same_thread=False)

    def add_contact(self, name, age, ci, email, phone):
        # Método para agregar un nuevo contacto a la base de datos.
        query = '''INSERT INTO datos (NOMBRE, EDAD, CI, CORREO, TELEFONO) 
                   VALUES (?, ?, ?, ?, ?)'''  # Consulta SQL para insertar un contacto.
        self.connection.execute(query, (name, age, ci, email, phone))  # Ejecuta la consulta con los datos proporcionados.
        self.connection.commit()  # Confirma los cambios en la base de datos.

    def get_contacts(self):
        # Método para obtener todos los contactos de la base de datos.
        cursor = self.connection.cursor()  # Crea un cursor para ejecutar consultas.
        query = "SELECT * FROM datos"  # Consulta SQL para seleccionar todos los contactos.
        cursor.execute(query)  # Ejecuta la consulta.
        contacts = cursor.fetchall()  # Obtiene todos los resultados de la consulta.
        return contacts  # Devuelve la lista de contactos.

    def delete_contact(self, name):
        # Método para eliminar un contacto basado en su nombre.
        query = "DELETE FROM datos WHERE NOMBRE = ?"  # Consulta SQL para eliminar un contacto.
        self.connection.execute(query, (name,))  # Ejecuta la consulta con el nombre proporcionado.
        self.connection.commit()  # Confirma los cambios en la base de datos.

    def update_contact(self, contact_id, name, age, ci, email, phone):
        # Método para actualizar un contacto existente en la base de datos.
        query = '''UPDATE datos SET NOMBRE = ?, EDAD = ?, CI = ?, CORREO = ?, TELEFONO = ?
                   WHERE ID = ?'''  # Consulta SQL para actualizar un contacto.
        self.connection.execute(query, (name, age, ci, email, phone, contact_id))  # Ejecuta la consulta con los nuevos datos.
        self.connection.commit()  # Confirma los cambios en la base de datos.

    def close_connection(self):
        # Método para cerrar la conexión a la base de datos.
        self.connection.close()  # Cierra la conexión.
        print("cerrar")  # Imprime un mensaje indicando que se ha cerrado la conexión.
