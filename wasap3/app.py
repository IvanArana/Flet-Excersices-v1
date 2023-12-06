from ctypes import alignment
from sqlite3 import Row
from typing import Container
from flet import *
from datetime import datetime

import json
wallpaper = 'assets/icons/wallpalper.png'
w= 1000
h=800
m1 = 50
m2 = 270
m3 = 300
dmw = w-300-50
espaciado = 12
w_btn = 40
h_btn = 35 
bgc1 = '#282828'
bgc2 = '#202020'
bgc3 = '#282828'
bg_interface = '#efefef'
bg_btns ='#E6353535'
ic = "#00a884"
bgc5 = '#25d366'
c_screen_padding = 20
ih_espaciado = 5
bgc6 = "#6a6a6a"
rc = "#363636"
sc = "#035d4d"
bgc9 = "#689e94"
bgc10 = "#cddfdb"

class Message():
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

#Definimos el text field para acceder a el
input_mensaje = TextField(
  value='',
  expand=True,
  multiline=True,
  border=InputBorder.NONE,
  hint_text='Escribe un mensaje',
  hint_style=TextStyle(
    size=14,
    font_family='arial',
    color=bgc6
  ),
  color=bg_interface,
  text_style=TextStyle(
    size=14,
    font_family='arial',
    color=bg_interface
  ),
)
    
