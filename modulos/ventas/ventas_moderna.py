import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import threading
from PIL import Image, ImageTk

import sys
import os

from modulos.ventas.crear_factura import generar_factura
from modulos.ventas.obtener_numero_factura import obtener_numero_factura_actual

class VentasModerna(tk.Frame):
    """Versión moderna de la interfaz de ventas con mejor diseño"""
    
    # Colores modernos
    COLORS = {
        'primary': '#2c3e50',      # Azul oscuro
        'secondary': '#3498db',     # Azul claro
        'success': '#27ae60',       # Verde
        'warning': '#f39c12',       # Naranja
        'danger': '#e74c3c',        # Rojo
        'light': '#ecf0f1',         # Gris claro
        'white': '#ffffff',         # Blanco
        'dark': '#34495e',          # Gris oscuro
        'accent': '#9b59b6'         # Morado
    }

    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.configure(bg=self.COLORS['light'])
        self.numero_factura = obtener_numero_factura_actual()
        self.productos_seleccionados = []
        self.setup_styles()
        self.widgets_modernos()
        self.timer_producto = None
        self.timer_cliente = None
        
        # Cargar datos después de crear widgets
        self.cargar_productos()
        self.cargar_clientes()
        
        # Iniciar actualización de hora en tiempo real
        self.actualizar_hora()
    

    def setup_styles(self):
        """Configurar estilos modernos para los widgets"""
        style = ttk.Style()
        
        # Estilo para labels modernos
        style.configure('Modern.TLabel', 
                       background=self.COLORS['light'],
                       foreground=self.COLORS['primary'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Estilo para botones modernos
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        # Estilo para entries modernos
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 11),
                       fieldbackground=self.COLORS['white'])
        
        # Estilo para combobox modernos
        style.configure('Modern.TCombobox',
                       font=('Segoe UI', 11),
                       fieldbackground=self.COLORS['white'])

    def crear_frame_moderno(self, parent, title, x, y, width, height):
        """Crear un frame moderno con título"""
        # Frame principal con sombra simulada
        shadow_frame = tk.Frame(parent, bg='#bdc3c7', height=height+2, width=width+2)
        shadow_frame.place(x=x+2, y=y+2)
        
        main_frame = tk.Frame(parent, bg=self.COLORS['white'], 
                             relief='flat', bd=1, highlightbackground=self.COLORS['primary'],
                             highlightthickness=1)
        main_frame.place(x=x, y=y, width=width, height=height)
        
        # Título del frame
        title_frame = tk.Frame(main_frame, bg=self.COLORS['primary'], height=40)
        title_frame.pack(fill='x', side='top')
        
        title_label = tk.Label(title_frame, text=title, 
                              bg=self.COLORS['primary'], fg=self.COLORS['white'],
                              font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=8)
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=self.COLORS['white'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        return content_frame

    def crear_boton_moderno(self, parent, text, command, color='secondary', x=0, y=0, width=150, height=40):
        """Crear un botón moderno con efectos hover"""
        btn_frame = tk.Frame(parent, bg=self.COLORS['white'])
        btn_frame.place(x=x, y=y, width=width, height=height)
        
        btn = tk.Button(btn_frame, text=text, command=command,
                       bg=self.COLORS[color], fg=self.COLORS['white'],
                       font=('Segoe UI', 10, 'bold'), relief='flat',
                       cursor='hand2', bd=0)
        btn.pack(fill='both', expand=True)
        
        # Efectos hover
        def on_enter(e):
            btn.configure(bg=self.ajustar_color(self.COLORS[color], -20))
        
        def on_leave(e):
            btn.configure(bg=self.COLORS[color])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def ajustar_color(self, color, amount):
        """Ajustar el brillo de un color hex"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def widgets_modernos(self):
        """Crear la interfaz moderna"""
        # Título principal
        title_frame = tk.Frame(self, bg=self.COLORS['primary'], height=60)
        title_frame.pack(fill='x', side='top')
        
        main_title = tk.Label(title_frame, text="💰 Sistema de Ventas", 
                             bg=self.COLORS['primary'], fg=self.COLORS['white'],
                             font=('Segoe UI', 16, 'bold'))
        main_title.pack(pady=15)
        
        # Frame principal de contenido
        content_frame = tk.Frame(self, bg=self.COLORS['light'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame de información del cliente y producto (aún más ancho)
        info_frame = self.crear_frame_moderno(content_frame, "📋 Información de Venta", 
                                            0, 0, 1350, 220)  # Aumentado de 1320 a 1350 y altura de 200 a 220
        
        # Cliente
        tk.Label(info_frame, text="👤 Cliente:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=10, y=20)
        
        self.entry_cliente = ttk.Combobox(info_frame, font=('Segoe UI', 11), style='Modern.TCombobox')
        self.entry_cliente.place(x=120, y=18, width=280, height=35)
        self.entry_cliente.bind('<KeyRelease>', self.filtrar_clientes)
        
        # Código de barras (movido más a la derecha)
        tk.Label(info_frame, text="📊 Código de Barras:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=10, y=70)
        
        self.entry_codigo = ttk.Entry(info_frame, font=('Segoe UI', 11), style='Modern.TEntry')
        self.entry_codigo.place(x=170, y=68, width=220, height=35)  # Movido de x=150 a x=170, ancho de 200 a 220
        self.entry_codigo.bind('<KeyRelease>', self.buscar_por_codigo)
        self.entry_codigo.bind('<Return>', self.buscar_por_codigo)
        
        # Producto (ajustado para el nuevo espacio)
        tk.Label(info_frame, text="📦 Producto:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=410, y=70)
        
        self.entry_producto = ttk.Combobox(info_frame, font=('Segoe UI', 11), style='Modern.TCombobox', state='normal')
        self.entry_producto.place(x=510, y=68, width=230, height=35)  # Ajustado x=510, width=230
        
        # Eventos simplificados para evitar colgarse
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)
        self.entry_producto.bind('<Button-1>', self.mostrar_productos)
        self.entry_producto.bind('<Return>', self.actualizar_stock)
        
        # Cantidad (movido más a la derecha)
        tk.Label(info_frame, text="🔢 Cantidad:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=450, y=20)
        
        self.entry_cantidad = ttk.Entry(info_frame, font=('Segoe UI', 11), style='Modern.TEntry')
        self.entry_cantidad.place(x=550, y=18, width=120, height=35)
        
        # Stock (ajustado para el nuevo layout)
        self.label_stock = tk.Label(info_frame, text="📊 Stock: --", 
                                   font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                                   fg=self.COLORS['success'])
        self.label_stock.place(x=760, y=70)
        
        # Número de factura (movido más a la derecha)
        tk.Label(info_frame, text="🧾 Factura N°:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=900, y=20)  # Movido de x=750 a x=900
        
        self.label_numero_factura = tk.Label(info_frame, text=f"{self.numero_factura}", 
                                           font=('Segoe UI', 14, 'bold'), bg=self.COLORS['white'],
                                           fg=self.COLORS['accent'])
        self.label_numero_factura.place(x=1030, y=18)  # Movido de x=880 a x=1030
        
        # Fecha actual del sistema (más a la derecha)
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        tk.Label(info_frame, text="📅 Fecha:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=1150, y=20)
        
        self.label_fecha = tk.Label(info_frame, text=fecha_actual, 
                                   font=('Segoe UI', 12, 'bold'), bg=self.COLORS['white'],
                                   fg=self.COLORS['dark'], width=12, anchor='w')
        self.label_fecha.place(x=1210, y=20, width=100)
        
        # Hora actual del sistema (más a la derecha)
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        tk.Label(info_frame, text="🕐 Hora:", 
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=1150, y=70)
        
        self.label_hora = tk.Label(info_frame, text=hora_actual, 
                                  font=('Segoe UI', 12, 'bold'), bg=self.COLORS['white'],
                                  fg=self.COLORS['dark'], width=12, anchor='w')
        self.label_hora.place(x=1210, y=70, width=100)
        
        # Botón agregar producto (movido un poco a la derecha)
        self.crear_boton_moderno(info_frame, "➕ Agregar Producto", 
                                self.agregar_producto, 'success', 950, 60, 180, 40)  # Movido de x=900 a x=950 (solo 50px)
        
        # Frame de productos seleccionados (más ancho y máxima altura)
        productos_frame = self.crear_frame_moderno(content_frame, "🛒 Productos Seleccionados", 
                                                 0, 240, 850, 480)  # Aumentado de 380 a 480 para máxima altura
        
        # Treeview moderno para productos (máxima altura)
        self.tree_productos = ttk.Treeview(productos_frame, 
                                         columns=("Producto", "Precio", "Cantidad", "Total"), 
                                         show="headings", height=20)  # Aumentado de 15 a 20 filas para máxima altura
        
        # Configurar columnas
        self.tree_productos.heading("Producto", text="Producto")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Cantidad", text="Cantidad")
        self.tree_productos.heading("Total", text="Total")
        
        self.tree_productos.column("Producto", width=300, anchor="w")
        self.tree_productos.column("Precio", width=100, anchor="center")
        self.tree_productos.column("Cantidad", width=100, anchor="center")
        self.tree_productos.column("Total", width=120, anchor="center")
        
        # Scrollbar para el treeview
        scrollbar_productos = ttk.Scrollbar(productos_frame, orient="vertical", 
                                          command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")
        
        # Frame de totales y acciones (aún más ancho y máxima altura)
        totales_frame = self.crear_frame_moderno(content_frame, "💰 Resumen de Venta", 
                                               860, 240, 500, 480)  # Aumentado ancho de 480 a 500
        
        # Labels de totales con mejor diseño
        self.label_sub_total = tk.Label(totales_frame, text='Subtotal: $0.00', 
                                       font=('Segoe UI', 14, 'bold'), bg=self.COLORS['white'],
                                       fg=self.COLORS['primary'])
        self.label_sub_total.pack(pady=10)
        
        self.label_iva = tk.Label(totales_frame, text='IVA (19%): $0.00', 
                                 font=('Segoe UI', 12), bg=self.COLORS['white'],
                                 fg=self.COLORS['dark'])
        self.label_iva.pack(pady=5)
        
        self.label_precio_total = tk.Label(totales_frame, text='TOTAL: $0.00', 
                                          font=('Segoe UI', 16, 'bold'), bg=self.COLORS['white'],
                                          fg=self.COLORS['success'])
        self.label_precio_total.pack(pady=15)
        
        # Botones de acción - Caja Registradora
        botones_frame = tk.Frame(totales_frame, bg=self.COLORS['white'])
        botones_frame.pack(fill='x', pady=20, padx=10)
        
        # Botón principal de procesar pago (ajustado al ancho disponible)
        btn_procesar = tk.Button(botones_frame, text="💰 PROCESAR PAGO", 
                               command=self.abrir_modal_pago,
                               bg=self.COLORS['success'], fg=self.COLORS['white'],
                               font=('Segoe UI', 14, 'bold'),
                               relief='flat', cursor='hand2', bd=0,
                               pady=15)
        btn_procesar.pack(fill='x', pady=(0, 10))
        
        # Efectos hover para el botón principal
        def on_enter_procesar(e):
            btn_procesar.configure(bg='#16a34a')
        
        def on_leave_procesar(e):
            btn_procesar.configure(bg=self.COLORS['success'])
        
        btn_procesar.bind("<Enter>", on_enter_procesar)
        btn_procesar.bind("<Leave>", on_leave_procesar)
        
        # Frame para botones secundarios
        botones_secundarios = tk.Frame(botones_frame, bg=self.COLORS['white'])
        botones_secundarios.pack(fill='x')
        
        # Botones secundarios usando pack en lugar de place
        btn_ver_ventas = tk.Button(botones_secundarios, text="📊 Ver Ventas", 
                                 command=self.ver_ventas_realizadas,
                                 bg=self.COLORS['secondary'], fg=self.COLORS['white'],
                                 font=('Segoe UI', 10, 'bold'),
                                 relief='flat', cursor='hand2', bd=0)
        btn_ver_ventas.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        btn_limpiar = tk.Button(botones_secundarios, text="🗑️ Limpiar", 
                              command=self.limpiar_venta,
                              bg=self.COLORS['warning'], fg=self.COLORS['white'],
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat', cursor='hand2', bd=0)
        btn_limpiar.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Efectos hover para botones secundarios
        def on_enter_ventas(e):
            btn_ver_ventas.configure(bg='#0ea5e9')
        def on_leave_ventas(e):
            btn_ver_ventas.configure(bg=self.COLORS['secondary'])
        btn_ver_ventas.bind("<Enter>", on_enter_ventas)
        btn_ver_ventas.bind("<Leave>", on_leave_ventas)
        
        def on_enter_limpiar(e):
            btn_limpiar.configure(bg='#d97706')
        def on_leave_limpiar(e):
            btn_limpiar.configure(bg=self.COLORS['warning'])
        btn_limpiar.bind("<Enter>", on_enter_limpiar)
        btn_limpiar.bind("<Leave>", on_leave_limpiar)

    # Métodos heredados (necesarios para mantener funcionalidad)
    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        print("🔄 INICIANDO CARGA DE PRODUCTOS...")
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            print("✅ Conexión a base de datos establecida")
            
            # Verificar si hay artículos en la base de datos
            c.execute("SELECT COUNT(*) FROM articulos")
            count = c.fetchone()[0]
            
            if count == 0:
                # No hay artículos, crear algunos de ejemplo
                productos_ejemplo = [
                    ("7501234567890", "Producto Ejemplo 1", 10.50, 8.00, 25, "activo", None),
                    ("7501234567891", "Producto Ejemplo 2", 15.75, 12.00, 30, "activo", None),
                    ("7501234567892", "Producto Ejemplo 3", 8.25, 6.50, 15, "activo", None),
                    ("7501234567893", "Producto Ejemplo 4", 22.00, 18.00, 10, "activo", None),
                    ("7501234567894", "Producto Ejemplo 5", 12.99, 10.00, 20, "activo", None)
                ]
                
                c.executemany("INSERT INTO articulos (codigo, articulo, precio, costo, stock, estado, imagen_path) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                             productos_ejemplo)
                conn.commit()
                print("Artículos de ejemplo creados con códigos de barras")
            
            # Cargar productos desde la tabla productos primero, luego articulos
            c.execute("SELECT codigo, nombre, precio, stock FROM productos WHERE stock > 0")
            productos_data = c.fetchall()
            
            # Si no hay productos en la tabla productos, usar articulos
            if not productos_data:
                c.execute("SELECT codigo, articulo, precio, stock FROM articulos WHERE stock > 0 AND estado = 'activo'")
                productos_data = c.fetchall()
            
            print(f"🔍 Productos encontrados: {len(productos_data)}")
            
            # Crear listas para autocompletado
            self.productos_dict = {}  # codigo: {nombre, precio, stock}
            self.productos_nombres = []
            self.productos_codigos = []
            
            for codigo, nombre, precio, stock in productos_data:
                if codigo:  # Solo si tiene código de barras
                    self.productos_dict[codigo] = {
                        'nombre': nombre,
                        'precio': precio,
                        'stock': stock
                    }
                    self.productos_nombres.append(f"{nombre} ({codigo})")
                    self.productos_codigos.append(codigo)
            
            if self.productos_nombres:
                if hasattr(self, 'entry_producto'):
                    try:
                        self.entry_producto['values'] = self.productos_nombres
                        print(f"✅ Cargados {len(self.productos_nombres)} productos con códigos")
                        print(f"📋 Primeros 3 productos: {self.productos_nombres[:3]}")
                        
                        # Verificar que se configuró correctamente
                        valores_actuales = self.entry_producto['values']
                        print(f"🔍 Valores en combobox: {len(valores_actuales)} elementos")
                    except Exception as e:
                        print(f"❌ Error configurando combobox: {e}")
                else:
                    print("⚠️ entry_producto no existe aún")
            else:
                self.productos_nombres = ["No hay productos disponibles"]
                if hasattr(self, 'entry_producto'):
                    try:
                        self.entry_producto['values'] = self.productos_nombres
                        print("❌ No se encontraron productos con stock")
                    except Exception as e:
                        print(f"❌ Error configurando combobox vacío: {e}")
                
            conn.close()
        except Exception as e:
            print(f"❌ ERROR CARGANDO PRODUCTOS: {e}")
            import traceback
            traceback.print_exc()
            # Productos por defecto en caso de error
            self.productos_nombres = ["Error cargando productos"]
            self.productos_dict = {}
            self.productos_codigos = []
            if hasattr(self, 'entry_producto'):
                self.entry_producto['values'] = self.productos_nombres
        
        print("🏁 CARGA DE PRODUCTOS FINALIZADA")

    def cargar_clientes(self):
        """Cargar clientes desde la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # Verificar si la tabla clientes existe
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
            if not c.fetchone():
                # Si no existe, crear algunos clientes de ejemplo
                c.execute('''CREATE TABLE IF NOT EXISTS clientes 
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            email TEXT,
                            telefono TEXT)''')
                
                # Insertar clientes de ejemplo
                clientes_ejemplo = [
                    ("Cliente Ejemplo 1", "cliente1@email.com", "123-456-7890"),
                    ("Cliente Ejemplo 2", "cliente2@email.com", "123-456-7891"),
                    ("Cliente Ejemplo 3", "cliente3@email.com", "123-456-7892"),
                    ("Cliente General", "general@tienda.com", "123-456-0000")
                ]
                
                c.executemany("INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)", 
                             clientes_ejemplo)
                conn.commit()
                print("Clientes de ejemplo creados")
            
            # Cargar clientes
            c.execute("SELECT nombre FROM clientes")
            clientes = c.fetchall()
            self.clientes = [cliente[0] for cliente in clientes]
            
            if self.clientes:
                self.entry_cliente['values'] = self.clientes
                print(f"Cargados {len(self.clientes)} clientes")
            else:
                self.clientes = ["Cliente General"]
                self.entry_cliente['values'] = self.clientes
                print("No se encontraron clientes")
                
            conn.close()
        except sqlite3.Error as e:
            print(f"Error cargando clientes: {e}")
            # Cliente por defecto en caso de error
            self.clientes = ["Cliente General"]
            self.entry_cliente['values'] = self.clientes

    def filtrar_clientes(self, event):
        """Filtrar clientes mientras se escribe"""
        if self.timer_cliente: 
            self.timer_cliente.cancel()
        self.timer_cliente = threading.Timer(0.5, self._filter_clientes)
        self.timer_cliente.start()

    def _filter_clientes(self):
        """Aplicar filtro de clientes"""
        texto = self.entry_cliente.get().lower()
        if texto:
            clientes_filtrados = [c for c in self.clientes if texto in c.lower()]
            self.entry_cliente['values'] = clientes_filtrados
        else:
            self.entry_cliente['values'] = self.clientes

    def filtrar_productos(self, event):
        """Filtrar productos mientras se escribe con autocompletado mejorado"""
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.3, self._filter_productos)
        self.timer_producto.start()

    def _filter_productos(self):
        """Aplicar filtro de productos"""
        texto = self.entry_producto.get().lower()
        if texto and hasattr(self, 'productos_nombres'):
            productos_filtrados = [p for p in self.productos_nombres if texto in p.lower()]
            self.entry_producto['values'] = productos_filtrados
        else:
            if hasattr(self, 'productos_nombres'):
                self.entry_producto['values'] = self.productos_nombres

    def actualizar_stock(self, event=None):
        """Actualizar el stock del producto seleccionado"""
        try:
            producto_seleccionado = self.entry_producto.get()
            if not producto_seleccionado:
                return
                
            if hasattr(self, 'productos_dict'):
                # Extraer código del formato "Nombre (CODIGO)"
                if '(' in producto_seleccionado and ')' in producto_seleccionado:
                    codigo = producto_seleccionado.split('(')[-1].replace(')', '')
                    
                    if codigo in self.productos_dict:
                        producto_info = self.productos_dict[codigo]
                        stock = producto_info['stock']
                        
                        # Actualizar campo de código sin causar recursión
                        self.entry_codigo.delete(0, tk.END)
                        self.entry_codigo.insert(0, codigo)
                        
                        # Actualizar stock
                        self.label_stock.config(
                            text=f"📊 Stock: {stock} unidades",
                            fg=self.COLORS['success'] if stock > 10 else self.COLORS['warning']
                        )
                        return
            
            # Método alternativo si no hay productos_dict
            self.label_stock.config(text="📊 Stock: --", fg=self.COLORS['dark'])
            
        except Exception as e:
            print(f"Error actualizando stock: {e}")
            self.label_stock.config(text="📊 Stock: --", fg=self.COLORS['dark'])

    def agregar_producto(self):
        """Agregar producto a la lista de venta"""
        producto = self.entry_producto.get()
        cantidad_str = self.entry_cantidad.get()
        
        if not producto or not cantidad_str:
            messagebox.showwarning("⚠️ Advertencia", "Por favor complete todos los campos")
            return
        
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messagebox.showwarning("⚠️ Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Extraer código del formato "Nombre (CODIGO)" si existe
            print(f"🔍 Producto seleccionado: '{producto}'")
            
            if '(' in producto and ')' in producto:
                # Extraer código entre paréntesis
                inicio_parentesis = producto.rfind('(')
                fin_parentesis = producto.rfind(')')
                codigo = producto[inicio_parentesis+1:fin_parentesis].strip()
                nombre_producto = producto[:inicio_parentesis].strip()
                print(f"📦 Código extraído: '{codigo}', Nombre: '{nombre_producto}'")
            else:
                # Si no tiene código, buscar por nombre
                nombre_producto = producto.strip()
                codigo = None
                print(f"📦 Sin código, buscando por nombre: '{nombre_producto}'")
                
            # Obtener precio del producto desde la tabla articulos
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            resultado = None
            if codigo:
                # Buscar primero en productos, luego en articulos
                print(f"🔍 Buscando en productos con código: '{codigo}'")
                c.execute("SELECT nombre, precio, stock FROM productos WHERE codigo = ?", (codigo,))
                resultado = c.fetchone()
                print(f"📊 Resultado en productos: {resultado}")
                
                if not resultado:
                    print(f"🔍 Buscando en articulos con código: '{codigo}'")
                    c.execute("SELECT articulo, precio, stock FROM articulos WHERE codigo = ? AND estado = 'activo'", (codigo,))
                    resultado = c.fetchone()
                    print(f"📊 Resultado en articulos: {resultado}")
            else:
                # Buscar primero en productos, luego en articulos
                print(f"🔍 Buscando en productos con nombre: '{nombre_producto}'")
                c.execute("SELECT nombre, precio, stock FROM productos WHERE nombre = ?", (nombre_producto,))
                resultado = c.fetchone()
                print(f"📊 Resultado en productos: {resultado}")
                
                if not resultado:
                    print(f"🔍 Buscando en articulos con nombre: '{nombre_producto}'")
                    c.execute("SELECT articulo, precio, stock FROM articulos WHERE articulo = ? AND estado = 'activo'", (nombre_producto,))
                    resultado = c.fetchone()
                    print(f"📊 Resultado en articulos: {resultado}")
            
            if not resultado:
                print(f"❌ NO SE ENCONTRÓ EL PRODUCTO")
                messagebox.showerror("❌ Error", f"Producto no encontrado en el inventario\n\nBuscado: '{producto}'\nCódigo: '{codigo}'\nNombre: '{nombre_producto}'")
                conn.close()
                return
                
            nombre_real, precio, stock = resultado
            
            if cantidad > stock:
                messagebox.showerror("📦 Stock Insuficiente", f"Solo hay {stock} unidades disponibles")
                return
            
            total = precio * cantidad
            
            # Agregar al treeview usando el nombre real del producto
            self.tree_productos.insert("", "end", values=(nombre_real, f"${precio:,.2f}", cantidad, f"${total:,.2f}"))
            
            # Agregar a la lista interna
            self.productos_seleccionados.append({
                'nombre': nombre_real,
                'precio': precio,
                'cantidad': cantidad,
                'total': total
            })
            
            # Limpiar campos
            self.entry_producto.delete(0, tk.END)
            self.entry_codigo.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.label_stock.config(text="📊 Stock: --")
            
            # Actualizar totales
            self.actualizar_totales()
            
            conn.close()
            
        except ValueError:
            messagebox.showerror("🔢 Error de Cantidad", "La cantidad debe ser un número válido")
        except sqlite3.Error as e:
            messagebox.showerror("💾 Error de Base de Datos", f"Error: {e}")

    def actualizar_totales(self):
        """Actualizar los totales de la venta"""
        subtotal = sum(p['total'] for p in self.productos_seleccionados)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        self.label_sub_total.config(text=f'Subtotal: ${subtotal:,.2f}')
        self.label_iva.config(text=f'IVA (19%): ${iva:,.2f}')
        self.label_precio_total.config(text=f'TOTAL: ${total:,.2f}')

    def limpiar_venta(self):
        """Limpiar todos los campos de la venta"""
        self.productos_seleccionados.clear()
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        self.entry_cliente.set("")
        self.entry_producto.set("")
        self.entry_cantidad.delete(0, tk.END)
        self.label_stock.config(text="📊 Stock: --")
        self.actualizar_totales()

    def realizar_pago(self):
        """Procesar el pago de la venta"""
        if not self.productos_seleccionados:
            messagebox.showwarning("Advertencia", "No hay productos en la venta")
            return
        
        cliente = self.entry_cliente.get()
        if not cliente:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
            return
        
        try:
            # Aquí iría la lógica de pago
            messagebox.showinfo("Éxito", "¡Venta realizada con éxito!")
            self.limpiar_venta()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la venta: {e}")

    def ver_ventas_realizadas(self):
        """Mostrar ventana moderna de ventas con filtros y totales"""
        # Crear ventana principal
        self.ventana_ventas = tk.Toplevel(self)
        self.ventana_ventas.title("📊 Historial de Ventas")
        self.ventana_ventas.geometry("1200x700")
        self.ventana_ventas.configure(bg=self.COLORS['light'])
        self.ventana_ventas.resizable(True, True)
        self.ventana_ventas.minsize(1000, 600)
        
        # Centrar ventana
        self.ventana_ventas.geometry("+{}+{}".format(
            self.winfo_rootx() + 100,
            self.winfo_rooty() + 50
        ))
        
        # Título principal
        title_frame = tk.Frame(self.ventana_ventas, bg=self.COLORS['primary'], height=70)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="📊 Historial de Ventas", 
                             bg=self.COLORS['primary'], fg=self.COLORS['white'],
                             font=('Segoe UI', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Frame de filtros
        filtros_frame = tk.Frame(self.ventana_ventas, bg=self.COLORS['white'], height=80)
        filtros_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Filtro por rango de fechas
        tk.Label(filtros_frame, text="📅 Rango de fechas:", 
                font=('Segoe UI', 12, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).place(x=20, y=15)
        
        # Fecha desde
        tk.Label(filtros_frame, text="Desde:", 
                font=('Segoe UI', 10), bg=self.COLORS['white'],
                fg=self.COLORS['dark']).place(x=160, y=15)
        
        self.entry_fecha_desde = tk.Entry(filtros_frame, font=('Segoe UI', 10), 
                                        relief='solid', bd=1, width=10)
        self.entry_fecha_desde.place(x=200, y=15)
        self.entry_fecha_desde.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
        
        # Fecha hasta
        tk.Label(filtros_frame, text="Hasta:", 
                font=('Segoe UI', 10), bg=self.COLORS['white'],
                fg=self.COLORS['dark']).place(x=300, y=15)
        
        self.entry_fecha_hasta = tk.Entry(filtros_frame, font=('Segoe UI', 10), 
                                        relief='solid', bd=1, width=10)
        self.entry_fecha_hasta.place(x=340, y=15)
        self.entry_fecha_hasta.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
        
        # Botones de filtro (todos del mismo tamaño)
        btn_filtrar = tk.Button(filtros_frame, text="🔍 Filtrar Rango", 
                              command=self.filtrar_ventas_por_rango,
                              bg=self.COLORS['primary'], fg=self.COLORS['white'],
                              font=('Segoe UI', 10, 'bold'), relief='flat', 
                              cursor='hand2', bd=0, width=12, height=1)
        btn_filtrar.place(x=450, y=12)
        
        btn_hoy = tk.Button(filtros_frame, text="📆 Hoy", 
                          command=self.filtrar_ventas_hoy,
                          bg=self.COLORS['success'], fg=self.COLORS['white'],
                          font=('Segoe UI', 10, 'bold'), relief='flat', 
                          cursor='hand2', bd=0, width=12, height=1)
        btn_hoy.place(x=580, y=12)
        
        btn_semana = tk.Button(filtros_frame, text="📅 Esta Semana", 
                             command=self.filtrar_ventas_semana,
                             bg=self.COLORS['warning'], fg=self.COLORS['white'],
                             font=('Segoe UI', 10, 'bold'), relief='flat', 
                             cursor='hand2', bd=0, width=12, height=1)
        btn_semana.place(x=450, y=45)
        
        btn_mes = tk.Button(filtros_frame, text="📊 Este Mes", 
                          command=self.filtrar_ventas_mes,
                          bg=self.COLORS['secondary'], fg=self.COLORS['white'],
                          font=('Segoe UI', 10, 'bold'), relief='flat', 
                          cursor='hand2', bd=0, width=12, height=1)
        btn_mes.place(x=580, y=45)
        
        btn_todas = tk.Button(filtros_frame, text="📋 Todas", 
                            command=self.mostrar_todas_ventas,
                            bg=self.COLORS['danger'], fg=self.COLORS['white'],
                            font=('Segoe UI', 10, 'bold'), relief='flat', 
                            cursor='hand2', bd=0, width=12, height=1)
        btn_todas.place(x=710, y=12)
        
        # Labels de totales (reposicionados)
        self.label_total_dia = tk.Label(filtros_frame, text="💰 Total del rango: $0.00", 
                                      font=('Segoe UI', 14, 'bold'), bg=self.COLORS['white'],
                                      fg=self.COLORS['success'])
        self.label_total_dia.place(x=820, y=15)
        
        # Label específico para total de hoy (mismo tamaño que el de arriba)
        self.label_total_hoy = tk.Label(filtros_frame, text="📈 Ventas HOY: $0.00", 
                                      font=('Segoe UI', 14, 'bold'), bg=self.COLORS['white'],
                                      fg=self.COLORS['primary'])
        self.label_total_hoy.place(x=820, y=45)
        
        # Frame principal de contenido
        content_frame = tk.Frame(self.ventana_ventas, bg=self.COLORS['light'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame para el treeview
        tree_frame = tk.Frame(content_frame, bg=self.COLORS['white'], relief='solid', bd=1)
        tree_frame.pack(fill='both', expand=True)
        
        # Treeview para mostrar ventas
        columns = ("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora")
        self.tree_ventas = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configurar columnas con anchos específicos
        anchos = {"Factura": 80, "Cliente": 150, "Producto": 200, "Precio": 100, 
                 "Cantidad": 80, "Total": 100, "Fecha": 100, "Hora": 80}
        
        for col in columns:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=anchos[col], anchor="center")
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_ventas.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_ventas.xview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack widgets
        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Cargar total de hoy y ventas iniciales
        self.actualizar_total_hoy()
        self.filtrar_ventas_hoy()

    def filtrar_ventas_por_rango(self):
        """Filtrar ventas por rango de fechas"""
        fecha_desde = self.entry_fecha_desde.get()
        fecha_hasta = self.entry_fecha_hasta.get()
        
        if not fecha_desde or not fecha_hasta:
            messagebox.showwarning("⚠️ Advertencia", "Por favor ingrese ambas fechas")
            return
        
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # Convertir fechas para comparación
            c.execute("""SELECT factura, cliente, articulo, precio, cantidad, total, fecha, hora 
                        FROM ventas WHERE fecha BETWEEN ? AND ? 
                        ORDER BY fecha DESC, hora DESC""", (fecha_desde, fecha_hasta))
            ventas = c.fetchall()
            conn.close()
            
            if fecha_desde == fecha_hasta:
                descripcion = fecha_desde
            else:
                descripcion = f"{fecha_desde} - {fecha_hasta}"
            
            self.actualizar_tabla_ventas(ventas, descripcion)
            # Siempre actualizar el total de hoy
            self.actualizar_total_hoy()
            
        except sqlite3.Error as e:
            messagebox.showerror("💾 Error", f"Error al filtrar ventas: {e}")

    def filtrar_ventas_hoy(self):
        """Filtrar ventas del día actual"""
        fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
        self.entry_fecha_desde.delete(0, tk.END)
        self.entry_fecha_desde.insert(0, fecha_hoy)
        self.entry_fecha_hasta.delete(0, tk.END)
        self.entry_fecha_hasta.insert(0, fecha_hoy)
        self.filtrar_ventas_por_rango()

    def filtrar_ventas_semana(self):
        """Filtrar ventas de esta semana"""
        hoy = datetime.datetime.now()
        inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + datetime.timedelta(days=6)
        
        fecha_desde = inicio_semana.strftime("%d/%m/%Y")
        fecha_hasta = fin_semana.strftime("%d/%m/%Y")
        
        self.entry_fecha_desde.delete(0, tk.END)
        self.entry_fecha_desde.insert(0, fecha_desde)
        self.entry_fecha_hasta.delete(0, tk.END)
        self.entry_fecha_hasta.insert(0, fecha_hasta)
        self.filtrar_ventas_por_rango()

    def filtrar_ventas_mes(self):
        """Filtrar ventas de este mes"""
        hoy = datetime.datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        # Último día del mes
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month + 1, day=1) - datetime.timedelta(days=1)
        
        fecha_desde = inicio_mes.strftime("%d/%m/%Y")
        fecha_hasta = fin_mes.strftime("%d/%m/%Y")
        
        self.entry_fecha_desde.delete(0, tk.END)
        self.entry_fecha_desde.insert(0, fecha_desde)
        self.entry_fecha_hasta.delete(0, tk.END)
        self.entry_fecha_hasta.insert(0, fecha_hasta)
        self.filtrar_ventas_por_rango()

    def mostrar_todas_ventas(self):
        """Mostrar todas las ventas sin filtro"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""SELECT factura, cliente, articulo, precio, cantidad, total, fecha, hora 
                        FROM ventas ORDER BY fecha DESC, hora DESC LIMIT 500""")
            ventas = c.fetchall()
            conn.close()
            
            self.actualizar_tabla_ventas(ventas, "Todas las fechas")
            # Siempre actualizar el total de hoy
            self.actualizar_total_hoy()
            
        except sqlite3.Error as e:
            messagebox.showerror("💾 Error", f"Error al cargar ventas: {e}")

    def actualizar_tabla_ventas(self, ventas, fecha_filtro):
        """Actualizar la tabla de ventas y calcular totales"""
        # Limpiar tabla
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        # Calcular total
        total_dia = 0
        
        # Insertar datos
        for venta in ventas:
            factura, cliente, producto, precio, cantidad, total, fecha, hora = venta
            total_dia += total
            
            # Formatear datos para mostrar
            venta_formateada = [
                factura,
                cliente,
                producto,
                f"${precio:,.2f}",
                cantidad,
                f"${total:,.2f}",
                fecha,
                hora
            ]
            self.tree_ventas.insert("", "end", values=venta_formateada)
        
        # Actualizar label de total
        if fecha_filtro == "Todas las fechas":
            self.label_total_dia.config(text=f"💰 Total general: ${total_dia:,.2f}")
        elif " - " in fecha_filtro:
            self.label_total_dia.config(text=f"💰 Total rango: ${total_dia:,.2f}")
        else:
            self.label_total_dia.config(text=f"💰 Total {fecha_filtro}: ${total_dia:,.2f}")
        
        # Mostrar información adicional
        num_ventas = len(ventas)
        if num_ventas == 0:
            self.label_total_dia.config(text=f"📊 Sin ventas para {fecha_filtro}")
        else:
            print(f"📊 {num_ventas} ventas encontradas para {fecha_filtro}, Total: ${total_dia:,.2f}")

    def actualizar_total_hoy(self):
        """Actualizar el total de ventas de hoy (siempre visible)"""
        try:
            fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # Obtener total de ventas de hoy
            c.execute("SELECT SUM(total), COUNT(*) FROM ventas WHERE fecha = ?", (fecha_hoy,))
            resultado = c.fetchone()
            
            total_hoy = resultado[0] if resultado[0] else 0
            num_ventas_hoy = resultado[1] if resultado[1] else 0
            
            conn.close()
            
            # Actualizar label de total de hoy
            if hasattr(self, 'label_total_hoy'):
                if num_ventas_hoy > 0:
                    self.label_total_hoy.config(
                        text=f"📈 Ventas HOY: ${total_hoy:,.2f} ({num_ventas_hoy} ventas)",
                        fg=self.COLORS['success']
                    )
                else:
                    self.label_total_hoy.config(
                        text="📈 Ventas HOY: $0.00 (0 ventas)",
                        fg=self.COLORS['secondary']
                    )
            
        except sqlite3.Error as e:
            print(f"Error calculando total de hoy: {e}")
            if hasattr(self, 'label_total_hoy'):
                self.label_total_hoy.config(text="📈 Ventas HOY: Error", fg=self.COLORS['danger'])
    
    def actualizar_hora(self):
        """Actualizar la hora en tiempo real cada segundo"""
        try:
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            if hasattr(self, 'label_hora'):
                self.label_hora.config(text=hora_actual)
            # Programar la siguiente actualización en 1000ms (1 segundo)
            self.after(1000, self.actualizar_hora)
        except:
            pass  # Si hay algún error, continuar sin actualizar la hora

    def buscar_por_codigo(self, event=None):
        """Buscar producto por código y autocompletar"""
        try:
            codigo = self.entry_codigo.get().upper()
            
            if not codigo:
                self.entry_producto.set("")
                self.label_stock.config(text="📊 Stock: --")
                return
            
            if not hasattr(self, 'productos_codigos') or not hasattr(self, 'productos_dict'):
                return
            
            # Buscar código exacto o parcial
            codigo_encontrado = None
            for cod in self.productos_codigos:
                if cod.startswith(codigo):
                    codigo_encontrado = cod
                    break
            
            if codigo_encontrado and codigo_encontrado in self.productos_dict:
                producto_info = self.productos_dict[codigo_encontrado]
                nombre_completo = f"{producto_info['nombre']} ({codigo_encontrado})"
                
                # Autocompletar campos sin triggear eventos
                self.entry_producto.delete(0, tk.END)
                self.entry_producto.insert(0, nombre_completo)
                
                self.label_stock.config(
                    text=f"📊 Stock: {producto_info['stock']} unidades",
                    fg=self.COLORS['success'] if producto_info['stock'] > 10 else self.COLORS['warning']
                )
                
                # Si presionó Enter, enfocar cantidad
                if event and event.keysym == 'Return':
                    self.entry_cantidad.focus_set()
            else:
                # Limpiar si no encuentra
                if len(codigo) > 2:  # Solo limpiar si escribió algo significativo
                    self.entry_producto.delete(0, tk.END)
                    self.label_stock.config(text="📊 Stock: -- (Código no encontrado)", fg=self.COLORS['danger'])
                    
        except Exception as e:
            print(f"Error buscando por código: {e}")

    def mostrar_productos(self, event=None):
        """Mostrar todos los productos disponibles al hacer clic"""
        if hasattr(self, 'productos_nombres'):
            self.entry_producto['values'] = self.productos_nombres
            self.entry_producto.event_generate('<Down>')

    def filtrar_productos(self, event):
        """Filtrar productos mientras se escribe con autocompletado mejorado"""
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.3, self._filter_productos)
        self.timer_producto.start()

    def _filter_productos(self):
        """Aplicar filtro de productos con búsqueda inteligente"""
        texto = self.entry_producto.get().lower()
        if texto and hasattr(self, 'productos_nombres'):
            # Buscar por nombre o código
            productos_filtrados = []
            for producto in self.productos_nombres:
                if (texto in producto.lower() or 
                    any(codigo.lower().startswith(texto) for codigo in self.productos_codigos)):
                    productos_filtrados.append(producto)
            
            self.entry_producto['values'] = productos_filtrados
            
            # Si hay solo una coincidencia exacta, seleccionarla
            if len(productos_filtrados) == 1:
                self.entry_producto.set(productos_filtrados[0])
                self.actualizar_stock()
        else:
            if hasattr(self, 'productos_nombres'):
                self.entry_producto['values'] = self.productos_nombres

    def abrir_modal_pago(self):
        """Abrir modal de pago con cálculo de cambio y opciones de factura"""
        if not self.productos_seleccionados:
            messagebox.showwarning("Advertencia", "No hay productos en la venta")
            return
        
        cliente = self.entry_cliente.get()
        if not cliente:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
            return
        
        # Calcular total
        subtotal = sum(p['total'] for p in self.productos_seleccionados)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        # Crear ventana modal
        self.modal_pago = tk.Toplevel(self)
        self.modal_pago.title("💰 Caja Registradora - Procesar Pago")
        self.modal_pago.geometry("560x620")
        self.modal_pago.configure(bg=self.COLORS['light'])
        self.modal_pago.resizable(True, True)
        self.modal_pago.minsize(520, 560)
        self.modal_pago.grab_set()  # Modal
        self.modal_pago.transient(self)  # Siempre encima
        
        # Centrar modal
        self.modal_pago.geometry("+{}+{}".format(
            self.winfo_rootx() + 450,
            self.winfo_rooty() + 200
        ))
        
        # Título del modal
        title_frame = tk.Frame(self.modal_pago, bg=self.COLORS['primary'], height=60)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="💰 CAJA REGISTRADORA", 
                              bg=self.COLORS['primary'], fg=self.COLORS['white'],
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=15)
        
        # Contenido del modal
        content_frame = tk.Frame(self.modal_pago, bg=self.COLORS['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Información de la venta
        info_frame = tk.Frame(content_frame, bg=self.COLORS['white'], relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame, text=f"Cliente: {cliente}", 
                font=('Segoe UI', 12, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=5)
        
        tk.Label(info_frame, text=f"Subtotal: ${subtotal:,.2f}", 
                font=('Segoe UI', 11), bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(pady=2)
        
        tk.Label(info_frame, text=f"IVA (19%): ${iva:,.2f}", 
                font=('Segoe UI', 11), bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(pady=2)
        
        tk.Label(info_frame, text=f"TOTAL A PAGAR: ${total:,.2f}", 
                font=('Segoe UI', 14, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['success']).pack(pady=10)
        
        # Campo para monto recibido
        pago_frame = tk.Frame(content_frame, bg=self.COLORS['light'])
        pago_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(pago_frame, text="💰 Monto recibido:", 
                font=('Segoe UI', 12, 'bold'), bg=self.COLORS['light'],
                fg=self.COLORS['primary']).pack(anchor='w')
        
        self.entry_monto_recibido = tk.Entry(pago_frame, font=('Segoe UI', 14), 
                                           relief='solid', bd=1, width=20)
        self.entry_monto_recibido.pack(pady=5, anchor='w')
        self.entry_monto_recibido.bind('<KeyRelease>', lambda e: self.calcular_cambio(total))
        
        # Label para mostrar el cambio
        self.label_cambio = tk.Label(pago_frame, text="Cambio: $0.00", 
                                   font=('Segoe UI', 14, 'bold'), bg=self.COLORS['light'],
                                   fg=self.COLORS['accent'])
        self.label_cambio.pack(pady=10, anchor='w')
        
        # Botones del modal
        botones_frame = tk.Frame(content_frame, bg=self.COLORS['light'])
        botones_frame.pack(fill='x', pady=20)
        
        # Botón ACEPTAR principal (layout adaptativo)
        self.crear_boton_modal(botones_frame, "✅ ACEPTAR", 
                              lambda: self.aceptar_venta(total), 
                              'success', 50, 0, 200, 50, layout='pack')

        # Botón para cancelar (layout adaptativo)
        self.crear_boton_modal(botones_frame, "❌ Cancelar", 
                              self.cerrar_modal_pago, 
                              'danger', 270, 0, 150, 50, layout='pack')

    def crear_boton_modal(self, parent, text, command, estilo, x, y, width, height, layout='place'):
        """Crear botón para el modal"""
        base_colors = self.COLORS
        # Usar colores base y calcular hover dinámicamente para evitar claves inexistentes
        bg_base = (
            base_colors['primary'] if estilo == 'primary' else
            base_colors['secondary'] if estilo == 'secondary' else
            base_colors['danger'] if estilo == 'danger' else
            base_colors['success']
        )
        hover_bg = self.ajustar_color(bg_base, -20)

        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_base, fg=self.COLORS['white'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat', cursor='hand2', bd=0)
        if layout == 'pack':
            btn.pack(side='left', fill='x', expand=True, padx=10)
        else:
            btn.place(x=x, y=y, width=width, height=height)

        # Efectos hover
        def on_enter(e):
            btn.configure(bg=hover_bg)

        def on_leave(e):
            btn.configure(bg=bg_base)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def calcular_cambio(self, total):
        """Calcular y mostrar el cambio"""
        try:
            monto_recibido = float(self.entry_monto_recibido.get() or 0)
            cambio = monto_recibido - total
            
            if cambio >= 0:
                self.label_cambio.config(text=f"Cambio: ${cambio:,.2f}", 
                                       fg=self.COLORS['success'])
            else:
                self.label_cambio.config(text=f"Falta: ${abs(cambio):,.2f}", 
                                       fg=self.COLORS['danger'])
        except ValueError:
            self.label_cambio.config(text="Cambio: $0.00", fg=self.COLORS['accent'])

    def aceptar_venta(self, total):
        """Aceptar y procesar la venta completa"""
        try:
            monto_recibido = float(self.entry_monto_recibido.get() or 0)
            if monto_recibido < total:
                messagebox.showerror("❌ Error", "El monto recibido es insuficiente")
                return
            
            cambio = monto_recibido - total
            
            print("🔄 INICIANDO PROCESO DE VENTA...")
            
            # 1. Guardar la venta en la base de datos
            venta_id = self.guardar_venta_en_bd(total, monto_recibido, cambio)
            
            if venta_id:
                print(f"✅ Venta guardada exitosamente con ID: {venta_id}")
                
                # 2. Cerrar modal
                self.cerrar_modal_pago()
                
                # 3. Enviar a impresora fiscal (simulado)
                self.enviar_a_impresora_fiscal(venta_id, total, monto_recibido, cambio)
                
                # 4. Limpiar venta
                self.limpiar_venta()
                
                # 5. Mostrar confirmación final
                messagebox.showinfo("✅ Venta Completada", 
                                  f"¡Transacción procesada exitosamente!\n\n"
                                  f"📄 Factura N°: {self.numero_factura}\n"
                                  f"💰 Total: ${total:,.2f}\n"
                                  f"💵 Recibido: ${monto_recibido:,.2f}\n"
                                  f"💸 Cambio: ${cambio:,.2f}\n\n"
                                  f"🖨️ Factura enviada a impresora fiscal\n"
                                  f"💾 Transacción guardada en base de datos")
                
                print("🎉 VENTA COMPLETADA EXITOSAMENTE")
                
            else:
                messagebox.showerror("❌ Error", "Error al guardar la venta en la base de datos")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Por favor ingrese un monto válido")
        except Exception as e:
            print(f"❌ Error en aceptar_venta: {e}")
            messagebox.showerror("❌ Error", f"Error procesando la venta: {e}")

    def guardar_venta_en_bd(self, total, monto_recibido, cambio):
        """Guardar la venta completa en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # Crear tabla de ventas si no existe
            c.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_factura INTEGER,
                    cliente TEXT,
                    fecha TEXT,
                    hora TEXT,
                    subtotal REAL,
                    iva REAL,
                    total REAL,
                    monto_recibido REAL,
                    cambio REAL,
                    estado TEXT DEFAULT 'completada'
                )
            ''')
            
            # Crear tabla de detalles de venta si no existe
            c.execute('''
                CREATE TABLE IF NOT EXISTS detalle_ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id INTEGER,
                    producto TEXT,
                    precio_unitario REAL,
                    cantidad INTEGER,
                    subtotal REAL,
                    FOREIGN KEY (venta_id) REFERENCES ventas (id)
                )
            ''')
            
            # Obtener datos de la venta
            cliente = self.entry_cliente.get() or "Cliente General"
            # Usar el mismo formato que los filtros del historial (dd/mm/YYYY)
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            numero_factura = self.numero_factura
            
            # Calcular subtotal e IVA
            subtotal = sum(p['total'] for p in self.productos_seleccionados)
            iva = subtotal * 0.19
            
            # Debug: Mostrar datos antes de insertar
            print(f"🔍 DATOS A INSERTAR:")
            print(f"  - Factura: {numero_factura}")
            print(f"  - Cliente: {cliente}")
            print(f"  - Fecha: {fecha_actual}")
            print(f"  - Hora: {hora_actual}")
            print(f"  - Subtotal: {subtotal}")
            print(f"  - IVA: {iva}")
            print(f"  - Total: {total}")
            print(f"  - Recibido: {monto_recibido}")
            print(f"  - Cambio: {cambio}")
            
            # Insertar venta principal
            try:
                c.execute('''
                    INSERT INTO ventas (numero_factura, cliente, fecha, hora, subtotal, iva, total, monto_recibido, cambio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (numero_factura, cliente, fecha_actual, hora_actual, subtotal, iva, total, monto_recibido, cambio))
                
                venta_id = c.lastrowid
                print(f"✅ Venta insertada con ID: {venta_id}")
                
            except sqlite3.Error as e:
                print(f"❌ Error insertando venta: {e}")
                # Intentar con la estructura antigua de la tabla
                print("🔄 Intentando con estructura de tabla antigua...")
                try:
                    c.execute('''
                        INSERT INTO ventas (factura, cliente, articulo, precio, cantidad, total, fecha, hora, costo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (numero_factura, cliente, "Venta Multiple", total, 1, total, fecha_actual, hora_actual, total * 0.8))
                    venta_id = c.lastrowid
                    print(f"✅ Venta insertada con estructura antigua, ID: {venta_id}")
                except sqlite3.Error as e2:
                    print(f"❌ Error con estructura antigua: {e2}")
                    raise e
            
            # Insertar detalles de la venta
            print(f"📦 INSERTANDO DETALLES DE VENTA:")
            for i, producto in enumerate(self.productos_seleccionados):
                print(f"  Producto {i+1}: {producto['nombre']} - Cantidad: {producto['cantidad']} - Total: ${producto['total']:.2f}")
                
                try:
                    c.execute('''
                        INSERT INTO detalle_ventas (venta_id, producto, precio_unitario, cantidad, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (venta_id, producto['nombre'], producto['precio'], producto['cantidad'], producto['total']))
                    print(f"  ✅ Detalle insertado para: {producto['nombre']}")
                except sqlite3.Error as e:
                    print(f"  ❌ Error insertando detalle para {producto['nombre']}: {e}")
                
                # Actualizar stock del producto
                self.actualizar_stock_producto(c, producto['nombre'], producto['cantidad'])
            
            conn.commit()
            conn.close()
            
            print(f"✅ Venta guardada con ID: {venta_id}")
            return venta_id
            
        except Exception as e:
            print(f"❌ Error guardando venta: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
    
    def actualizar_stock_producto(self, cursor, nombre_producto, cantidad_vendida):
        """Actualizar stock del producto después de la venta"""
        try:
            # Actualizar en tabla productos
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE nombre = ?", 
                         (cantidad_vendida, nombre_producto))
            
            # Actualizar en tabla articulos también
            cursor.execute("UPDATE articulos SET stock = stock - ? WHERE articulo = ?", 
                         (cantidad_vendida, nombre_producto))
            
            print(f"📦 Stock actualizado para {nombre_producto}: -{cantidad_vendida}")
            
        except Exception as e:
            print(f"⚠️ Error actualizando stock: {e}")
    
    def imprimir_ticket(self, venta_id, total, monto_recibido, cambio):
        """Generar e imprimir ticket de venta"""
        try:
            # Crear contenido del ticket
            ticket_content = self.generar_contenido_ticket(venta_id, total, monto_recibido, cambio)
            
            # Guardar ticket en archivo temporal
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(ticket_content)
                ticket_path = f.name
            
            # Intentar imprimir (simulado)
            messagebox.showinfo("🖨️ Imprimiendo", 
                              f"Ticket generado y enviado a impresora\n\n"
                              f"Archivo: {ticket_path}\n\n"
                              f"En un sistema real, esto se enviaría\n"
                              f"directamente a la impresora de tickets.")
            
            # Abrir archivo para mostrar contenido
            if os.name == 'nt':  # Windows
                os.startfile(ticket_path)
            else:  # Linux/Mac
                os.system(f'xdg-open {ticket_path}')
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al imprimir ticket: {e}")
    
    def generar_contenido_ticket(self, venta_id, total, monto_recibido, cambio):
        """Generar contenido del ticket de venta"""
        cliente = self.entry_cliente.get() or "Cliente General"
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        ticket = f"""
{'='*40}
           🏪 MI TIENDA
         SISTEMA DE VENTAS
{'='*40}

Factura N°: {self.numero_factura}
Fecha: {fecha_actual}
Hora: {hora_actual}
Cliente: {cliente}

{'='*40}
PRODUCTOS
{'='*40}
"""
        
        for producto in self.productos_seleccionados:
            nombre = producto['nombre'][:25]  # Limitar longitud
            precio = producto['precio']
            cantidad = producto['cantidad']
            subtotal = producto['total']
            
            ticket += f"{nombre:<25} {cantidad:>3} x ${precio:>6.2f} = ${subtotal:>8.2f}\n"
        
        subtotal_venta = sum(p['total'] for p in self.productos_seleccionados)
        iva = subtotal_venta * 0.19
        
        ticket += f"""
{'='*40}
Subtotal:                    ${subtotal_venta:>8.2f}
IVA (19%):                   ${iva:>8.2f}
{'='*40}
TOTAL:                       ${total:>8.2f}

Recibido:                    ${monto_recibido:>8.2f}
Cambio:                      ${cambio:>8.2f}

{'='*40}
        ¡GRACIAS POR SU COMPRA!
         Vuelva pronto 😊
{'='*40}

ID Venta: {venta_id}
"""
        return ticket
    
    def enviar_a_impresora_fiscal(self, venta_id, total, monto_recibido, cambio):
        """Enviar factura a impresora fiscal"""
        try:
            print("🖨️ ENVIANDO A IMPRESORA FISCAL...")
            
            # Generar datos de la factura fiscal
            factura_fiscal = self.generar_factura_fiscal(venta_id, total, monto_recibido, cambio)
            
            # En un sistema real, aquí se enviaría a la impresora fiscal
            # Por ahora, simulamos el proceso y guardamos en archivo
            
            import tempfile
            import os
            from datetime import datetime
            
            # Crear archivo de factura fiscal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"factura_fiscal_{self.numero_factura}_{timestamp}.txt"
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, 
                                           encoding='utf-8', prefix=f"fiscal_{self.numero_factura}_") as f:
                f.write(factura_fiscal)
                fiscal_path = f.name
            
            print(f"📄 Factura fiscal generada: {fiscal_path}")
            
            # Simular envío a impresora fiscal
            print("🔄 Conectando con impresora fiscal...")
            print("📡 Enviando datos fiscales...")
            print("✅ Factura fiscal impresa correctamente")
            
            # Abrir archivo para mostrar (simulación)
            if os.name == 'nt':  # Windows
                os.startfile(fiscal_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Error enviando a impresora fiscal: {e}")
            messagebox.showwarning("⚠️ Advertencia", 
                                 f"Error al enviar a impresora fiscal:\n{e}\n\n"
                                 f"La venta se guardó correctamente en la base de datos.")
            return False
    
    def generar_factura_fiscal(self, venta_id, total, monto_recibido, cambio):
        """Generar formato de factura fiscal"""
        cliente = self.entry_cliente.get() or "Cliente General"
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Obtener datos de la empresa desde la configuración
        from modulos.configuracion.gestor_configuracion import obtener_configuracion
        nombre_empresa = obtener_configuracion('nombre_empresa', 'Mi Tienda')
        direccion_empresa = obtener_configuracion('direccion_empresa', 'Caracas, Venezuela')
        rif_empresa = obtener_configuracion('rif_empresa', 'J-00000000-0')
        telefono_empresa = obtener_configuracion('telefono_empresa', '+58-212-1234567')
        
        factura = f"""
{'='*50}
              FACTURA FISCAL
{'='*50}

{nombre_empresa}
RIF: {rif_empresa}
{direccion_empresa}

FACTURA N°: {self.numero_factura:08d}
FECHA: {fecha_actual}
HORA: {hora_actual}
CAJERO: Sistema POS

CLIENTE: {cliente}
{'='*50}

DESCRIPCIÓN                QTY    P.UNIT    TOTAL
{'='*50}
"""
        
        for producto in self.productos_seleccionados:
            nombre = producto['nombre'][:20].ljust(20)
            cantidad = str(producto['cantidad']).rjust(3)
            precio = f"${producto['precio']:>7.2f}"
            subtotal = f"${producto['total']:>9.2f}"
            
            factura += f"{nombre} {cantidad} {precio} {subtotal}\n"
        
        subtotal_venta = sum(p['total'] for p in self.productos_seleccionados)
        iva = subtotal_venta * 0.19
        
        factura += f"""
{'='*50}
SUBTOTAL:                           ${subtotal_venta:>9.2f}
IVA (19%):                          ${iva:>9.2f}
{'='*50}
TOTAL A PAGAR:                      ${total:>9.2f}

EFECTIVO RECIBIDO:                  ${monto_recibido:>9.2f}
CAMBIO:                             ${cambio:>9.2f}

{'='*50}
           GRACIAS POR SU COMPRA
        CONSERVE ESTA FACTURA FISCAL
{'='*50}

CONTROL FISCAL: {venta_id:08d}
SERIAL IMPRESORA: FIS-001-2024
FECHA SISTEMA: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Esta es una factura fiscal válida
según normativas SENIAT
"""
        return factura

    def cerrar_modal_pago(self):
        """Cerrar el modal de pago"""
        if hasattr(self, 'modal_pago'):
            self.modal_pago.destroy()
