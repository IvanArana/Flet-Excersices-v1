import flet as ft
from connection import conectar_bd  # Asegúrate de que el nombre del archivo sea correcto

def main(page: ft.Page):
    page.title = "Carrusel de Historias"

    # Conexión a la base de datos
    db = conectar_bd()
    
    # Obtener rutas de imágenes desde la base de datos
    imagenes = [doc["ruta"] for doc in db.find()] 
    
    # Contenedores y variables de estado
    imagen_grande_container = ft.Column()
    miniaturas = ft.Row(wrap=True, visible=True)
    boton_regresar = ft.IconButton(icon=ft.icons.ARROW_BACK, visible=False, on_click=lambda e: ocultar_imagen_grande())
    current_index = [0]  # Índice actual de la imagen grande

    # Función para manejar la selección de una historia
    def seleccionar_historia(e, index):
        current_index[0] = index
        imagen_seleccionada = ft.Image(src=imagenes[current_index[0]], width=400, height=400)
        imagen_grande_container.controls.clear()
        imagen_grande_container.controls.append(imagen_seleccionada)
        miniaturas.visible = False
        boton_regresar.visible = True
        page.update()

    # Función para ocultar la imagen grande
    def ocultar_imagen_grande():
        imagen_grande_container.controls.clear()
        miniaturas.visible = True
        boton_regresar.visible = False
        page.update()

    # Crear miniaturas para cada historia
    for i, img in enumerate(imagenes):
        boton_miniatura = ft.IconButton(icon=ft.icons.IMAGE, data=img, on_click=lambda e, i=i: seleccionar_historia(e, i))
        miniaturas.controls.append(boton_miniatura)

    # Botones de navegación manual
    def navegar(direccion):
        nuevo_index = (current_index[0] + direccion) % len(imagenes)
        seleccionar_historia(None, nuevo_index)

    boton_anterior = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: navegar(-1))
    boton_siguiente = ft.IconButton(icon=ft.icons.ARROW_FORWARD, on_click=lambda e: navegar(1))

    # Agregar los controles a la página
    page.add(boton_regresar, boton_anterior, miniaturas, imagen_grande_container, boton_siguiente)

# Ejecutar la aplicación
ft.app(target=main)
