import os
import mysql.connector
from mysql.connector import Error


def conectare_mysql():
    try:
        conexiune = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "booker")
        )

        if conexiune.is_connected():
            print("Conectat cu succes la MySQL")
            return conexiune

        conexiune.close()
        return None

    except Error as e:
        print(f"Eroare la conectarea MySQL: {e}")
        return None