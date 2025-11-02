import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import hashlib
from modulos.utils.estilos_modernos import estilos
from modulos.utils.utils import resource_path
from PIL import Image

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def verificar_login(usuario, password):
    """Verificar credenciales simples"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (usuario,))
        user_data = cursor.fetchone()
        
        if user_data and (user_data[2] == password_hash or user_data[2] == password):
            conn.close()
            return True
        
        conn.close()
        return False
    except:
        return False

def mostrar_login_simple():
    """Mostrar login moderno con CustomTkinter"""
    root = ctk.CTk()
    root.title("🔐 Sistema de Punto de Venta - Login")
    root.geometry("500x700+400+50")
    root.configure(fg_color=estilos.COLORS['bg_primary'])
    root.resizable(False, False)
    # Icono de la ventana
    try:
        icon_path = resource_path("media/icons/tienda.png")
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon_image)
        root._icon_image_ref = icon_image
    except Exception:
        pass
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"500x700+{x}+{y}")
    
    # Variables
    login_exitoso = False
    
    def intentar_login():
        nonlocal login_exitoso
        usuario = usuario_entry.get().strip()
        password = password_entry.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("❌ Error", "Por favor ingrese usuario y contraseña")
            return
        
        if verificar_login(usuario, password):
            login_exitoso = True
            messagebox.showinfo("✅ Bienvenido", f"¡Bienvenido {usuario}!\n\nAcceso concedido al sistema")
            root.quit()
            root.destroy()
        else:
            messagebox.showerror("❌ Error de Autenticación", 
                               "Usuario o contraseña incorrectos.\n\nVerifique sus credenciales e intente nuevamente.")
            password_entry.delete(0, 'end')
            usuario_entry.focus()
    
    # Frame principal
    main_frame = ctk.CTkFrame(root, 
                             fg_color=estilos.COLORS['white'],
                             corner_radius=20)
    main_frame.pack(fill='both', expand=True, padx=30, pady=30)
    
    # Logo/Icono principal (imagen tienda.png)
    try:
        _logo_img = ctk.CTkImage(light_image=Image.open(resource_path("media/icons/tienda.png")), size=(96, 96))
        logo_label = ctk.CTkLabel(main_frame, text="", image=_logo_img)
        logo_label.pack(pady=(40, 20))
        root._logo_img_ref = _logo_img
    except Exception:
        logo_label = ctk.CTkLabel(main_frame, text="🏪", font=ctk.CTkFont(size=80))
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
    
    usuario_entry = ctk.CTkEntry(form_frame, 
                                placeholder_text="Ingrese su usuario",
                                font=ctk.CTkFont(family="Segoe UI", size=12),
                                height=45,
                                corner_radius=10)
    usuario_entry.pack(fill='x', pady=(0, 20))
    
    # Campo Password
    password_label = ctk.CTkLabel(form_frame, 
                                 text="🔒 Contraseña:", 
                                 font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                 text_color=estilos.COLORS['dark'])
    password_label.pack(anchor='w', pady=(0, 5))
    
    password_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text="Ingrese su contraseña",
                                  font=ctk.CTkFont(family="Segoe UI", size=12),
                                  height=45,
                                  corner_radius=10,
                                  show="*")
    password_entry.pack(fill='x', pady=(0, 30))
    
    # Botón de Login
    login_button = ctk.CTkButton(form_frame, 
                                text="🔐 Iniciar Sesión", 
                                command=intentar_login,
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
    root.bind('<Return>', lambda event: intentar_login())
    
    # Focus en campo usuario
    usuario_entry.focus()
    
    # Ejecutar ventana
    root.mainloop()
    return login_exitoso

if __name__ == "__main__":
    if mostrar_login_simple():
        print("Login exitoso!")
    else:
        print("Login cancelado")
