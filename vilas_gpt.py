import json
import flet as ft
from operator import attrgetter
import os
from typing import Union
from time import sleep
# from display import Display
# from meuscontrolesflet2  import Display



class Display2(ft.Container):
    def __init__(self,
                 
            data = None,
            value = None,
            opitions = None, #lista
            height =40,
            width = 120, 
            bgcolor = 'black' ,
            tipos_dados: Union[float, int, str] = [int, float],
            borda_width = 4,
            text_size = 25,
            border_radius = 10,
            func = None,
            on_click = None,
            text_color = None
        ): 
        super().__init__()
        self.opitions = opitions
        self.func = func
        self.on_click = on_click
        self.data = data
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in opitions]

        self.border_radius =border_radius
        self.borda_width = borda_width
        self.text_size = text_size
        if borda_width > 0:
            self.border = ft.border.all(self.borda_width, ft.colors.with_opacity(0.6,'blue'))
        else:
            self.border = None
        self.data = data
        self._value = value
        self.bgcolor = bgcolor
        self.height =height
        self.width = width
        self.padding = ft.Padding(0,0,0,0)
        self._text_color = text_color
        self.tipos_dados = tipos_dados

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
            
        
        )



    def Clicou(self,e):
        if type(e.control.text) in [int, float]:
            valor = round(e.control.text,1)
        else:
           valor = e.control.text 
        self.content.content.controls[0].value = valor
        self._value = valor
        if not self.func is None:
            self.func(valor)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()



    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, valor):
        if type(valor in self.tipos_dados):
            self._value = valor
            self.content.items.append(ft.PopupMenuItem(valor, on_click = self.Clicou))
            self.content.content.controls[0].value = valor
            self.Atualizar()
        else:
            print('número inválido')
  

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, cor):
        self._text_color = cor  
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }        

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,        
        )
         
        self.Atualizar()

class Display(ft.Container):
    def __init__(self,
                 #adicionar clique duplo para abrit campo de txto
            data = None,
            value = None,
            opitions = None, #lista
            height =40,
            width = 120, 
            bgcolor = 'black' ,
            tipos_dados: Union[float, int, str] = [int, float],
            borda_width = 4,
            text_size = 25,
            border_radius = 10,
            func = None,
            on_click = None,
            text_color = None,
            col = None
        ): 
        super().__init__()
        self.opitions = opitions
        self.col = col
        self.func = func
        self.on_click = on_click
        self.data = data
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in opitions]

        self.border_radius =border_radius
        self.borda_width = borda_width
        self.text_size = text_size
        if borda_width > 0:
            self.border = ft.border.all(self.borda_width, ft.colors.with_opacity(0.6,'blue'))
        else:
            self.border = None
        self.data = data
        self._value = value
        self.bgcolor = bgcolor
        self.height =height
        self.width = width
        self.padding = ft.Padding(0,0,0,0)
        self._text_color = text_color        
        self.tipos_dados = tipos_dados
        self._campotexto = ft.TextField(dense=True, on_submit=self.SetarValue)
        self.on_long_press = self.VirarCampoTexto

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
           
        )

    def SetarValue(self,e):
        self._value = self._campotexto.value
        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = 'white', weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER
        )
        self.Atualizar()
        if not self.func is None:
            self.func(self._value)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()        

    def VirarCampoTexto(self,e):
        content_antigo = self.content
        self.content = self._campotexto
        if not self.on_click is None:
            self.on_click(e)  
        self.Atualizar()
   

    async def Clicou(self,e):
        if type(e.control.text) in [int, float]:
            valor = round(e.control.text,1)
        else:
           valor = e.control.text 
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }   
        # self.content.content.controls[0].color =  colors.get(valor, 'white')        
        self.content.content.controls[0].value = valor
        self._value = valor
        if not self.func is None:
            await self.func(valor)
        if not self.on_click is None:
            await self.on_click(e)            
        # self.Atualizar()


    @property
    def value(self):
        try:
            v = int(self._value)
        except:
            try:
                v = float(self._value)
            except:            
                v = self._value
        return v

    def Atualizar(self):
        try:
            self.update()
        except:
            print('erou')
            pass

    @value.setter
    def value(self, valor):
        if isinstance(self.content, ft.PopupMenuButton):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.items.append(ft.PopupMenuItem(valor, on_click = self.Clicou))
                self.content.content.controls[0].value = valor
                self.Atualizar()
            else:
                print('número inválido')
        elif isinstance(self.content, ft.TextField):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.value = valor
                self.Atualizar()
            else:
                print('número inválido')
  
    # @property
    # def bgcolor(self):
    #     return self._bgcolor

    # @bgcolor.setter
    # def bgcolor(self, bgcolor):
    #     self._bgcolor = bgcolor
    #     self.Atualizar()


    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, cor):
        self._text_color = cor 
        print('cor = ', cor) 
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }        

        # self.content = ft.PopupMenuButton(
        #     content=ft.Column(
        #         [
        #             ft.Text(
        #                 self._value, 
        #                 color = self._text_color, 
        #                 weight='BOLD', 
        #                 size=self.text_size, 
        #                 no_wrap = False,
        #                 text_align = 'center' 
                        
        #             )
        #         ], 
        #         alignment='center', 
        #         horizontal_alignment='center'
        #     ),
        #     items=self.opitions,
        #     menu_position=ft.PopupMenuPosition.UNDER,        
        # )
        self.content.content.controls[0].color = cor
        print(self.content.content.controls[0].color, 'conte')
        self.content.update()
        self.Atualizar()

