from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class Informacion(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
    def widgets(self):
        self.labelframe = tk.LabelFrame(self, bg="#C6D9E3")
        self.labelframe.place(x=100, y=20, width=1000,  height=600)

        # Título principal
        lbl_titulo = tk.Label(self.labelframe, text="Información", font="sans 24 bold", bg="#C6D9E3")
        lbl_titulo.place(x=250, y=20)  # Centrado aproximado

        image_report = Image.open("media/icons/report.png")
        image_report_resize = image_report.resize((129, 144))
        self.image_report_tk = ImageTk.PhotoImage(image_report_resize)

        button_report = ttk.Button(self.labelframe, text="Generar reporte", image=self.image_report_tk, compound=TOP) 
        button_report.image = self.image_report_tk  
        button_report.place(y=200, x=100, height=200, width=200)

        image_bcv = Image.open("media/icons/bcv.png")
        image_bcv_resize = image_bcv.resize((150, 150))
        self.image_bcv_tk = ImageTk.PhotoImage(image_bcv_resize)

        button_bcv = ttk.Button(self.labelframe, text="Precio del dia", image=self.image_bcv_tk, compound=TOP) 
        button_bcv.image = self.image_bcv_tk  
        button_bcv.place(y=200, x=400, height=200, width=200)

        image_inf = Image.open("media/icons/info.png")
        image_inf_resize = image_inf.resize((150, 150))
        self.image_inf_tk = ImageTk.PhotoImage(image_inf_resize)

        button_inf = ttk.Button(self.labelframe, text="Informacion", image=self.image_inf_tk, compound=TOP) 
        button_inf.image = self.image_inf_tk  
        button_inf.place(y=200, x=700, height=200, width=200)







     
       

    