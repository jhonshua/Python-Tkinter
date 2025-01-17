from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Login(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.controlador = controlador
        self.widgets()
        
    def widgets(self):
        fondo = tk.Frame(self, bg='#C6D9E3')
        fondo.pack()
        fondo.place(x = 0, y = 0, width = 1100, height = 650)
        
        self.bg_image = Image.open('media/img/fondo.png')
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image = self.bg_image)
        self.bg_label.place(x = 0, y = 0, width = 1100, height = 650 )
    
class Registro(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.widgets()
        
    def widgets(self):
        pass