class Verificar_pasta:
    def __init__(self,pastalocal = 'tabelamandadostjse'):
        self.pastalocal = pastalocal
        self.verificar_pasta()

    def verificar_pasta(self):
        user_profile = os.environ.get('USERPROFILE')
        # print(user_profile)
        if not user_profile:
            # return False  # USERPROFILE não está definido
            self.local = None

        # caminho = os.path.join(user_profile, self.pastalocal)
        caminho = self.pastalocal

        if os.path.exists(caminho):
            self.local = caminho
            # return self.caminho
        else:
            os.mkdir(caminho)
            # print(caminho)
            if os.path.exists(caminho):
                self.local = caminho
                # return self.caminho
            # else:
                # return None
    

    def caminho(self, nome):
        # self.verificar_pasta()
        return os.path.join(self.local, nome)

class ConfirmarSaida:
    def __init__(self, page, funcao=None):
        self.page = page
        self.funcao = funcao
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.page.window.prevent_close = True 

    def window_event(self, e):
        if e.data == "close":
            self.page.overlay.append(self.confirm_dialog)
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self, e):
        if self.funcao:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self, page):
        self.page = page
        self.page.on_resized = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
        self.page.overlay.append(self.pw)

    def page_resize(self, e):
        self.pw.value = f"{self.page.window.width}*{self.page.window.height} px"
        self.pw.update()

class Saida2(ft.Container):
    def __init__(self, width=300,height=100, col = None):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
         
        self.bgcolor='white,0.03' 
        self.col = col  

        self.content = ft.ListView([self.saidad],
                                   auto_scroll=True,
                                   col = self.col,
                                   expand = True,
                                   )

    def pprint(self, *texto):
        for i in texto:
            self.saidad.value += f'{i}\n'
        try:
            self.page.update()
        except:
            pass


class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
                    content = ft.Text('', selectable=True, color=ft.colors.BROWN_100),
                    open=True,
                    bgcolor=ft.colors.GREY_900,
                )
 
    
    def pprint(self, *texto):
        for i in list(texto):
            self.snac.content.value = f'{i}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass


