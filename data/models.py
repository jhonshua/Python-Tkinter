# modelos/database.py
import sqlite3
import sys
def crear_base_de_datos():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Tabla de artículos (con código de barras)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                articulo TEXT NOT NULL,
                precio REAL NOT NULL,
                costo REAL NOT NULL,
                stock INTEGER NOT NULL,
                estado TEXT NOT NULL,
                imagen_path TEXT
            )
        ''')
        
        # Agregar columna codigo si no existe (para bases de datos existentes)
        try:
            cursor.execute("ALTER TABLE articulos ADD COLUMN codigo TEXT UNIQUE")
            print("Columna 'codigo' agregada a tabla articulos")
        except sqlite3.OperationalError:
            # La columna ya existe, continuar
            pass

        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cedula NUMERIC,
                celular NUMERIC,
                direccion TEXT,
                correo TEXT
            )
        ''')

        # Tabla de usuarios (si es necesario)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,  -- UNIQUE para evitar nombres de usuario repetidos
                password TEXT NOT NULL
            )
        ''')

        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura INTEGER,
                cliente TEXT,
                articulo TEXT,
                precio REAL,
                cantidad INTEGER,
                total REAL,
                fecha TEXT,
                hora TEXT,
                costo REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa TEXT NOT NULL,
                rif TEXT UNIQUE NOT NULL,  -- UNIQUE para evitar RIFs repetidos
                celular TEXT,
                direccion TEXT,
                correo TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("Base de datos y tablas creadas (o ya existentes).")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
        sys.exit()  # Salir de la app si no se puede crear la base de datos