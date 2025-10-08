"""
Demo de la nueva interfaz moderna
Ejecuta este archivo para ver las mejoras visuales implementadas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modulos.utils.estilos_modernos import estilos
from PIL import Image, ImageTk
import sys
import os

class DemoInterfazModerna:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Demo - Interfaz Moderna vs Antigua")
        self.root.geometry("1400x800")
        self.root.configure(bg=estilos.COLORS['bg_primary'])
        
        self.setup_demo()
        
    def setup_demo(self):
        """Configurar la demostración"""
        # Título principal
        title_frame = tk.Frame(self.root, bg=estilos.COLORS['primary'], height=80)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, 
                              text="🎨 Comparación: Interfaz Antigua vs Moderna",
                              bg=estilos.COLORS['primary'],
                              fg=estilos.COLORS['white'],
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=estilos.COLORS['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Dividir en dos columnas
        # Columna izquierda - Interfaz antigua
        antigua_frame = tk.LabelFrame(main_frame, 
                                     text="❌ Interfaz Antigua (Estilo Windows 98)",
                                     font=('Arial', 14, 'bold'),
                                     bg='#C6D9E3',
                                     fg='black')
        antigua_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.crear_interfaz_antigua(antigua_frame)
        
        # Columna derecha - Interfaz moderna
        moderna_frame = tk.LabelFrame(main_frame,
                                     text="✅ Interfaz Moderna (Material Design)",
                                     font=('Segoe UI', 14, 'bold'),
                                     bg=estilos.COLORS['white'],
                                     fg=estilos.COLORS['primary'])
        moderna_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.crear_interfaz_moderna(moderna_frame)
        
        # Botón para cerrar
        close_btn = tk.Button(self.root,
                             text="Cerrar Demo",
                             command=self.root.destroy,
                             bg=estilos.COLORS['danger'],
                             fg=estilos.COLORS['white'],
                             font=('Segoe UI', 12, 'bold'),
                             relief='flat',
                             cursor='hand2',
                             pady=10)
        close_btn.pack(pady=20)
        
    def crear_interfaz_antigua(self, parent):
        """Crear ejemplo de interfaz antigua"""
        # Frame de información
        info_frame = tk.LabelFrame(parent, text="Información", bg='#C6D9E3')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        # Cliente
        tk.Label(info_frame, text="Cliente:", font='sans 14 bold', bg='#C6D9E3').pack(anchor='w', padx=5, pady=2)
        cliente_entry = tk.Entry(info_frame, font='sans 14 bold')
        cliente_entry.pack(fill='x', padx=5, pady=2)
        
        # Producto
        tk.Label(info_frame, text="Producto:", font='sans 14 bold', bg='#C6D9E3').pack(anchor='w', padx=5, pady=2)
        producto_entry = tk.Entry(info_frame, font='sans 14 bold')
        producto_entry.pack(fill='x', padx=5, pady=2)
        
        # Botones antiguos
        botones_frame = tk.Frame(info_frame, bg='#C6D9E3')
        botones_frame.pack(fill='x', padx=5, pady=10)
        
        tk.Button(botones_frame, text="Agregar", bg="lightgray", relief='raised', bd=2).pack(side='left', padx=2)
        tk.Button(botones_frame, text="Pagar", bg="lightblue", relief='raised', bd=2).pack(side='left', padx=2)
        tk.Button(botones_frame, text="Cancelar", bg="lightcoral", relief='raised', bd=2).pack(side='left', padx=2)
        
        # Lista antigua
        lista_frame = tk.Frame(parent, bg='#C6D9E3')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(lista_frame, text="Productos:", font='sans 12 bold', bg='#C6D9E3').pack(anchor='w')
        
        # Listbox antigua
        listbox = tk.Listbox(lista_frame, font='sans 10')
        listbox.pack(fill='both', expand=True, pady=5)
        listbox.insert(0, "Producto 1 - $10.00")
        listbox.insert(1, "Producto 2 - $25.50")
        
        # Total antiguo
        total_frame = tk.Frame(lista_frame, bg='#C6D9E3')
        total_frame.pack(fill='x', pady=5)
        tk.Label(total_frame, text="Total: $35.50", font='sans 14 bold', bg='#C6D9E3').pack()
        
    def crear_interfaz_moderna(self, parent):
        """Crear ejemplo de interfaz moderna"""
        parent.configure(bg=estilos.COLORS['white'])
        
        # Frame de información moderno
        info_frame = self.crear_card_moderna(parent, "👤 Información del Cliente")
        info_frame.pack(fill='x', padx=15, pady=15)
        
        # Cliente moderno
        tk.Label(info_frame, text="👤 Cliente:", 
                font=('Segoe UI', 11, 'bold'),
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['primary']).pack(anchor='w', padx=10, pady=(10, 2))
        
        cliente_entry = tk.Entry(info_frame, 
                               font=('Segoe UI', 11),
                               bg=estilos.COLORS['white'],
                               relief='solid',
                               bd=1,
                               highlightbackground=estilos.COLORS['border'],
                               highlightcolor=estilos.COLORS['border_focus'],
                               highlightthickness=1)
        cliente_entry.pack(fill='x', padx=10, pady=(0, 5))
        
        # Producto moderno
        tk.Label(info_frame, text="📦 Producto:", 
                font=('Segoe UI', 11, 'bold'),
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['primary']).pack(anchor='w', padx=10, pady=(5, 2))
        
        producto_entry = tk.Entry(info_frame, 
                                font=('Segoe UI', 11),
                                bg=estilos.COLORS['white'],
                                relief='solid',
                                bd=1,
                                highlightbackground=estilos.COLORS['border'],
                                highlightcolor=estilos.COLORS['border_focus'],
                                highlightthickness=1)
        producto_entry.pack(fill='x', padx=10, pady=(0, 10))
        
        # Botones modernos
        botones_frame = tk.Frame(info_frame, bg=estilos.COLORS['white'])
        botones_frame.pack(fill='x', padx=10, pady=(0, 15))
        
        self.crear_boton_moderno(botones_frame, "➕ Agregar", None, 'success').pack(side='left', padx=(0, 5))
        self.crear_boton_moderno(botones_frame, "💳 Pagar", None, 'primary').pack(side='left', padx=5)
        self.crear_boton_moderno(botones_frame, "❌ Cancelar", None, 'danger').pack(side='left', padx=5)
        
        # Lista moderna
        lista_frame = self.crear_card_moderna(parent, "🛒 Productos Seleccionados")
        lista_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Treeview moderno
        tree = ttk.Treeview(lista_frame, columns=("Producto", "Precio"), show="headings", height=6)
        tree.heading("Producto", text="Producto")
        tree.heading("Precio", text="Precio")
        tree.column("Producto", width=200)
        tree.column("Precio", width=100)
        
        tree.insert("", "end", values=("Producto Premium 1", "$10.00"))
        tree.insert("", "end", values=("Producto Premium 2", "$25.50"))
        
        tree.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Total moderno
        total_frame = tk.Frame(lista_frame, bg=estilos.COLORS['white'])
        total_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(total_frame, text="💰 TOTAL: $35.50", 
                font=('Segoe UI', 16, 'bold'),
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['success']).pack()
        
    def crear_card_moderna(self, parent, titulo):
        """Crear una tarjeta moderna con título"""
        # Frame sombra
        shadow_frame = tk.Frame(parent, bg='#e2e8f0', height=202, width=302)
        
        # Frame principal
        main_frame = tk.Frame(parent, 
                             bg=estilos.COLORS['white'],
                             relief='flat',
                             bd=1,
                             highlightbackground=estilos.COLORS['border'],
                             highlightthickness=1)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=estilos.COLORS['primary'], height=40)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text=titulo,
                              bg=estilos.COLORS['primary'],
                              fg=estilos.COLORS['white'],
                              font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=8)
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=estilos.COLORS['white'])
        content_frame.pack(fill='both', expand=True)
        
        return content_frame
        
    def crear_boton_moderno(self, parent, text, command, style='primary'):
        """Crear un botón moderno con efectos hover"""
        style_config = estilos.BUTTON_STYLES[style]
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=style_config['bg'],
                       fg=style_config['fg'],
                       font=style_config['font'],
                       relief=style_config['relief'],
                       cursor=style_config['cursor'],
                       bd=0,
                       padx=15,
                       pady=8)
        
        # Efectos hover
        def on_enter(e):
            btn.configure(bg=style_config['hover_bg'])
        
        def on_leave(e):
            btn.configure(bg=style_config['bg'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def run(self):
        """Ejecutar la demostración"""
        self.root.mainloop()

if __name__ == "__main__":
    demo = DemoInterfazModerna()
    demo.run()
