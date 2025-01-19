import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

class Ventas(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
    def widgets(self):
        labelframe  = tk.LabelFrame(self, font='sans 12 bold', bg='#C6D9E3')
        labelframe.place(x=25, y=30, width=1045, height=180)
        
        label_Cliente = tk.Label(labelframe, text="Cliente: ", font='sans 14 bold', bg='#C6D9E3')
        label_Cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        
        label_producto = tk.Label(labelframe,text="Producto: ", font="sans 14 bold", bg='#C6D9E3' )
        label_producto.place(x = 10, y = 70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold" )
        self.entry_producto.place(x=120, y=66, width=260, height=40)
          
        label_cantidad = tk.Label(labelframe, text="cantidad: ", font='sans 14 bold', bg='#C6D9E3')
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)
        
        self.label_stock = tk.Label(labelframe, text="Stock: ", font='sans 14 bold', bg='#C6D9E3')
        self.label_stock.place(x=500, y=70)
        
        label_factura = tk.Label(labelframe, text="Numero de Factura: ", font='sans 14 bold', bg='#C6D9E3')
        label_factura.place(x=750, y=11)
        
        boton_agregar = tk.Button(labelframe, text="Agregar Articulo", font='sans 14 bold')
        boton_agregar.place(x=90, y=120, height=40, width=200)
        
        boton_eliminar = tk.Button(labelframe, text="Eliminar Articulo", font='sans 14 bold')
        boton_eliminar.place(x=310, y=120, height=40, width=200)
        
        boton_editar = tk.Button(labelframe, text="Editar Articulo", font='sans 14 bold')
        boton_editar.place(x=530, y=120, height=40, width=200)
        
        boton_limpiar = tk.Button(labelframe, text="Limpiar lista", font='sans 14 bold')
        boton_limpiar.place(x=750, y=120, height=40, width=200)
        
        treFrame = tk.Frame(self, background='white')
        treFrame.place(x=70, y=220, width=980,height=300)
        
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=X)
        
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set,height=40, columns=('Factura','Cliente','Producto','Precio','Cantidad','Total'), show='headings')
        self.tre.pack(expand=True, fill=BOTH)

        scrol_x.config(command=self.tre.xview)
        scrol_y.config(command=self.tre.yview)

        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")

        self.label_precio_total = tk.Label(self, text='Precio a Pagar: $ 0', font='sans 18 bold', bg='#C6D9E3' )
        self.label_precio_total.place(x=680, y=550)

        boton_pagar = tk.Button(self, text="Pagar", font='sans 14 bold')
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ver ventas realizadas", font='sans 14 bold')
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)

      

