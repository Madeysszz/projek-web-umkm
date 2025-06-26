import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",     
            database="sistem_absensi"
        )
        print("Koneksi berhasil!")
        return db
    except Error as err:
        print(f"Gagal koneksi ke database: {err}")

connect_db()
