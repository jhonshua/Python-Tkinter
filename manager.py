from tkinter import *
from tkinter import ttk
from data.models import crear_base_de_datos
from PIL import Image, ImageTk

from modulos.login.login import Login, Registro
from container import Container
from modulos.utils.utils import resource_path
from modulos.utils.estilos_modernos import estilos

import sys
import os

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        self.title("🏪 Mi Tienda - Sistema de Ventas Moderno")
        self.geometry("1400x900+200+50")  # Ventana más grande y mejor posicionada
        self.resizable(True, True)  # Permitir redimensionar
        self.minsize(1200, 800)  # Tamaño mínimo
        
        # Aplicar colores modernos de fondo
        self.configure(bg=estilos.COLORS['bg_primary'])
        
        # Icono de la aplicación
        try:
            icon_path = resource_path("media/icons/mi_tienda.ico")  
            self.iconbitmap(icon_path)
        except:
            pass  # Si no encuentra el icono, continúa sin error

        # Container principal con estilos modernos
        container = Frame(self, bg=estilos.COLORS['bg_primary'])
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(width=1400, height=900)
        
        self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame
            
        # self.show_frame(Login)
        self.show_frame(Container)
        
        # Configurar tema y estilos modernos
        self.configurar_estilos_modernos()

        crear_base_de_datos()

    def configurar_estilos_modernos(self):
        """Configurar todos los estilos modernos de la aplicación"""
        try:
            from ttkthemes import ThemedStyle
            self.style = ThemedStyle(self)
            self.style.set_theme("arc")  # Tema base moderno
        except ImportError:
            # Si no está disponible ttkthemes, usar ttk.Style normal
            self.style = ttk.Style()
            self.style.theme_use("clam")
        
        # Configurar estilos personalizados usando nuestro sistema
        # Labels modernos
        self.style.configure('Modern.TLabel', 
                           background=estilos.COLORS['bg_primary'],
                           foreground=estilos.COLORS['primary'],
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']))
        
        self.style.configure('Title.TLabel',
                           background=estilos.COLORS['bg_primary'],
                           foreground=estilos.COLORS['primary'],
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['2xl']) + ' bold')
        
        # Botones modernos
        self.style.configure('Modern.TButton',
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']) + ' bold',
                           padding=(15, 8))
        
        # Entries modernos
        self.style.configure('Modern.TEntry',
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']),
                           fieldbackground=estilos.COLORS['white'],
                           borderwidth=1,
                           relief='solid')
        
        # Combobox modernos
        self.style.configure('Modern.TCombobox',
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']),
                           fieldbackground=estilos.COLORS['white'],
                           borderwidth=1,
                           relief='solid')
        
        # Treeview moderno
        self.style.configure('Modern.Treeview',
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']),
                           background=estilos.COLORS['white'],
                           foreground=estilos.COLORS['dark'],
                           fieldbackground=estilos.COLORS['white'])
        
        self.style.configure('Modern.Treeview.Heading',
                           font=estilos.FONTS['primary'] + ' ' + str(estilos.FONTS['sizes']['base']) + ' bold',
                           background=estilos.COLORS['primary'],
                           foreground=estilos.COLORS['white'])

    def show_frame(self, container):    
        frame = self.frames[container]   
        frame.tkraise()
        
def main():
    app = Manager()
    app.mainloop()
    
if __name__ == "__main__":
    main()