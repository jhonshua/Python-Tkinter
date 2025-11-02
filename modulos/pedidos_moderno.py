import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
from datetime import datetime

# Configurar CustomTkinter
ctk.set_appearance_mode("light")

class PedidosModerno(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre, bg=estilos.COLORS['bg_primary'])
        self.crear_tablas()
        self.widgets()
        # Cargar datos iniciales si las funciones existen
        if hasattr(self, 'cargar_pedidos'):
            self.cargar_pedidos()
        if hasattr(self, 'cargar_proveedores'):
            self.cargar_proveedores()
    
    def actualizar_moneda(self, nueva_moneda):
        """Actualizar precios cuando cambia la moneda"""
        try:
            # Recargar pedidos con nueva moneda
            self.cargar_pedidos()
            print(f"Módulo Pedidos actualizado a moneda: {nueva_moneda}")
        except Exception as e:
            print(f"Error al actualizar moneda en Pedidos: {e}")
        
    def crear_tablas(self):
        """Crear tablas de pedidos y detalles si no existen"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Tabla de pedidos a proveedores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos_proveedor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proveedor_nombre TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    estado TEXT DEFAULT 'Pendiente',
                    total REAL DEFAULT 0.0,
                    observaciones TEXT
                )
            ''')
            
            # Tabla de detalles de pedidos (productos solicitados)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos_detalle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id INTEGER,
                    producto_codigo TEXT NOT NULL,
                    producto_nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL DEFAULT 0.0,
                    subtotal REAL DEFAULT 0.0,
                    FOREIGN KEY (pedido_id) REFERENCES pedidos_proveedor (id)
                )
            ''')
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al crear tablas: {e}")
        
    def widgets(self):
        # Frame principal de formulario
        form_frame = tk.LabelFrame(self, text="📦 Pedidos a Proveedores", 
                                  font=('Segoe UI', 16, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['primary'])
        form_frame.place(x=20, y=20, width=320, height=720)

        # Título del formulario
        title_label = tk.Label(form_frame, text="📝 Pedido de Reposición", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg=estilos.COLORS['white'],
                              fg=estilos.COLORS['secondary'])
        title_label.place(x=10, y=10)

        # Campo Proveedor
        tk.Label(form_frame, text="🏢 Proveedor:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=10, y=50)
        
        self.proveedor_entry = tk.Entry(form_frame, font=('Segoe UI', 11), relief='solid', bd=1)
        self.proveedor_entry.place(x=10, y=80, width=290, height=35)

        # Campo Estado
        tk.Label(form_frame, text="📊 Estado:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=10, y=130)
        
        self.estado_combo = ttk.Combobox(form_frame, font=('Segoe UI', 11), 
                                        values=["Pendiente", "En Proceso", "Completado", "Cancelado"],
                                        state="readonly")
        self.estado_combo.set("Pendiente")
        self.estado_combo.place(x=10, y=160, width=290, height=35)

        # Campo Producto a Pedir
        tk.Label(form_frame, text="📦 Producto:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=10, y=210)
        
        self.producto_combo = ttk.Combobox(form_frame, font=('Segoe UI', 11), state="readonly")
        self.producto_combo.place(x=10, y=240, width=290, height=35)
        self.cargar_productos()
        
        # Campo Cantidad
        tk.Label(form_frame, text="🔢 Cantidad:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=10, y=290)
        
        self.cantidad = tk.Entry(form_frame, font=('Segoe UI', 12), relief='solid', bd=1)
        self.cantidad.place(x=10, y=320, width=140, height=35)
        
        # Campo Precio Unitario
        tk.Label(form_frame, text="💰 Precio:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=160, y=290)
        
        self.precio = tk.Entry(form_frame, font=('Segoe UI', 12), relief='solid', bd=1)
        self.precio.place(x=160, y=320, width=140, height=35)

        # Campo Observaciones
        tk.Label(form_frame, text="📝 Observaciones:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).place(x=10, y=370)
        
        self.observaciones = tk.Text(form_frame, font=('Segoe UI', 10), 
                                   relief='solid', bd=1, wrap='word')
        self.observaciones.place(x=10, y=400, width=290, height=60)

        # Botones modernos
        btn_crear = ctk.CTkButton(
            form_frame, 
            text="➕ Crear Pedido", 
            command=self.crear_pedido,
            width=290,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=estilos.COLORS['success'],
            hover_color="#28a745"
        )
        btn_crear.place(x=10, y=480)

        btn_modificar = ctk.CTkButton(
            form_frame, 
            text="✏️ Modificar Estado", 
            command=self.modificar_pedido,
            width=290,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=estilos.COLORS['warning'],
            hover_color="#ffc107"
        )
        btn_modificar.place(x=10, y=540)

        btn_recibir = ctk.CTkButton(
            form_frame, 
            text="📥 Recibir Pedido", 
            command=self.recibir_pedido,
            width=290,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=estilos.COLORS['info'],
            hover_color="#0ea5e9"
        )
        btn_recibir.place(x=10, y=600)
        
        # Etiqueta de estadísticas dentro del form_frame
        self.stats_label = tk.Label(form_frame, text="Total pedidos: 0", 
                                   font=('Segoe UI', 10, 'bold'), 
                                   bg=estilos.COLORS['white'],
                                   fg=estilos.COLORS['primary'])
        self.stats_label.place(x=10, y=660)

        # Frame para la tabla
        table_frame = tk.LabelFrame(self, text="📋 Lista de Pedidos", 
                                   font=('Segoe UI', 16, 'bold'), 
                                   bg=estilos.COLORS['white'],
                                   fg=estilos.COLORS['primary'])
        table_frame.place(x=360, y=20, width=860, height=720)

        # Configurar Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                       background=estilos.COLORS['white'],
                       foreground=estilos.COLORS['dark'],
                       fieldbackground=estilos.COLORS['white'],
                       font=('Segoe UI', 10))
        
        style.configure("Treeview.Heading",
                       background=estilos.COLORS['primary'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'))
        
        style.map('Treeview',
                 background=[('selected', estilos.COLORS['primary'])],
                 foreground=[('selected', 'white')])

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame, orient='vertical')
        scrollbar_y.pack(side='right', fill='y')

        scrollbar_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')

        # Treeview
        self.tree = ttk.Treeview(table_frame, 
                                yscrollcommand=scrollbar_y.set, 
                                xscrollcommand=scrollbar_x.set,
                                columns=("ID", "Cliente", "Fecha", "Estado", "Total", "Observaciones"), 
                                show="headings",
                                height=30)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Configurar encabezados
        self.tree.heading("ID", text="🆔 ID")
        self.tree.heading("Cliente", text="🏢 Proveedor")
        self.tree.heading("Fecha", text="📅 Fecha")
        self.tree.heading("Estado", text="📊 Estado")
        self.tree.heading("Total", text="💰 Total")
        self.tree.heading("Observaciones", text="📝 Observaciones")

        # Configurar columnas
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Cliente", width=150, anchor="w")
        self.tree.column("Fecha", width=120, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")
        self.tree.column("Total", width=100, anchor="e")
        self.tree.column("Observaciones", width=200, anchor="w")

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def cargar_productos(self):
        """Cargar productos en el combobox"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre FROM productos ORDER BY nombre")
            productos = cursor.fetchall()
            
            producto_list = [f"{producto[0]} - {producto[1]}" for producto in productos]
            self.producto_combo['values'] = producto_list
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar productos: {e}")

    def crear_pedido(self):
        """Crear un nuevo pedido a proveedor"""
        if not self.proveedor_entry.get().strip():
            messagebox.showerror("❌ Error", "Debe ingresar el nombre del proveedor")
            return
        
        if not self.producto_combo.get():
            messagebox.showerror("❌ Error", "Debe seleccionar un producto")
            return
            
        if not self.cantidad.get().strip() or not self.precio.get().strip():
            messagebox.showerror("❌ Error", "Debe ingresar cantidad y precio")
            return

        try:
            # Extraer información del producto
            producto_info = self.producto_combo.get()
            producto_codigo = producto_info.split(' - ')[0]
            producto_nombre = producto_info.split(' - ')[1]
            
            proveedor_nombre = self.proveedor_entry.get().strip()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            estado = self.estado_combo.get()
            cantidad = int(self.cantidad.get())
            precio_unitario = float(self.precio.get())
            subtotal = cantidad * precio_unitario
            observaciones = self.observaciones.get("1.0", "end-1c")

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Crear pedido principal
            cursor.execute("""INSERT INTO pedidos_proveedor (proveedor_nombre, fecha, estado, total, observaciones) 
                            VALUES (?,?,?,?,?)""", 
                          (proveedor_nombre, fecha, estado, subtotal, observaciones))
            
            pedido_id = cursor.lastrowid
            
            # Crear detalle del pedido
            cursor.execute("""INSERT INTO pedidos_detalle (pedido_id, producto_codigo, producto_nombre, 
                            cantidad, precio_unitario, subtotal) VALUES (?,?,?,?,?,?)""", 
                          (pedido_id, producto_codigo, producto_nombre, cantidad, precio_unitario, subtotal))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("✅ Éxito", f"Pedido creado correctamente\nTotal: ${subtotal:.2f}")
            self.limpiar_campos()
            self.limpiar_treeview()
            self.cargar_registros()

        except ValueError:
            messagebox.showerror("❌ Error", "Cantidad y precio deben ser números válidos")
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al crear pedido: {e}")

    def cargar_registros(self):
        """Cargar todos los pedidos"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos_proveedor ORDER BY fecha DESC")
            rows = cursor.fetchall()
            
            for row in rows:
                # Formatear el total como moneda
                total_formateado = f"${row[4]:.2f}"
                row_formateada = list(row)
                row_formateada[4] = total_formateado
                self.tree.insert("", "end", values=row_formateada)
            
            if hasattr(self, 'stats_label'):
                self.stats_label.config(text=f"Total pedidos: {len(rows)}")
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar pedidos: {e}")

    def limpiar_treeview(self):
        """Limpiar el Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def limpiar_campos(self):
        """Limpiar todos los campos"""
        self.proveedor_entry.delete(0, 'end')
        self.producto_combo.set("")
        self.estado_combo.set("Pendiente")
        self.cantidad.delete(0, 'end')
        self.precio.delete(0, 'end')
        self.observaciones.delete("1.0", 'end')

    def on_select(self, event):
        """Manejar selección en el Treeview"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            
            if len(values) >= 6:
                # Llenar campos con datos del pedido seleccionado
                self.proveedor_entry.delete(0, 'end')
                self.proveedor_entry.insert(0, values[1])  # Proveedor
                self.estado_combo.set(values[3])  # Estado
                self.observaciones.delete("1.0", 'end')
                self.observaciones.insert("1.0", values[5])  # Observaciones
                
                # Cargar detalles del pedido
                self.cargar_detalle_pedido(values[0])  # ID del pedido

    def modificar_pedido(self):
        """Modificar estado del pedido seleccionado"""
        if not self.tree.selection():
            messagebox.showerror("❌ Error", "Seleccione un pedido para modificar")
            return

        try:
            item = self.tree.selection()[0]
            pedido_id = self.tree.item(item, "values")[0]
            nuevo_estado = self.estado_combo.get()
            observaciones = self.observaciones.get("1.0", "end-1c")

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""UPDATE pedidos_proveedor SET estado=?, observaciones=? WHERE id=?""", 
                          (nuevo_estado, observaciones, pedido_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("✅ Éxito", f"Estado del pedido actualizado a: {nuevo_estado}")
            self.limpiar_campos()
            self.limpiar_treeview()
            self.cargar_registros()

        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al modificar pedido: {e}")

    def recibir_pedido(self):
        """Recibir pedido y actualizar inventario"""
        if not self.tree.selection():
            messagebox.showerror("❌ Error", "Seleccione un pedido para recibir")
            return

        item = self.tree.selection()[0]
        pedido_id = self.tree.item(item, "values")[0]
        proveedor_nombre = self.tree.item(item, "values")[1]
        estado_actual = self.tree.item(item, "values")[3]
        
        if estado_actual == "Completado":
            messagebox.showwarning("⚠️ Advertencia", "Este pedido ya fue recibido")
            return
        
        respuesta = messagebox.askyesno("📥 Confirmar Recepción", 
                                      f"¿Marcar como recibido el pedido del proveedor '{proveedor_nombre}'?\n\nEsto actualizará el inventario automáticamente.")
        
        if respuesta:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                
                # Obtener detalles del pedido
                cursor.execute("SELECT producto_codigo, cantidad FROM pedidos_detalle WHERE pedido_id=?", (pedido_id,))
                detalles = cursor.fetchall()
                
                # Actualizar inventario para cada producto
                for detalle in detalles:
                    producto_codigo, cantidad = detalle
                    cursor.execute("""UPDATE productos SET stock = stock + ? WHERE codigo = ?""", 
                                 (cantidad, producto_codigo))
                
                # Marcar pedido como completado
                cursor.execute("UPDATE pedidos_proveedor SET estado='Completado' WHERE id=?", (pedido_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("✅ Éxito", f"Pedido recibido correctamente\nInventario actualizado para {len(detalles)} producto(s)")
                self.limpiar_campos()
                self.limpiar_treeview()
                self.cargar_registros()
                
            except sqlite3.Error as e:
                messagebox.showerror("❌ Error", f"Error al recibir pedido: {e}")
    
    def cargar_detalle_pedido(self, pedido_id):
        """Cargar el primer producto del pedido en el formulario"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT producto_codigo, producto_nombre, cantidad, precio_unitario 
                            FROM pedidos_detalle WHERE pedido_id=? LIMIT 1""", (pedido_id,))
            detalle = cursor.fetchone()
            
            if detalle:
                producto_codigo, producto_nombre, cantidad, precio_unitario = detalle
                # Buscar el producto en el combo
                producto_texto = f"{producto_codigo} - {producto_nombre}"
                for producto in self.producto_combo['values']:
                    if producto_codigo in producto:
                        self.producto_combo.set(producto)
                        break
                
                self.cantidad.delete(0, 'end')
                self.cantidad.insert(0, str(cantidad))
                self.precio.delete(0, 'end')
                self.precio.insert(0, str(precio_unitario))
            
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar detalle: {e}")
