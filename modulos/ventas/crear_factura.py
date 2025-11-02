from tkinter import *
from tkinter import messagebox
import datetime
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import sqlite3

import sys
import os

from modulos.ventas.obtener_numero_factura import obtener_numero_factura_actual
from modulos.configuracion.gestor_configuracion import obtener_configuracion


def generar_factura(total_venta, cliente):
        
    numero_factura = obtener_numero_factura_actual()
    productos_seleccionados = []

    try:
        try:
            # Ruta absoluta para la carpeta de facturas
            factura_path = os.path.abspath("facturas")
            if not os.path.exists(factura_path):
                os.makedirs(factura_path)

            factura_nombre = f"Factura_{numero_factura}.pdf"
            factura_path = os.path.join(factura_path, factura_nombre)
            c = canvas.Canvas(factura_path)
            # ... Resto del código para crear el PDF

        except Exception as e:
                   messagebox.showerror("Error", f"No se pudo generar la factura: {e}")

   #---------------------------------------------------------------------------

        # Obtener datos de la empresa desde la configuración
        empresa_nombre = obtener_configuracion('nombre_empresa', 'Mi Tienda')
        empresa_direccion = obtener_configuracion('direccion_empresa', 'Caracas, Venezuela')
        empresa_telefono = obtener_configuracion('telefono_empresa', '+58-212-1234567')
        empresa_rif = obtener_configuracion('rif_empresa', 'J-00000000-0')
        empresa_email = "info@marketsystem.com"  # Mantener como opcional
        empresa_website = "www.marketsystem.com"  # Mantener como opcional


        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.darkblue)
        c.drawCentredString(300, 750, "FACTURA DE SERVICIOS")

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 710, f"{empresa_nombre}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 690, f"RIF: {empresa_rif}")
        c.drawString(50, 670, f"Direccion: {empresa_direccion}")
        c.drawString(50, 650, f"Telefono: {empresa_telefono}")
        c.drawString(50, 630, f"Email: {empresa_email}")
        c.drawString(50, 610, f"Website: {empresa_website}")

        c.setLineWidth(0.5)
        c.setStrokeColor(colors.gray)
        c.line(50, 600, 550, 600)

        c.setFont("Helvetica", 12)
        c.drawString(50, 580, f"Numero de factura: {numero_factura}")
        c.drawString(50, 560, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

        c.line(50, 540, 550, 540)
            
        c.drawString(50, 520, f"Cliente: {cliente}")
        c.drawString(50, 500, f"Descripcion de productos:")

        y_offset = 480
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y_offset, "Propducto")
        c.drawString(270, y_offset, "Cantidad")
        c.drawString(370, y_offset, "Precio")
        c.drawString(470, y_offset, "Total")

        c.line(50, y_offset - 10, 550, y_offset - 10)
        y_offset -= 30
        c.setFont("Helvetica", 12)
        for item in productos_seleccionados:
            factura, cliente, producto, precio, cantidad, total, costo = item
            c.drawString(70, y_offset, producto)
            c.drawString(270, y_offset, str(cantidad) )
            c.drawString(370, y_offset, "${:,.0f})".format(precio))
            c.drawString(470, y_offset, total)
            y_offset-= 20

        c.line(50, y_offset , 550, y_offset )
        y_offset -= 20

        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(50, y_offset, f"Total a Pagar : ${total_venta:,.0f}")
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)

        y_offset-= 20
        c.line(50, y_offset , 550, y_offset )

        c.setFont("Helvetica-Bold", 16)
        c.drawString(150, y_offset - 60, "Gracias por tu compra, vuelve pronto!")

        y_offset -= 100
        c.setFont("Helvetica", 10)
        c.drawString(50, y_offset, "Terminos y Condiciones: ")
        c.drawString(50, y_offset - 20,  "1. Los productos comprados no tienen devolucion.")
        c.drawString(50, y_offset- 40, "2 .  Conserve esta factura como comprobante de su compra")
        c.drawString(50, y_offset - 60, "3. Para mas informacion visite nuestro sitio web o contacte a servicios al cliente")

        c.save()

        messagebox.showinfo("Factura generada", f"Se ha generado la factura en : {factura_path}")
        os.startfile(os.path.abspath(factura_path))

    except Exception as e :
        messagebox.showerror("Error", f"No se pudo generar la factura: {e}")

    #---------------------------------------------------------------------------------


# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import mm

# # Define el tamaño de página personalizado
# width = 57 * mm
# height = 100 * mm  # Ajusta la altura según tus necesidades
# pagesize = (width, height)

# # Crea el objeto canvas
# c = canvas.Canvas("factura.pdf", pagesize=pagesize)

# # Añade contenido a la factura
# c.drawString(10, height - 10, "Tu texto aquí")

# # Guarda el PDF
# c.save()