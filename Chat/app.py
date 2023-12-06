from flet import *
import json

#Configuramos el frame
w = 1000
h = 800
titulo = "aaa"
m1 = 50
m2 = 270
m3 = 300
espacio = 12
w_btn = 40
h_btn = 35

#config los colores de fondo
bgc1 = '#282828'
bgc2 = '#202020'
bgc3 = '#282828'
bg_interface = '#efefef'
bg_btns = '#E6353535'
bg4 = '#00a884'
bg5 = '#25d366'
c_screen_padding = 20
bg6 = "#6a6a6a"
bg7 = "#363636"
bg8 = "#035d4d"
bg9 = "#689e94"
bg10 = "#cddfdb"

class App(UserControl):
    def __init__(self, pg:Page):
        super().__init__()
        self.pg = pg
        self.pg.window_bgcolor = colors.TRANSPARENT
        self.pg.bgcolor = colors.TRANSPARENT
        self.pg.window_title_bar_buttons_hidden = True
        self.pg.window_frameless = False

        #Nota aqui meter las funciones de inicilizacion de container y los helpers
    
    def cargar_chat(self):
        pass
    def init_helper_contain(self):
        self.pg.add(
            Container(
                clip_behavior= ClipBehavior.ANTI_ALIAS,
                border_radius= espacio,
                expand=True,
                bgcolor=bgc3,
                content=Stack(
                    expand=True,
                    controls=[
                        Row(
                            spacing=1,
                            controls=[
                                self.sidebar
                            ]
                        )
                    ]
                )
            )
        )
    def containers_init(self):
        #Inicializara los contenedores
        pass

    def base_containers(self):
        #Agregada propiedades a cada container
        pass

    def sidebar_btn_hovered(self, e:HoverEvent):
        if e.data == 'true':
            e.control.bgcolor = bg_btns
        else:
            e.control.bgcolor = None
        e.control.update()

    #Clase 18/10/23

    def screen_chats(self):
        pass
    def sidebar(self):
        pass

    def show_hide_csa(self, e: TabError):
        if e.control.data == 'opened':
            self.screen_chats.width = 0
            self.sidebar.bgColor = bg6
            e.control.data = 'closed'
        else:
            self.screen.chats.width = m2
            self.sidebar.bgColor = bg6
            e.control.data = 'opened'
        
        e.control.update()
        self.screen_chats.update()
        self.sidebar.update()

    # def go_store(e):
    #     page.route ="/Chat"
    #     page.update()

    