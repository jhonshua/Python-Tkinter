from tkinter import *
import tkinter as tk
import customtkinter as ctk
from modulos.ventas.ventas_moderna import VentasModerna as Ventas
from modulos.inventario.inventario_simple import InventarioSimple as Inventario
from modulos.clientes_moderno import ClientesModerno as Clientes
from modulos.pedidos_moderno import PedidosModerno as Pedidos
from modulos.proveedores.proveedor_moderno import ProveedorModerno as Proveedor
from modulos.informacion.informacion_moderna import InformacionModerna as Informacion
from modulos.utils.estilos_modernos import estilos
from PIL import Image, ImageTk
import sys
import os

# Configurar CustomTkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        
        # Configurar el frame principal con estilos modernos
        self.configure(bg=estilos.COLORS['bg_primary'])
        self.pack()
        self.place(x=0, y=0, width=1400, height=900)  # Tamaño actualizado
        
        # Inicializar antes de widgets_modernos() porque los botones necesitan estos atributos
        self.frames = {}
        self.buttons = []
        self.active_button = None  # Botón activo actual
        self.button_map = {}  # Mapeo de módulos a botones
        
        self.widgets_modernos()
        
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
        
        # Actualizar el color del botón activo
        self.actualizar_boton_activo(container) 
        
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
    
    def actualizar_boton_activo(self, container):
        """Actualizar el color del botón activo y restaurar los demás"""
        # Restaurar todos los botones a su color normal
        for btn in self.buttons:
            btn.configure(fg_color=estilos.COLORS['primary_light'])
        
        # Cambiar el color del botón activo
        if container in self.button_map:
            active_btn = self.button_map[container]
            active_btn.configure(fg_color=estilos.COLORS['secondary'])  # Color diferente para activo
            self.active_button = active_btn
            
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
            {"text": "💰 Ventas", "command": self.Ventas, "icon": "venta_icon.png", "module": Ventas},
            {"text": "📦 Inventario", "command": self.Inventario, "icon": "inventario_icon.png", "module": Inventario},
            {"text": "👥 Clientes", "command": self.Clientes, "icon": "cliente_icon.png", "module": Clientes},
            {"text": "📋 Pedidos", "command": self.Pedidos, "icon": "pedido_icon.png", "module": Pedidos},
            {"text": "🏭 Proveedores", "command": self.Proveedor, "icon": "proveedor_icon.png", "module": Proveedor},
            {"text": "ℹ️ Info", "command": self.Informacion, "icon": "informacion_icon.png", "module": Informacion}
        ]
        
        self.buttons = []
        x_position = 0
        
        for config in button_configs:
            # Crear botón moderno
            btn = self.crear_boton_navbar(buttons_frame, config["text"], config["command"], x_position)
            self.buttons.append(btn)
            # Mapear el módulo al botón
            self.button_map[config["module"]] = btn
            x_position += 135  # Espaciado entre botones ajustado
        
        # Actualizar el botón activo inicial (Ventas)
        if Ventas in self.button_map:
            self.actualizar_boton_activo(Ventas)
    
    def crear_boton_navbar(self, parent, text, command, x_pos):
        """Crear un botón moderno con CustomTkinter (esquinas perfectamente redondeadas)"""
        
        # Crear botón CustomTkinter con esquinas redondeadas nativas
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=130,
            height=40,
            corner_radius=15,  # Esquinas muy redondeadas
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=estilos.COLORS['primary_light'],  # Color normal
            hover_color=estilos.COLORS['secondary'],   # Color hover
            text_color=estilos.COLORS['white'],        # Color del texto
            border_width=0,                            # Sin borde
            cursor="hand2"                             # Cursor de mano
        )
        
        # Posicionar el botón
        btn.place(x=x_pos, y=5)
        
        return btn
        
        
        