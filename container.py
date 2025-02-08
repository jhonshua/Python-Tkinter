from tkinter import *
import tkinter as tk
from modulos.ventas import Ventas
from modulos.inventario import Inventario
from modulos.clientes import Clientes
from modulos.pedidos import Pedidos
from modulos.proveedores.proveedor import Proveedor
from modulos.informacion import Informacion
from PIL import Image, ImageTk
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1200, height=800)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Ventas, Inventario, Clientes, Pedidos, Proveedor, Informacion ):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg='#C6D9E3', highlightbackground='gray')
            frame.place(x= 0, y= 40, width= 1200, height= 800 )
        self.show_frames( Ventas)
        
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise() 
        
    def Ventas(self):
        self.show_frames(Ventas)
        
    def Inventario(self):
        self.show_frames(Inventario)
        
    def Clientes(self):
        self.show_frames(Clientes)
        
    def Pedidos(self):
        self.show_frames(Pedidos)
        
    def Proveedor(self):
        self.show_frames(Proveedor)
    
    def Informacion(self):
        self.show_frames(Informacion)
            
    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x= 0, y= 0, width= 1200, height= 45 )

        #-------------------------------------------------------------------------------------------------------------------------------------------

        image_venta = Image.open("media/icons/venta_icon.png")
        image_venta_resize = image_venta.resize((50, 50))
        image_venta_tk = ImageTk.PhotoImage(image_venta_resize)

        self.btn_ventas = Button(frame2, fg = "black", text = "Ventas", font = "sans 16 bold", command= self.Ventas )
        self.btn_ventas.config(image=image_venta_tk , compound=LEFT, padx=20)
        self.btn_ventas.image = image_venta_tk
        self.btn_ventas.place(x = 0, y = 0, width = 200, height = 40)
        #-------------------------------------------------------------------------------------------------------------------------------------------
        image_inventario = Image.open("media/icons/inventario_icon.png")
        image_inventario_resize = image_inventario.resize((50, 50))
        image_inventario_tk = ImageTk.PhotoImage(image_inventario_resize)

        self.btn_inventario = Button(frame2, fg = "black", text = "Inventario", font = "sans 16 bold", command= self.Inventario)
        self.btn_inventario.config(image=image_inventario_tk , compound=LEFT, padx=20)
        self.btn_inventario.image = image_inventario_tk
        self.btn_inventario.place(x = 200, y = 0, width = 200, height = 40)
        #-------------------------------------------------------------------------------------------------------------------------------------------
        image_cliente = Image.open("media/icons/cliente_icon.png")
        image_cliente_resize = image_cliente.resize((50, 50))
        image_cliente_tk = ImageTk.PhotoImage(image_cliente_resize)
        
        self.btn_clientes = Button(frame2, fg = "black", text = "Clientes", font = "sans 16 bold", command= self.Clientes )
        self.btn_clientes.config(image=image_cliente_tk , compound=LEFT, padx=20)
        self.btn_clientes.image = image_cliente_tk
        self.btn_clientes.place(x = 400, y = 0, width = 200, height = 40)

        #-------------------------------------------------------------------------------------------------------------------------------------------

        image_pedido = Image.open("media/icons/pedido_icon.png")
        image_pedido_resize = image_pedido.resize((50, 50))
        image_pedido_tk = ImageTk.PhotoImage(image_pedido_resize)
        
        self.btn_pedidos = Button(frame2, fg = "black", text = "Pedidos", font = "sans 16 bold", command= self.Pedidos )
        self.btn_pedidos.config(image=image_pedido_tk , compound=LEFT, padx=20)
        self.btn_pedidos.image = image_pedido_tk
        self.btn_pedidos.place(x = 600, y = 0, width = 200, height = 40)

        #-------------------------------------------------------------------------------------------------------------------------------------------

        image_proveedor = Image.open("media/icons/proveedor_icon.png")
        image_proveedor_resize = image_proveedor.resize((50, 50))
        image_proveedor_tk = ImageTk.PhotoImage(image_proveedor_resize)
        
        self.btn_proveedor = Button(frame2, fg = "black", text = "Proveedor", font = "sans 16 bold", command= self.Proveedor )
        self.btn_proveedor.config(image=image_proveedor_tk , compound=LEFT, padx=5)
        self.btn_proveedor.image = image_proveedor_tk 
        self.btn_proveedor.place(x = 800, y = 0, width = 200, height = 40)

        #-------------------------------------------------------------------------------------------------------------------------------------------
        image_informacion = Image.open("media/icons/informacion_icon.png")
        image_informacion_resize = image_informacion.resize((50, 50))
        image_informacion_tk = ImageTk.PhotoImage(image_informacion_resize)
        
        self.btn_informacion = Button(frame2, fg = "black", text = "Info", font = "sans 16 bold", command= self.Informacion )
        self.btn_informacion.config(image=image_informacion_tk , compound=LEFT)
        self.btn_informacion.image = image_informacion_tk 
        self.btn_informacion.place(x = 1000, y = 0, width = 200, height = 40)
        
        #-------------------------------------------------------------------------------------------------------------------------------------------

        self.buttons = [ self.btn_ventas, self.btn_inventario, self.btn_clientes, self.btn_pedidos, self.btn_proveedor, self.btn_informacion]
        
        
        