class Vila(ft.Container):
    def __init__(self, nome=None, nivel_cv=None, forca=None, cv_exposto=None, equipe=None, metodo=2, mapa=None, func=None, bgcolor = None):
        super().__init__()
        self.func = func
        self.bgcolor  = bgcolor
        # self._nome = ft.Dropdown(value=nome, options=[ft.dropdown.Option(i) for i in range(51)], dense=True, content_padding=5, width=60, on_change=self.Chenge_nome)
        self._nome = Display(value=nome, opitions=[i for i in range(51)],borda_width=0, text_size = 12, 
                             width=60, height=20,border_radius= 2,on_click=self.Chenge_nome,col = 2, bgcolor = ft.colors.TRANSPARENT)
        # self.cv = ft.Dropdown(focused_bgcolor=None, bgcolor=None, filled=True, value=nivel_cv, options=[ft.dropdown.Option(i) for i in range(20)], dense=True, content_padding=5, width=60, on_change=self.cor, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
        self.cor2(str(nivel_cv))
        self.cv = Display(value=nivel_cv, opitions=[i for i in range(7,20)], text_color = self.corTextoCV, col = 2,
                          bgcolor = self.corCV, borda_width=0, border_radius= 8,text_size = 12, width=50, height=18,func=self.cor)
        # self.cv.bgcolor = 'red'
        # self.exposicao = ft.Dropdown(value=cv_exposto, options=[ft.dropdown.Option(i) for i in range(2)], dense=True, content_padding=5, width=50, on_change=self.change_exposicao)
        self.exposicao = Display(value=cv_exposto, opitions=[0,1], borda_width=0, border_radius= 2,text_size = 12, width=60, height=20, 
                                 on_click=self.change_exposicao,col = 2, bgcolor = ft.colors.TRANSPARENT)
        # self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        
        self.controls = [self._nome, self.cv, self.exposicao]
        self.content = ft.ResponsiveRow(
            controls = self.controls, 
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            spacing = 0,
            run_spacing = 0,
            columns=6
        )
        # self.tight = True

        self.nome = nome
        self._nivel_cv = nivel_cv
        self.forca = forca
        self.cv_exposto = cv_exposto
        self.estrelas_l = 0
        self.atacante = 0
        self.estrela = 0
        self.metodo = metodo
        self.mapa = mapa
        self._equipe = equipe
        if isinstance(self._equipe, dict):
            self.set_equipe(self._equipe)

    def set_equipe(self, equipe):
        self.GRUPO_MASTER = int(equipe['GRUPO MASTER'])
        self.GRUPO_ELITE = int(equipe['GRUPO ELITE'])
        self.GRUPO_A = int(equipe['GRUPO A'])
        self.GRUPO_B = int(equipe['GRUPO B'])
        self.GRUPO_C = int(equipe['GRUPO C'])
        self.GRUPO_D = int(equipe['GRUPO D'])
        self.GRUPO_E = int(equipe['GRUPO E'])

    @property
    def equipe(self):
        return self._equipe

    @equipe.setter
    def equipe(self, equipe):
        self._equipe = equipe
        if isinstance(self._equipe, dict):
            self.set_equipe(self._equipe)

    def recebe_ataque(self, lista_jogadores):
        estrelas = 0
        for jogador in lista_jogadores:
            estrela_temp = 1 if self.cv_exposto == 1 else 0
            estrelas = self.calcular_estrelas(jogador, estrela_temp)
        self.estrelas_l = estrelas

    @property
    def cv_exp(self):
        return self.cv_exposto
    
    @cv_exp.setter
    def cv_exp(self, cv_exp):
        self.cv_exposto = cv_exp
        self.exposicao.value = 0

    @property
    def nivel_cv(self):
        return self._nivel_cv
    
    @nivel_cv.setter
    def nivel_cv(self, nivel_cv):
        self._nivel_cv = self.cv.value


    
    def calcular_estrelas(self, jogador, estrela_temp):
        estrelas = 0
        if self.metodo == 1:
            estrelas = self.metodo_1(jogador, estrela_temp)
        elif self.metodo in [2, 4]:
            estrelas = self.metodo_2_4(jogador, estrela_temp)
        elif self.metodo == 3:
            estrelas = self.metodo_3(jogador)
        return estrelas

    def metodo_1(self, jogador, estrela_temp):
        estrelas = 0
        if jogador.nivel_cv == 15:
            estrelas = self.estrelas_para_cv_15(jogador)
        elif jogador.nivel_cv == 14:
            estrelas = self.estrelas_para_cv_14(jogador)
        elif jogador.nivel_cv == 13:
            estrelas = self.estrelas_para_cv_13(jogador)
        elif jogador.nivel_cv == 12:
            estrelas = self.estrelas_para_cv_12(jogador)
        elif jogador.nivel_cv == 11:
            estrelas = self.estrelas_para_cv_11(jogador)
        elif jogador.nivel_cv == 10:
            estrelas = self.estrelas_para_cv_10(jogador)
        elif jogador.nivel_cv == 9:
            estrelas = self.estrelas_para_cv_9(jogador)
        elif jogador.nivel_cv == 8:
            estrelas = self.estrelas_para_cv_8(jogador)
        return estrelas

    def metodo_2_4(self, jogador, estrela_temp):
        estrelas = 0
        if jogador.forca >= self.GRUPO_MASTER:
            estrelas = 3 if self._nivel_cv <= 15 else 2        
        elif jogador.forca >= self.GRUPO_ELITE:
            estrelas = 3 if self._nivel_cv <= 14 else 2
        elif jogador.forca >= self.GRUPO_A:
            estrelas = 3 if self._nivel_cv <= 13 else 2
        elif jogador.forca >= self.GRUPO_B:
            estrelas = 3 if self._nivel_cv <= 12 else 2
        elif jogador.forca >= self.GRUPO_C:
            estrelas = 3 if self._nivel_cv <= 11 else (2 if self._nivel_cv in [12, 13] else estrela_temp + 1)
        elif jogador.forca >= self.GRUPO_D:
            estrelas = 3 if self._nivel_cv <= 10 else (2 if self._nivel_cv in [11, 12] else (1 + estrela_temp if self._nivel_cv == 13 else estrela_temp))
        elif jogador.forca >= self.GRUPO_E:
            estrelas = 3 if self._nivel_cv <= 9 else (2 if self._nivel_cv == 10 else (estrela_temp + 1 if self._nivel_cv == 11 else (1 if self._nivel_cv == 12 else estrela_temp)))
        return estrelas

    def metodo_3(self, jogador):
        try:
            estrelas = self.mapa.loc[str(jogador.nome), str(self.nome)]
        except:
            estrelas = self.mapa.loc[str(jogador.nome), str(self.nome) + '.0']
        return estrelas

    def estrelas_para_cv_15(self, jogador):
        if self._nivel_cv == 13:
            return 3 if jogador.forca > 90 else 2
        elif self._nivel_cv <= 12:
            return 3
        elif self._nivel_cv == 15:
            return 3 if self.forca < 40 else 2
        elif self._nivel_cv == 14:
            return 2 if self.forca > 60 else 3
        return 0

    def estrelas_para_cv_14(self, jogador):
        if self._nivel_cv <= 12:
            return 3 if jogador.forca > 50 else 2
        elif self._nivel_cv > 14:
            return 3 if self.forca < 20 else (2 if jogador.forca > 50 else 1)
        elif self._nivel_cv == 14:
            return 3 if self.forca < 40 else (2 if jogador.forca > 50 else 1)
        elif self._nivel_cv == 13:
            return 3 if jogador.forca > 90 else (3 if self.forca < 50 else 2)
        return 0

    def estrelas_para_cv_13(self, jogador):
        if self._nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self._nivel_cv == 14:
            return 3 if self.forca < 20 else 1
        elif self._nivel_cv == 13:
            return 3 if self.forca < 30 else 2
        elif self._nivel_cv == 12:
            return 3 if self.forca < 30 else 2
        elif self._nivel_cv <= 11:
            return 3
        return 0

    def estrelas_para_cv_12(self, jogador):
        if self._nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self._nivel_cv == 14:
            return 2 if self.forca < 60 else 1
        elif self._nivel_cv == 13:
            return 2 if self.forca < 50 else 1
        elif self._nivel_cv == 12:
            return 3 if self.forca < 20 else (2 if jogador.forca > 60 else 1)
        elif self._nivel_cv == 11:
            return 3 if self.forca < 30 else 2
        elif self._nivel_cv <= 10:
            return 3
        return 0

    def estrelas_para_cv_11(self, jogador):
        if self._nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self._nivel_cv == 14:
            return 2 if self.forca < 40 else 1
        elif self._nivel_cv == 13:
            return 2 if self.forca < 40 else 1
        elif self._nivel_cv == 12:
            return 3 if self.forca < 20 else 1
        elif self._nivel_cv == 11:
            return 3 if self.forca < 40 else 2
        elif self._nivel_cv <= 10:
            return 3
        return 0

    def estrelas_para_cv_10(self, jogador):
        if self._nivel_cv <= 9:
            return 3
        elif self._nivel_cv >= 14:
            return 1 if self.forca < 20 else 1
        elif self._nivel_cv == 13:
            return 2 if self.forca > 20 else 3
        elif self._nivel_cv == 12:
            return 2 if self.forca > 20 else 3
        elif self._nivel_cv == 11:
            return 2 if self.forca > 20 else 3
        elif self._nivel_cv == 10:
            return 2 if self.forca > 80 else 3
        return 0

    def estrelas_para_cv_9(self, jogador):
        if self._nivel_cv <= 8:
            return 3
        elif self._nivel_cv == 12:
            return 1 if self.forca < 20 else 0
        elif self._nivel_cv == 10:
            return 2 if self.forca > 50 else 3
        elif self._nivel_cv == 9:
            return 2 if jogador.forca < 90 else 3
        return 0

    def estrelas_para_cv_8(self, jogador):
        if self._nivel_cv <= 8:
            return 3
        elif self._nivel_cv >= 11:
            return 1 if self.forca < 20 else 0
        elif self._nivel_cv == 10:
            return 1 if self.forca > 50 else 2
        elif self._nivel_cv == 9:
            return 2
        return 0

    def Chenge_nome(self, e):
        self.nome = int(self._nome.value)
        if self.func:
            self.func(int(self.cv.value))

    async def change_exposicao(self, e):
        self.cv_exposto = int(self.exposicao.value)
        if self.func:
            # print('aqui, change')
            await self.func(int(self.cv.value))

    async def cor(self, e):
        self.cv.color = None
        self.update()
        self.cor3(str(e))
        self._nivel_cv = int(self.cv.value)
        if self.func:
            await self.func(int(self.cv.value))
        self.Atualizar()

    def cor2(self, cv):
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }
        # self.cv.bgcolor = colors.get(cv, None)
        self.corCV = colors.get(cv, None)
        if cv in ['14', '13', '12', '11', '10', '9', '8']:
            # self.cv.color = 'red'
            self.corTextoCV = 'red'
        else:
            self.corTextoCV = None

    def cor3(self, cv):
        # print(cv)
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }
        # print('cv=', cv)
        self.cv.bgcolor = colors.get(cv, None)
        # self.corCV = colors.get(cv, None)
        if cv in ['14', '13', '12', '11', '10', '9', '8']:
            # self.cv.color = 'red'
            print('cv=', cv)

            self.cv.text_color = 'red'
        else:
            self.cv.text_color = None            

    def Atualizar(self):
        try:
          self.update()  
        except:
            pass



