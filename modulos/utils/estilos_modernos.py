"""
Módulo de estilos modernos para la aplicación de punto de venta
Contiene paletas de colores, fuentes y configuraciones de estilo
"""

class EstilosModernos:
    """Clase que contiene todos los estilos modernos para la aplicación"""
    
    # Paleta de colores principal (Material Design inspired)
    COLORS = {
        # Colores primarios
        'primary': '#1e3a8a',          # Azul profundo
        'primary_light': '#3b82f6',    # Azul claro
        'primary_dark': '#1e40af',     # Azul oscuro
        
        # Colores secundarios
        'secondary': '#10b981',        # Verde esmeralda
        'secondary_light': '#34d399',  # Verde claro
        'secondary_dark': '#059669',   # Verde oscuro
        
        # Colores de estado
        'success': '#22c55e',          # Verde éxito
        'warning': '#f59e0b',          # Amarillo advertencia
        'danger': '#ef4444',           # Rojo peligro
        'info': '#3b82f6',             # Azul información
        
        # Colores neutros
        'white': '#ffffff',            # Blanco puro
        'light': '#f8fafc',            # Gris muy claro
        'light_gray': '#e2e8f0',       # Gris claro
        'gray': '#64748b',             # Gris medio
        'dark_gray': '#475569',        # Gris oscuro
        'dark': '#1e293b',             # Gris muy oscuro
        'black': '#0f172a',            # Negro
        
        # Colores de acento
        'accent': '#8b5cf6',           # Morado
        'accent_light': '#a78bfa',     # Morado claro
        'accent_dark': '#7c3aed',      # Morado oscuro
        
        # Colores de fondo
        'bg_primary': '#f1f5f9',       # Fondo principal
        'bg_secondary': '#ffffff',     # Fondo secundario
        'bg_card': '#ffffff',          # Fondo de tarjetas
        'bg_hover': '#f1f5f9',         # Fondo hover
        
        # Colores de borde
        'border': '#e2e8f0',           # Borde normal
        'border_focus': '#3b82f6',     # Borde enfocado
        'border_error': '#ef4444',     # Borde error
    }
    
    # Fuentes
    FONTS = {
        'primary': 'Segoe UI',
        'secondary': 'Arial',
        'monospace': 'Consolas',
        'sizes': {
            'xs': 8,
            'sm': 10,
            'base': 11,
            'lg': 12,
            'xl': 14,
            '2xl': 16,
            '3xl': 18,
            '4xl': 20,
            '5xl': 24,
        }
    }
    
    # Configuraciones de botones
    BUTTON_STYLES = {
        'primary': {
            'bg': COLORS['primary'],
            'fg': COLORS['white'],
            'hover_bg': COLORS['primary_dark'],
            'active_bg': COLORS['primary_light'],
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'secondary': {
            'bg': COLORS['secondary'],
            'fg': COLORS['white'],
            'hover_bg': COLORS['secondary_dark'],
            'active_bg': COLORS['secondary_light'],
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'success': {
            'bg': COLORS['success'],
            'fg': COLORS['white'],
            'hover_bg': '#16a34a',
            'active_bg': '#22c55e',
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'warning': {
            'bg': COLORS['warning'],
            'fg': COLORS['white'],
            'hover_bg': '#d97706',
            'active_bg': '#f59e0b',
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'danger': {
            'bg': COLORS['danger'],
            'fg': COLORS['white'],
            'hover_bg': '#dc2626',
            'active_bg': '#ef4444',
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'outline': {
            'bg': COLORS['white'],
            'fg': COLORS['primary'],
            'hover_bg': COLORS['bg_hover'],
            'active_bg': COLORS['light_gray'],
            'font': (FONTS['primary'], FONTS['sizes']['base'], 'bold'),
            'padding': (15, 8),
            'relief': 'solid',
            'bd': 1,
            'cursor': 'hand2'
        }
    }
    
    # Configuraciones de frames/tarjetas
    CARD_STYLES = {
        'default': {
            'bg': COLORS['bg_card'],
            'relief': 'flat',
            'bd': 1,
            'highlightbackground': COLORS['border'],
            'highlightthickness': 1
        },
        'elevated': {
            'bg': COLORS['bg_card'],
            'relief': 'raised',
            'bd': 2,
            'highlightbackground': COLORS['light_gray'],
            'highlightthickness': 1
        }
    }
    
    # Configuraciones de entrada (Entry/Combobox)
    ENTRY_STYLES = {
        'default': {
            'font': (FONTS['primary'], FONTS['sizes']['base']),
            'bg': COLORS['white'],
            'fg': COLORS['dark'],
            'relief': 'solid',
            'bd': 1,
            'highlightbackground': COLORS['border'],
            'highlightcolor': COLORS['border_focus'],
            'highlightthickness': 1
        }
    }
    
    # Configuraciones de etiquetas
    LABEL_STYLES = {
        'title': {
            'font': (FONTS['primary'], FONTS['sizes']['3xl'], 'bold'),
            'fg': COLORS['dark'],
            'bg': COLORS['bg_primary']
        },
        'subtitle': {
            'font': (FONTS['primary'], FONTS['sizes']['xl'], 'bold'),
            'fg': COLORS['dark_gray'],
            'bg': COLORS['bg_primary']
        },
        'body': {
            'font': (FONTS['primary'], FONTS['sizes']['base']),
            'fg': COLORS['gray'],
            'bg': COLORS['bg_primary']
        },
        'caption': {
            'font': (FONTS['primary'], FONTS['sizes']['sm']),
            'fg': COLORS['gray'],
            'bg': COLORS['bg_primary']
        }
    }
    
    @staticmethod
    def ajustar_brillo_color(color_hex, factor):
        """
        Ajusta el brillo de un color hexadecimal
        factor: -100 a 100 (negativo para oscurecer, positivo para aclarar)
        """
        color_hex = color_hex.lstrip('#')
        rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        
        # Ajustar cada componente RGB
        rgb_ajustado = []
        for componente in rgb:
            if factor > 0:  # Aclarar
                nuevo_valor = componente + (255 - componente) * (factor / 100)
            else:  # Oscurecer
                nuevo_valor = componente * (1 + factor / 100)
            rgb_ajustado.append(max(0, min(255, int(nuevo_valor))))
        
        return f"#{rgb_ajustado[0]:02x}{rgb_ajustado[1]:02x}{rgb_ajustado[2]:02x}"
    
    @staticmethod
    def crear_gradiente_color(color1, color2, pasos=10):
        """
        Crea una lista de colores que forman un gradiente entre color1 y color2
        """
        color1 = color1.lstrip('#')
        color2 = color2.lstrip('#')
        
        rgb1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
        
        gradiente = []
        for i in range(pasos):
            factor = i / (pasos - 1)
            rgb_intermedio = tuple(
                int(rgb1[j] + (rgb2[j] - rgb1[j]) * factor) for j in range(3)
            )
            color_hex = f"#{rgb_intermedio[0]:02x}{rgb_intermedio[1]:02x}{rgb_intermedio[2]:02x}"
            gradiente.append(color_hex)
        
        return gradiente

# Instancia global para fácil acceso
estilos = EstilosModernos()
