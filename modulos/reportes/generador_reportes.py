import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
import sqlite3
from datetime import datetime, timedelta
import os
import subprocess
import platform

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class GeneradorReportes:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        
    def abrir_ventana_reportes(self):
        """Abrir ventana principal de reportes"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Generador de Reportes")
        self.window.geometry("900x700+300+50")
        self.window.configure(bg=estilos.COLORS['bg_primary'])
        self.window.resizable(True, True)
        self.window.grab_set()
        self.window.focus_set()
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg=estilos.COLORS['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="📊 Centro de Reportes", 
                              font=('Segoe UI', 20, 'bold'), 
                              bg=estilos.COLORS['bg_primary'],
                              fg=estilos.COLORS['primary'])
        title_label.pack(pady=(0, 20))
        
        # Frame de opciones
        options_frame = tk.LabelFrame(main_frame, text="🎯 Opciones de Reporte", 
                                     font=('Segoe UI', 14, 'bold'), 
                                     bg=estilos.COLORS['white'],
                                     fg=estilos.COLORS['primary'])
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Tipo de reporte
        tk.Label(options_frame, text="📋 Tipo de Reporte:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.tipo_reporte = ttk.Combobox(options_frame, font=('Segoe UI', 11), 
                                        values=["Ventas Diarias", "Ventas por Período", 
                                               "Inventario Actual", "Productos Más Vendidos",
                                               "Clientes Registrados", "Proveedores",
                                               "Reporte Completo"], 
                                        state="readonly", width=25)
        self.tipo_reporte.set("Ventas Diarias")
        self.tipo_reporte.grid(row=0, column=1, padx=10, pady=10)
        
        # Período de fechas
        tk.Label(options_frame, text="📅 Fecha Inicio:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        self.fecha_inicio = tk.Entry(options_frame, font=('Segoe UI', 11), width=15)
        self.fecha_inicio.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.fecha_inicio.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(options_frame, text="📅 Fecha Fin:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white'],
                fg=estilos.COLORS['dark']).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        
        self.fecha_fin = tk.Entry(options_frame, font=('Segoe UI', 11), width=15)
        self.fecha_fin.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.fecha_fin.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        # Botones de acción
        buttons_frame = tk.Frame(options_frame, bg=estilos.COLORS['white'])
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        btn_generar = ctk.CTkButton(buttons_frame, text="📊 Generar Reporte", 
                                   command=self.generar_reporte,
                                   width=150, height=40,
                                   font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                   fg_color=estilos.COLORS['primary'],
                                   hover_color=estilos.COLORS['primary_dark'])
        btn_generar.pack(side='left', padx=5)
        
        btn_pdf = ctk.CTkButton(buttons_frame, text="📄 Exportar PDF", 
                               command=self.exportar_pdf,
                               width=150, height=40,
                               font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                               fg_color=estilos.COLORS['danger'],
                               hover_color="#dc3545")
        btn_pdf.pack(side='left', padx=5)
        
        btn_imprimir = ctk.CTkButton(buttons_frame, text="🖨️ Imprimir", 
                                    command=self.imprimir_reporte,
                                    width=150, height=40,
                                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                    fg_color=estilos.COLORS['secondary'],
                                    hover_color="#059669")
        btn_imprimir.pack(side='left', padx=5)
        
        # Frame de vista previa
        preview_frame = tk.LabelFrame(main_frame, text="👁️ Vista Previa del Reporte", 
                                     font=('Segoe UI', 14, 'bold'), 
                                     bg=estilos.COLORS['white'],
                                     fg=estilos.COLORS['primary'])
        preview_frame.pack(fill='both', expand=True)
        
        # Área de texto con scroll
        text_frame = tk.Frame(preview_frame, bg=estilos.COLORS['white'])
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = ttk.Scrollbar(text_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Área de texto
        self.texto_reporte = tk.Text(text_frame, 
                                    font=('Consolas', 10),
                                    bg='white',
                                    fg=estilos.COLORS['dark'],
                                    yscrollcommand=v_scrollbar.set,
                                    xscrollcommand=h_scrollbar.set,
                                    wrap='none')
        self.texto_reporte.pack(fill='both', expand=True)
        
        v_scrollbar.config(command=self.texto_reporte.yview)
        h_scrollbar.config(command=self.texto_reporte.xview)
        
        # Generar reporte inicial
        self.generar_reporte()
    
    def generar_reporte(self):
        """Generar el reporte seleccionado"""
        tipo = self.tipo_reporte.get()
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        
        try:
            if tipo == "Ventas Diarias":
                contenido = self.reporte_ventas_diarias(fecha_inicio)
            elif tipo == "Ventas por Período":
                contenido = self.reporte_ventas_periodo(fecha_inicio, fecha_fin)
            elif tipo == "Inventario Actual":
                contenido = self.reporte_inventario()
            elif tipo == "Productos Más Vendidos":
                contenido = self.reporte_productos_vendidos()
            elif tipo == "Clientes Registrados":
                contenido = self.reporte_clientes()
            elif tipo == "Proveedores":
                contenido = self.reporte_proveedores()
            elif tipo == "Reporte Completo":
                contenido = self.reporte_completo()
            else:
                contenido = "Tipo de reporte no implementado"
            
            # Mostrar en el área de texto
            self.texto_reporte.delete('1.0', 'end')
            self.texto_reporte.insert('1.0', contenido)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al generar reporte: {e}")
    
    def reporte_ventas_diarias(self, fecha):
        """Generar reporte de ventas diarias"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM ventas WHERE fecha = ?", (fecha,))
            ventas = cursor.fetchall()
            
            total_ventas = sum(venta[6] for venta in ventas)  # total
            total_cantidad = sum(venta[5] for venta in ventas)  # cantidad
            
            reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📊 REPORTE DE VENTAS DIARIAS               ║
