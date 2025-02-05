from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox


class Informacion(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
    def widgets(self):
        self.labelframe = tk.LabelFrame(self, bg="#C6D9E3")
        self.labelframe.place(x=100, y=20, width=900,  height=560)

        lblnombre = tk.Label(self.labelframe, text="Informacion", font="sans 20 bold", bg="#C6D9E3")
        lblnombre.place(x=310, y=20)

              # Título principal
        lbl_titulo = tk.Label(self.labelframe, text="Información de la Aplicación", font="sans 24 bold", bg="#C6D9E3")
        lbl_titulo.place(x=250, y=20)  # Centrado aproximado

        # Sección de Descripción
        lbl_descripcion_titulo = tk.Label(self.labelframe, text="Descripción :", font="sans 16 bold", bg="#C6D9E3")
        lbl_descripcion_titulo.place(x=50, y=80)
        txt_descripcion = tk.Text(self.labelframe, wrap=tk.WORD, bg="#FFFFFF", height=5, width=80) # Ajustar tamaño
        txt_descripcion.place(x=50, y=120)
        txt_descripcion.insert(tk.END, "Esta aplicación de escritorio con Python te ayuda a gestionar el inventario de tu negocio de manera eficiente.  Permite registrar productos, realizar ventas, generar reportes y mucho más.") # Ejemplo

        # Sección de Licencia
        lbl_licencia_titulo = tk.Label(self.labelframe, text="MIT License", font="sans 16 bold", bg="#C6D9E3")
        lbl_licencia_titulo.place(x=50, y=220)
        txt_licencia = tk.Text(self.labelframe, wrap=tk.WORD, bg="#FFFFFF", height=3, width=80) # Ajustar tamaño
        txt_licencia.place(x=50, y=260)
        txt_licencia.insert(tk.END, "Esta aplicación se distribuye bajo la licencia MIT.                                    Copyright (c) 2025 Julio Cesar Llinas ") 

        # Sección de Desarrollador
        lbl_desarrollador_titulo = tk.Label(self.labelframe, text="Desarrollador", font="sans 16 bold", bg="#C6D9E3")
        lbl_desarrollador_titulo.place(x=50, y=320)
        lbl_nombre_desarrollador = tk.Label(self.labelframe, text="Julio Cesar Llinas", bg="#C6D9E3")
        lbl_nombre_desarrollador.place(x=50, y=360)
        lbl_contacto = tk.Label(self.labelframe, text="julio.llinas@gmail.com", bg="#C6D9E3") # O enlace a web
        lbl_contacto.place(x=50, y=380)

        # Versión (Opcional)
        lbl_version_titulo = tk.Label(self.labelframe, text="Versión :", font="sans 16 bold", bg="#C6D9E3")
        lbl_version_titulo.place(x=50, y=420)
        lbl_version = tk.Label(self.labelframe, text="V 1.0", bg="#C6D9E3") # Reemplaza con tu versión
        lbl_version.place(x=50, y=460)
       

    