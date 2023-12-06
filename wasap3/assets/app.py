from flet import *
import json

#Configuramos el frame
w = 1000
h = 800
titulo = "xxxx"
m1 = 50
m2 = 270
m3 = 300
espaciado = 12
w_btn = 40
h_btn = 35
 #configuramos los colores de fondo
bgc1 = '#282828'
bgc2 = '#202020'
bg3 = '#282828'
bg_interface = '#efefef'
bg_btns = '#E6353535'
bg4= '#00a884'
bg5='#25d366'
c_screen_padding = 20
bg6 = "#6a6a6a"
bg7= "#363636"
bg8 = "#035d4d"
bg9 = "#689e94"
bg10 = "#cddfdb"

class App(UserControl):
    def __init__(self, pg:Page):
        super().__init__()
        self.pg = pg
        self.pg.window_bgcolor = colors.TRANSPARENT
        self.pg.bgcolor = colors.TRANSPARENT
        self.pg.window_title_bar_hidden = True
        self.pg.window_frameless = False

        #NOTA AQUÍ METER LAS FUNCIONES DE INICIALIZACIÓN DE CONTAINER Y LOS HELPERS
    
    def cargar_chat(self):
        pass
    def init_helper_contain(self):
        self.pg.add(
            Container(
                
            )
        )
