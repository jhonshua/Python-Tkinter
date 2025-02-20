from tkinter import *
from tkinter import ttk
from data.models import crear_base_de_datos
from PIL import Image, ImageTk

from modulos.login.login import Login, Registro
from container import Container

import sys
import os

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        self.title("Mi tienda v1.0")
        self.geometry("1200x800+420+20")
        self.resizable(False, False)
        self.iconbitmap("media/icons/mi_tienda.ico")

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure( width=1200, height=800)
        
        self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame
            
        # self.show_frame(Login)
        self.show_frame(Container)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")

        crear_base_de_datos()

    def show_frame(self, container):    
        frame = self.frames[container]   
        frame.tkraise()
        
def main():
    app = Manager()
    app.mainloop()
    
if __name__ == "__main__":
    main()