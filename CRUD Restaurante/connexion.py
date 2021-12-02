import mysql.connector
class DataBase:
    def __init__(self):
        self.connection=mysql.connector.connect(
            host="localhost",
            port = 3306,
            user="root",
            password="toor", #Cambia la contraseña
            database="restaurante" #Aqui pon tu base de datos
        )
        self.cursor=self.connection.cursor()

"""print("conectada")
db = DataBase()"""      # Hablitida estas lineas para revisar que la conexion se establecio