import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from modulos.utils.estilos_modernos import estilos
import sqlite3
import hashlib
from datetime import datetime

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class GestorConfiguracion:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.modo_edicion = False
        self.usuario_editando_id = None
        self.crear_tablas_configuracion()
        
    def crear_tablas_configuracion(self):
        """Crear tablas de configuración"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Tabla de configuración del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion_sistema (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT UNIQUE NOT NULL,
                    valor TEXT NOT NULL,
                    descripcion TEXT,
                    fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insertar configuraciones por defecto
            configuraciones_default = [
                ('moneda_principal', 'USD', 'Moneda principal del sistema (USD/VES)'),
                ('tasa_cambio', '36.50', 'Tasa de cambio USD a VES'),
                ('simbolo_ves', 'Bs.', 'Símbolo para Bolívares'),
                ('simbolo_usd', '$', 'Símbolo para Dólares'),
                ('mostrar_ambas_monedas', '1', 'Mostrar precios en ambas monedas (1=Sí, 0=No)'),
                ('nombre_empresa', 'Mi Tienda', 'Nombre de la empresa'),
                ('direccion_empresa', 'Caracas, Venezuela', 'Dirección de la empresa'),
                ('telefono_empresa', '+58-212-1234567', 'Teléfono de la empresa'),
                ('rif_empresa', 'J-00000000-0', 'RIF de la empresa')
            ]
            
            for clave, valor, descripcion in configuraciones_default:
                cursor.execute('''
                    INSERT OR IGNORE INTO configuracion_sistema (clave, valor, descripcion)
                    VALUES (?, ?, ?)
                ''', (clave, valor, descripcion))
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al crear tablas de configuración: {e}")
    
    def abrir_ventana_configuracion(self):
        """Abrir ventana principal de configuración"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Configuración del Sistema")
        self.window.geometry("1000x700+250+50")
        self.window.configure(bg=estilos.COLORS['bg_primary'])
        self.window.resizable(True, True)
        self.window.grab_set()
        self.window.focus_set()
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pestaña 1: Usuarios
        self.crear_pestaña_usuarios(notebook)
        
        # Pestaña 2: Monedas
        self.crear_pestaña_monedas(notebook)
        
        # Pestaña 3: Empresa
        self.crear_pestaña_empresa(notebook)
    
    def crear_pestaña_usuarios(self, notebook):
        """Crear pestaña de gestión de usuarios"""
        frame_usuarios = tk.Frame(notebook, bg=estilos.COLORS['bg_primary'])
        notebook.add(frame_usuarios, text="👥 Usuarios")
        
        # Título
        title_label = tk.Label(frame_usuarios, text="👥 Gestión de Usuarios", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=estilos.COLORS['bg_primary'],
                              fg=estilos.COLORS['primary'])
        title_label.pack(pady=(20, 30))
        
        # Frame principal dividido
        main_frame = tk.Frame(frame_usuarios, bg=estilos.COLORS['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Frame izquierdo - Formulario
        self.form_frame_label = tk.LabelFrame(main_frame, text="➕ Nuevo Usuario", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['primary'])
        self.form_frame_label.pack(side='left', fill='y', padx=(0, 10), pady=10)
        
        # Campos del formulario
        tk.Label(self.form_frame_label, text="👤 Usuario:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.nuevo_usuario = tk.Entry(self.form_frame_label, font=('Segoe UI', 11), width=20)
        self.nuevo_usuario.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.form_frame_label, text="🔒 Contraseña:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.nueva_password = tk.Entry(self.form_frame_label, font=('Segoe UI', 11), width=20, show="*")
        self.nueva_password.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.form_frame_label, text="📝 Nombre:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.nuevo_nombre = tk.Entry(self.form_frame_label, font=('Segoe UI', 11), width=20)
        self.nuevo_nombre.grid(row=2, column=1, padx=10, pady=5)
        
        # Frame para botones
        buttons_form_frame = tk.Frame(self.form_frame_label, bg=estilos.COLORS['white'])
        buttons_form_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Botones
        self.btn_crear_guardar = ctk.CTkButton(buttons_form_frame, text="➕ Crear Usuario", 
                                 command=self.crear_o_actualizar_usuario,
                                 width=180, height=40,
                                 font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                 fg_color=estilos.COLORS['success'])
        self.btn_crear_guardar.pack(side='left', padx=5)
        
        self.btn_cancelar = ctk.CTkButton(buttons_form_frame, text="❌ Cancelar", 
                                 command=self.cancelar_edicion,
                                 width=100, height=40,
                                 font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                 fg_color=estilos.COLORS['danger'])
        self.btn_cancelar.pack(side='left', padx=5)
        self.btn_cancelar.pack_forget()  # Ocultar inicialmente
        
        # Frame derecho - Lista de usuarios
        list_frame = tk.LabelFrame(main_frame, text="📋 Usuarios Registrados", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['primary'])
        list_frame.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=10)
        
        # Treeview para usuarios
        self.tree_usuarios = ttk.Treeview(list_frame, 
                                         columns=("ID", "Usuario", "Nombre"), 
                                         show="headings", height=15)
        self.tree_usuarios.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_usuarios.heading("ID", text="ID")
        self.tree_usuarios.heading("Usuario", text="Usuario")
        self.tree_usuarios.heading("Nombre", text="Nombre")
        
        self.tree_usuarios.column("ID", width=50, anchor="center")
        self.tree_usuarios.column("Usuario", width=150, anchor="w")
        self.tree_usuarios.column("Nombre", width=200, anchor="w")
        
        # Frame para botones de acción
        buttons_list_frame = tk.Frame(list_frame, bg=estilos.COLORS['white'])
        buttons_list_frame.pack(pady=10)
        
        # Botón editar
        btn_editar = ctk.CTkButton(buttons_list_frame, text="✏️ Editar Usuario", 
                                    command=self.editar_usuario,
                                    width=180, height=40,
                                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                    fg_color=estilos.COLORS['info'])
        btn_editar.pack(side='left', padx=5)
        
        # Botón eliminar
        btn_eliminar = ctk.CTkButton(buttons_list_frame, text="🗑️ Eliminar Usuario", 
                                    command=self.eliminar_usuario,
                                    width=180, height=40,
                                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                    fg_color=estilos.COLORS['danger'])
        btn_eliminar.pack(side='left', padx=5)
        
        # Permitir doble clic para editar
        self.tree_usuarios.bind('<Double-1>', lambda e: self.editar_usuario())
        
        self.cargar_usuarios()
    
    def crear_pestaña_monedas(self, notebook):
        """Crear pestaña de configuración de monedas"""
        frame_monedas = tk.Frame(notebook, bg=estilos.COLORS['bg_primary'])
        notebook.add(frame_monedas, text="💰 Monedas")
        
        # Título
        title_label = tk.Label(frame_monedas, text="💰 Configuración de Monedas", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=estilos.COLORS['bg_primary'],
                              fg=estilos.COLORS['primary'])
        title_label.pack(pady=(20, 30))
        
        # Frame principal
        main_frame = tk.Frame(frame_monedas, bg=estilos.COLORS['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=40)
        
        # Configuración de moneda principal
        moneda_frame = tk.LabelFrame(main_frame, text="🏦 Moneda Principal", 
                                    font=('Segoe UI', 14, 'bold'), 
                                    bg=estilos.COLORS['white'],
                                    fg=estilos.COLORS['primary'])
        moneda_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(moneda_frame, text="💵 Moneda Principal:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=0, column=0, sticky='w', padx=20, pady=15)
        
        self.moneda_principal = ttk.Combobox(moneda_frame, font=('Segoe UI', 11), 
                                           values=["USD", "VES"], state="readonly", width=10)
        self.moneda_principal.grid(row=0, column=1, padx=20, pady=15)
        
        # Tasa de cambio
        tasa_frame = tk.LabelFrame(main_frame, text="📈 Tasa de Cambio", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['primary'])
        tasa_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(tasa_frame, text="💱 1 USD = ", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=0, column=0, sticky='w', padx=20, pady=15)
        
        self.tasa_cambio = tk.Entry(tasa_frame, font=('Segoe UI', 11), width=15)
        self.tasa_cambio.grid(row=0, column=1, padx=5, pady=15)
        
        # Bind para actualizar vista previa automáticamente
        self.tasa_cambio.bind('<KeyRelease>', lambda e: self.actualizar_preview())
        self.moneda_principal.bind('<<ComboboxSelected>>', lambda e: self.actualizar_preview())
        
        tk.Label(tasa_frame, text="Bs.", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=0, column=2, sticky='w', padx=5, pady=15)
        
        # Switch para mostrar ambas monedas
        switch_frame = tk.LabelFrame(main_frame, text="🔄 Opciones de Visualización", 
                                    font=('Segoe UI', 14, 'bold'), 
                                    bg=estilos.COLORS['white'],
                                    fg=estilos.COLORS['primary'])
        switch_frame.pack(fill='x', pady=(0, 20))
        
        self.mostrar_ambas = tk.BooleanVar()
        switch_check = tk.Checkbutton(switch_frame, text="Mostrar precios en ambas monedas", 
                                     variable=self.mostrar_ambas,
                                     font=('Segoe UI', 12), 
                                     bg=estilos.COLORS['white'],
                                     command=self.actualizar_preview)
        switch_check.pack(padx=20, pady=15, anchor='w')
        
        # Botones de acción
        buttons_frame = tk.Frame(main_frame, bg=estilos.COLORS['bg_primary'])
        buttons_frame.pack(fill='x', pady=20)
        
        btn_guardar = ctk.CTkButton(buttons_frame, text="💾 Guardar Configuración", 
                                   command=self.guardar_configuracion_monedas,
                                   width=200, height=45,
                                   font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                   fg_color=estilos.COLORS['success'])
        btn_guardar.pack(side='left', padx=10)
        
        btn_actualizar_tasa = ctk.CTkButton(buttons_frame, text="💱 Ingresar Tasa del Día", 
                                           command=self.ingresar_tasa_dia,
                                           width=200, height=45,
                                           font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                           fg_color=estilos.COLORS['info'])
        btn_actualizar_tasa.pack(side='left', padx=10)
        
        # Vista previa de conversión
        preview_frame = tk.LabelFrame(main_frame, text="👁️ Vista Previa", 
                                     font=('Segoe UI', 14, 'bold'), 
                                     bg=estilos.COLORS['white'],
                                     fg=estilos.COLORS['primary'])
        preview_frame.pack(fill='x')
        
        self.preview_label = tk.Label(preview_frame, text="Ejemplo: $10.00 = Bs. 365.00", 
                                     font=('Segoe UI', 12), 
                                     bg=estilos.COLORS['white'],
                                     fg=estilos.COLORS['dark'])
        self.preview_label.pack(pady=15)
        
        self.cargar_configuracion_monedas()
    
    def crear_pestaña_empresa(self, notebook):
        """Crear pestaña de información de la empresa"""
        frame_empresa = tk.Frame(notebook, bg=estilos.COLORS['bg_primary'])
        notebook.add(frame_empresa, text="🏢 Empresa")
        
        # Título
        title_label = tk.Label(frame_empresa, text="🏢 Información de la Empresa", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=estilos.COLORS['bg_primary'],
                              fg=estilos.COLORS['primary'])
        title_label.pack(pady=(20, 30))
        
        # Frame principal
        main_frame = tk.LabelFrame(frame_empresa, text="📋 Datos de la Empresa", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg=estilos.COLORS['white'],
                                  fg=estilos.COLORS['primary'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Campos de la empresa
        tk.Label(main_frame, text="🏢 Nombre:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=0, column=0, sticky='w', padx=20, pady=15)
        self.nombre_empresa = tk.Entry(main_frame, font=('Segoe UI', 11), width=40)
        self.nombre_empresa.grid(row=0, column=1, padx=20, pady=15)
        
        tk.Label(main_frame, text="📍 Dirección:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=1, column=0, sticky='w', padx=20, pady=15)
        self.direccion_empresa = tk.Entry(main_frame, font=('Segoe UI', 11), width=40)
        self.direccion_empresa.grid(row=1, column=1, padx=20, pady=15)
        
        tk.Label(main_frame, text="📞 Teléfono:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=2, column=0, sticky='w', padx=20, pady=15)
        self.telefono_empresa = tk.Entry(main_frame, font=('Segoe UI', 11), width=40)
        self.telefono_empresa.grid(row=2, column=1, padx=20, pady=15)
        
        tk.Label(main_frame, text="🏢 RIF:", font=('Segoe UI', 12, 'bold'), 
                bg=estilos.COLORS['white']).grid(row=3, column=0, sticky='w', padx=20, pady=15)
        self.rif_empresa = tk.Entry(main_frame, font=('Segoe UI', 11), width=40)
        self.rif_empresa.grid(row=3, column=1, padx=20, pady=15)
        
        # Botón guardar
        btn_guardar_empresa = ctk.CTkButton(main_frame, text="💾 Guardar Información", 
                                           command=self.guardar_info_empresa,
                                           width=250, height=45,
                                           font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                           fg_color=estilos.COLORS['success'])
        btn_guardar_empresa.grid(row=4, column=0, columnspan=2, pady=30)
        
        self.cargar_info_empresa()
    
    # Funciones de usuarios
    def crear_o_actualizar_usuario(self):
        """Crear nuevo usuario o actualizar usuario existente"""
        usuario = self.nuevo_usuario.get().strip()
        password = self.nueva_password.get().strip()
        nombre = self.nuevo_nombre.get().strip()
        
        if not usuario:
            messagebox.showerror("❌ Error", "El campo Usuario es requerido")
            return
        
        if not self.modo_edicion and not password:
            messagebox.showerror("❌ Error", "El campo Contraseña es requerido para nuevos usuarios")
            return
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            if self.modo_edicion:
                # Modo edición: actualizar usuario existente
                if self.usuario_editando_id is None:
                    messagebox.showerror("❌ Error", "Error: No se ha seleccionado un usuario para editar")
                    conn.close()
                    return
                
                # Verificar si el nuevo nombre de usuario ya existe (y no es el mismo usuario)
                cursor.execute("SELECT id, username FROM usuarios WHERE username = ?", (usuario,))
                usuario_existente = cursor.fetchone()
                if usuario_existente and usuario_existente[0] != self.usuario_editando_id:
                    messagebox.showerror("❌ Error", "El nombre de usuario ya existe")
                    conn.close()
                    return
                
                # Obtener el nombre de usuario actual antes de cambiar
                cursor.execute("SELECT username FROM usuarios WHERE id = ?", (self.usuario_editando_id,))
                usuario_actual = cursor.fetchone()
                es_admin = usuario_actual and usuario_actual[0] == 'admin'
                
                # Actualizar usuario
                if password:
                    # Si se ingresó una nueva contraseña, actualizarla
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    cursor.execute("UPDATE usuarios SET username = ?, password = ? WHERE id = ?", 
                                  (usuario, password_hash, self.usuario_editando_id))
                else:
                    # Si no se ingresó contraseña, solo actualizar el nombre de usuario
                    cursor.execute("UPDATE usuarios SET username = ? WHERE id = ?", 
                                  (usuario, self.usuario_editando_id))
                
                # Advertencia especial si se cambió el admin
                if es_admin:
                    mensaje_extra = "\n\n⚠️ IMPORTANTE: Se han modificado las credenciales del usuario administrador."
                    if password:
                        mensaje_extra += "\n🔒 La nueva contraseña ha sido actualizada."
                else:
                    mensaje_extra = ""
                
                conn.commit()
                conn.close()
                
                mensaje_exito = f"Usuario '{usuario}' actualizado correctamente"
                if es_admin:
                    mensaje_exito += mensaje_extra
                messagebox.showinfo("✅ Éxito", mensaje_exito)
                
            else:
                # Modo creación: crear nuevo usuario
                if not password:
                    messagebox.showerror("❌ Error", "El campo Contraseña es requerido")
                    conn.close()
                    return
                
                # Verificar si el usuario ya existe
                cursor.execute("SELECT username FROM usuarios WHERE username = ?", (usuario,))
                if cursor.fetchone():
                    messagebox.showerror("❌ Error", "El usuario ya existe")
                    conn.close()
                    return
                
                # Hash de la contraseña
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Insertar usuario
                cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", 
                              (usuario, password_hash))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("✅ Éxito", f"Usuario '{usuario}' creado correctamente")
            
            # Limpiar campos y salir del modo edición
            self.cancelar_edicion()
            
            # Recargar lista
            self.cargar_usuarios()
            
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al {'actualizar' if self.modo_edicion else 'crear'} usuario: {e}")
    
    def editar_usuario(self):
        """Cargar datos del usuario seleccionado para editar"""
        selection = self.tree_usuarios.selection()
        if not selection:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione un usuario para editar")
            return
        
        item = selection[0]
        valores = self.tree_usuarios.item(item, "values")
        usuario_id = int(valores[0])
        username = valores[1]
        
        # Advertencia especial si es el usuario admin
        if username == 'admin':
            respuesta = messagebox.askyesno(
                "⚠️ Advertencia de Seguridad",
                "Está intentando editar el usuario administrador.\n\n"
                "⚠️ IMPORTANTE:\n"
                "• Asegúrese de recordar la nueva contraseña.\n"
                "• Si olvida la contraseña, no podrá acceder al sistema.\n"
                "• Se recomienda crear un usuario alternativo antes de cambiar el admin.\n\n"
                "¿Desea continuar con la edición del usuario administrador?",
                icon='warning'
            )
            if not respuesta:
                return
        
        try:
            # Obtener datos del usuario
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM usuarios WHERE id = ?", (usuario_id,))
            usuario_data = cursor.fetchone()
            conn.close()
            
            if not usuario_data:
                messagebox.showerror("❌ Error", "Usuario no encontrado")
                return
            
            # Activar modo edición
            self.modo_edicion = True
            self.usuario_editando_id = usuario_id
            
            # Cargar datos en el formulario
            self.nuevo_usuario.delete(0, 'end')
            self.nuevo_usuario.insert(0, usuario_data[1])
            
            self.nueva_password.delete(0, 'end')
            self.nueva_password.insert(0, "")  # Dejar vacío para no mostrar contraseña
            
            self.nuevo_nombre.delete(0, 'end')
            self.nuevo_nombre.insert(0, usuario_data[1])  # Usar username como nombre por defecto
            
            # Actualizar interfaz
            if username == 'admin':
                self.form_frame_label.config(text="⚠️ Editar Usuario Administrador")
                self.btn_crear_guardar.config(text="💾 Guardar Cambios", fg_color=estilos.COLORS['warning'])
            else:
                self.form_frame_label.config(text="✏️ Editar Usuario")
                self.btn_crear_guardar.config(text="💾 Guardar Cambios", fg_color=estilos.COLORS['info'])
            self.btn_cancelar.pack(side='left', padx=5)
            
            # Seleccionar el campo de usuario
            self.nuevo_usuario.focus()
            
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar usuario: {e}")
    
    def cancelar_edicion(self):
        """Cancelar modo edición y limpiar formulario"""
        self.modo_edicion = False
        self.usuario_editando_id = None
        
        # Limpiar campos
        self.nuevo_usuario.delete(0, 'end')
        self.nueva_password.delete(0, 'end')
        self.nuevo_nombre.delete(0, 'end')
        
        # Restaurar interfaz
        self.form_frame_label.config(text="➕ Nuevo Usuario")
        self.btn_crear_guardar.config(text="➕ Crear Usuario", fg_color=estilos.COLORS['success'])
        self.btn_cancelar.pack_forget()
        
        # Deseleccionar en el treeview
        for item in self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(item)
    
    def eliminar_usuario(self):
        """Eliminar usuario seleccionado"""
        selection = self.tree_usuarios.selection()
        if not selection:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione un usuario para eliminar")
            return
        
        item = selection[0]
        valores = self.tree_usuarios.item(item, "values")
        usuario_id = valores[0]
        username = valores[1]
        
        if username == 'admin':
            messagebox.showerror("❌ Error", "No se puede eliminar el usuario administrador")
            return
        
        respuesta = messagebox.askyesno("⚠️ Confirmar", 
                                      f"¿Eliminar el usuario '{username}'?\n\nEsta acción no se puede deshacer.")
        
        if respuesta:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("✅ Éxito", f"Usuario '{username}' eliminado")
                self.cargar_usuarios()
                
            except sqlite3.Error as e:
                messagebox.showerror("❌ Error", f"Error al eliminar usuario: {e}")
    
    def cargar_usuarios(self):
        """Cargar lista de usuarios"""
        try:
            # Limpiar tabla
            for item in self.tree_usuarios.get_children():
                self.tree_usuarios.delete(item)
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM usuarios ORDER BY username")
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                # Usar username como nombre si no hay campo nombre
                self.tree_usuarios.insert("", "end", values=(usuario[0], usuario[1], usuario[1]))
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar usuarios: {e}")
    
    # Funciones de monedas
    def cargar_configuracion_monedas(self):
        """Cargar configuración de monedas"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Cargar configuraciones
            cursor.execute("SELECT clave, valor FROM configuracion_sistema WHERE clave IN ('moneda_principal', 'tasa_cambio', 'mostrar_ambas_monedas')")
            configs = dict(cursor.fetchall())
            
            self.moneda_principal.set(configs.get('moneda_principal', 'USD'))
            self.tasa_cambio.delete(0, 'end')
            self.tasa_cambio.insert(0, configs.get('tasa_cambio', '36.50'))
            self.mostrar_ambas.set(configs.get('mostrar_ambas_monedas', '1') == '1')
            
            conn.close()
            self.actualizar_preview()
            
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar configuración: {e}")
    
    def guardar_configuracion_monedas(self):
        """Guardar configuración de monedas"""
        try:
            tasa = float(self.tasa_cambio.get())
            if tasa <= 0:
                raise ValueError("La tasa debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("❌ Error", "Ingrese una tasa de cambio válida")
            return
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Actualizar configuraciones
            configs = [
                ('moneda_principal', self.moneda_principal.get()),
                ('tasa_cambio', self.tasa_cambio.get()),
                ('mostrar_ambas_monedas', '1' if self.mostrar_ambas.get() else '0')
            ]
            
            for clave, valor in configs:
                cursor.execute('''
                    INSERT OR REPLACE INTO configuracion_sistema 
                    (clave, valor, descripcion, fecha_modificacion) 
                    VALUES (?, ?, ?, ?)
                ''', (clave, valor, f'Configuración de {clave}', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            # Verificar que se guardó correctamente
            cursor.execute("SELECT valor FROM configuracion_sistema WHERE clave = 'tasa_cambio'")
            tasa_guardada = cursor.fetchone()
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("✅ Éxito", f"Configuración guardada correctamente\n\nTasa de cambio: {tasa_guardada[0] if tasa_guardada else 'Error'}")
            self.actualizar_preview()
            
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al guardar configuración: {e}")
    
    def ingresar_tasa_dia(self):
        """Permitir ingresar manualmente la tasa del día"""
        from tkinter import simpledialog
        
        # Obtener tasa actual
        tasa_actual = self.tasa_cambio.get()
        
        # Solicitar nueva tasa
        nueva_tasa = simpledialog.askfloat(
            "💱 Tasa del Día",
            f"Ingrese la tasa de cambio actual:\n\n" +
            f"Tasa actual: {tasa_actual} Bs. por USD\n\n" +
            f"Nueva tasa (solo números):",
            initialvalue=float(tasa_actual) if tasa_actual else 36.50,
            minvalue=1.0,
            maxvalue=1000.0
        )
        
        if nueva_tasa:
            try:
                # Actualizar el campo
                self.tasa_cambio.delete(0, 'end')
                self.tasa_cambio.insert(0, str(nueva_tasa))
                
                # Actualizar vista previa
                self.actualizar_preview()
                
                messagebox.showinfo("✅ Tasa Actualizada", 
                                   f"Nueva tasa ingresada:\n\n" +
                                   f"💱 1 USD = {nueva_tasa} Bs.\n\n" +
                                   f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n" +
                                   "⚠️ Recuerde guardar la configuración para aplicar los cambios.")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error al actualizar tasa: {e}")
    
    def actualizar_preview(self):
        """Actualizar vista previa de conversión"""
        try:
            tasa = float(self.tasa_cambio.get())
            ejemplo_usd = 1.00  # Cambiar a 1 USD para que coincida con la interfaz
            ejemplo_ves = ejemplo_usd * tasa
            
            if self.mostrar_ambas.get():
                preview_text = f"Ejemplo: ${ejemplo_usd:.2f} = Bs. {ejemplo_ves:,.2f} (Ambas monedas)"
            else:
                moneda = self.moneda_principal.get()
                if moneda == 'USD':
                    preview_text = f"Ejemplo: ${ejemplo_usd:.2f} (Solo USD)"
                else:
                    preview_text = f"Ejemplo: Bs. {ejemplo_ves:,.2f} (Solo VES)"
            
            self.preview_label.config(text=preview_text)
        except:
            self.preview_label.config(text="Vista previa no disponible")
    
    # Funciones de empresa
    def cargar_info_empresa(self):
        """Cargar información de la empresa"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT clave, valor FROM configuracion_sistema WHERE clave IN ('nombre_empresa', 'direccion_empresa', 'telefono_empresa', 'rif_empresa')")
            configs = dict(cursor.fetchall())
            
            self.nombre_empresa.delete(0, 'end')
            self.nombre_empresa.insert(0, configs.get('nombre_empresa', 'Mi Tienda'))
            
            self.direccion_empresa.delete(0, 'end')
            self.direccion_empresa.insert(0, configs.get('direccion_empresa', 'Caracas, Venezuela'))
            
            self.telefono_empresa.delete(0, 'end')
            self.telefono_empresa.insert(0, configs.get('telefono_empresa', '+58-212-1234567'))
            
            self.rif_empresa.delete(0, 'end')
            self.rif_empresa.insert(0, configs.get('rif_empresa', 'J-00000000-0'))
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al cargar información: {e}")
    
    def guardar_info_empresa(self):
        """Guardar información de la empresa"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            configs = [
                ('nombre_empresa', self.nombre_empresa.get()),
                ('direccion_empresa', self.direccion_empresa.get()),
                ('telefono_empresa', self.telefono_empresa.get()),
                ('rif_empresa', self.rif_empresa.get())
            ]
            
            for clave, valor in configs:
                cursor.execute('''
                    INSERT OR REPLACE INTO configuracion_sistema 
                    (clave, valor, descripcion, fecha_modificacion) 
                    VALUES (?, ?, ?, ?)
                ''', (clave, valor, f'Configuración de {clave}', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("✅ Éxito", "Información de la empresa guardada correctamente")
            
        except sqlite3.Error as e:
            messagebox.showerror("❌ Error", f"Error al guardar información: {e}")

# Funciones globales para obtener configuración
def obtener_configuracion(clave, default=None):
    """Obtener valor de configuración"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT valor FROM configuracion_sistema WHERE clave = ?", (clave,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else default
    except:
        return default

def formatear_precio(precio, mostrar_ambas=None):
    """Formatear precio según configuración de monedas"""
    try:
        if mostrar_ambas is None:
            mostrar_ambas = obtener_configuracion('mostrar_ambas_monedas', '1') == '1'
        
        moneda_principal = obtener_configuracion('moneda_principal', 'USD')
        tasa_cambio = float(obtener_configuracion('tasa_cambio', '36.50'))
        
        precio_float = float(precio)
        
        if mostrar_ambas:
            if moneda_principal == 'USD':
                precio_ves = precio_float * tasa_cambio
                return f"${precio_float:.2f} (Bs. {precio_ves:,.2f})"
            else:
                precio_usd = precio_float / tasa_cambio
                return f"Bs. {precio_float:,.2f} (${precio_usd:.2f})"
        else:
            if moneda_principal == 'USD':
                return f"${precio_float:.2f}"
            else:
                return f"Bs. {precio_float:,.2f}"
    except:
        return f"${precio:.2f}"