class LayoutVilas(ft.ResponsiveRow):
    def __init__(self, num_vilas=15, printt=None,  func = None, page = None):
        super().__init__()
        self.page = page
        self.printt = printt
        self.func = func
        self.spacing = 0
        self.run_spacing = 0
        # self.width = 300
        self.columns = 12
        self.vertical_alignment = ft.MainAxisAlignment.START
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.num_vilas = ft.Dropdown(label='Número de Vilas', value=num_vilas, 
                                     options=[ft.dropdown.Option(i) for i in range(51)], 
                                     dense=True, content_padding=12,
                                     padding= ft.Padding(0,5,0,0),
                                    #  width=110,
                                     border_width=1, 
                                     on_change=self.Chenge_num_vilas)
        self.botao_salvar = ft.ElevatedButton('Salvar', on_click=self.Salvar,  scale=0.8)
        self.botao_zerar = ft.ElevatedButton('zerar exp', on_click=self.Zerar_exposicoes, scale=0.8)
        self.botao_ordenar = ft.ElevatedButton('Ordenar', on_click=self.Ordenar_vilas,  scale=0.8)
        self.botao_atualizar = ft.ElevatedButton('Atualizar', on_click=self.AtualizarVilas2, scale=0.8)
        self.botao_carregarvilas = ft.ElevatedButton('Carregar vilas', 
                                                     on_click=self.CarregarVilas, 
                                                    #  width=300, 
                                                     expand_loose=True,
                                                     scale=0.8)
        # self.saida = Saida(100,200, 8)


        self.col_A = ft.ListView([

            self.num_vilas,
            self.botao_salvar,self.botao_zerar,self.botao_ordenar,self.botao_atualizar, 
            
            ],col = {'xs':8, 'sm':9, 'md':7}, 
            # horizontal_alignment='start'
        )
        # self.col_A.controls.append(self.saida)

        c1 = self.columns-self.col_A.col['xs']
        c2 = self.columns-self.col_A.col['sm']
        c3 = self.columns-self.col_A.col['md']
        self.col_B = ft.ListView(
            spacing=10, 
            # run_spacing=0, 
            col =  {'xs':c1, 'sm':c2, 'md':c3}, 
            # horizontal_alignment='end'
        )
        # if self.page is None:
        #     pw = 450
        # else:
        #     pw = self.page.window.height
        self.col_B.controls.append(
            ft.Container(
                ft.ResponsiveRow(
                    [ft.Text('  Nome    ', col = 2, size = 10, text_align='center', weight='BOLD'), 
                     ft.Text(' CV  ', col = 2, size = 10, text_align='center', weight='BOLD'), 
                     ft.Text('Exposição', col = 2, size = 10, text_align='center', weight='BOLD')],
                    columns = 6,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ), 
                border=ft.Border(
                    top = ft.BorderSide(1, 'white,0.5'),
                    left = ft.BorderSide(1, 'white,0.5'),
                    bottom = ft.BorderSide(1, 'white,0.5'),
                    right = ft.BorderSide(1, 'white,0.5'),
                ), 
                # width=180,
                
            )
        )
        # cumprimento_coluna = min(pw-160, 165 + (36 * int(num_vilas)))
        self.col_B.controls.append(ft.Container(ft.ListView(
            # height=cumprimento_coluna, 
            # scroll=ft.ScrollMode.ADAPTIVE
            spacing=8
            ), 
            border=ft.Border(
                bottom = ft.BorderSide(1, 'white,0.5'),
                left = ft.BorderSide(1, 'white,0.5'),
                top = None,
                right = ft.BorderSide(1, 'white,0.5'),
            ), 
            # width=180,
            border_radius=8
            ))
        self.config_vilas = Verificar_pasta('Guerra_clash').caminho('vilas_config.json')
        # self.lista_vilas = self.inicializar_vilas()
        # sleep(5)
        # while not self.lista_vilas:
        #     sleep(1)
    # def did_mount(self):

        self.inicializar_vilas()

        # self.printt = self.saida.pprint
        # self.height = 500
        self.controls = [self.botao_carregarvilas]

        # self.col_B.controls[1].content.controls = self.lista_vilas
        # self.controls= [self.col_A ,self.col_B ]


        


        
    def inicializar_vilas(self):
        lista_vilas = []
        try:
            self.arquiv = self.page.client_storage.get('vilas')
            # self.arquiv = self.Ler_json(self.config_vilas)
            
            for nome, nivel_cv, cv_exposto , c in zip(self.arquiv['nome'], self.arquiv['nivel_cv'], self.arquiv['cv_exposto'], range(60)):
                cor  = ft.colors.TRANSPARENT if c%2 == 0 else ft.colors.GREY_500
                lista_vilas.append(
                   
                        Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar,bgcolor=cor),
                  
                  
                    )        
        except:
            lista_vilas = [Vila(nome=i, nivel_cv=16, cv_exposto=0, func=self.Salvar) for i in range(1, int(self.num_vilas.value) + 1)]
        self.lista_vilas = lista_vilas


    def AtualizarVilas(self,e):
        # self.arquiv = await self.page.client_storage.get_async('vilas')
        # if isinstance(self.arquiv, dict):
        #     lista_vilas = []

        #     for nome, nivel_cv, cv_exposto, c in zip(self.arquiv['nome'], self.arquiv['nivel_cv'], self.arquiv['cv_exposto'], range(60)):
        #             # lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar))
        #         cor  = ft.colors.TRANSPARENT if c%2 == 0 else ft.colors.GREY_800
        #         lista_vilas.append(
            
        #                 Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar, bgcolor=cor),
                        
                   
        #             )                    
        #     self.lista_vilas = lista_vilas
        self.col_B.controls[1].content.controls = self.lista_vilas        
        self.update()

    async def AtualizarVilas2(self,e):
        self.arquiv = await self.page.client_storage.get_async('vilas')
        if isinstance(self.arquiv, dict):
            lista_vilas = []

            for nome, nivel_cv, cv_exposto, c in zip(self.arquiv['nome'], self.arquiv['nivel_cv'], self.arquiv['cv_exposto'], range(60)):
                    # lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar))
                cor  = ft.colors.TRANSPARENT if c%2 == 0 else ft.colors.GREY_800
                lista_vilas.append(
            
                        Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar, bgcolor=cor),
                        
                   
                    )                    
            self.lista_vilas = lista_vilas
            self.col_B.controls[1].content.controls = self.lista_vilas        
        self.update()



    def AtualizarVilas2(self,e):
        self.arquiv = self.page.client_storage.get('vilas')
        lista_vilas = []

        for nome, nivel_cv, cv_exposto in zip(self.arquiv['nome'], self.arquiv['nivel_cv'], self.arquiv['cv_exposto']):
                lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar))
        self.lista_vilas = lista_vilas
        self.col_B.controls[1].content.controls = self.lista_vilas        
        self.update()        

    def CarregarVilas(self,e):
        self.AtualizarVilas(1)
        self.col_B.controls[1].content.controls = self.lista_vilas
        self.controls= [self.col_A ,self.col_B ]
        self.update()

    def Gera_Lista_de_Vilas(self, equipee=None):
        # self.AtualizarVilas(1)
        for vila in self.lista_vilas:
            vila.equipe = equipee
            vila.forca = (50 - vila.nome) + 50 * vila.nivel_cv
        self.printt('Lista de vilas gerada com sucesso!')
        return self.lista_vilas
        
    def Chenge_num_vilas(self, e):
            # self.page.window.height = 165+(36*int(self.num_vilas.value)) 
            self.controls[1].controls[1].content.controls = []  
            # self.controls[1].controls[1].content.controls.append(ft.Container(ft.Row([ft.Text('  Nome    '),ft.Text(' CV  '),ft.Text('Exposição')]),border=ft.border.all(1,'white,0.5'),width=180))
            self.lista_vilas = []
            try:
                self.arquiv = self.Ler_json(self.config_vilas)
                # self.arquiv = self.LerDadosLocais('vilas')
                if int(self.num_vilas.value) <= len(self.arquiv['nome']):
                    for i,j,k,l in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['cv_exposto'], range(1,int(self.num_vilas.value)+1)):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = j,cv_exposto = k, func=self.Salvar))
                else:
                    for i,j,k,l in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['cv_exposto'], range(1,int(self.num_vilas.value)+1)):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = j,cv_exposto = k, func=self.Salvar))  
                    for i  in range(l+1,int(self.num_vilas.value)+1):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = 15,cv_exposto = 0, func=self.Salvar))                     
            except:
                for i in range(1,int(self.num_vilas.value)+1):
                    self.lista_vilas.append(Vila(nome = i,nivel_cv = 15,cv_exposto = 0, func=self.Salvar))        
            
            self.controls[1].controls[1].content.controls = self.lista_vilas   
            self.page.update()    
        
    def Zerar_exposicoes(self,e):
        for i in self.lista_vilas:
            i.cv_exp = 0
        self.controls[1].controls[1].content.controls = self.lista_vilas
        self.update()

    async def Salvar(self, e):
        dic = {'nome': [], 'nivel_cv': [], 'cv_exposto': []}
        for vila in self.lista_vilas:
            dic['nome'].append(vila.nome)
            dic['nivel_cv'].append(vila.nivel_cv)
            dic['cv_exposto'].append(vila.cv_exposto)
        # self.Escrever_json(dic, self.config_vilas)
        # print('aqio')
        await self.page.client_storage.set_async('vilas',dic)
        # self.SalvarDadosLocais('vilas', dic)

        # lista_vilas = []
        # for nome, nivel_cv, cv_exposto in zip(dic['nome'], dic['nivel_cv'], dic['cv_exposto']):
        #         lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar))
        # self.lista_vilas = lista_vilas       
        # self.col_B.controls[1].content.controls = self.lista_vilas  

        # self.update()
        self.AtualizarVilas(e)
        # self.func(['vilas', self.lista_vilas])
        self.printt('Vilas salvas com sucesso')





    async def ArmazenarDados(self):
        if not self.page.session.contains_key("vilas"): # True if the key exists
            dic = {'nome': [], 'nivel_cv': [], 'cv_exposto': []}
            for vila in self.lista_vilas:
                dic['nome'].append(vila.nome)
                dic['nivel_cv'].append(vila.nivel_cv)
                dic['cv_exposto'].append(vila.cv_exposto)
            # self.Escrever_json(dic, self.config_vilas)
            self.page.client_storage.set('vilas',dic)        

    # def SalvarDadosLocais(self, nome, valor):
    #     self.page.client_storage.set(nome, valor)
      

    # def LerDadosLocais(self, nome):
    #     return self.page.client_storage.get(nome)

    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if not nomedoarquivo.endswith('json'):
            nomedoarquivo += '.json'
        with open(nomedoarquivo, 'w') as f:
            json.dump(nomedodicionario, f, indent=4)

    def Ler_json(self, nomedoarquivo):
        if not nomedoarquivo.endswith('json'):
            nomedoarquivo += '.json'
        try:
            with open(nomedoarquivo, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {}
        

    def OrdenarListadeClasses(self, lista, atributo, decrecente=True):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)    

    def Ordenar_vilas(self, e):
        self.controls[1].controls[1].content.controls = self.OrdenarListadeClasses(self.controls[1].controls[1].content.controls,'nivel_cv')
        self.update()     


def main(page: ft.Page):
    page.window.width = 350
    page.window.height = 690
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START
    # page.theme = ft.ThemeMode.DARK
    ConfirmarSaida(page)
    saida = Saida(page)
    Resize(page)
    v = LayoutVilas(15, printt=saida.pprint, page=page)
    # page.add(ft.Row([ft.Column([v]), ft.Column([saida], alignment='center', width=150, height=600)]))
    page.add(v)

if __name__ == '__main__':
    ft.app(main)
