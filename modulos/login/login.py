from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

 #---------------------------------------------------------------------------------

class Login(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.controlador = controlador
        self.widgets()
        
    def validaciones(self, user, password):
        return len(user)> 0 and len(password)
        
    def widgets(self):
        #---------------------------------------------------------------------------------
        #imagen de fondo
        fondo = tk.Frame(self, bg='#C6D9E3')
        fondo.pack()
        fondo.place(x = 0, y = 0, width = 1100, height = 650)
        
        self.bg_image = Image.open('media/img/fondo.png')
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image = self.bg_image)
        self.bg_label.place(x = 0, y = 0, width = 1100, height = 650 )
        
        #---------------------------------------------------------------------------------
        #cuadro de entrada usuario y pass
        
        frame1 = tk.Frame(self, bg = '#ffffff', highlightbackground ='black', highlightthickness = 1 )
        frame1.place(x = 350, y = 50, width = 400, height = 560 )
        
        #---------------------------------------------------------------------------------
        #input usuario
        user = ttk.Label(frame1, text = "Nombre de usuario", font = "arial 16 bold", background = "#ffffff")
        user.place(x = 100, y = 250)
        self.username = ttk.Entry(frame1, font = "arial 16 bold")
        self.username.place(x = 80, y = 290, width = 240, height = 40 )
    
        #---------------------------------------------------------------------------------
        #input pass
        password = ttk.Label(frame1, text = "Contraseña",font = "arial 16 bold", background = "#ffffff")
        password.place(x = 100, y = 340)
        self.pass_word = ttk.Entry(frame1, show='*', font = "arial 16 bold")
        self.pass_word.place(x = 80, y = 380, width = 240, height = 40 )
        
        #---------------------------------------------------------------------------------
        #boton aceptar
        
        # Create a custom style for the buttons (optional)
        style = ttk.Style()
        style.configure('my.TButton', font=("arial", 18, "bold"))
        
        # Login button
        btn1 = ttk.Button(frame1, text='Iniciar', style='my.TButton')
        btn1.place(x=80, y=440, width=240, height=40)

        # Register button
        btn2 = ttk.Button(frame1, text='Registrar', style='my.TButton')
        btn2.place(x=80, y=500, width=240, height=40)

 #---------------------------------------------------------------------------------     
        
class Registro(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.controlador = controlador
        self.widgets()
        
    def widgets(self):
         #---------------------------------------------------------------------------------
        #imagen de fondo
        fondo = tk.Frame(self, bg='#C6D9E3')
        fondo.pack()
        fondo.place(x = 0, y = 0, width = 1100, height = 650)
        
        self.bg_image = Image.open('media/img/fondo.png')
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image = self.bg_image)
        self.bg_label.place(x = 0, y = 0, width = 1100, height = 650 )
        
        #---------------------------------------------------------------------------------
        #cuadro de entrada usuario y pass
        
        frame1 = tk.Frame(self, bg = '#ffffff', highlightbackground ='black', highlightthickness = 1 )
        frame1.place(x = 350, y = 10, width = 400, height = 630 )
        
        #---------------------------------------------------------------------------------
        #input usuario
        user = ttk.Label(frame1, text = "Nombre de usuario", font = "arial 16 bold", background = "#ffffff")
        user.place(x = 100, y = 250)
        self.username = ttk.Entry(frame1, font = "arial 16 bold")
        self.username.place(x = 80, y = 290, width = 240, height = 40 )
    
        #---------------------------------------------------------------------------------
        #input pass
        password = ttk.Label(frame1, text = "Contraseña",font = "arial 16 bold", background = "#ffffff")
        password.place(x = 100, y = 340)
        self.pass_word = ttk.Entry(frame1, show='*', font = "arial 16 bold")
        self.pass_word.place(x = 80, y = 380, width = 240, height = 40 )
        
        #---------------------------------------------------------------------------------
        #input codigo de registro
        key = ttk.Label(frame1, text = "Codigo de registro",font = "arial 16 bold", background = "#ffffff")
        key.place(x = 100, y = 430)
        self.key = ttk.Entry(frame1, show='*', font = "arial 16 bold")
        self.key.place(x = 80, y = 470, width = 240, height = 40 )
        
        #---------------------------------------------------------------------------------
        #boton aceptar
        
        # Create a custom style for the buttons (optional)
        style = ttk.Style()
        style.configure('my.TButton', font=("arial", 18, "bold"))
        
        # Login button
        btn3 = ttk.Button(frame1, text='Registarse', style='my.TButton')
        btn3.place(x=80, y=520, width=240, height=40)

        # Register button
        btn4 = ttk.Button(frame1, text='Regresar', style='my.TButton')
        btn4.place(x=80, y=570, width=240, height=40)