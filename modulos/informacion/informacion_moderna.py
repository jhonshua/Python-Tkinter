import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import webbrowser

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class InformacionModerna(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre, bg=estilos.COLORS['bg_primary'])
        self.widgets()
    
    def actualizar_moneda(self, nueva_moneda):
        """Actualizar estadísticas cuando cambia la moneda"""
        try:
            # Recargar estadísticas con nueva moneda si existen
            if hasattr(self, 'cargar_estadisticas'):
                self.cargar_estadisticas()
            print(f"Módulo Información actualizado a moneda: {nueva_moneda}")
        except Exception as e:
            print(f"Error al actualizar moneda en Información: {e}")
        
    def widgets(self):
        # Título principal
        title_frame = tk.Frame(self, bg=estilos.COLORS['bg_primary'])
        title_frame.place(x=0, y=20, width=1400, height=80)
        
        title_label = tk.Label(title_frame, text="📊 Centro de Información", 
                              font=('Segoe UI', 24, 'bold'), 
                              bg=estilos.COLORS['bg_primary'],
                              fg=estilos.COLORS['primary'])
        title_label.place(x=50, y=20)
        
        subtitle_label = tk.Label(title_frame, text="Reportes, estadísticas y información del sistema", 
                                 font=('Segoe UI', 12), 
                                 bg=estilos.COLORS['bg_primary'],
                                 fg=estilos.COLORS['gray'])
        subtitle_label.place(x=50, y=55)

        # Frame principal para las cards
        main_frame = tk.Frame(self, bg=estilos.COLORS['bg_primary'])
        main_frame.place(x=50, y=120, width=1300, height=600)

        # Card 1: Reportes de Ventas
        self.crear_card_reporte(main_frame, x=50, y=50)
        
        # Card 2: Estadísticas del Sistema
        self.crear_card_estadisticas(main_frame, x=450, y=50)
        
        # Card 3: Información del Sistema
        self.crear_card_info_sistema(main_frame, x=850, y=50)
        
        # Card 4: Resumen de Inventario
        self.crear_card_inventario(main_frame, x=50, y=350)
        
        # Card 5: Actividad Reciente
        self.crear_card_actividad(main_frame, x=450, y=350)
        
        # Card 6: Configuración
        self.crear_card_configuracion(main_frame, x=850, y=350)

    def crear_card_reporte(self, parent, x, y):
        """Crear card de reportes"""
        card = tk.LabelFrame(parent, text="📈 Reportes de Ventas", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="📊", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['success'])
        icon_label.place(x=150, y=30)
        
        # Descripción
        desc_label = tk.Label(card, text="Generar reportes detallados\nde ventas y transacciones", 
                             font=('Segoe UI', 11), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['dark'],
                             justify='center')
        desc_label.place(x=75, y=100)
        
        # Botón moderno
        btn_reporte = ctk.CTkButton(
            card, 
            text="📊 Generar Reporte", 
            command=self.generar_reporte,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['success'],
            hover_color="#28a745"
        )
        btn_reporte.place(x=25, y=180)

    def crear_card_estadisticas(self, parent, x, y):
        """Crear card de estadísticas"""
        card = tk.LabelFrame(parent, text="📊 Estadísticas del Sistema", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="📈", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['info'])
        icon_label.place(x=150, y=30)
        
        # Estadísticas en tiempo real
        self.stats_frame = tk.Frame(card, bg=estilos.COLORS['white'])
        self.stats_frame.place(x=25, y=100, width=300, height=80)
        
        self.cargar_estadisticas()
        
        # Botón moderno
        btn_stats = ctk.CTkButton(
            card, 
            text="🔄 Actualizar Stats", 
            command=self.actualizar_estadisticas,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['info'],
            hover_color="#0ea5e9"
        )
        btn_stats.place(x=25, y=180)

    def crear_card_info_sistema(self, parent, x, y):
        """Crear card de información del sistema"""
        card = tk.LabelFrame(parent, text="ℹ️ Información del Sistema", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="💻", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['accent'])
        icon_label.place(x=150, y=30)
        
        # Información del sistema
        info_text = f"""Sistema de Punto de Venta
Versión: 2.0 Moderna
Fecha: {datetime.now().strftime('%Y-%m-%d')}
Estado: Operativo ✅"""
        
        info_label = tk.Label(card, text=info_text, 
                             font=('Segoe UI', 10), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['dark'],
                             justify='center')
        info_label.place(x=75, y=100)
        
        # Botón moderno
        btn_info = ctk.CTkButton(
            card, 
            text="ℹ️ Más Información", 
            command=self.mostrar_info_detallada,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['accent'],
            hover_color="#7c3aed"
        )
        btn_info.place(x=25, y=180)

    def crear_card_inventario(self, parent, x, y):
        """Crear card de resumen de inventario"""
        card = tk.LabelFrame(parent, text="📦 Resumen de Inventario", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="📦", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['warning'])
        icon_label.place(x=150, y=30)
        
        # Frame para estadísticas de inventario
        self.inventario_frame = tk.Frame(card, bg=estilos.COLORS['white'])
        self.inventario_frame.place(x=25, y=100, width=300, height=80)
        
        self.cargar_resumen_inventario()
        
        # Botón moderno
        btn_inventario = ctk.CTkButton(
            card, 
            text="📦 Ver Inventario", 
            command=self.ver_inventario_detallado,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['warning'],
            hover_color="#ffc107"
        )
        btn_inventario.place(x=25, y=180)

    def crear_card_actividad(self, parent, x, y):
        """Crear card de actividad reciente"""
        card = tk.LabelFrame(parent, text="🕒 Actividad Reciente", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="📋", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['secondary'])
        icon_label.place(x=150, y=30)
        
        # Frame para actividad reciente
        self.actividad_frame = tk.Frame(card, bg=estilos.COLORS['white'])
        self.actividad_frame.place(x=25, y=100, width=300, height=80)
        
        self.cargar_actividad_reciente()
        
        # Botón moderno
        btn_actividad = ctk.CTkButton(
            card, 
            text="📋 Ver Historial", 
            command=self.ver_historial_completo,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['secondary'],
            hover_color="#059669"
        )
        btn_actividad.place(x=25, y=180)

    def crear_card_configuracion(self, parent, x, y):
        """Crear card de configuración"""
        card = tk.LabelFrame(parent, text="⚙️ Configuración", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg=estilos.COLORS['white'],
                            fg=estilos.COLORS['primary'],
                            relief='solid', bd=1)
        card.place(x=x, y=y, width=350, height=250)
        
        # Icono grande
        icon_label = tk.Label(card, text="⚙️", font=('Segoe UI', 48), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['gray'])
        icon_label.place(x=150, y=30)
        
        # Descripción
        desc_label = tk.Label(card, text="Configurar parámetros\ndel sistema y preferencias", 
                             font=('Segoe UI', 11), 
                             bg=estilos.COLORS['white'],
                             fg=estilos.COLORS['dark'],
                             justify='center')
        desc_label.place(x=75, y=100)
        
        # Botón moderno
        btn_config = ctk.CTkButton(
            card, 
            text="⚙️ Configuración", 
            command=self.abrir_configuracion,
            width=300,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=estilos.COLORS['gray'],
            hover_color="#475569"
        )
        btn_config.place(x=25, y=180)

    def cargar_estadisticas(self):
        """Cargar estadísticas del sistema"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Contar productos
            cursor.execute("SELECT COUNT(*) FROM productos")
            total_productos = cursor.fetchone()[0]
            
            # Contar clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clientes = cursor.fetchone()[0]
            
            # Contar pedidos
            cursor.execute("SELECT COUNT(*) FROM pedidos_proveedor")
            total_pedidos = cursor.fetchone()[0]
            
            conn.close()
            
            # Mostrar estadísticas
            stats_text = f"📦 Productos: {total_productos}\n👥 Clientes: {total_clientes}\n📋 Pedidos: {total_pedidos}"
            
            stats_label = tk.Label(self.stats_frame, text=stats_text, 
                                  font=('Segoe UI', 10, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['dark'],
                                  justify='left')
            stats_label.place(x=0, y=0)
            
        except sqlite3.Error as e:
            error_label = tk.Label(self.stats_frame, text="Error al cargar estadísticas", 
                                  font=('Segoe UI', 10), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['danger'])
            error_label.place(x=0, y=0)

    def cargar_resumen_inventario(self):
        """Cargar resumen del inventario"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Stock total
            cursor.execute("SELECT SUM(stock) FROM productos")
            stock_total = cursor.fetchone()[0] or 0
            
            # Productos con stock bajo (menos de 10)
            cursor.execute("SELECT COUNT(*) FROM productos WHERE stock < 10")
            stock_bajo = cursor.fetchone()[0]
            
            conn.close()
            
            # Mostrar resumen
            resumen_text = f"📊 Stock Total: {stock_total}\n⚠️ Stock Bajo: {stock_bajo} productos"
            
            resumen_label = tk.Label(self.inventario_frame, text=resumen_text, 
                                    font=('Segoe UI', 10, 'bold'), 
                                    bg=estilos.COLORS['white'],
                                    fg=estilos.COLORS['dark'],
                                    justify='left')
            resumen_label.place(x=0, y=0)
            
        except sqlite3.Error as e:
            error_label = tk.Label(self.inventario_frame, text="Error al cargar inventario", 
                                  font=('Segoe UI', 10), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['danger'])
            error_label.place(x=0, y=0)

    def cargar_actividad_reciente(self):
        """Cargar actividad reciente"""
        actividad_text = f"🕒 Última actualización:\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n✅ Sistema operativo"
        
        actividad_label = tk.Label(self.actividad_frame, text=actividad_text, 
                                  font=('Segoe UI', 10), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['dark'],
                                  justify='left')
        actividad_label.place(x=0, y=0)

    # Funciones de los botones
    def generar_reporte(self):
        """Generar reporte de ventas"""
        try:
            from modulos.reportes.generador_reportes import GeneradorReportes
            generador = GeneradorReportes(self)
            generador.abrir_ventana_reportes()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"Error al cargar módulo de reportes: {e}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir reportes: {e}")

    def actualizar_estadisticas(self):
        """Actualizar estadísticas"""
        # Limpiar frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Recargar estadísticas
        self.cargar_estadisticas()
        messagebox.showinfo("🔄 Actualizado", "Estadísticas actualizadas correctamente")

    def mostrar_info_detallada(self):
        """Mostrar información detallada del sistema"""
        info_detallada = f"""
🖥️ Sistema de Punto de Venta Moderno

📋 Información Técnica:
• Versión: 2.0 Moderna
• Tecnología: Python + Tkinter + CustomTkinter
• Base de datos: SQLite
• Interfaz: Material Design

✨ Características:
• Gestión de inventario
• Registro de clientes
• Pedidos a proveedores
• Interfaz moderna y responsive
• Actualización automática de stock

👨‍💻 Desarrollado con estilos modernos
📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        messagebox.showinfo("ℹ️ Información del Sistema", info_detallada)

    def ver_inventario_detallado(self):
        """Ver inventario detallado"""
        messagebox.showinfo("📦 Inventario", "Para ver el inventario detallado,\nnavega a la sección 'Inventario' en el menú principal.")

    def ver_historial_completo(self):
        """Ver historial completo"""
        try:
            from modulos.historial.gestor_historial import GestorHistorial
            gestor = GestorHistorial(self)
            gestor.abrir_ventana_historial()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"Error al cargar módulo de historial: {e}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir historial: {e}")

    def abrir_configuracion(self):
        """Abrir configuración"""
        try:
            from modulos.configuracion.gestor_configuracion import GestorConfiguracion
            gestor = GestorConfiguracion(self)
            gestor.abrir_ventana_configuracion()
        except ImportError as e:
            messagebox.showerror("❌ Error", f"Error al cargar módulo de configuración: {e}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir configuración: {e}")
