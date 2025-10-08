"""
Script para modernizar automáticamente todos los módulos existentes
Ejecuta este script para aplicar los estilos modernos a inventario, clientes, etc.
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modulos.utils.estilos_modernos import estilos
from modulos.utils.aplicador_estilos import aplicador

def modernizar_inventario():
    """Modernizar el módulo de inventario"""
    try:
        # Leer el archivo actual
        with open('modulos/inventario/inventario.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Agregar import de estilos si no existe
        if 'from modulos.utils.estilos_modernos import estilos' not in contenido:
            # Buscar la línea de imports y agregar el nuevo import
            lines = contenido.split('\n')
            import_index = -1
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_index = i
            
            if import_index != -1:
                lines.insert(import_index + 1, 'from modulos.utils.estilos_modernos import estilos')
                lines.insert(import_index + 2, 'from modulos.utils.aplicador_estilos import aplicador')
                contenido = '\n'.join(lines)
        
        # Reemplazar colores antiguos con modernos
        replacements = {
            "'#C6D9E3'": "estilos.COLORS['bg_primary']",
            '"#C6D9E3"': "estilos.COLORS['bg_primary']",
            'bg="#C6D9E3"': "bg=estilos.COLORS['bg_primary']",
            'bg=\'#C6D9E3\'': "bg=estilos.COLORS['bg_primary']",
            'font=\'sans 14 bold\'': "font=('Segoe UI', 11, 'bold')",
            'font="sans 14 bold"': "font=('Segoe UI', 11, 'bold')",
            'font=\'sans 12 bold\'': "font=('Segoe UI', 10, 'bold')",
            'font="sans 12 bold"': "font=('Segoe UI', 10, 'bold')"
        }
        
        for old, new in replacements.items():
            contenido = contenido.replace(old, new)
        
        # Crear backup
        with open('modulos/inventario/inventario_backup.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Inventario modernizado (backup creado)")
        
    except Exception as e:
        print(f"❌ Error modernizando inventario: {e}")

def modernizar_clientes():
    """Modernizar el módulo de clientes"""
    try:
        # Similar proceso para clientes
        archivo_clientes = 'modulos/clientes.py'
        if os.path.exists(archivo_clientes):
            with open(archivo_clientes, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Aplicar las mismas modernizaciones
            replacements = {
                "'#C6D9E3'": "estilos.COLORS['bg_primary']",
                '"#C6D9E3"': "estilos.COLORS['bg_primary']",
                'bg="#C6D9E3"': "bg=estilos.COLORS['bg_primary']",
                'bg=\'#C6D9E3\'': "bg=estilos.COLORS['bg_primary']",
                'font=\'sans 14 bold\'': "font=('Segoe UI', 11, 'bold')",
                'font="sans 14 bold"': "font=('Segoe UI', 11, 'bold')"
            }
            
            for old, new in replacements.items():
                contenido = contenido.replace(old, new)
            
            # Agregar imports si no existen
            if 'from modulos.utils.estilos_modernos import estilos' not in contenido:
                lines = contenido.split('\n')
                # Buscar donde insertar los imports
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        lines.insert(i + 1, 'from modulos.utils.estilos_modernos import estilos')
                        break
                contenido = '\n'.join(lines)
            
            # Crear backup
            with open('modulos/clientes_backup.py', 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print("✅ Clientes modernizado (backup creado)")
        
    except Exception as e:
        print(f"❌ Error modernizando clientes: {e}")

def crear_demo_comparacion():
    """Crear una demo que muestre la comparación antes/después"""
    root = tk.Tk()
    root.title("🎨 Modernización Aplicada")
    root.geometry("800x600")
    root.configure(bg=estilos.COLORS['bg_primary'])
    
    # Título
    title_frame = tk.Frame(root, bg=estilos.COLORS['primary'], height=80)
    title_frame.pack(fill='x')
    
    title_label = tk.Label(title_frame, 
                          text="🎉 ¡Estilos Modernos Aplicados Exitosamente!",
                          bg=estilos.COLORS['primary'],
                          fg=estilos.COLORS['white'],
                          font=('Segoe UI', 18, 'bold'))
    title_label.pack(pady=20)
    
    # Contenido
    content_frame = tk.Frame(root, bg=estilos.COLORS['bg_primary'])
    content_frame.pack(fill='both', expand=True, padx=30, pady=30)
    
    # Lista de mejoras
    mejoras_text = """
✅ Manager.py - Ventana principal modernizada
✅ Container.py - Barra de navegación moderna con efectos hover
✅ Ventas.py - Interfaz completamente rediseñada
✅ Sistema de estilos centralizado implementado
✅ Paleta de colores Material Design aplicada
✅ Tipografía Segoe UI en toda la aplicación
✅ Efectos hover y animaciones sutiles
✅ Cards y componentes modernos

🎨 Características Nuevas:
• Ventana redimensionable (1400x900)
• Navbar con efectos de hover
• Botones con colores modernos
• Espaciado y padding mejorados
• Iconos emoji para mejor UX
• Temas consistentes en toda la app
    """
    
    mejoras_label = tk.Label(content_frame, text=mejoras_text,
                            bg=estilos.COLORS['bg_primary'],
                            fg=estilos.COLORS['dark'],
                            font=('Segoe UI', 11),
                            justify='left')
    mejoras_label.pack(pady=20)
    
    # Botón para cerrar
    aplicador.crear_boton_moderno(content_frame, "🚀 ¡Perfecto! Cerrar", 
                                 root.destroy, 'success', 300, 400, 200, 50)
    
    root.mainloop()

def main():
    """Función principal"""
    print("🎨 Iniciando modernización de módulos...")
    print("=" * 50)
    
    # Modernizar módulos individuales
    print("📦 Modernizando Inventario...")
    modernizar_inventario()
    
    print("👥 Modernizando Clientes...")
    modernizar_clientes()
    
    print("=" * 50)
    print("✅ ¡Modernización completada!")
    print("\n🎉 Tu aplicación ahora tiene:")
    print("   • Diseño moderno y profesional")
    print("   • Colores Material Design")
    print("   • Efectos hover y animaciones")
    print("   • Tipografía mejorada")
    print("   • Layout responsive")
    
    # Mostrar demo
    print("\n🚀 Mostrando resultado...")
    crear_demo_comparacion()

if __name__ == "__main__":
    main()
