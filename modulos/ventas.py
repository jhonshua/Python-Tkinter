import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import threading
import sys
import os

class Ventas(tk.Frame):

    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.numero_factura = self.obtener_numero_factura_actual()
        self.productos_seleccionados = []
        self.widgets()
        self.cargar_productos()
        self.timer_producto = None
        

    def  obtener_numero_factura_actual(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = c.fetchone()[0]
            conn.close
            return last_invoice_number + 1 if last_invoice_number is not None else 1
        except sqlite3.Error as e:
            print("Error obteniendo el numero de la factura: ", e)
            return 1

    #---------------------------------------------------------------------------------

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT articulo FROM articulos")
            self.products = [product[0] for product in c.fetchall()]
            self.entry_producto['values'] = self.products
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando producto:", e)
    
    #---------------------------------------------------------------------------------

    def filtrar_productos(self, event):
        if self.timer_producto: 
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()
    
    #---------------------------------------------------------------------------------

    def _filter_products(self):
        typed = self.entry_producto.get()

        if typed == '':
            data == self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]

        if data:
            self.entry_producto['values'] = data
            self.entry_producto.event_generate('<Down>')
        else:
            self.entry_producto['value'] = ['No se encuentra resultado']
            self.entry_producto.event_generate('<Down>')
            self.entry_producto.delete(0, tk.END)

    #---------------------------------------------------------------------------------

    def agregar_articulos(self): 
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()

        if not cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente.")
        
        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")

        if not cantidad.isdigit() or int(cantidad) <= 0 :
            messagebox.showerror("Error", "Por favor ingrese una cantidad validad.")
            return
        
        cantidad = int(cantidad)
        cliente = self.entry_cliente.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio, costo, stock FROM articulos WHERE articulo=?",(producto,))
            resultado = c.fetchone()

            if resultado is None:
                messagebox.showerror("Error","Producto no encontrado")
                return
            precio, costo, stock = resultado

            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponiobles.")

            total = precio * cantidad
            total_cop = "{:,.0f}".format(total)

            self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, "{:,.0f}".format(precio), cantidad, total_cop))
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total_cop, costo))

            conn.close()

            self.entry_producto.set('')
            self.entry_cantidad.delete(0,'end')

        except sqlite3.Error as e:
            print("Error al agregar articulo", e)
            
        self.calcular_precio_total()
    
    #---------------------------------------------------------------------------------

    def calcular_precio_total(self):
        total_pagar = sum(float(str(self.tre.item(item)["values"][-1]).replace("", "").replace(",", ""))for item in self.tre.get_children())
        total_pagar_cop = "{:,.0f}".format(total_pagar)
        self.label_precio_total.config(text=f"Precio a Pagar: $ {total_pagar_cop}")
    
    #---------------------------------------------------------------------------------

    def actualizar_stock(self, event=None):
        producto_seleccionado = self.entry_producto.get()

        try :

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('SELECT stock FROM articulos WHERE articulo=?',(producto_seleccionado,))
            stock = c.fetchone()[0]
            conn.close()

            self.label_stock.config(text=f"Stock: {stock}")

        except sqlite3.Error as e:
            print("Error al obtener el stock del producto: ", e)
        
    #---------------------------------------------------------------------------------
    
    def realizar_pago(self):
        if not self.tre.get_children():
            messagebox.showerror("Error", ' No hay producto0s seleccionados para realizar el pago.')

        total_venta = sum(float(item[5].replace(" ", "").replace(",", "")) for item in self.productos_seleccionados)

        total_formateado = "{:,.0f}".format(total_venta)

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pagos")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift

        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 30 bold",bg="#C6D9E3")
        label_titulo.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total_formateado}", font="sans 14 bold",bg="#C6D9E3")
        label_total.place(x=80, y=100)

        label_monto = tk.Label(ventana_pago, text="Ingrese monto pagado", font="sans 14 bold",bg="#C6D9E3")
        label_monto.place(x=80, y=160)

        entry_monto = ttk.Entry( ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        button_confirmar_pago = tk.Button(ventana_pago, text="Confirmar pago", font="sans 14 bold", command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta))
        button_confirmar_pago.place(x=80, y=270,width=240,height=40)

    #---------------------------------------------------------------------------------

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
        cantidad_pagada = float(cantidad_pagada)
        cliente = self.entry_cliente.get()

        if cantidad_pagada < total_venta:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente. ")
            return
        
        cambio = cantidad_pagada - total_venta

        total_formateado = "{:,.0}".format(total_venta)

        mensaje = f"Total: {total_formateado}\nCantidad pagada: {cantidad_pagada:,.0f} \nCambio: {cambio:,.0f}"

        messagebox.showinfo("Pago realizado", mensaje)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total, costo = item
                c.execute("INSERT INTO ventas (factura, cliente, articulo, precio, cantidad, total, costo, fecha, hora) VALUES (?,?,?,?,?,?,?,?,?)",
                          (factura, cliente, producto, precio, cantidad, total.replace(" ", "").replace(",",""), costo * cantidad, fecha_actual, hora_actual))
                c.execute("UPDATE articulos SET stock = stock - ? WHERE articulo = ?", (cantidad, producto))
            
            conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror("Error",f"Error al registrar la venta : {e}")

        self.numero_factura += 1
        self.label_numero_factura.config(text=str(self.numero_factura))

        self.productos_seleccionados = []
        self.limpiar_campos()

        ventana_pago.destroy()

    #---------------------------------------------------------------------------------

    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text='Precio a pagar: $ 0')

        self.entry_producto.set('')
        self.entry_cantidad.delete(0, 'end')

    #---------------------------------------------------------------------------------

    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        self.calcular_precio_total()

    #---------------------------------------------------------------------------------

    def eliminar_articulo(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningun articulo seleccionado.")
            return
        
        item_id = item_seleccionado[0]
        valores_item = self.tre.item(item_id)["values"]
        factura, cliente, articulo, precio, cantidad, total = valores_item

        self.tre.delete(item_id)

        self.productos_seleccionados = [producto for producto in self.productos_seleccionados if producto[2] != articulo]

        self.calcular_precio_total()
    
    #---------------------------------------------------------------------------------

    def editar_articulo(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un articulo para editar")
            return
        
        item_values = self.tre.item(selected_item[0], "values")
        if not item_values:
            return
        
        current_producto = item_values[2]
        current_cantidad = item_values[4]

        new_cantidad = simpledialog.askinteger("Editar articulo", "ingresar la nueva cantidad:" , initialvalue=current_cantidad)

        if  new_cantidad is not None:
                try:
                    conn = sqlite3.connect(self.db_name)
                    c = conn.cursor()
                    c.execute("SELECT precio, costo, stock FROM articulos WHERE articulo=?", (current_producto,))
                    resultado = c.fetchone()

                    if resultado is None:
                        messagebox.showerror("Error", "Producto no encontrado")
                        
                    precio, costo, stock = resultado

                    if new_cantidad > stock:
                        messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles")
                        return
                
                    total = precio * new_cantidad
                    total_cop = "{:,.0f}".format(total)


                    self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cantidad.get(), current_producto, "{:,.0f}".format(precio), new_cantidad, total_cop))

                    for idx, producto in enumerate(self.productos_seleccionados):
                        if producto[2] == current_producto:
                            self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), current_producto, precio, new_cantidad, total_cop, costo)
                        break
                    conn.close()

                    self.calcular_precio_total()

                except sqlite3.Error as e:
                    print("Error al editar el articulo: ", e)

    #---------------------------------------------------------------------------------

    def ver_ventas_realizadas(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            ventas = c.fetchall()
            conn.close()

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.configure(bg='#C6D9E3')
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()

            def filtar_ventas():
                factura_a_buscar = entry_factura.get()
                cliente_a_buscar = entry_cliente.get()
                for item in tree.get_children():
                    tree.delete(item)

                ventas_filtradas = [
                    venta for venta in ventas
                    if (str(ventas[0])== factura_a_buscar or not factura_a_buscar) and
                    (venta[1].lower() == cliente_a_buscar.lower() or not cliente_a_buscar)
                ]

                for venta in venta in ventas_filtradas:
                    venta = list(venta)
                    venta[3] = "{:,.0f}".format(venta[3])
                    venta[5] = "{:,.0f}".format(venta[5])
                    venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strptime("%d-%m-%Y")
                    tree.insert("", "end", values=venta)

            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas realizadas", font='sans 14 bold', bg='#C6D9E3')
            label_ventas_realizadas.place(x=350, y=20)

            filtro_frame = tk.Frame(ventana_ventas, bg='#C6D9E3')
            filtro_frame.place(x=20, y=60, width=1060, height=60)

            label_factura = tk.Label(filtro_frame, text="Numero de factura", font='sans 14 bold', bg='#C6D9E3')
            label_factura.place(x=10, y=15)

            entry_factura = ttk.Entry(filtro_frame, font='sans 14 bold' )
            entry_factura.place(x=200, y=10, width=200, height=40)

            label_cliente = tk.Label(filtro_frame, text="Cliente", font='sans 14 bold', bg='#C6D9E3')
            label_cliente.place(x=420, y=15)

            entry_cliente= ttk.Entry(filtro_frame, font='sans 14 bold' )
            entry_cliente.place(x=620, y=10, width=200, height=40)

            btn_filtrar = tk.Button(filtro_frame, text="Filtar",font='sans 14 bold', command=filtar_ventas )
            btn_filtrar.place(x=840, y=10)


            tree_frame = tk.Frame(ventana_ventas, bg="white")
            tree_frame.place(x=20, y=130, width=1060, height=500)

            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)

            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", "Precio", " Cantidad", "Total", "Fecha", "Hora" ), show="headings")
            tree.pack(expand=True, fill=BOTH)

            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)


            tree.heading(0, text="Factura")  # Índice 0 para "Factura"
            tree.heading(1, text="Cliente")  # Índice 1 para "Cliente"
            tree.heading(2, text="Producto") # Índice 2 para "Producto"
            tree.heading(3, text="Precio") # Índice 3 para "Precio"
            tree.heading(4, text="Cantidad") # Índice 4 para "Cantidad"
            tree.heading(5, text="Total")   # Índice 5 para "Total"
            tree.heading(6, text="Fecha")   # Índice 6 para "Fecha"
            tree.heading(7, text="Hora")   # Índice 7 para "Hora"

            tree.column(0, width=60, anchor="center") # Índice 0 para "Factura"
            tree.column(1, width=120, anchor="center") # Índice 1 para "Cliente"
            tree.column(2, width=120, anchor="center") # Índice 2 para "Producto"
            tree.column(3, width=80, anchor="center") # Índice 3 para "Precio"
            tree.column(4, width=80, anchor="center") # Índice 4 para "Cantidad"
            tree.column(5, width=80, anchor="center") # Índice 5 para "Total"
            tree.column(6, width=80, anchor="center") # Índice 6 para "Fecha"
            tree.column(7, width=80, anchor="center") # Índice 7 para "Hora"

            for venta in ventas : 
                venta = list(venta)
                venta[3] = "{:,.0f}".format(venta[3])
                venta[5] = "{:,.0f}".format(venta[5])
                # venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strptime("%d-%m-%Y")
                tree.insert("", "end", values=venta)

        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al obtener las ventas : ", e)


    #---------------------------------------------------------------------------------

    def widgets(self):
        labelframe  = tk.LabelFrame(self, font='sans 12 bold', bg='#C6D9E3')
        labelframe.place(x=25, y=30, width=1045, height=180)
        
        label_Cliente = tk.Label(labelframe, text="Cliente: ", font='sans 14 bold', bg='#C6D9E3')
        label_Cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        
        label_producto = tk.Label(labelframe,text="Producto: ", font="sans 14 bold", bg='#C6D9E3' )
        label_producto.place(x = 10, y = 70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold" )
        self.entry_producto.place(x=120, y=66, width=260, height=40)
        self.entry_producto.bind('<KeyRelease>', self.filtrar_productos)
          
        label_cantidad = tk.Label(labelframe, text="cantidad: ", font='sans 14 bold', bg='#C6D9E3')
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)
        
        self.label_stock = tk.Label(labelframe, text="Stock: ", font='sans 14 bold', bg='#C6D9E3')
        self.label_stock.place(x=500, y=70)
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)
        
        label_factura = tk.Label(labelframe, text="Numero de Factura: ", font='sans 14 bold', bg='#C6D9E3')
        label_factura.place(x=750, y=11)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font='sans 14 bold', bg='#C6D9E3')
        self.label_numero_factura.config(fg="green") 
        self.label_numero_factura.place(x=950, y=11)
        
        boton_agregar = tk.Button(labelframe, text="Agregar Articulo", font='sans 14 bold',command=self.agregar_articulos)
        boton_agregar.place(x=90, y=120, height=40, width=200)
        
        boton_eliminar = tk.Button(labelframe, text="Eliminar Articulo", font='sans 14 bold', command= self.eliminar_articulo)
        boton_eliminar.place(x=310, y=120, height=40, width=200)
        
        boton_editar = tk.Button(labelframe, text="Editar Articulo", font='sans 14 bold', command=self.editar_articulo)
        boton_editar.place(x=530, y=120, height=40, width=200)
        
        boton_limpiar = tk.Button(labelframe, text="Limpiar lista", font='sans 14 bold', command= self.limpiar_lista)
        boton_limpiar.place(x=750, y=120, height=40, width=200)
        
        treFrame = tk.Frame(self, background='white')
        treFrame.place(x=70, y=220, width=980,height=300)
        
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=X)
        
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set,height=40, columns=('Factura','Cliente','Producto','Precio','Cantidad','Total'), show='headings')
        self.tre.pack(expand=True, fill=BOTH)

        scrol_x.config(command=self.tre.xview)
        scrol_y.config(command=self.tre.yview)

        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")

        self.label_precio_total = tk.Label(self, text='Precio a Pagar: $ 0', font='sans 18 bold', bg='#C6D9E3' )
        self.label_precio_total.place(x=680, y=550)

        boton_pagar = tk.Button(self, text="Pagar", font='sans 14 bold', command= self.realizar_pago)
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ver ventas realizadas", font='sans 14 bold', command=self.ver_ventas_realizadas)
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)

    #---------------------------------------------------------------------------------

    
