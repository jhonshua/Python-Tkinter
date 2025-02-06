import qrcode
import os

def generar_qr_producto():
    """Genera un código QR con la información de un producto y lo guarda en media/qr.

    Args:
        producto (dict): Diccionario con la información del producto.
    """

    # Crea la información del producto en formato de cadena
    info_producto = f"""
    Nombre: {producto['nombre']}
    Precio: {producto['precio']}
    Descripción: {producto['descripcion']}
    """

    # Crea el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(info_producto)
    qr.make(fit=True)

    # Define la ruta a la carpeta media/qr
    ruta_qr = os.path.join("media", "qr")

    # Asegúrate de que la carpeta media/qr existe. Si no, créala.
    os.makedirs(ruta_qr, exist_ok=True)

    # Define el nombre del archivo
    nombre_archivo = f"qr_{producto['nombre']}.png"

    # Define la ruta completa al archivo
    ruta_completa = os.path.join(ruta_qr, nombre_archivo)

    # Guarda el código QR en el archivo PNG
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(ruta_completa)

    print(f"Código QR guardado en: {ruta_completa}")


# Ejemplo de uso
producto = {
    "nombre": "Camiseta",
    "precio": 20.00,
    "descripcion": "Camiseta de algodón de alta calidad",
}

