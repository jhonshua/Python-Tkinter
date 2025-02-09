from tkinter import *
import sqlite3

import sys
import os

def  obtener_numero_factura_actual():

    db_name = "database.db"
        
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT MAX(factura) FROM ventas")
        last_invoice_number = c.fetchone()[0]
        conn.close
        return last_invoice_number + 1 if last_invoice_number is not None else 1
    except sqlite3.Error as e:
        print("Error obteniendo el numero de la factura: ", e)
        return 1