╠══════════════════════════════════════════════════════════════╣
║ Fecha: {fecha}                                    ║
║ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
╚══════════════════════════════════════════════════════════════╝

📈 RESUMEN EJECUTIVO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total de Ventas: ${total_ventas:.2f}
• Número de Transacciones: {len(ventas)}
• Productos Vendidos: {total_cantidad} unidades
• Promedio por Venta: ${(total_ventas/len(ventas) if ventas else 0):.2f}

📋 DETALLE DE VENTAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'Factura':<10} {'Cliente':<20} {'Producto':<25} {'Cant':<6} {'Precio':<10} {'Total':<10}
{'-'*10} {'-'*20} {'-'*25} {'-'*6} {'-'*10} {'-'*10}
"""
            
            for venta in ventas:
                reporte += f"{str(venta[1]):<10} {str(venta[2])[:20]:<20} {str(venta[3])[:25]:<25} {str(venta[5]):<6} ${venta[4]:<9.2f} ${venta[6]:<9.2f}\n"
            
            reporte += f"""
{'-'*88}
TOTAL GENERAL: ${total_ventas:.2f}

📊 ESTADÍSTICAS ADICIONALES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Venta Máxima: ${max([v[6] for v in ventas]) if ventas else 0:.2f}
• Venta Mínima: ${min([v[6] for v in ventas]) if ventas else 0:.2f}
• Hora de Mayor Actividad: {self.obtener_hora_pico(ventas)}

═══════════════════════════════════════════════════════════════
                    Fin del Reporte
═══════════════════════════════════════════════════════════════
"""
            
            conn.close()
            return reporte
            
        except Exception as e:
            return f"Error al generar reporte de ventas: {e}"
    
    def reporte_inventario(self):
        """Generar reporte de inventario actual"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM productos ORDER BY nombre")
            productos = cursor.fetchall()
            
            valor_total = sum(p[3] * p[5] for p in productos)  # precio * stock
            productos_bajo_stock = [p for p in productos if p[5] < 10]
            
            reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📦 REPORTE DE INVENTARIO                   ║
╠══════════════════════════════════════════════════════════════╣
║ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
╚══════════════════════════════════════════════════════════════╝

📈 RESUMEN EJECUTIVO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total de Productos: {len(productos)}
• Valor Total del Inventario: ${valor_total:.2f}
• Productos con Stock Bajo (<10): {len(productos_bajo_stock)}
• Stock Total: {sum(p[5] for p in productos)} unidades

📋 INVENTARIO DETALLADO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'Código':<15} {'Producto':<30} {'Stock':<8} {'Precio':<10} {'Valor':<12} {'Estado':<10}
{'-'*15} {'-'*30} {'-'*8} {'-'*10} {'-'*12} {'-'*10}
"""
            
            for producto in productos:
                codigo = str(producto[1]) if producto[1] else 'N/A'
                nombre = str(producto[2])[:30]
                stock = producto[5]
                precio = producto[3]
                valor = precio * stock
                estado = "⚠️ BAJO" if stock < 10 else "✅ OK"
                
                reporte += f"{codigo:<15} {nombre:<30} {stock:<8} ${precio:<9.2f} ${valor:<11.2f} {estado:<10}\n"
            
            if productos_bajo_stock:
                reporte += f"""

