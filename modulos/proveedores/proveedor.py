import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk
from typing import Self

class Proveedor(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_registros()
        
    def widgets(self):
        self.labelframe = tk.LabelFrame(self, text="Proveedor", font="sans 20 bold", bg="#C6D9E3")
        self.labelframe.place(x=20, y=20, width=250,  height=560)

        lblnombre = tk.Label(self.labelframe, text="Empresa:", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.nombre.place(x=10, y=50, width=220, height=40)

        lblcedula = tk.Label(self.labelframe, text="RIF:", font="sans 14 bold", bg="#C6D9E3")
        lblcedula.place(x=10,y=100)
        self.cedula =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.cedula.place(x=10, y=130, width=220, height=40)


        bt0 = Button(self.labelframe, fg= "Black", text="Buscar", font="sans 16 bold", )
        bt0.place(x=10, y=370, width=220, height=40)

        bt1 = Button(self.labelframe, command=self.registrar_ventana_open, fg= "Black", text="Ingresar", font="sans 16 bold", )
        bt1.place(x=10, y=420, width=220, height=40)

        bt2 = Button(self.labelframe, fg="Black", text="Modificar", font="sans 16 bold",command=self.modificar)
        bt2.place(x=10, y=470, width=220, height=40)

        treFrame = Frame(self, bg="white")
        treFrame.place(x=280, y=20, width=850, height=720)

        Scrollbar_y = ttk.Scrollbar(treFrame)
        Scrollbar_y.pack(side = RIGHT, fill = Y)

        Scrollbar_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        Scrollbar_x.pack(side = BOTTOM, fill = X)

        self.tree = ttk.Treeview(treFrame, yscrollcommand = Scrollbar_y.set, xscrollcommand=Scrollbar_x.set, height=40, columns=("ID", "Empresa", "Rif", "Celular", "Direccion", "Correo"), show="headings")

        self.tree.pack(expand=True, fill=BOTH)

        Scrollbar_y.config(command=self.tree.yview)
        Scrollbar_x.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Empresa", text="Empresa")
        self.tree.heading("Rif", text="Rif")
        self.tree.heading("Celular", text="Celular")
        self.tree.heading("Direccion", text="Direccion")
        self.tree.heading("Correo", text="Correo")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Empresa", width=150, anchor="center")
        self.tree.column("Rif", width=120, anchor="center")
        self.tree.column("Celular", width=120, anchor="center")
        self.tree.column("Direccion", width=200, anchor="center")
        self.tree.column("Correo", width=200, anchor="center")

    #--------------------------------------------------------------------------------- 

    def  cargar_registros(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores")
            rows = cursor.fetchall()
            for row in rows :
                self.tree.insert("", "end", values = row) 
            conn.close()
        except sqlite3.Error as e:
             messagebox.showerror("Error", f"No se puedo cargar los registros: {e}")

    #--------------------------------------------------------------------------------- 

    def limpiar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    #---------------------------------------------------------------------------------

    def modificar(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Porfavor seleccione un proveedor para modificar")
            return
        item = self.tree.selection()[0]

        id_proveedor = self.tree.item(item, "values")[0]

        empresa_actual = self.tree.item(item, "value")[1]
        rif_actual = self.tree.item(item, "value")[2]
        celular_actual = self.tree.item(item, "value")[3]
        direccion_actual = self.tree.item(item, "value")[4]
        correo_actual = self.tree.item(item, "value")[5]

        top_modificar = Toplevel(self)
        top_modificar.title("Modificar proveedor")
        top_modificar.geometry("500x400+400+50")
        top_modificar.config(bg="#C6D9E3")
        top_modificar.resizable(False, False)
        top_modificar.grab_set()
        top_modificar.focus_set()
        top_modificar.lift()

        tk.Label(top_modificar, text="Empresa: ", font="sans 14 bold", bg="#C6D9E3").grid(row=0, column=0, padx=10, pady=5)
        empresa_modificar = tk.Entry(top_modificar, font="sans 14 bold")
        empresa_modificar.insert(0, empresa_actual)
        empresa_modificar.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="RIF: ", font="sans 14 bold", bg="#C6D9E3").grid(row=1, column=0, padx=10, pady=5)
        rif_modificar = tk.Entry(top_modificar, font="sans 14 bold")
        rif_modificar.insert(0, rif_actual)
        rif_modificar.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Celular: ", font="sans 14 bold", bg="#C6D9E3").grid(row=2, column=0, padx=10, pady=5)
        celular_modificar = tk.Entry(top_modificar, font="sans 14 bold")
        celular_modificar.insert(0, celular_actual)
        celular_modificar.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Direccion: ", font="sans 14 bold", bg="#C6D9E3").grid(row=3, column=0, padx=10, pady=5)
        direccion_modificar = tk.Entry(top_modificar, font="sans 14 bold")
        direccion_modificar.insert(0, direccion_actual)
        direccion_modificar.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Correo: ", font="sans 14 bold", bg="#C6D9E3").grid(row=4, column=0, padx=10, pady=5)
        correo_modificar = tk.Entry(top_modificar, font="sans 14 bold")
        correo_modificar.insert(0, correo_actual)
        correo_modificar.grid(row=4, column=1, padx=10, pady=5)
        

        def guardar_modificado():
            modificar_empresa= empresa_modificar.get()
            modificar_cedula = rif_modificar.get()
            modificar_celular = celular_modificar.get()
            modificar_direccion = direccion_modificar.get()
            modificar_correo =  correo_modificar.get()

            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("""UPDATE proveedores SET empresa = ?, rif = ?, celular = ?, direccion = ?, correo = ? WHERE id = ? """, ( modificar_empresa, modificar_cedula,modificar_celular, modificar_direccion, modificar_correo, id_proveedor))
                conn.commit()
                conn.close()
                messagebox.showinfo("Exito", "Cliente modificado correctamente")
                self.limpiar_treeview()
                self.cargar_registros()
                top_modificar.destroy()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente : {e}")

        btn_guardar = tk.Button(top_modificar,command=guardar_modificado, text="Guardar cambios" , font="sans 14 bold")
        btn_guardar.grid(row=5, column=1, columnspan=2, pady=20)

        btn_guardar = tk.Button(top_modificar, fg="white", bg="red", text="Eliminar proveedor" , font="sans 14 bold")
        btn_guardar.grid(row=6, column=1, columnspan=2, pady=20)

  
    #--------------------------------------------------------------------------------- 

    def registrar_empresa(self, empresa, rif, celular, direccion, correo, top_crear):
        
        if not empresa or not rif or not celular or not direccion or not correo:
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO proveedores (empresa, rif, celular, direccion, correo) VALUES (?,?,?,?,?)", (empresa, rif, celular, direccion, correo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Exito", "Cliente registrado correctamente")
            self.limpiar_treeview()
            self.cargar_registros()
            top_crear.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se puedo registar el cliente: {e}")

    
    def registrar_ventana_open(self):

        top_crear = Toplevel(self)
        top_crear.title("crear proveedor")
        top_crear.geometry("500x400+400+50")
        top_crear.config(bg="#C6D9E3")
        top_crear.resizable(False, False)
        top_crear.grab_set()
        top_crear.focus_set()
        top_crear.lift()

        tk.Label(top_crear, text="Empresa: ", font="sans 14 bold", bg="#C6D9E3").grid(row=0, column=0, padx=10, pady=5)
        empresa_nuevo = tk.Entry(top_crear, font="sans 14 bold")
        empresa_nuevo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_crear, text="RIF: ", font="sans 14 bold", bg="#C6D9E3").grid(row=1, column=0, padx=10, pady=5)
        rif_nuevo = tk.Entry(top_crear, font="sans 14 bold")
        rif_nuevo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_crear, text="Celular: ", font="sans 14 bold", bg="#C6D9E3").grid(row=2, column=0, padx=10, pady=5)
        celular_nuevo = tk.Entry(top_crear, font="sans 14 bold")
        celular_nuevo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_crear, text="Direccion: ", font="sans 14 bold", bg="#C6D9E3").grid(row=3, column=0, padx=10, pady=5)
        direccion_nuevo = tk.Entry(top_crear, font="sans 14 bold")
        direccion_nuevo.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_crear, text="Correo: ", font="sans 14 bold", bg="#C6D9E3").grid(row=4, column=0, padx=10, pady=5)
        correo_nuevo = tk.Entry(top_crear, font="sans 14 bold")
        correo_nuevo.grid(row=4, column=1, padx=10, pady=5)

        btn_guardar = tk.Button(top_crear, 
                           command=lambda: self.registrar_empresa(empresa_nuevo.get(), rif_nuevo.get(), celular_nuevo.get(), direccion_nuevo.get(), correo_nuevo.get(),top_crear), text="Guardar ", font="sans 14 bold")  
        btn_guardar.grid(row=5, column=1, columnspan=2, pady=20)

    #---------------------------------------------------------------------------------
      


