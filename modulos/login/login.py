import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from container import Container
from PIL import Image, ImageTk

#---------------------------------------------------------------------------------
class Login(tk.Frame):
    
    db_name = "database.db"
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.controlador = controlador
        self.widgets()
        
    #---------------------------------------------------------------------------------       
    def validacion(self, user, clave):
        return len(user)> 0 and len(clave)
    
    #---------------------------------------------------------------------------------   
    def login(self):
        user = self.username.get()
        pas = self.pass_word.get()
        
      
        
        if self.validacion(user, pas):
            consulta = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
            parametros = (user, pas)
            
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    result = cursor.fetchall()
                    
                    if result: 
                        self.control1()
                    else:
                        self.username.delete(0, 'end')
                        self.pass_word.delete(0, 'end')
                        messagebox.showerror(title='Error', message='Usuario y/o contrasena incorrecta')
                        
            except sqlite3.Error as e:
                messagebox.showerror(title='Error', message='No se conecto a la base datos: {}'.format(e))
        
        else:
            messagebox.showerror(title='Error', message='Llene todas las casillas')
            
    #---------------------------------------------------------------------------------     
    def control1(self):
        self.controlador.show_frame(Container)
        
     #---------------------------------------------------------------------------------     
    def control2(self):
        self.controlador.show_frame(Registro)
        
    #---------------------------------------------------------------------------------       
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
        
        frame1 = tk.Frame(self, bg ='#77BEF0', highlightbackground ='black', highlightthickness = 2 )
        frame1.place(x = 350, y = 50, width = 400, height = 560 )
           
        self.logo_image = Image.open('media/icons/tienda.png')
        self.logo_image = self.logo_image.resize((200, 200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(frame1, image = self.logo_image)
        self.logo_label.place(x = 100, y = 20)
        
        #---------------------------------------------------------------------------------
        #input usuario
        user = ttk.Label(frame1, text = "Nombre de usuario :", font = "arial 16 bold", background = "#77BEF0")
        user.place(x = 100, y = 250)
        self.username = ttk.Entry(frame1, font = "arial 16 bold", justify='center')
        self.username.place(x = 80, y = 290, width = 240, height = 40 )
    
        #---------------------------------------------------------------------------------
        #input pass
        password = ttk.Label(frame1, text = "Contraseña :",font = "arial 16 bold", background = "#77BEF0")
        password.place(x = 100, y = 340)
        self.pass_word = ttk.Entry(frame1, show='*', font = "arial 16 bold",  justify='center')
        self.pass_word.place(x = 80, y = 380, width = 240, height = 40 )
        
        #---------------------------------------------------------------------------------
        #boton aceptar
        
        # Login button
        btn1 = tk.Button(frame1, text='Iniciar', font = "arial 16 bold", command=self.login)
        btn1.place(x=100, y=440, width=200, height=40)

        # Register button
        btn2 = tk.Button(frame1, text='Registrar', font = "arial 16 bold", command=self.control2)
        btn2.place(x=100, y=500, width=200, height=40)

#---------------------------------------------------------------------------------           
class Registro(tk.Frame):
    
    db_name = "database.db"
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.controlador = controlador
        self.widgets()
    
    #---------------------------------------------------------------------------------       
    def validacion(self, user, clave):
        return len(user)> 0 and len(clave)
    
    #---------------------------------------------------------------------------------      
    def eje_consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit
                
        except sqlite3.Error as e:
             messagebox.showerror(title='Error', message='Error al ejecutar la consulta: {}'.format(e))
    
    #---------------------------------------------------------------------------------        
    def registro(self):
        user = self.username.get()
        pas = self.pass_word.get()
        key = self.key.get()
        
        if self.validacion(user, pas):
            if len(pas) < 6:
                messagebox.showinfo(title='Error', message='Contrasena demasiado corta')
                self.username.delete(0, 'end')
                self.pass_word.delete(0, 'end')
                
            else:
                
                if key == '1234':
                    consulta = 'INSERT INTO usuarios VALUES (?,?,?)'
                    parametros = (None, user, pas )
                    self.eje_consulta(consulta, parametros)
                    self.control1()
                else:
                    messagebox.showerror(title="Registro", message='Error al ingresar el codigo de registro')
        else:
            messagebox.showerror(title='Error', message='Llene sus datos')
     
    #---------------------------------------------------------------------------------        
    def control1(self):
        self.controlador.show_frame(Container)
        
        
    #--------------------------------------------------------------------------------- 
    def control2(self):
        self.controlador.show_frame(Login)
        
        
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
        
        self.logo_image = Image.open('media/icons/tienda.png')
        self.logo_image = self.logo_image.resize((200, 200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(frame1, image = self.logo_image)
        self.logo_label.place(x = 100, y = 20)
        
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
        btn3 = ttk.Button(frame1, text='Registarse', style='my.TButton', command=self.registro)
        btn3.place(x=80, y=520, width=240, height=40)

        # Register button
        btn4 = ttk.Button(frame1, text='Regresar', style='my.TButton',command=self.control2)
        btn4.place(x=80, y=570, width=240, height=40)