⚠️ PRODUCTOS CON STOCK BAJO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                for producto in productos_bajo_stock:
                    reporte += f"• {producto[2]} - Stock: {producto[5]} unidades\n"
            
            reporte += f"""

═══════════════════════════════════════════════════════════════
                    Fin del Reporte
═══════════════════════════════════════════════════════════════
"""
            
            conn.close()
            return reporte
            
        except Exception as e:
            return f"Error al generar reporte de inventario: {e}"
    
    def reporte_clientes(self):
        """Generar reporte de clientes"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clientes ORDER BY nombre")
            clientes = cursor.fetchall()
            
            reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║                    👥 REPORTE DE CLIENTES                     ║
╠══════════════════════════════════════════════════════════════╣
║ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
╚══════════════════════════════════════════════════════════════╝

📈 RESUMEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total de Clientes Registrados: {len(clientes)}

📋 LISTADO DE CLIENTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'ID':<5} {'Nombre':<25} {'Cédula':<15} {'Teléfono':<15} {'Email':<30}
{'-'*5} {'-'*25} {'-'*15} {'-'*15} {'-'*30}
"""
            
            for cliente in clientes:
                reporte += f"{cliente[0]:<5} {str(cliente[1])[:25]:<25} {str(cliente[2]):<15} {str(cliente[3]):<15} {str(cliente[5])[:30]:<30}\n"
            
            reporte += f"""

═══════════════════════════════════════════════════════════════
                    Fin del Reporte
═══════════════════════════════════════════════════════════════
"""
            
            conn.close()
            return reporte
            
        except Exception as e:
            return f"Error al generar reporte de clientes: {e}"
    
    def obtener_hora_pico(self, ventas):
        """Obtener la hora de mayor actividad"""
        if not ventas:
            return "N/A"
        
        horas = {}
        for venta in ventas:
            if len(venta) > 8 and venta[8]:  # Si hay campo hora
                hora = str(venta[8])[:2]  # Primeros 2 caracteres de la hora
                horas[hora] = horas.get(hora, 0) + 1
        
        if horas:
            hora_pico = max(horas, key=horas.get)
            return f"{hora_pico}:00"
        return "N/A"
    
    def exportar_pdf(self):
        """Exportar reporte a PDF"""
        try:
            # Obtener contenido del reporte
            contenido = self.texto_reporte.get('1.0', 'end-1c')
            
            if not contenido.strip():
                messagebox.showwarning("⚠️ Advertencia", "No hay contenido para exportar")
                return
            
            # Seleccionar ubicación del archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Guardar Reporte"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(contenido)
                
                messagebox.showinfo("✅ Éxito", f"Reporte guardado como:\n{filename}")
                
                # Preguntar si quiere abrir el archivo
                if messagebox.askyesno("📄 Abrir Archivo", "¿Desea abrir el archivo guardado?"):
                    self.abrir_archivo(filename)
                    
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al exportar: {e}")
    
    def imprimir_reporte(self):
        """Imprimir el reporte"""
        try:
            contenido = self.texto_reporte.get('1.0', 'end-1c')
            
            if not contenido.strip():
                messagebox.showwarning("⚠️ Advertencia", "No hay contenido para imprimir")
                return
            
            # Crear archivo temporal
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(contenido)
                temp_filename = temp_file.name
            
            # Abrir con la aplicación predeterminada para imprimir
            if platform.system() == 'Windows':
                os.startfile(temp_filename, 'print')
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['lpr', temp_filename])
            else:  # Linux
                subprocess.run(['lp', temp_filename])
            
            messagebox.showinfo("🖨️ Impresión", "Reporte enviado a la impresora")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al imprimir: {e}")
    
    def abrir_archivo(self, filename):
        """Abrir archivo con la aplicación predeterminada"""
        try:
            if platform.system() == 'Windows':
                os.startfile(filename)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filename])
            else:  # Linux
                subprocess.run(['xdg-open', filename])
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al abrir archivo: {e}")
    
    def reporte_proveedores(self):
        """Generar reporte de proveedores"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM proveedores ORDER BY empresa")
            proveedores = cursor.fetchall()
            
            reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🏢 REPORTE DE PROVEEDORES                  ║
╠══════════════════════════════════════════════════════════════╣
║ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
╚══════════════════════════════════════════════════════════════╝

📈 RESUMEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total de Proveedores: {len(proveedores)}

📋 LISTADO DE PROVEEDORES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'ID':<5} {'Empresa':<30} {'RIF':<15} {'Teléfono':<15} {'Email':<25}
{'-'*5} {'-'*30} {'-'*15} {'-'*15} {'-'*25}
"""
            
            for proveedor in proveedores:
                reporte += f"{proveedor[0]:<5} {str(proveedor[1])[:30]:<30} {str(proveedor[2]):<15} {str(proveedor[3]):<15} {str(proveedor[5])[:25]:<25}\n"
            
            reporte += f"""

═══════════════════════════════════════════════════════════════
                    Fin del Reporte
═══════════════════════════════════════════════════════════════
"""
            
            conn.close()
            return reporte
            
        except Exception as e:
            return f"Error al generar reporte de proveedores: {e}"
    
    def reporte_completo(self):
        """Generar reporte completo del sistema"""
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        
        reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📊 REPORTE COMPLETO DEL SISTEMA            ║
╠══════════════════════════════════════════════════════════════╣
║ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
╚══════════════════════════════════════════════════════════════╝

"""
        
        # Agregar cada sección
        reporte += "1️⃣ " + "="*60 + "\n"
        reporte += "   VENTAS DEL DÍA\n"
        reporte += "="*60 + "\n"
        reporte += self.reporte_ventas_diarias(fecha_actual)
        
        reporte += "\n\n2️⃣ " + "="*60 + "\n"
        reporte += "   ESTADO DEL INVENTARIO\n"
        reporte += "="*60 + "\n"
        reporte += self.reporte_inventario()
        
        reporte += "\n\n3️⃣ " + "="*60 + "\n"
        reporte += "   CLIENTES REGISTRADOS\n"
        reporte += "="*60 + "\n"
        reporte += self.reporte_clientes()
        
        return reporte
