from tkinter import *
import tkinter as tk
from modulos.ventas.ventas_moderna import VentasModerna as Ventas
from modulos.inventario.inventario import Inventario
from modulos.clientes import Clientes
from modulos.pedidos import Pedidos
from modulos.proveedores.proveedor import Proveedor
from modulos.informacion.informacion import Informacion
from modulos.utils.estilos_modernos import estilos
from PIL import Image, ImageTk
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        
        # Configurar el frame principal con estilos modernos
        self.configure(bg=estilos.COLORS['bg_primary'])
        self.pack()
        self.place(x=0, y=0, width=1400, height=900)  # Tamaño actualizado
        
        self.widgets_modernos()
        self.frames = {}
        self.buttons = []
        
        # Crear los frames de los módulos con estilos modernos
        for i in (Ventas, Inventario, Clientes, Pedidos, Proveedor, Informacion):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg=estilos.COLORS['bg_primary'])
            frame.place(x=0, y=70, width=1400, height=830)  # Más espacio para navbar
        
        self.show_frames(Ventas)
        
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
            
    def widgets_modernos(self):
        """Crear la barra de navegación moderna"""
        # Navbar principal con gradiente simulado
        navbar_frame = tk.Frame(self, bg=estilos.COLORS['primary'], height=70)
        navbar_frame.place(x=0, y=0, width=1400, height=70)
        
        # Título de la aplicación
        title_label = tk.Label(navbar_frame, text="🏪 Mi Tienda - Sistema de Ventas", 
                              bg=estilos.COLORS['primary'], fg=estilos.COLORS['white'],
                              font=('Segoe UI', 18, 'bold'))
        title_label.place(x=20, y=20)
        
        # Contenedor de botones de navegación (movido más a la derecha)
        buttons_frame = tk.Frame(navbar_frame, bg=estilos.COLORS['primary'])
        buttons_frame.place(x=550, y=10, width=850, height=50)  # Movido de x=400 a x=550
        
        from modulos.utils.utils import resource_path
        
        # Configuración de botones modernos
        button_configs = [
            {"text": "💰 Ventas", "command": self.Ventas, "icon": "venta_icon.png"},
            {"text": "📦 Inventario", "command": self.Inventario, "icon": "inventario_icon.png"},
            {"text": "👥 Clientes", "command": self.Clientes, "icon": "cliente_icon.png"},
            {"text": "📋 Pedidos", "command": self.Pedidos, "icon": "pedido_icon.png"},
            {"text": "🏭 Proveedores", "command": self.Proveedor, "icon": "proveedor_icon.png"},
            {"text": "ℹ️ Info", "command": self.Informacion, "icon": "informacion_icon.png"}
        ]
        
        self.buttons = []
        x_position = 0
        
        for config in button_configs:
            # Crear botón moderno
            btn = self.crear_boton_navbar(buttons_frame, config["text"], config["command"], x_position)
            self.buttons.append(btn)
            x_position += 135  # Espaciado entre botones ajustado
    
    def crear_boton_navbar(self, parent, text, command, x_pos):
        """Crear un botón moderno para la barra de navegación"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=estilos.COLORS['primary_light'], 
                       fg=estilos.COLORS['white'],
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat', bd=0, cursor='hand2',
                       padx=15, pady=8)
        btn.place(x=x_pos, y=5, width=130, height=40)
        
        # Efectos hover modernos
        def on_enter(e):
            btn.configure(bg=estilos.COLORS['secondary'])
        
        def on_leave(e):
            btn.configure(bg=estilos.COLORS['primary_light'])
        
        def on_click(e):
            # Efecto de click - cambiar temporalmente el color
            btn.configure(bg=estilos.COLORS['accent'])
            self.after(100, lambda: btn.configure(bg=estilos.COLORS['secondary']))
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)
        
        return btn
        
        
        