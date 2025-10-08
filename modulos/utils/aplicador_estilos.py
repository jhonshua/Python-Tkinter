"""
Utilidades para aplicar estilos modernos a módulos existentes
"""

import tkinter as tk
from tkinter import ttk
from .estilos_modernos import estilos

class AplicadorEstilos:
    """Clase para aplicar estilos modernos a widgets existentes"""
    
    @staticmethod
    def aplicar_a_frame(frame):
        """Aplicar estilos modernos a un frame"""
        frame.configure(bg=estilos.COLORS['bg_primary'])
        
    @staticmethod
    def aplicar_a_label(label, estilo='body'):
        """Aplicar estilos modernos a un label"""
        style_config = estilos.LABEL_STYLES.get(estilo, estilos.LABEL_STYLES['body'])
        label.configure(
            font=style_config['font'],
            fg=style_config['fg'],
            bg=style_config['bg']
        )
    
    @staticmethod
    def aplicar_a_button(button, estilo='primary'):
        """Aplicar estilos modernos a un botón"""
        style_config = estilos.BUTTON_STYLES.get(estilo, estilos.BUTTON_STYLES['primary'])
        
        button.configure(
            bg=style_config['bg'],
            fg=style_config['fg'],
            font=style_config['font'],
            relief=style_config['relief'],
            cursor=style_config['cursor'],
            bd=0
        )
        
        # Agregar efectos hover
        def on_enter(e):
            button.configure(bg=style_config['hover_bg'])
        
        def on_leave(e):
            button.configure(bg=style_config['bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    @staticmethod
    def aplicar_a_entry(entry):
        """Aplicar estilos modernos a un Entry"""
        style_config = estilos.ENTRY_STYLES['default']
        entry.configure(
            font=style_config['font'],
            bg=style_config['bg'],
            fg=style_config['fg'],
            relief=style_config['relief'],
            bd=style_config['bd'],
            highlightbackground=style_config['highlightbackground'],
            highlightcolor=style_config['highlightcolor'],
            highlightthickness=style_config['highlightthickness']
        )
    
    @staticmethod
    def crear_card_moderna(parent, titulo, x, y, width, height):
        """Crear una tarjeta moderna"""
        # Frame sombra
        shadow_frame = tk.Frame(parent, bg=estilos.COLORS['light_gray'])
        shadow_frame.place(x=x+3, y=y+3, width=width, height=height)
        
        # Frame principal
        main_frame = tk.Frame(parent, 
                             bg=estilos.COLORS['white'],
                             relief='flat',
                             bd=1,
                             highlightbackground=estilos.COLORS['border'],
                             highlightthickness=1)
        main_frame.place(x=x, y=y, width=width, height=height)
        
        # Título
        if titulo:
            title_frame = tk.Frame(main_frame, bg=estilos.COLORS['primary'], height=40)
            title_frame.pack(fill='x')
            
            title_label = tk.Label(title_frame, text=titulo,
                                  bg=estilos.COLORS['primary'],
                                  fg=estilos.COLORS['white'],
                                  font=('Segoe UI', 12, 'bold'))
            title_label.pack(pady=8)
            
            # Frame de contenido
            content_frame = tk.Frame(main_frame, bg=estilos.COLORS['white'])
            content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        else:
            content_frame = main_frame
        
        return content_frame
    
    @staticmethod
    def crear_boton_moderno(parent, text, command, estilo='primary', x=0, y=0, width=150, height=40):
        """Crear un botón moderno con efectos"""
        style_config = estilos.BUTTON_STYLES.get(estilo, estilos.BUTTON_STYLES['primary'])
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=style_config['bg'],
                       fg=style_config['fg'],
                       font=style_config['font'],
                       relief=style_config['relief'],
                       cursor=style_config['cursor'],
                       bd=0)
        btn.place(x=x, y=y, width=width, height=height)
        
        # Efectos hover
        def on_enter(e):
            btn.configure(bg=style_config['hover_bg'])
        
        def on_leave(e):
            btn.configure(bg=style_config['bg'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    @staticmethod
    def modernizar_treeview(tree):
        """Aplicar estilos modernos a un Treeview"""
        style = ttk.Style()
        
        # Configurar el estilo del Treeview
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 10),
                       background=estilos.COLORS['white'],
                       foreground=estilos.COLORS['dark'],
                       fieldbackground=estilos.COLORS['white'],
                       borderwidth=1,
                       relief='solid')
        
        # Configurar el estilo de los headers
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=estilos.COLORS['primary'],
                       foreground=estilos.COLORS['white'],
                       borderwidth=1,
                       relief='flat')
        
        # Aplicar el estilo
        tree.configure(style='Modern.Treeview')
    
    @staticmethod
    def modernizar_modulo_completo(frame_principal):
        """Modernizar un módulo completo aplicando estilos a todos sus widgets"""
        # Aplicar estilo al frame principal
        AplicadorEstilos.aplicar_a_frame(frame_principal)
        
        # Recorrer todos los widgets hijos y aplicar estilos
        def aplicar_recursivo(widget):
            widget_class = widget.winfo_class()
            
            if widget_class == 'Frame':
                widget.configure(bg=estilos.COLORS['bg_primary'])
            elif widget_class == 'Label':
                AplicadorEstilos.aplicar_a_label(widget)
            elif widget_class == 'Button':
                AplicadorEstilos.aplicar_a_button(widget)
            elif widget_class == 'Entry':
                AplicadorEstilos.aplicar_a_entry(widget)
            elif widget_class == 'Treeview':
                AplicadorEstilos.modernizar_treeview(widget)
            
            # Aplicar recursivamente a los hijos
            for child in widget.winfo_children():
                aplicar_recursivo(child)
        
        aplicar_recursivo(frame_principal)

# Instancia global para fácil acceso
aplicador = AplicadorEstilos()
