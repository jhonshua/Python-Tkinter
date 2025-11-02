import tkinter as tk
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
from modulos.configuracion.gestor_configuracion import obtener_configuracion

class SwitchMoneda:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.moneda_actual = obtener_configuracion('moneda_principal', 'USD')
        self.crear_switch()
    
    def crear_switch(self):
        """Crear el switch de moneda"""
        # Frame contenedor
        self.frame = tk.Frame(self.parent, bg=estilos.COLORS['bg_primary'])
        
        # Label indicador
        self.label_moneda = tk.Label(self.frame, 
                                    text=f"💰 {self.moneda_actual}", 
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=estilos.COLORS['bg_primary'],
                                    fg=estilos.COLORS['primary'])
        self.label_moneda.pack(side='left', padx=(0, 5))
        
        # Switch button
        self.switch_btn = ctk.CTkButton(self.frame,
                                       text="🔄",
                                       width=40,
                                       height=30,
                                       command=self.cambiar_moneda,
                                       font=ctk.CTkFont(size=12),
                                       fg_color=estilos.COLORS['info'],
                                       hover_color=estilos.COLORS['primary'])
        self.switch_btn.pack(side='left')
        
        # Tooltip
        self.crear_tooltip()
    
    def crear_tooltip(self):
        """Crear tooltip explicativo"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='black')
            
            label = tk.Label(tooltip, text="Click para cambiar entre USD y Bs.",
                           bg='black', fg='white', font=('Segoe UI', 9))
            label.pack()
            
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            
            def ocultar_tooltip():
                tooltip.destroy()
            
            tooltip.after(2000, ocultar_tooltip)
        
        self.switch_btn.bind('<Enter>', mostrar_tooltip)
    
    def cambiar_moneda(self):
        """Cambiar entre USD y VES"""
        try:
            import sqlite3
            
            # Cambiar moneda
            nueva_moneda = 'VES' if self.moneda_actual == 'USD' else 'USD'
            
            # Actualizar en base de datos
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO configuracion_sistema 
                (clave, valor, descripcion, fecha_modificacion) 
                VALUES (?, ?, ?, ?)
            ''', ('moneda_principal', nueva_moneda, 'Moneda principal del sistema', 
                  __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            
            # Actualizar interfaz
            self.moneda_actual = nueva_moneda
            self.label_moneda.config(text=f"💰 {nueva_moneda}")
            
            # Llamar callback si existe
            if self.callback:
                self.callback(nueva_moneda)
                
        except Exception as e:
            print(f"Error al cambiar moneda: {e}")
    
    def pack(self, **kwargs):
        """Empaquetar el frame"""
        self.frame.pack(**kwargs)
    
    def place(self, **kwargs):
        """Posicionar el frame"""
        self.frame.place(**kwargs)