class App(UserControl):
  
  def __init__(self,pg:Page):
    super().__init__()
    self.pg = pg
    # self.pg.window_maximizable = True
    # self.pg.window_minimizable = True

    self.pg.window_bgcolor = colors.TRANSPARENT
    self.pg.bgcolor = colors.TRANSPARENT
    self.pg.window_title_bar_hidden =True
    self.pg.window_frameless = False
    self.containers_init()
    self.init_helper()
    #Agregando mensajes online:
    self.chat = Column()

    def on_message(message: Message):
      hora_actual = datetime.now().strftime("%I:%M %p")  # Definir hora_actual aquí
      if message.message_type == "chat_message":
          self.msg_obj.append(Container(
              on_long_press=self.show_msg_menu,
              on_hover=self.msg_hovered,
              content=Row(
                  spacing=25,
                  alignment='end',
                  vertical_alignment='center',
                  controls=[
                      self.msg_hover_emoji,
                      Container(
                          margin=margin.only(right=6),
                          alignment=alignment.center_left,
                          width=500,
                          padding=10,
                          bgcolor=sc,
                          border_radius=ih_espaciado,
                          content=Column(
                              spacing=4,
                              controls=[
                                  Text(
                                      value=f"{message.user}: {message.text}",
                                      selectable=True,
                                      color=bgc10,
                                      weight=FontWeight.W_400,
                                      size=14,
                                  ),
                                  Row(
                                      spacing=4,
                                      alignment='end',
                                      controls=[
                                          Text(
                                              hora_actual,  # Mostramos la hora actual
                                              size=10,
                                              weight=FontWeight.W_600,
                                              color=bgc9
                                          ),
                                          Icon(
                                              icons.DONE,
                                              color=bgc9,
                                              size=10
                                          )
                                      ]
                                  )
                              ]
                          )
                      )
                  ]
              )
          ))
      elif message.message_type == "login_message":
          self.msg_obj.append(
              Row(
                    spacing=25,
                    alignment='center',
                    vertical_alignment='center',
                    controls=[
                      Container(
                          margin=margin.only(right=6),
                          alignment=alignment.center,
                          width=500,
                          padding=10,
                          bgcolor=colors.GREY_900,
                          border_radius=ih_espaciado,
                          content=
                            Column(
                              spacing=4,
                              controls=[
                                Text(
                                  value=message.text,
                                  selectable=True,
                                  color=bgc10,
                                  weight=FontWeight.W_400,
                                  size=18,
                                )
                              ]
                      )
                  )
              ]
            )
          )
          
      pg.update()

    pg.pubsub.subscribe(on_message)

    def send_click(e):
        pg.pubsub.send_all(Message(user=pg.session.get('user_name'), text=input_mensaje.value, message_type="chat_message"))
        input_mensaje.value = ""
        pg.update()

    user_name = TextField(label="Introduce tu nombre")

    def join_click(e):
        if not user_name.value:
            user_name.error_text = "El nombre no puede estar en blanco!"
            user_name.update()
        else:
            pg.session.set("user_name", user_name.value)
            pg.dialog.open = False
            pg.pubsub.send_all(Message(user=user_name.value, text=f"{user_name.value} se ha unido al chat.", message_type="login_message"))
            pg.update()

    pg.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text("Bienvenido!"),
        content=Column([user_name], tight=True),
        actions=[ElevatedButton(text="Unirte al chat", on_click=join_click)],
        actions_alignment="end",
    )
    pg.add()
      
  def send_click(pg, input_mensaje, e):
        pg.pubsub.send_all(Message(user=pg.session.get('user_name'), text=input_mensaje.value, message_type="chat_message"))
        input_mensaje.value = ""
        pg.update()

  def load_chat_dummy(self):
    # for n in range(50):
    #   self.chats_contents_column.controls.append(self.chat_row) 
    pass

  def init_helper(self):
    self.pg.add(
      Container(
        clip_behavior=ClipBehavior.ANTI_ALIAS,
        border_radius=espaciado,
        expand=True,
        bgcolor=bgc3,
        content=Stack(
          expand=True,
          controls=[
            Row(
              spacing=0,
              controls=[
                self.sidebar,
                self.chats_screen,
                self.dm_screen,
              ]
            ),
            
            self.settings_popup,

            self.emoji_popup
            
            
          ]
        )
      )
    )  
  
  def containers_init(self):
    self.chat_user_details()
    self.dm_screen_content_main()
    self.chats_column_f()
    self.chat_screen()
    self.sidebar()
    self.base_containers()
    self.load_chat_dummy()
    
  def base_containers(self):
    self.sidebar = Container(
      padding=padding.only(top=50,bottom=50),
      width=m1,
      bgcolor=bgc1,
      content=self.sidebar_column,
    )
    self.chats_screen = Container(
      animate=animation.Animation(500,AnimationCurve.BOUNCE_OUT),
      width=m3,
      bgcolor=bgc2,
      content=self.chat_screen_items,
    )
    self.dm_screen = Container(
      expand=True,
      bgcolor=bgc3,
      content=self.dm_screen_content
    )

  def sidebar_btn_hovered(self,e:HoverEvent):
    if e.data == 'true':
      e.control.bgcolor = bg_btns
      
    else:  
      e.control.bgcolor = None
    e.control.update()  
  
  def show_hide_csa(self,e: TapEvent):
    if e.control.data == 'opened':
      self.chats_screen.width = 0
      self.sidebar.bgcolor = bgc2
      e.control.data = 'closed'
    else:
      self.chats_screen.width = m3
      self.sidebar.bgcolor = bgc1
      e.control.data = 'opened'
        
    e.control.update()    
    self.sidebar.update()
    self.chats_screen.update()

  def sidebar(self):
    self.sidebar_column = Column(
      horizontal_alignment='center',
      alignment='spaceBetween',
      spacing=0,
      controls=[
        Column(
          controls=[
            Container(
              # on_hover=self.sidebar_btn_hovered,
              alignment=alignment.center,
              height=h_btn,
              width=w_btn,
              bgcolor = bg_btns,
              border_radius=5,
              content=Row(
                spacing=0,
                alignment='spaceBetween',
                vertical_alignment='center',
                controls=[
                  Container(
                    offset=transform.Offset(0, 0),
                    animate_offset=animation.Animation(1000),
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    height=17,
                    width=3,
                    bgcolor=ic,
                    border_radius=5
                  ),
                  
                  Container(
                    margin=margin.only(right=10),
                    content= Stack(
                      controls=[
                        Container(
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          height=20,
                          width=20,
                          content=Image(
                            src='assets/icons/c.png',
                            fit=ImageFit.COVER,
                            color=bg_interface
                          )
                        ),
                        Container(
                          right=1,
                          top=1,
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          height=8,
                          width=8,
                          bgcolor=bgc5,
                          border_radius=20
                        ),
                      ]
                    )
                
                  )
                 
                 ]
              )
            ),
            
            Container(
              on_hover=self.sidebar_btn_hovered,
              alignment=alignment.center,
              height=h_btn,
              width=w_btn,
              # bgcolor = bg_btns,
              border_radius=ih_espaciado,
              content=Row(
                spacing=0,
                alignment='spaceBetween',
                vertical_alignment='center',
                controls=[
                  Container(
                    offset=transform.Offset(0, 0),
                    animate_offset=animation.Animation(1000),
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    height=17,
                    width=3,
                    # bgcolor=ic,
                    border_radius=5
                  ),
                  Container(
                    margin=margin.only(right=10),
                    content= Stack(
                      controls=[
                        Container(
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          height=20,
                          width=20,
                          content=Image(
                            src='assets/icons/s.png',
                            fit=ImageFit.COVER,
                            color=bg_interface
                          )
                        ),
                        Container(
                          right=0,
                          top=1,
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          height=9,
                          width=9,
                          bgcolor=bgc5,
                          border_radius=20,
                          # border=border.all(color=bgc1,width=1)
                        ),
                      ]
                    )
                
                  )
                 ]
              )
            ),

          ]

        ),


        Column(
          spacing=5,
          controls=[
            Container(
              data = 'opened',
              on_hover=self.sidebar_btn_hovered,
              on_click=self.show_hide_csa,
              alignment=alignment.center,
              height=h_btn,
              width=w_btn,
              border_radius=5,
              content=Row(
                spacing=0,
                alignment='center',
                controls=[
                  Icon(
                    icons.MENU_OUTLINED,
                    size=20,
                    color=bg_interface
                  )
                ]
              )
            ),
            Container(
              on_hover=self.sidebar_btn_hovered,
              on_click=self.show_settings_popup,
              alignment=alignment.center,
              height=h_btn,
              width=w_btn,
              border_radius=5,
              content=Row(
                spacing=0,
                alignment='center',
                controls=[
                  Icon(
                    icons.SETTINGS_OUTLINED,
                    size=20,
                    color=bg_interface
                  )
                ]
              )
            ),


            Container(
              on_hover=self.sidebar_btn_hovered,
              on_click=self.show_settings_popup,
              alignment=alignment.center,
              height=h_btn,
              width=w_btn,
              border_radius=ih_espaciado,
              content=Row(
                spacing=0,
                alignment='center',
                controls=[
                  Container(
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    height=20,
                    width=20,
                    border_radius=20,
                    content=Image(
                      src='assets/dp.jpg',
                      fit=ImageFit.COVER
                    )
                  )
                ]
              )
            ),

            
          ]
        ),

      ]

    )
    
  def chat_screen(self):
    
    self.chat_screen_items = Stack(
      controls=[
        Column(
          controls=[
            Container(
              height=40,
              padding = padding.only(left=10),
              # margin=margin.only(bottom=10),
              content=Row(
                controls=[
                  Image(
                    src='assets/icons/logo.png',

                  ),
                  Text(
                    value='WhatsApp',
                    size=14,
                  )

                ]
              )
            ), # whatsapp icon
            
            Container(
              padding = padding.only(left=c_screen_padding,right=c_screen_padding),
              content=Row(
                spacing=0,
                alignment='spaceBetween',
                vertical_alignment='center',
                controls=[
                  Text(
                    value='Chats',
                    size=24,
                    weight=FontWeight.W_500
                  ),
                  Row(
                    controls=[
                      Container(
                        on_hover=self.sidebar_btn_hovered,
                        height=40,
                        width=40,
                        border_radius=ih_espaciado,
                        content=Image(
                          src='assets/icons/newchat.png',
                          color=bg_interface
                        ),
                      ),
                      Container(
                        on_hover=self.sidebar_btn_hovered,
                        height=40,
                        width=40,
                        border_radius=ih_espaciado,
                        content=Image(
                          src='assets/icons/more.png',
                          color=bg_interface
                        ),
                      ),
                    ]
                  )
                ]
              )
            ), # Chats label text and new chat icon and more
            
            Container(
              content=Row(
                alignment='center',
                controls=[
                  Container(
                    
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    border_radius = ih_espaciado,
                    content=Container(
                      # on_hover=self.sidebar_btn_hovered,
                      clip_behavior=ClipBehavior.ANTI_ALIAS,
                      border_radius = ih_espaciado,
                      height=35,
                      width=m2,
                      bgcolor=bgc1,
                      border=border.only(bottom=border.BorderSide(width=1,color=bgc6)),
                      content=Row(
                        controls=[
                          Container(
                            width=230,
                            padding=padding.only(left=15,top=5),
                            content=TextField(
                              border=InputBorder.NONE,
                              hint_text='Search or start a new chat',
                              hint_style=TextStyle(
                                size=14,
                                font_family='arial',
                                color=bgc6
                              ),
                              color=bg_interface,
                              text_style=TextStyle(
                                size=14,
                                font_family='arial',
                                color=bg_interface
                              ),
                            ),
                          ),

                          Container(
                            height=25,
                            width=25,
                            border_radius=ih_espaciado,
                            on_hover=self.sidebar_btn_hovered,
                            content=Icon(
                              icons.SEARCH_OUTLINED,
                              size=16,
                              color=bgc6
                            ),
                          )

                        ]
                      )
                    )
                  )
                ]

              )
            ), # search box
            
            Container(
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              height=40,
              padding=padding.only(left=10,right=10),
              # border_radius=20,
              content=Container(
                border_radius=ih_espaciado,
                on_hover=self.sidebar_btn_hovered,
                padding=padding.only(left=10,right=10),
                content=Row(
                  vertical_alignment='center',
                  alignment='spaceBetween',
                  controls=[
                    Icon(
                      icons.DELETE_OUTLINE
                    ),
                    Container(
                      content=Text(
                        value='Archived',
                        weight=FontWeight.W_600
                      ),
                      margin=margin.only(right=100)
                    ),
                    Text(
                      value='2',
                      color=ic,
                      weight=FontWeight.W_600
                    )

                  ]
                )
              )

            ), # archived chat button

            self.chats_contents_column,  
            
          ]
        ),
        
        Column(
          controls=[
            Container(), # whatsapp icon
            Container(), # Status text label
            Container(), # my stat
            Container(), # recent updates label
            Container(), # stats column container
          ]
        ),
      ]
    )
  
  def search_on_focus(self,e):
    pass

  def chats_column_f(self):
    self.chat_row = Container(
      height=70,
      padding=padding.only(left=10,right=10),
      content=Container(
        border_radius=ih_espaciado,
        on_hover=self.sidebar_btn_hovered,
        content=Row(
          spacing=0,
          alignment='spaceBetween',
          vertical_alignment='center',
          controls=[
            Container(
              height=50,
              width=50,
              border_radius=30,
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              content=Image(
                src='assets/dp.jpg',
                fit=ImageFit.COVER,
              )
            ),
            
            Column(
              alignment='center',
              horizontal_alignment='center',
              controls=[
                Container(
                  width=200,
                  content=Row(
                      alignment='spaceBetween',
                      # vertical_alignment='center',
                      spacing=0,
                      controls=[
                        Container(
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          width=120,
                          content=Text(
                          '#IDYGS101',
                          no_wrap=True
                        ),
                        ),
                        Text(
                          '12:20AM'
                        ),
                      ]
                    ),
                ),
                
                


                Container(
                  width=200,
                  content=Row(
                      alignment='spaceBetween',
                      # vertical_alignment='center',
                      spacing=0,
                      controls=[
                        Container(
                          clip_behavior=ClipBehavior.ANTI_ALIAS,
                          width=120,
                          content=Text(
                            'ULTIMO MENSAJE',
                            no_wrap=True
                          ),
                        ),
                      ]
                    ),
                ),
                
                

                

              ]
            )
          ]
        )
      )

    )
            
    self.chats_contents_column = Column(
              scroll='auto',
              expand=True,
              controls=[
                self.chat_row,
           
              ]
            ) # chats column container

  def msg_hovered(self,e):
    if e.data == 'true':
      self.msg_hover_emoji.visible = True
    else:  
      self.msg_hover_emoji.visible = False
    self.msg_hover_emoji.update()

  def show_msg_menu(self,e:LongPressEndEvent):
    print(e.target)

  def close_window(self,e):
    self.pg.window_destroy()

  def mini_window(self,e):
    self.pg.window_minimized = True

    self.pg.update()

  def max_window(self,e):
    self.pg.window_maximized = True
    self.pg.update()
    
  def hide_emojis_popup(self,e):
    self.emoji_popup.offset = transform.Offset(0,1.5)
    self.emoji_popup.update()
    sleep(0.51)
    self.emoji_popup.height = 0
    self.emoji_popup.update()
  
  def show_emojis_popup(self,e):
    self.emoji_popup.height = None
    self.emoji_popup.offset = transform.Offset(0,0)
    self.emoji_popup.update()

  def chat_user_details(self):

    self.chat_user_details_sidebar_item_info =  Container(
                                  expand=True,
                                  padding=15,
                                  content=Column(
                                    # expand=True,
                                    height=475,
                                    scroll='auto',
                                    controls=[
                                      Row(
                                        alignment='center',
                                        controls=[
                                          Container(
                                            alignment=alignment.center,
                                            height=100,
                                            width=100,
                                            border_radius=80,
                                            bgcolor='white12',
                                            content=Icon(
                                              icons.PERSON,
                                              size=50
                                            ),
                                          ),
                                        ]
                                      ),
                                      Row(
                                        alignment='center',
                                        controls=[
                                          Text(
                                            'IDYGS😊',
                                            size=20,
                                            weight=FontWeight.W_600
                                          )
                                        ]
                                      ),
                                      Text(
                                        'About',
                                        size=14,
                                        weight=FontWeight.W_300,
                                        color='white24',
                                      ),
                                      Text(
                                        'Hey there! I am using WhatsApp',
                                        size=14,
                                        weight=FontWeight.W_400,
                                        color='#CCffffff',
                                      ),
                                      Text(
                                        'Phone number',
                                        size=14,
                                        weight=FontWeight.W_300,
                                        color='white24',
                                      ),
                                      Text(
                                        '+233 548 007 499',
                                        size=14,
                                        weight=FontWeight.W_400,
                                        color='#CCffffff',
                                      ),


                                      Text(
                                        'Disappearing messages',
                                        size=14,
                                        weight=FontWeight.W_300,
                                        color='white24',
                                      ),
                                      Text(
                                        'Off',
                                        size=14,
                                        weight=FontWeight.W_400,
                                        color='#CCffffff',
                                      ),
                                      Text(
                                        'Muted notifications',
                                        size=14,
                                        weight=FontWeight.W_300,
                                        color='white24',
                                      ),
                                      Container(
                                        width=120,
                                        height=35,
                                        bgcolor=bg_btns,
                                        padding=padding.only(left=10),
                                        border_radius=ih_espaciado,
                                        content=Row(
                                          controls=[
                                            # Image(
                                            #   src='assets/icons/audio.png',
                                            #   color='#CCffffff'
                                            # )
                                            Icon(
                                              icons.MUSIC_NOTE_OUTLINED,
                                              size=16,
                                              color='#CCffffff',

                                            ),
                                            Dropdown(
                                              alignment=alignment.center,
                                              label_style=TextStyle(size=12,color='#CCffffff',),
                                              expand=True,
                                              label='Mute',
                                              options=[
                                                  dropdown.Option("For 8hrs",),
                                                  dropdown.Option("For 1 Week"),
                                                  dropdown.Option("Always"),
                                              ],
                                              border_color=bg_btns,

                                            ),
                                          ]

                                        ),
                                      ),

                                      Text(
                                        'Notification tone',
                                        size=14,
                                        weight=FontWeight.W_300,
                                        color='white24',
                                      ),
                                      Container(
                                        height=35,
                                        border_radius=ih_espaciado,
                                        content=Row(
                                          spacing=10,
                                          controls=[
                                            # Image(
                                            #   src='assets/icons/audio.png',
                                            #   color='#CCffffff'
                                            # )
                                            Container(
                                              height=35,
                                              width=35 ,
                                              border_radius=ih_espaciado,
                                              bgcolor=bg_btns,
                                              content=Icon(
                                              icons.PLAY_ARROW_OUTLINED,
                                              size=16,
                                              color='#CCffffff',

                                            )
                                            ),
                                            Container(
                                              border_radius=ih_espaciado,
                                              bgcolor=bg_btns,
                                              width=120,
                                              content=Dropdown(
                                              # icon=icons.MUSic_NOTE_OUTLINED,
                                              alignment=alignment.center,
                                              label_style=TextStyle(size=12,color='#CCffffff',),
                                              expand=True,
                                              label='Default',
                                              options=[
                                                  dropdown.Option("None",),
                                                  dropdown.Option("Default"),
                                                  dropdown.Option("Alert 1"),
                                                  dropdown.Option("Alert 2"),
                                                  dropdown.Option("Alert 3"),
                                              ],
                                              border_color=bg_btns,

                                            ),
                                            )
                                          ]

                                        ),
                                      ),

                                      Container(
                                        # expand=True,
                                        width=500,
                                        height=1,
                                        bgcolor=bg_btns
                                      ),
                                      Row(
                                        alignment='spaceBetween',
                                        controls=[
                                          Container(
                                            alignment=alignment.center,
                                            height=35,
                                            width=155,
                                            border_radius=ih_espaciado,
                                            bgcolor=bg_btns,
                                            content=Text(
                                              'Block',
                                              size=14,
                                              weight=FontWeight.W_400,
                                              color='#CCffffff',
                                            ),
                                          ),
                                          Container(
                                            alignment=alignment.center,
                                            height=35,
                                            width=155,
                                            border_radius=ih_espaciado,
                                            bgcolor=bg_btns,
                                            content=Text(
                                              'Report contact',
                                              size=14,
                                              weight=FontWeight.W_400,
                                              color='#CCffffff',
                                            ),
                                          ),
                                        ]
                                      )


                                    ]
                                  )
                                )

    

    self.settings_sidebar_details_column =  Container(
        expand=True,
        padding=15,
        content=Column(
          # expand=True,
          height=475,
          scroll='auto',
          controls=[
            Row(
              alignment='center',
              controls=[
                Container(
                  alignment=alignment.center,
                  height=100,
                  width=100,
                  border_radius=80,
                  bgcolor='white12',
                  content=Icon(
                    icons.PERSON,
                    size=50
                  ),
                ),
              ]
            ),
            Row(
              alignment='spaceBetween',
              controls=[
                # Text(
                #   'Mr. Newton😊',
                  # size=20,
                #   weight=FontWeight.W_600
                # ),
                TextField(
                  width=200,
                  value='Mr. Newton😊',
                  text_size=20,
                  border=InputBorder.NONE
                ),
                Container(
                  margin=margin.only(right=15),
                  on_hover=self.sidebar_btn_hovered,
                  border_radius=ih_espaciado,
                  height=35,
                  width=35,
                  content=Icon(
                    icons.EDIT_OUTLINED,
                    size=14,
                    color=bg_interface
                  )
                )
              ]
            ),
            
            Text(
              'About',
              size=14,
              weight=FontWeight.W_300,
              color='white24',
            ),
            Row(
              alignment='spaceBetween',
              controls=[
                TextField(
                  width=250,
                  multiline=True,
                  value='Hey there! WhatsApp is using me!',
                  text_size=14,
                  border=InputBorder.NONE,
                  text_style=TextStyle(
                    size=14,
                    weight=FontWeight.W_400,
                    color='#CCffffff',

                  )
                ),
                Container(
                  margin=margin.only(right=15),
                  on_hover=self.sidebar_btn_hovered,
                  border_radius=ih_espaciado,
                  height=35,
                  width=35,
                  content=Icon(
                    icons.EDIT_OUTLINED,
                    size=14,
                    color=bg_interface
                  )
                )
              ]
            ),
            Text(
              'Phone number',
              size=14,
              weight=FontWeight.W_300,
              color='white24',
            ),
            Text(
              '+233 548 007 499',
              size=14,
              weight=FontWeight.W_400,
              color='#CCffffff',
            ),
          ]
        )
      )


    self.chat_user_details_sidebar_item  =  Container(
      bgcolor=bg_btns,
      height=35,
      border_radius=ih_espaciado,

      content=Row(
        spacing=12,
        # alignment='spaceBetween',
        vertical_alignment='center',
        controls=[
          Container(
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(1000),
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            height=17,
            width=3,
            bgcolor=ic,
            border_radius=5
          ),
          
          Row(
            vertical_alignment='center',
            spacing=10,
            controls = [
              Image(
                        src='assets/icons/info.png',
                        color=bg_interface,
                        # scale=0.5
                      ),
              Text(
                'Overview'
              )      
          ]
        ),
        
        
        ]
      ),
    )
                       
    
    self.settings_sidebar_item  =  Container(
      bgcolor=bg_btns,
      height=35,
      border_radius=ih_espaciado,

      content=Row(
        spacing=12,
        # alignment='spaceBetween',
        vertical_alignment='center',
        controls=[
          Container(
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(1000),
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            height=17,
            width=3,
            bgcolor=ic,
            border_radius=5
          ),
          
          Row(
            vertical_alignment='center',
            spacing=10,
            controls = [
              Image(
                        src='assets/icons/info.png',
                        color=bg_interface,
                        # scale=0.5
                      ),
              Text(
                'Overview'
              )      
          ]
        ),
        
        
        ]
      ),
    )


    self.chat_user_popup = Container(
      offset=transform.Offset(0,-1),
      clip_behavior=ClipBehavior.ANTI_ALIAS,
      height=0,
      animate_offset=animation.Animation(500,'decelerate'),
      bgcolor=bgc1,
      content=Card(
        expand=True,
        elevation=15,
        content=Container(
          height=500,
          width=500,
          bgcolor=bgc1,
          content=Row(
            controls=[
              Container(
                padding=8,
                width=140,
                bgcolor=bgc2,
                content=Column(
                  alignment='spaceBetween',
                  spacing=5,
                  controls=[
                    Column(
                      expand=True,
                      scroll='auto',
                      controls=[
                        self.chat_user_details_sidebar_item,
                      ]
                    ),
                    Column(
                      controls=[
                        Container(
                          on_click=self.close_chat_user_popup,
                          bgcolor=bg_btns,
                          height=35,
                          border_radius=ih_espaciado,

                          content=Row(
                            alignment='center',
                            vertical_alignment='center',
                            controls=[
                              Row(
                                vertical_alignment='center',
                                spacing=10,
                                controls = [
                                  Image(
                                            src='assets/icons/info.png',
                                            color=bg_interface,
                                            # scale=0.5
                                          ),
                                  Text(
                                    'Close'
                                  )      
                              ]
                            ),
                            
                            
                            ]
                          ),
                        )
                      ,
                      ]
                    )
                    
                  ]
                ),
              ),
              
              
              Column(
                expand=True,
                controls=[
                  Stack(
                    controls=[
                      self.chat_user_details_sidebar_item_info
                    ]
                  )
                ]
              ),
            
            
            ]
          ),
        )
      )
    )

   
    self.settings_popup = Container(
      border_radius=ih_espaciado,
      bottom=30,
      left=80,
      height=0,
      offset=transform.Offset(0,1.5),
      animate_offset=animation.Animation(500,'decelerate'),
      bgcolor=bgc1,
      content=Card(
        expand=True,
        elevation=15,
        content=Container(
          border_radius=ih_espaciado,
          height=500,
          width=500,
          bgcolor=bgc1,
          content=Row(
            controls=[
              Container(
                padding=8,
                width=140,
                bgcolor=bgc2,
                content=Column(
                  alignment='spaceBetween',
                  spacing=5,
                  controls=[
                    Column(
                      expand=True,
                      scroll='auto',
                      controls=[
                        self.settings_sidebar_item,
                      ]
                    ),
                    Column(
                      controls=[
                        Container(
                          on_click=self.close_settings_popup,
                          bgcolor=bg_btns,
                          height=35,
                          border_radius=ih_espaciado,

                          content=Row(
                            alignment='center',
                            vertical_alignment='center',
                            controls=[
                              Row(
                                vertical_alignment='center',
                                spacing=10,
                                controls = [
                                  Image(
                                    src='assets/icons/info.png',
                                    color=bg_interface,
                                    # scale=0.5
                                  ),
                                  Text(
                                    'Profile'
                                  )      
                              ]
                            ),
                            
                            
                            ]
                          ),
                        ),
                        Container(
                          on_click=self.close_settings_popup,
                          bgcolor=bg_btns,
                          height=35,
                          border_radius=ih_espaciado,

                          content=Row(
                            alignment='center',
                            vertical_alignment='center',
                            controls=[
                              Row(
                                vertical_alignment='center',
                                spacing=10,
                                controls = [
                                  Image(
                                            src='assets/icons/info.png',
                                            color=bg_interface,
                                            # scale=0.5
                                          ),
                                  Text(
                                    'Close'
                                  )      
                              ]
                            ),
                            
                            
                            ]
                          ),
                        ),
                     
                      ]
                    )
                    
                  ]
                ),
              ),
              
              
              Column(
                expand=True,
                controls=[
                  Stack(
                    controls=[
                      self.settings_sidebar_details_column
                    ]
                  )
                ]
              ),
            
            
            ]
          ),
        )
      )
    )


    self.emoji_popup = Container(
      animate_offset=animation.Animation(500,'decelerate'),
      border_radius=ih_espaciado,
      bottom=50,
      left=120,
      height=0,
      offset=transform.Offset(0,1.5),
      content=Stack(
        controls=[
          Card(
            expand=True,
            elevation=30,
            height=380,
            width=500,
          ),
          
            Container(
              padding=padding.only(top=10,left=10,right=10),
              border_radius = ih_espaciado,
              height=400,
              width=500,
              bgcolor=bgc2,
              
              content=Column(
                controls=[
                  Row(
                    alignment='spaceBetween',
                    controls=[
                      
                      Row(
                        controls=[
                          Text(
                            'Emoji',
                            size=16
                          ),
                          Text(
                            'GIFs',
                            size=16,
                            color='white24',
                          ),
                          Text(
                            'Stickers',
                            size=16,
                            color='white24',
                          ),
                        ]
                      ),

                      Container(
                        on_click=self.hide_emojis_popup,
                        height=20,width=20,border_radius=ih_espaciado,bgcolor='white12',content=Icon(
                          icons.CLOSE,
                          size=12,

                        )
                      )
                    ]
                  ),

                  
                  Container(
                    height=35,
                    bgcolor=bgc1,
                    border_radius = ih_espaciado,
                    border=border.only(bottom=border.BorderSide(width=1,color=bgc6)),
                    content=Row(
                      alignment='spaceBetween',
                      controls=[
                        Container(
                          padding=padding.only(left=15,top=5),
                          content=TextField(
                            border=InputBorder.NONE,
                            hint_text='Search emojis',
                            hint_style=TextStyle(
                              size=14,
                              font_family='arial',
                              color=bgc6
                            ),
                            color=bg_interface,
                            text_style=TextStyle(
                              size=14,
                              font_family='arial',
                              color=bg_interface
                            ),
                          ),
                        ),

                        
                        Container(
                          height=25,
                          width=25,
                          border_radius=ih_espaciado,
                          on_hover=self.sidebar_btn_hovered,
                          content=Icon(
                            icons.SEARCH_OUTLINED,
                            size=16,
                            color=bgc6
                          ),
                        ),


                      ]
                    )
                  )

                ]
              )
            )
        ]
      )
      
    )

  def load_messages(self,e):
    # Read the JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Access the data for a specific user
    username = "xxx"
    for user_data in data['users']:
        if user_data["name"] == username:
            break

    # Access the messages for the user
    messages = user_data["messages"]

    # Iterate through the messages
    for message in messages:
        print(message["message"])
        
  def close_settings_popup(self,e):
    print('fired')
    self.settings_popup.offset = transform.Offset(0,1.5)
    self.settings_popup.update()
    sleep(0.51)
    self.settings_popup.height = 0
    self.settings_popup.update()
  
  def show_settings_popup(self,e):
    self.settings_popup.height = None
    self.settings_popup.offset = transform.Offset(0,0)
    self.settings_popup.update()

  def close_chat_user_popup(self,e):
    self.chat_user_popup.offset = transform.Offset(0,-1)
    self.chat_user_popup.update()
    sleep(0.51)
    self.chat_user_popup.height = 0
    self.chat_user_popup.update()
  
  def show_chat_user_popup(self,e):
    self.chat_user_popup.height = None
    self.chat_user_popup.offset = transform.Offset(0,0)
    self.chat_user_popup.update()
    
  def dm_screen_content_main(self):
    self.audio_msg_btn = Container(
      on_click=self.load_messages,
      on_hover=self.sidebar_btn_hovered,
      alignment=alignment.center,
      height=40,
      width=40,
      border_radius=5,
      content=Row(
        spacing=0,
        alignment='center',
        controls=[
          Icon(
            icons.MIC_NONE_OUTLINED,
            size=20,
            color=bg_interface
          )
        ]
      )
    )
    
    self.send_msg_btn = Container(
      on_click=lambda e: App.send_click(self.pg, input_mensaje, e),
      on_hover=self.sidebar_btn_hovered,
      alignment=alignment.center,
      height=40,
      width=40,
      border_radius=5,
      content=Row(
        spacing=0,
        alignment='center',
        controls=[
          Icon(
            icons.SEND,
            size=20,
            color=bg_interface
          )
        ]
      )
    )

    self.msg_hover_emoji = PopupMenuButton(
        tooltip=None,
        content=Container(
          # on_click=
          tooltip=None,
          height=20,
          width=20,
          border_radius=25,
          content=Icon(
            icons.EMOJI_EMOTIONS_OUTLINED,
            color=bgc6
          ),
        ),
        items=[
            PopupMenuItem(
              content=Row(
                controls=[
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                  Image(
                    src='assets/icons/laugh.png',
                  ),
                ]
              )
            )
           
        ]
    # )
    )

    self.msg_container = Stack(
      # spacing=0,
      controls=[
        Container(
          margin=margin.only(right=6),
          alignment=alignment.center_left,
          width = 500,
          padding=10,
          bgcolor=sc,
          border_radius=ih_espaciado,
          content=Column(
            spacing=4,
            controls=[
              Text(
                value="Lorem  Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
                selectable=True,
                color=bgc10,
                weight=FontWeight.W_400,
                size=14,
                
              ),
              Row(
                spacing=4,
                alignment='end',
                controls=[
                  Text(
                    '5:30 AM',
                    size=10,
                    weight=FontWeight.W_600,
                    color=bgc9
                  ),
                  Icon(
                    icons.DONE,
                    color=bgc9,
                    size=10
                  )
                ]
              )
            ]
          )
        ),
        Container(
          height=20,
          width=20,
          shape=BoxShape.RECTANGLE,
          bgcolor=sc,
          right=0,
          border_radius=BorderRadius(top_left=0, top_right=0, bottom_left=0, bottom_right=20)

        ),
        
      ]
    )
    
    #AGREGAR MENSAJE
    
    #Modificamos msg_obj para que sea un arreglo
    self.msg_obj = []
    
    #agregamos una funcion para agregar un nuevo mensaje
    def agregar_nuevo_mensaje(self, texto_mensaje):
      #extrae la hora actual
      hora_actual = datetime.now().strftime("%I:%M %p")
      #definimos nuevo mensaje
      nuevo_mensaje = Container(
          on_long_press=self.show_msg_menu,
          on_hover=self.msg_hovered,
          content=Row(
              spacing=25,
              alignment='end',
              vertical_alignment='center',
              controls=[
                  self.msg_hover_emoji,
                  Container(
                      margin=margin.only(right=6),
                      alignment=alignment.center_left,
                      width=500,
                      padding=10,
                      bgcolor=sc,
                      border_radius=ih_espaciado,
                      content=Column(
                          spacing=4,
                          controls=[
                              Text(
                                  value=texto_mensaje,
                                  selectable=True,
                                  color=bgc10,
                                  weight=FontWeight.W_400,
                                  size=14,
                              ),
                              Row(
                                  spacing=4,
                                  alignment='end',
                                  controls=[
                                      Text(
                                          hora_actual,  #mostramos la hora actual
                                          size=10,
                                          weight=FontWeight.W_600,
                                          color=bgc9
                                      ),
                                      Icon(
                                          icons.DONE,
                                          color=bgc9,
                                          size=10
                                      )
                                  ]
                              )
                          ]
                      )
                  )
              ]
          )
      )
      self.chat.controls.append(nuevo_mensaje)

      self.msg_obj.append(nuevo_mensaje)
      self.pg.update()
    
    #asignamos una funcion para agregar el mensaje
    self.agregar_nuevo_mensaje = agregar_nuevo_mensaje
    
    self.enviar_mensaje = lambda: self.enviar_mensaje()
    
    self.dm_screen_content = Stack(
      controls=[
        Container(
          content=Column(
            spacing=0,
            controls=[
              Row(
                alignment='spaceBetween',
                controls=[
                  WindowDragArea(
                      expand=True,
                      content=Container(height=40,)
                    ),
                    Row(
                      spacing=0,
                      controls=[
                        Container(
                          on_click=self.mini_window,
                          height=40,
                          width=40,
                          content=Image(
                            src='assets/icons/mini.png'
                          )

                        ),
                        Container(
                          on_click=self.max_window,
                          height=40,
                          width=40,
                          content=Image(
                            src='assets/icons/max.png'
                          )

                        ),
                        Container(
                          on_click=self.close_window,
                          height=40,
                          width=40,
                          content=Image(
                            src='assets/icons/close.png'
                          )

                        ),
                      ]
                    )
                ]
              ),
              
              Container(
                padding=padding.only(left=20,right=15),
                height=50,
                content=Row(
                  alignment='spaceBetween',
                  controls=[
                    Container(
                      on_click=self.show_chat_user_popup,
                      expand=True,
                      content=Row(
                        controls=[
                          Container(
                            height=40,
                            width=40,
                            border_radius=20,
                            bgcolor=rc,
                            content=Icon(
                              icons.PERSON
                            )
                          ),
                          Text(
                            value='#Se7en🙏'
                          )
                          
                        ]
                      )
                    ),

                    Row(
                      controls=[
                        Container(
                          on_hover=self.sidebar_btn_hovered,
                          alignment=alignment.center,
                          height=h_btn,
                          width=w_btn,
                          border_radius=5,
                          content=Row(
                            spacing=0,
                            alignment='center',
                            controls=[
                              Icon(
                                icons.VIDEO_CALL_OUTLINED,
                                size=20,
                                color=bg_interface
                              )
                            ]
                          )
                        ),


                        Container(
                          on_hover=self.sidebar_btn_hovered,
                          alignment=alignment.center,
                          height=h_btn,
                          width=w_btn,
                          border_radius=5,
                          content=Row(
                            spacing=0,
                            alignment='center',
                            controls=[
                              Icon(
                                icons.CALL_OUTLINED,
                                size=20,
                                color=bg_interface
                              )
                            ]
                          )
                        ),
                        
                        Container(
                          height=25,
                          width=2,
                          bgcolor=bg_btns
                        ),
                        
                        Container(
                          on_hover=self.sidebar_btn_hovered,
                          alignment=alignment.center,
                          height=h_btn,
                          width=w_btn,
                          border_radius=5,
                          content=Row(
                            spacing=0,
                            alignment='center',
                            controls=[
                              Icon(
                                icons.SEARCH_OUTLINED,
                                size=20,
                                color=bg_interface
                              )
                            ]
                          )
                        ),

                      ]
                    ),
                  ]
                )

              ),
              
              Container(
                alignment=alignment.top_left,
                padding=padding.only(left=20,right=20,top=10,bottom=10),
                expand=True,
                image_src=wallpaper,
                image_opacity=0.2,
                image_fit=ImageFit.COVER,
                bgcolor='#1a343434',
                content=Column(
                  scroll='auto',
                  spacing=10,
                  controls=self.msg_obj
                )

              ),
              
              Container(
                margin=margin.only(left=2),
                padding=padding.only(left=10,right=10),
                height=50,
                bgcolor=bgc2,
                content=Row(
                  controls=[
                    Container(
                      on_hover=self.sidebar_btn_hovered,
                      on_click=self.show_emojis_popup,
                      alignment=alignment.center,
                      height=40,
                      width=40,
                      border_radius=5,
                      content=Row(
                        spacing=0,
                        alignment='center',
                        controls=[
                          Icon(
                            icons.EMOJI_EMOTIONS_OUTLINED,
                            size=20,
                            color=bg_interface
                          )
                        ]
                      )
                    ),
                    
                    Container(
                      on_hover=self.sidebar_btn_hovered,
                      alignment=alignment.center,
                      height=40,
                      width=40,
                      border_radius=5,
                      content=Row(
                        spacing=0,
                        alignment='center',
                        controls=[
                          Icon(
                            icons.SHARE_OUTLINED,
                            size=20,
                            color=bg_interface
                          )
                        ]
                      )
                    ),
                    
                    Container(
                      on_hover=self.sidebar_btn_hovered,
                      expand=True,
                      content=input_mensaje,
                      ),
                    
                    self.send_msg_btn,
                    self.audio_msg_btn,

                  ]
                )

              ),
            
            ]
          )
        ),

        Container(
          content=Stack(
            controls=[
              self.chat_user_popup,
            ]
          )
        ),
      ]
    )

t = App  
app(target=t, view=AppView.WEB_BROWSER,assets_dir='assets')
