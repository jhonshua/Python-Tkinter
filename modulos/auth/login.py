import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
import sqlite3
import hashlib
from PIL import Image, ImageTk

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self):
        self.window = None
        self.usuario_autenticado = False
        self.crear_tabla_usuarios()
        self.crear_usuario_admin()  # Crear usuario admin por defecto
        
    def crear_tabla_usuarios(self):
        """Crear tabla de usuarios si no existe o actualizar estructura"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Verificar si la tabla usuarios ya existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
            tabla_existe = cursor.fetchone()
            
            if tabla_existe:
                # La tabla existe, verificar y agregar columnas faltantes
                cursor.execute("PRAGMA table_info(usuarios)")
                columnas = [col[1] for col in cursor.fetchall()]
                print(f"📊 Columnas existentes en usuarios: {columnas}")
                
                # Agregar columnas faltantes si no existen
                if 'usuario' not in columnas and 'username' in columnas:
                    # Usar la tabla existente con username
                    print("✅ Usando tabla usuarios existente con username")
                elif 'usuario' not in columnas:
                    try:
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN usuario TEXT")
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN nombre TEXT")
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'usuario'")
                        cursor.execute("ALTER TABLE usuarios ADD COLUMN activo INTEGER DEFAULT 1")
                        print("✅ Columnas agregadas a tabla usuarios existente")
                    except sqlite3.OperationalError as e:
                        print(f"⚠️ No se pudieron agregar columnas: {e}")
            else:
                # Crear tabla nueva
                cursor.execute('''
                    CREATE TABLE usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        nombre TEXT NOT NULL,
                        rol TEXT DEFAULT 'usuario',
                        activo INTEGER DEFAULT 1,
                        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                print("✅ Tabla usuarios creada")
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"❌ Error al crear tabla de usuarios: {e}")
    
    def crear_usuario_admin(self):
        """Crear usuario administrador por defecto"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Verificar estructura de la tabla
            cursor.execute("PRAGMA table_info(usuarios)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            
            # Verificar si usar 'usuario' o 'username'
            if 'usuario' in columnas:
                # Verificar si ya existe el admin
                cursor.execute("SELECT id FROM usuarios WHERE usuario = 'admin'")
                if not cursor.fetchone():
                    if 'nombre' in columnas and 'rol' in columnas:
                        cursor.execute("""INSERT INTO usuarios (usuario, password, nombre, rol) 
                                        VALUES (?, ?, ?, ?)""", 
                                      ('admin', password_hash, 'Administrador', 'admin'))
                    else:
                        cursor.execute("""INSERT INTO usuarios (usuario, password) 
                                        VALUES (?, ?)""", 
                                      ('admin', password_hash))
                    conn.commit()
                    print("✅ Usuario admin creado: admin/admin123")
            elif 'username' in columnas:
                # Usar esquema existente
                cursor.execute("SELECT id FROM usuarios WHERE username = 'admin'")
                if not cursor.fetchone():
                    cursor.execute("""INSERT INTO usuarios (username, password) 
                                    VALUES (?, ?)""", 
                                  ('admin', password_hash))
                    conn.commit()
                    print("✅ Usuario admin creado: admin/admin123")
            
            conn.close()
        except sqlite3.Error as e:
            print(f"❌ Error al crear usuario admin: {e}")
    
    def hash_password(self, password):
        """Hashear password con SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_credenciales(self, usuario, password):
        """Verificar credenciales del usuario"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            # Buscar usuario
            cursor.execute("SELECT id, username, password FROM usuarios WHERE username = ?", (usuario,))
            usuario_db = cursor.fetchone()
            
            if usuario_db:
                id_usuario, username_db, password_db = usuario_db
                
                # Verificar contraseña (hash o texto plano)
                if password_db == password_hash or password_db == password:
                    conn.close()
                    return (id_usuario, username_db, 'admin')
            
            conn.close()
            return None
            
        except sqlite3.Error as e:
            print(f"❌ Error al verificar credenciales: {e}")
            return None
    
    def mostrar_login(self):
        """Mostrar ventana de login"""
        self.window = ctk.CTk()
        self.window.title("🔐 Sistema de Punto de Venta - Login")
        self.window.geometry("500x700+400+50")
        self.window.configure(fg_color=estilos.COLORS['bg_primary'])
        self.window.resizable(False, False)
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"500x700+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.window, 
                                 fg_color=estilos.COLORS['white'],
                                 corner_radius=20)
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Logo/Icono principal
        logo_label = ctk.CTkLabel(main_frame, 
                                 text="🏪", 
                                 font=ctk.CTkFont(size=80))
        logo_label.pack(pady=(40, 20))
        
        # Título principal
        title_label = ctk.CTkLabel(main_frame, 
                                  text="Sistema de Punto de Venta", 
                                  font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
                                  text_color=estilos.COLORS['primary'])
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(main_frame, 
                                     text="Versión 2.0 Moderna", 
                                     font=ctk.CTkFont(family="Segoe UI", size=14),
                                     text_color=estilos.COLORS['gray'])
        subtitle_label.pack(pady=(0, 40))
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(main_frame, 
                                 fg_color="transparent")
        form_frame.pack(fill='x', padx=40, pady=20)
        
        # Campo Usuario
        user_label = ctk.CTkLabel(form_frame, 
                                 text="👤 Usuario:", 
                                 font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                 text_color=estilos.COLORS['dark'])
        user_label.pack(anchor='w', pady=(0, 5))
        
        self.usuario_entry = ctk.CTkEntry(form_frame, 
                                         placeholder_text="Ingrese su usuario",
                                         font=ctk.CTkFont(family="Segoe UI", size=12),
                                         height=45,
                                         corner_radius=10)
        self.usuario_entry.pack(fill='x', pady=(0, 20))
        
        # Campo Password
        password_label = ctk.CTkLabel(form_frame, 
                                     text="🔒 Contraseña:", 
                                     font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                     text_color=estilos.COLORS['dark'])
        password_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(form_frame, 
                                          placeholder_text="Ingrese su contraseña",
                                          font=ctk.CTkFont(family="Segoe UI", size=12),
                                          height=45,
                                          corner_radius=10,
                                          show="*")
        self.password_entry.pack(fill='x', pady=(0, 30))
        
        # Botón de Login
        login_button = ctk.CTkButton(form_frame, 
                                    text="🔐 Iniciar Sesión", 
                                    command=self.iniciar_sesion,
                                    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                    height=50,
                                    corner_radius=15,
                                    fg_color=estilos.COLORS['primary'],
                                    hover_color=estilos.COLORS['primary_dark'])
        login_button.pack(fill='x', pady=(0, 20))
        
        # Información de usuario demo
        info_frame = ctk.CTkFrame(main_frame, 
                                 fg_color=estilos.COLORS['light'],
                                 corner_radius=10)
        info_frame.pack(fill='x', padx=40, pady=20)
        
        info_title = ctk.CTkLabel(info_frame, 
                                 text="ℹ️ Credenciales de Prueba", 
                                 font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                 text_color=estilos.COLORS['info'])
        info_title.pack(pady=(15, 5))
        
        info_text = ctk.CTkLabel(info_frame, 
                                text="Usuario: admin\nContraseña: admin123", 
                                font=ctk.CTkFont(family="Segoe UI", size=11),
                                text_color=estilos.COLORS['dark'])
        info_text.pack(pady=(0, 15))
        
        # Footer
        footer_label = ctk.CTkLabel(main_frame, 
                                   text="© 2024 Sistema POS Moderno", 
                                   font=ctk.CTkFont(family="Segoe UI", size=10),
                                   text_color=estilos.COLORS['gray'])
        footer_label.pack(side='bottom', pady=20)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda event: self.iniciar_sesion())
        
        # Focus en campo usuario
        self.usuario_entry.focus()
        
        # Ejecutar ventana
        self.window.mainloop()
        
        return self.usuario_autenticado
    
    def iniciar_sesion(self):
        """Procesar inicio de sesión"""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()
        
        print(f"🔐 Intento de login: usuario='{usuario}', password='{password}'")
        
        # Validaciones básicas
        if not usuario or not password:
            messagebox.showerror("❌ Error", "Por favor ingrese usuario y contraseña")
            return
        
        # Verificar credenciales
        resultado = self.verificar_credenciales(usuario, password)
        print(f"🎯 Resultado verificación: {resultado}")
        
        if resultado:
            user_id, nombre, rol = resultado
            self.usuario_autenticado = True
            print(f"✅ Login exitoso para: {nombre}")
            
            # Mostrar mensaje de bienvenida
            messagebox.showinfo("✅ Bienvenido", 
                              f"¡Bienvenido {nombre}!\n\nRol: {rol.title()}\nAcceso concedido al sistema")
            
            # Cerrar ventana de login
            print("🚪 Cerrando ventana de login...")
            self.window.quit()  # Cambiar destroy() por quit()
            self.window.destroy()
            
        else:
            print("❌ Login fallido")
            # Credenciales incorrectas
            messagebox.showerror("❌ Error de Autenticación", 
                               "Usuario o contraseña incorrectos.\n\nVerifique sus credenciales e intente nuevamente.")
            
            # Limpiar campos
            self.password_entry.delete(0, 'end')
            self.usuario_entry.focus()
    
    def cerrar_aplicacion(self):
        """Cerrar aplicación"""
        self.window.destroy()

# Función para mostrar login
def mostrar_login():
    """Función principal para mostrar login"""
    login = LoginWindow()
    return login.mostrar_login()
