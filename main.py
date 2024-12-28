import argparse
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

def leer_frases_desde_archivo(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        frases = [line.strip() for line in file]
    return frases

def crear_matriz(frases):
    matriz = [frases[i:i+10] for i in range(0, len(frases), 10)]
    return matriz

def crear_imagen(platilla_path, frases, text_color):
    # Cargar la imagen de la plantilla
    plantilla = Image.open(platilla_path)

    # Crear la matriz de frases
    matriz_frases = crear_matriz(frases)

    # Configurar la fuente y tamaño de texto
    fuente_path = "Roboto-Bold.ttf"
    fuente_path_italic = "Roboto-BoldItalic.ttf"

    # Crear un objeto ImageDraw
    draw = ImageDraw.Draw(plantilla)

    # Tamaño de celda en la matriz
    ancho_celda = plantilla.width // 10
    alto_celda = plantilla.height // 7

    # Margen a la izquierda para cada línea de texto
    margen_izquierdo = 50.0  # Ajusta según tus preferencias

    # Escribir las frases en la plantilla
    for i, fila in enumerate(matriz_frases):
        for j, frase in enumerate(fila):
            # Dividir la frase en líneas permitiendo un ancho específico
            lineas = textwrap.wrap(frase, width=15)
            line_height = 35

            # Calcular la posición vertical inicial para centrar el texto
            espacio_restante = alto_celda - len(lineas) * line_height
            y_inicio = i * alto_celda + espacio_restante // 2

            font_size = 35

            while espacio_restante < 240:
                font_size -= 10
                line_height -= 10
                espacio_restante = alto_celda - len(lineas) * line_height
                y_inicio = i * alto_celda + espacio_restante // 2
                
            # Verificar si la frase está entre comillas y usar la fuente cursiva en ese caso
            if re.search(r'"([^"]*)"', frase):
                fuente = ImageFont.truetype(fuente_path_italic, font_size)
            else:
                fuente = ImageFont.truetype(fuente_path, font_size)
                
            # Escribir cada línea en la imagen con margen a la izquierda y separación vertical
            for k, linea in enumerate(lineas):
                x = j * ancho_celda + margen_izquierdo
                y = y_inicio + k * line_height

                draw.text((x, y), linea, font=fuente, fill=text_color)

    # Guardar la imagen resultante
    plantilla.save("imagen_resultante.png")

def main():
    # Configurar el parser de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Crear imagen con frases en una plantilla.')
    parser.add_argument('plantilla', type=str, help='Ruta de la imagen de la plantilla')
    parser.add_argument('archivo_frases', type=str, help='Ruta del archivo de texto con las frases')
    parser.add_argument('text_color', type=str, help='Color del texto')

    # Obtener las rutas desde los argumentos de línea de comandos
    args = parser.parse_args()
    plantilla_path = args.plantilla
    archivo_frases = args.archivo_frases
    text_color = args.text_color if args.text_color else "black"
    
    if text_color not in ["black", "white"]:
        print("El color del texto debe ser 'black' o 'white'.")
        return

    # Leer las frases desde el archivo
    frases = leer_frases_desde_archivo(archivo_frases)

    # Crear la imagen resultante
    crear_imagen(plantilla_path, frases, text_color)

if __name__ == "__main__":
    main()
