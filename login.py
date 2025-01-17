from tkinter import *
import tkinter as tk

class Login(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.widgets()
        
    def widgets(self):
        pass
    
class Registro(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.widgets()
        
    def widgets(self):
        pass