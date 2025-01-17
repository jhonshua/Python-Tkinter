from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from pedidos import Pedidos
from proveedor import Proveedor
from informacion import Informacion
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Ventas, Inventario, Clientes, Pedidos, Proveedor, Informacion ):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg='#C6D9E3', highlightbackground='gray')
            frame.place(x= 0, y= 40, width= 1100, height= 610 )
        self.show_frames( Ventas)
        
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise() 
            
    def widgets(self):
        pass
