import flet as ft
import json
# import pandas as pd
from operator import attrgetter
import threading
# from concurrent.futures import ThreadPoolExecutor
from typing import Union
import time
import random
import os


from vilas_gpt import LayoutVilas,Vila
from jogadores import layout_jogadores,Jogador
from equipes_gpt import LayoutEquipes as layout_equipes
from importar import layout_Importar
# from meuscontrolesflet2 import Display


class Display(ft.Container):
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
            text_color = None,
            text_align = 'center', #Optional[TextAlign] = None,
            horizontal_alignment = 'center' #CrossAxisAlignment
        ): 
        super().__init__()
        self.opitions = opitions
        self.func = func
        self.on_click = on_click
        self.data = data
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0), mouse_cursor = None) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0), mouse_cursor = None) for i in opitions]

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
        self.text_align = text_align
        self.horizontal_alignment = horizontal_alignment
        self._campotexto = ft.TextField(dense=True, on_submit=self.SetarValue)
        self.on_long_press = self.VirarCampoTexto

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = self.text_align  )], alignment='center', horizontal_alignment= self.horizontal_alignment),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
        
        )

    def SetarValue(self,e):
        self._value = self._campotexto.value
        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = self.text_align  )], alignment='center', horizontal_alignment= self.horizontal_alignment),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
        
        )
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
        try:
            v = int(self._value)
        except:
            try:
                v = float(self._value)
            except:            
                v = self._value
        return v

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

class BotaoCT(ft.Container):
    def __init__(self,nome,on_click = None, bgcolor = None, scale = None, text_size = None, col = None ):
        super().__init__()
        self.on_click=on_click
        self.border_radius = 0
        self.bgcolor_og = bgcolor
        self.bgcolor = bgcolor+',0.7' if bgcolor else None
        self.scale = scale
        self.col = col
        self.text_size = text_size
        self.expand = True
        self.padding = ft.Padding(4,0,4,0)
        # self.border=ft.Border(right=ft.BorderSide(2,'white,0.4'))
        self.nome = nome
        # self.content = ft.Row([ft.VerticalDivider(color='blue', width=2), ft.Text(nome, weight='BOLD', text_align='center'),ft.VerticalDivider(color='blue', width=2),],alignment='center')
        self.content = ft.Text(nome, weight='BOLD', text_align='center', size = self.text_size, )
        self.on_hover = self.Passoumouse                                       


    def Passoumouse(self,e):
        self.content.color = 'blue' if e.data == "true"else 'white'
        self.update()

class My_Dropdown(ft.Dropdown):
    def __init__(self, nome,on_change, *itens):
        super().__init__()
        self.label = nome
        self.options = [ft.dropdown.Option(i) for i in list(itens)]
        self.on_change = on_change
        self.width = 150
        self.value = None
        self.dense = True
        self.content_padding = 7
        self.scale = 0.8
    
class My_tabela(ft.DataTable):
    def __init__(self, dic#DataFrame ou dicionário
                 ):
        super().__init__(columns=[ft.DataColumn(label = ft.Text('meu ovo') )])
        self._dic = dic 
        self.border = ft.border.all(1,'white,0.9')
        self.heading_row_color = 'white,0.5'
        self.heading_row_height = 35
        self.column_spacing = 15
        # self.heading_row_color=colors.BLACK12
        self.vertical_lines = ft.border.all(20,'white')
        self.horizontal_margin = 0
        self.data_row_max_height = 35
        # self.data_row_min_height = 50
        self.divider_thickness = 0
        self.show_checkbox_column = True
        self.sort_column_index = 0
        self.sort_ascending = True
        # self.data_row_color={"hovered": "0x30FF0000"}
        self.visible = False
        self.textsize = 15

        self.Colunas_tabela()
        self.Linhas_tabela()

    def Colunas_tabela(self):
        self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM)],alignment='center')) for i in list(self._dic.keys())]
        
    
    def Linhas_tabela(self):
        linhas = []
        # df_lista = self._df.values.tolist()
        # opcoes = [ft.dropdown.Option(i[0]) for i in df_lista]
        # opcoes = [i[0] for i in df_lista]
        opcoes = [i for i in self._dic[list(self._dic.keys())[0]]]
        df_lista = []
        for i in range(len(self._dic[list(self._dic.keys())[0]])):
            l = []
            for j in list(self._dic.keys()):
                l.append(self._dic[j][i])
            df_lista.append(l)

        # df_lista = [self._dic[i] for i in list(self._dic.keys())]
        for l,i in enumerate(df_lista):
            cell = [ft.DataCell(ft.Row([
                                        # ft.Dropdown(value = i[0],options=opcoes, dense = True, width=165, content_padding=7)
                                        Display(value = i[0],opitions=opcoes, width=165,height=20,text_size = 15, borda_width = 0, 
                                                text_align= ft.TextAlign.END, horizontal_alignment=ft.CrossAxisAlignment.END)
                                        ],width=165,alignment='center',spacing = 3,vertical_alignment='center'))]
            
            

            cell += [ ft.DataCell(ft.Row([ft.Text(j,text_align='center',selectable = True, size = self.textsize)],
                        alignment='center',spacing = 3,vertical_alignment='center')) for j in i[1:]]
            
            cor  = 'black' if l % 2 == 0 else 'white,0.01'
            linhas.append(ft.DataRow(cells = cell, color = cor))
        self.rows = linhas

    @property
    def dic(self):
        return self._dic
    @dic.setter
    def dic(self, dic):
        if isinstance(dic, dict):
            self._dic = dic 
            self.Colunas_tabela()
            self.Linhas_tabela()
        else:
            raise(f'{dic} não é um dicionário')


# class My_tabelaE(ft.DataTable):
#     def __init__(self, df,#DataFrame ou dicionário
#                  on_tap_down = None
#                  ):
#         super().__init__()
#         self._df = df if type(df) != dict else pd.DataFrame(df)
#         self.border = ft.border.all(1,'white,0.9')
#         self.heading_row_color = 'white,0.5'
#         self.heading_row_height = 35
#         self.column_spacing = 15
#         # self.heading_row_color=colors.BLACK12
#         self.vertical_lines = ft.border.all(20,'white')
#         self.horizontal_margin = 0
#         self.data_row_max_height = 35
#         # self.data_row_min_height = 50
#         self.divider_thickness = 0
#         self.show_checkbox_column = True
#         self.sort_column_index = 4
#         self.sort_ascending = True
#         self.on_tap_down = on_tap_down
#         self.tabela = None
#         # self.data_row_color={"hovered": "0x30FF0000"}
                
#         self.textsize = 15
#         self.Colunas_tabela()
#         self.Linhas_tabela()

#     def Colunas_tabela(self):
#         self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM,width=50 if k != 0 else 150)],alignment='center')) for k,i in enumerate(list(self._df.columns))]
        
    
#     def Linhas_tabela(self):
#         linhas = []
#         df_lista = self._df.values.tolist()
#         for l,i in enumerate(df_lista):
#             cell = [ ft.DataCell(ft.Row([ft.TextField(value = j,text_align='center', content_padding = 0,text_size = self.textsize, dense = True,height= 30, width=50 if k != 0 else 150)],
#                     alignment='center',spacing = 3,vertical_alignment='center'), data = [l, k, 'cel'], on_tap_down = None) for k,j in enumerate(i)]
#             cor  = 'black' if l % 2 == 0 else 'white,0.01'
#             linhas.append(ft.DataRow(cells = cell, color = cor))
#         self.rows = linhas

#     @property
#     def df(self):
#         return self._df
#     @df.setter
#     def df(self, df):
#         self._df = df if type(df) != dict else pd.DataFrame(df)
#         self.Colunas_tabela()
#         self.Linhas_tabela()


#     def func(self,e):
#         # e.control.data
#         valor = e.control.content.controls[0].value
#         # self.on_tap_down(valor)
#         self.update()

#     def Gerar_df(self):
#         colunas = self._df.columns
#         linhas = [i.cells for i in self.rows]
#         linhas2 = []

#         for i in linhas:
#             l = []
#             for j in i:
#                 l.append(j.content.controls[0].value)
#             linhas2.append(l)


#         self.tabela =  pd.DataFrame(linhas2,columns=colunas)
#         return self.tabela

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

class Guerra2:
    def __init__(self, metodo, fase=None, arq_configuracoes=None, page = None, 
                 listavilas = None,
                listajogadores=None,
                equipe=None,
                 ):
        # super().__init__()
        self.arq_configuracoes = arq_configuracoes
        self.metodo = metodo
        self.fase = fase
        self.page = page
        self.config_equipes = Verificar_pasta('Guerra_clash').caminho('config_guerra.json')        


        # self.lista_jogadores = self.jogadores()[:]  # chama a função jogadores
        self.lista_jogadores = layout_jogadores(printt = print,page = self.page).Gera_Lista_de_jogadores()
        # self.lista_jogadores
        # self.ord_jogs = self.DefinirPesos()
        # chama a função lista_de_vilas
        self.equipe = self.Buscar_equipe()
        # self.lista_vilas

        if listavilas:
            self.lista_vilas = listavilas
        if self.equipe != None:
            # self.lista_vilas = self.lista_de_vilas_func()[:]
            # v = layout_vilas(printt = print)
            if not self.lista_vilas:
                self.vilas = LayoutVilas(printt = print, page = self.page)
                self.lista_vilas = self.vilas.Gera_Lista_de_Vilas(self.equipe)
            # self.AtualizarVilas()
            

        if listajogadores:
            self.lista_jogadores = listajogadores
        if equipe:
            self.equipe = equipe            
        self.GerarMapaInicial()
        self.seq = [[0], [0]]
        self.pl = 0
        self.estrelas = 0
        self.parar = False
        self.rodou = False
        self.meus_jogadores = None
        # self.tempo_inicial = 0
        # self.tempo_final = None
        # self.delta_t = None
        self.df = None




    def Buscar_equipe(self):
      equipe = self.Ler_json(self.config_equipes,
                default={
            "equipe A": {
                    "Nome da Equipe": "equipe A",
                    "GRUPO MASTER": "1930",
                    "GRUPO ELITE": "1825",
                    "GRUPO A": "1794",
                    "GRUPO B": "1585",
                    "GRUPO C": "1444",
                    "GRUPO D": "1440",
                    "GRUPO E": "1430"
                }
        })  

    #   equipe = self.LerDadosLocais('equipes',
    #             default={
    #         "equipe A": {
    #                 "Nome da Equipe": "equipe A",
    #                 "GRUPO MASTER": "1930",
    #                 "GRUPO ELITE": "1825",
    #                 "GRUPO A": "1794",
    #                 "GRUPO B": "1585",
    #                 "GRUPO C": "1444",
    #                 "GRUPO D": "1440",
    #                 "GRUPO E": "1430"
    #             }
    #     })                                
      
      self.equipe = equipe['equipe A']
    #   print(self.equipe)
      return self.equipe
#  Método 4

    def Minhas_contas(self):
        a1 = Ler_celulas2(intervalo="A2:C40",
                          key='13JWOtfPbyPQ4BgerTncnbNsSVEoQMFeHW6aRY4_9I5Q',
                          pagina="minhas",
                          credencial='cliente.json'
                          )

        a = pd.DataFrame(a1, columns=['Jogador', 'cv', 'força']).dropna()
        a = a[a['Jogador'].str.len() > 1].values.tolist()
        j = [i[:3] for i in a]
        # cria uma lista vazia de tamanho zero para armazenas as instâncias Jogadores
        self.meus_jogadores = [Jogador(*h) for h in j]

    def Outras_contas(self):
        if self.meus_jogadores == None:
            self.Minhas_contas()
        nome_meus_jogadores = [i.nome for i in self.meus_jogadores]
        nomes_lista_jogadores = [i.nome for i in self.lista_jogadores]
        nomes_outros_jogadores = list(
            set(set(nomes_lista_jogadores) - set(nome_meus_jogadores)))

        self.outros_jogadores = []
        for i in nomes_outros_jogadores:
            for j in self.lista_jogadores:
                if j.nome == i:
                    self.outros_jogadores.append(j)

    def OrdenarListadeClasses(self, lista, atributo, decrecente=False):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)


    def AtualizarVilas(self):
        arquiv = self.page.client_storage.get('vilas')
        
        # print(arquiv)
        lista_vilas = []

        for nome, nivel_cv, cv_exposto in zip(arquiv['nome'], arquiv['nivel_cv'], arquiv['cv_exposto']):
                lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=None))
        
        for vila in lista_vilas:
                    vila.equipe = self.equipe
                    vila.forca = (50 - vila.nome) + 50 * vila.nivel_cv        

        self.lista_vilas = lista_vilas

    # async def AtualizarVilas(self):
    #     arquiv = await self.page.client_storage.get_async('vilas')
    #     time.sleep(2)
    #     if arquiv:
    #         lista_vilas = []
    #         for nome, nivel_cv, cv_exposto in zip(arquiv['nome'], arquiv['nivel_cv'], arquiv['cv_exposto']):
    #             lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=None))

    #         for vila in lista_vilas:
    #             vila.equipe = self.equipe
    #             vila.forca = (50 - vila.nome) + 50 * vila.nivel_cv
    #         self.lista_vilas = lista_vilas
    #     else:
    #         print("Nenhuma vila encontrada no client_storage.")


    def Resultado_metodo_4(self):
        atacantes = []

        # self.AtualizarVilas()
        # time.sleep(5)

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=False)

        lista_de_vilas_forca = self.OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=False)

        
        self.GerarMapaInicial()
        vilas = self.mapa
        # print('MEU OVO')
        # print(vilas)

        # print(lista_de_vilas_forca)
        for i in lista_de_vilas_forca:
            estrelas = max(vilas[str(i.nome)])
            while i.atacante == 0:
                for j in self.lista_jogadores:
                    index = vilas['Jogador'].index(j.nome)
                    if vilas[str(i.nome)][index] == estrelas and j.nome not in atacantes:
                        i.atacante = j.nome
                        i.estrela = estrelas
                        atacantes.append(j.nome)
                        break
                estrelas += -1
                if estrelas < 0:
                    i.atacante = ''
                    break
        dic = {'Jogador': [], 'Vilas': [], 'Estrelas': [], 'CV':[]}
        lista_de_vilas_forca = self.OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=True)
        for i in lista_de_vilas_forca:
            dic['Jogador'].append(i.atacante)
            dic['Vilas'].append(i.nome)
            dic['Estrelas'].append(i.estrela)
            dic['CV'].append(i.nivel_cv)

        total_es = sum(dic['Estrelas'])
        dic['Estrelas'].append(total_es)
        dic['Jogador'].append('Total')
        dic['Vilas'].append(' ')
        dic['CV'].append(' ')


        # df = pd.DataFrame(dic)
        # df = df.sort_values(by='Vilas')
        # df.to_clipboard(index=False)
        # print(df)
        # self.df = df
        # print(dic)
        self.dic = dic

    def Resultado_outras_contas(self):
        self.Minhas_contas()

        # num_vilas = g.mapa.shape[1] - 1
        atacantes = []
        atacadas = []
        estrelas = []

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=True)
        self.GerarMapaInicial()
        vilas = self.mapa

        minhascontas = self.OrdenarListadeClasses(
            self.meus_jogadores, 'forca', decrecente=True)
        nome_minhas_contas = [i.nome for i in minhascontas]

        lista_de_vilas_forca = [int(list(vilas.columns)[-i])
                                for i in range(1, len(list(vilas.columns)))]

        for i in lista_de_vilas_forca:
            for j in range(1, len(vilas['1'])+1):
                try:
                    if vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j] not in atacantes+nome_minhas_contas:
                        self.lista_vilas[i-1].atacante = vilas[vilas[str(
                            i)] == max(vilas[str(i)])]['Jogador'][-j]
                        estrelas.append(max(vilas[str(i)]))
                        atacadas.append(i)
                        atacantes.append(
                            vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j])
                        # print(vilas[vilas[str(i)]==max(vilas[str(i)])]['Jogador'][-j])
                        break
                except:
                    break

        dic = {'Jogador': atacantes, 'Vilas': atacadas, 'Estrelas': estrelas}

        df = pd.DataFrame(dic)
        df = df.sort_values(by='Vilas')
        self.df = df
        # df.to_clipboard(index=False)

    def Resultado_vilas_q_sobraram(self):
        self.Outras_contas()

        # g.Minhas_contas()
        # print(g.mapa)
        # num_vilas = g.mapa.shape[1] - 1
        atacantes = []
        atacadas = []
        estrelas = []
        outrascontas = self.OrdenarListadeClasses(
            self.outros_jogadores, 'forca', decrecente=True)
        nome_outras_contas = [i.nome for i in outrascontas]

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=True)
        self.GerarMapaInicial()
        vilas = self.mapa

        a1 = Ler_celulas2(intervalo="A1:A46",
                          key='13JWOtfPbyPQ4BgerTncnbNsSVEoQMFeHW6aRY4_9I5Q',
                          pagina="sobra",
                          credencial='cliente.json'
                          )
        try:
            d = list(pd.DataFrame(a1)[0])

            lista_vilas_q_sobraram = [int(d[-i]) for i in range(1, len(d)+1)]

            for i in lista_vilas_q_sobraram:
                for j in range(1, len(vilas['1'])+1):
                    try:
                        if vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j] not in atacantes+nome_outras_contas:
                            self.lista_vilas[i-1].atacante = vilas[vilas[str(
                                i)] == max(vilas[str(i)])]['Jogador'][-j]
                            estrelas.append(max(vilas[str(i)]))
                            atacadas.append(i)
                            atacantes.append(
                                vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j])
                            # print(vilas[vilas[str(i)]==max(vilas[str(i)])]['Jogador'][-j])
                            break
                    except:
                        break

            dic = {'Jogador': atacantes, 'Vilas': atacadas, 'Estrelas': estrelas}

            df = pd.DataFrame(dic)
            df = df.sort_values(by='Vilas')
            self.df = df
            # df.to_clipboard(index=False)
        except:
            print('ERRO!')
            print(
                'A aba "sobra" da planlha não está devidamente preecnhida com os números das vilas que sobraram')

        # lista_vilas_q_sobraram = [15,23,22,19,18,17,16,9,8,7,6,5,4,3,2,1]
        # lista_vilas_q_sobraram = [str(i) for i in lista_vilas_q_sobraram]

    def TipoArquivo(self):
        try:
            a = (__file__[-2:])
            return 'py'
        except:
            a = os.getcwd()[-2:]
            return 'jupter'

    def LimparTela(self):
        if self.TipoArquivo() != 'py':
            clear_output()
        else:
            os.system('cls')

    def jogadores(self):
        # a = pd.read_excel('vilas-04-03-2023.xlsx', sheet_name='jogadores').values.tolist()  #recebe todos os valores da aba3 da planilha do google sheets
        # .iloc[:15,:4].values.tolist()  #recebe todos os valores da aba3 da planilha do google sheets
        a = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vR5G05936eje6gI30Y6MBQDoBe8cwDjq72Hm1H0av-wASMT-h-8ud2o6cb5ag4YNsu5WDpe1mWEwOYK/pub?gid=164556332&single=true&output=csv')
        a = a[a['Jogador'].str.len() > 1].values.tolist()
        j = [i[:3] for i in a]
        jg = []  # cria uma lista vazia de tamanho zero para armazenas as instâncias Jogadores
        for h in range(len(j)):  # percorre todos os dados da  lista J
            # adiciona cada uma das instãncias jogadore à lista Jg
            jg.append(Jogador(*j[h]))
        return jg  # Retorna uma lista com todas as instâncias jogadores

    def lista_de_vilas_func(self):
        # criando uma lista de vilas########################################################################################################################################
        # all_rows = pd.read_excel('vilas-04-03-2023.xlsx', sheet_name='Página1').values.tolist() #recebe a planilha vilas do google sheets
        # .iloc[:15,:4].astype(int).values.tolist()
        all_rows = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vR5G05936eje6gI30Y6MBQDoBe8cwDjq72Hm1H0av-wASMT-h-8ud2o6cb5ag4YNsu5WDpe1mWEwOYK/pub?gid=0&single=true&output=csv').iloc[:, :4]
        all_rows = all_rows.dropna().values.tolist()
        lista_vilas = []
        for i in all_rows:
            lista_vilas.append(Vila(*i, equipe=self.equipe,
                                    metodo=2, mapa=None))
            # print(lista_vilas[0].metodo)
        return lista_vilas

    def Embaralhar(self, lista):
        s5 = lista[:]
        random.shuffle(s5)
        return s5

    def gera_alvos_e_estrelas_de_lista_de_vilas_embralhada(self):
        estrelas_01 = []
        alvos_0 = []
        lista_de_vilas_embralhada = self.Embaralhar(self.lista_de_vilas)
        for y, e in enumerate(self.lista_jogadores):
            # print(lista_jogadores[y].nome)
            alvos_0.append(lista_de_vilas_embralhada[y].nome)
            lista_de_vilas_embralhada[y].recebe_ataque([e])
            estrelas_01.append(lista_de_vilas_embralhada[y].estrelas_l)
            # print(f'Vila {lista_de_vilas_embralhada[y].nome} recebendo ataque de {e.nome} resultou em {lista_de_vilas_embralhada[y].estrelas_l} estrelas')

        al_est = [alvos_0, estrelas_01]
        return al_est

    def gera_jogadores_e_estrelas_de_lista_de_jogadores_embralhada(self):
        estrelas_01 = []
        jogadores_0 = []
        lista_de_jogadores_embralhada = self.Embaralhar(self.lista_jogadores)
        for y, e in enumerate(self.lista_vilas):
            # print(lista_jogadores[y].nome)
            jogadores_0.append(lista_de_jogadores_embralhada[y])
            e.recebe_ataque([lista_de_jogadores_embralhada[y]])
            estrelas_01.append(e.estrelas_l)
        al_est = [jogadores_0, estrelas_01]
        return al_est

    def ConverterListadeListaParaDicionario(self, listaDeLista):
        if isinstance(listaDeLista, list) and isinstance(listaDeLista[0], list):
            return {i[0]:i[1:]for i in listaDeLista}
        else:
            raise('lista de lista inválida')

    def OrdenarDicionario(self, dic, col):
        coluna_old = dic[col]
        ord = sorted(dic[col])
        novo_index = [coluna_old.index(i) for i in ord]
        for i in dic.keys():
            dic[i]= [dic[i][k] for k in novo_index ]
        return dic

    def ConverterListadeListaParadiciomarioColunas(self, listadelistas, chaves):
        dic = {i:[] for i in chaves}
        for i in range(len(chaves)):
            l = []
            for j in range(len(listadelistas)):
                l.append(listadelistas[j][i])
            dic[chaves[i]].extend(l)
        return dic

    def GerarMapaDeEstrelas(self):
        mapa = []
        for i in self.lista_jogadores:
            estrelas_02 = []
            for j in self.lista_vilas:
                # print(i.nome)
                j.recebe_ataque([i])
                estrelas_02.append(j.estrelas_l)
            # i.estrelas = estrelas_02
            mapa.append([i.nome] + estrelas_02)
        # print(mapa)
        # gm = pd.DataFrame(
        #     mapa, columns=['Jogador']+[str(i.nome) for i in self.lista_vilas])
        # gm.to_clipboard()
        # print(gm)
        # self.df = gm
        chaves=['Jogador']+[str(i.nome) for i in self.lista_vilas]

        dic = {i:[] for i in chaves}
        for i in range(len(chaves)):
            l = []
            for j in range(len(mapa)):
                l.append(mapa[j][i])
            dic[chaves[i]].extend(l)

        return dic




    def GerarMapa_de_lista(self, lista):
        mapa = []
        for i in lista:
            estrelas_02 = []
            for j in self.lista_vilas:
                # print(i.nome)
                j.recebe_ataque([i])
                estrelas_02.append(j.estrelas_l)
            mapa.append([i.nome] + estrelas_02)

        gm = pd.DataFrame(
            mapa, columns=['Jogador']+[str(i.nome) for i in self.lista_vilas])
        # gm.to_clipboard()
        # self.mada_de_lista = gm
        return gm

    def GerarMapaInicial(self):    
        if self.metodo in [3, 4] and self.lista_vilas != None:
            plan = self.GerarMapaDeEstrelas()
            # plan.index = plan['Jogador']
            self.mapa = plan
            for j in self.lista_vilas:
                j.mapa = self.mapa
                j.metodo = self.metodo
            print('mapa gerado!')
            # print( self.mapa)
        else:
            self.mapa = None

            # print( self.mapa)

    def Rodar(self,
              ciclos=5000000,
              # lista com poucos ataques de 0 estrela:
              pocucas_0_estrelas=False,
              # lista com poucos ataques de 1 estrela:
              poucas_1_estrelas=False,
              # lista com poucos ataques de 2 estrela:
              poucas_2_estrelas=False,
              poucas_3_estrelas=True,  # lista com poucos ataques de 3 estrela:
              inverter=False,
              ):
        self.rodou = True

        def SinalOp(qtd, sinal='maior'):
            if inverter == False:
                if sinal == 'maior':
                    return self.seq[1].count(qtd) > r1[1].count(qtd)
                elif sinal == 'menor':
                    return self.seq[1].count(qtd) < r1[1].count(qtd)
                elif sinal == 'igual':
                    return self.seq[1].count(qtd) == r1[1].count(qtd)
            else:
                if sinal == 'maior':
                    return self.seq[1].count(qtd) < r1[1].count(qtd)
                elif sinal == 'menor':
                    return self.seq[1].count(qtd) > r1[1].count(qtd)
                elif sinal == 'igual':
                    return self.seq[1].count(qtd) == r1[1].count(qtd)

        def ResultTemp():
            print(f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - {self.seq[1].count(3)} (3 stars) - {self.seq[1].count(2)} (2 stars) - {self.seq[1].count(1)} (1 stars) - {self.seq[1].count(0)} (0 stars)')

        ordenacao = 0
        self.parar = False
        ti = time.time()
        tempo = 15
        duracao = 0
# ['Geral', 'Outras contas', 'Minhas contas']
        if self.metodo == 4:
            if self.fase == 'Geral':
                self.Resultado_metodo_4()
                # self.GerarMapaInicial()
            elif self.fase == 'Outras contas':
                self.Resultado_outras_contas()
            elif self.fase == 'Minhas contas':
                self.Resultado_vilas_q_sobraram()

        elif self.metodo in [1, 2, 3]:
            
            for w in range(ciclos):
                if self.parar:
                    print('Parada')
                    break
                r1 = self.gera_jogadores_e_estrelas_de_lista_de_jogadores_embralhada()
                sr = sum(r1[1])
                ss = sum(self.seq[1])
                if sr > ss:
                    self.seq = r1[:]
                    print(
                        f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - soma maior')
                    self.pl += 1

                elif sr == ss:
                    if poucas_3_estrelas:  # para o caso de querer uma lista final com menos ataques de 3 estrela
                        if SinalOp(3, sinal='maior'):
                            self.seq = r1[:]
                            print(' 3')

                            ResultTemp()
                            self.pl += 1

                        elif SinalOp(3, sinal='igual') and SinalOp(0, sinal='maior'):
                            self.seq = r1[:]
                            print('3 e 0')

                            ResultTemp()
                            self.pl += 1

                    if poucas_2_estrelas:  # para o caso de querer uma lista final com menos ataques de 0 estrela
                        if SinalOp(2, sinal='maior'):
                            self.seq = r1[:]
                            print('2')

                            ResultTemp()
                            self.pl += 1

                    if poucas_1_estrelas:  # para o caso de querer uma lista final com menos ataques de 1 estrela
                        if SinalOp(1, sinal='maior'):
                            self.seq = r1[:]
                            print('1')

                            ResultTemp()
                            self.pl += 1

                    if pocucas_0_estrelas:  # para o caso de querer uma lista final com menos ataques de 0 estrela
                        if SinalOp(0, sinal='maior'):
                            self.seq = r1[:]
                            print(' 0')

                            ResultTemp()
                            self.pl += 1
                        elif SinalOp(0, sinal='igual') and SinalOp(2, sinal='maior'):
                            self.seq = r1[:]
                            print(' 0 e 2')
                            ResultTemp()
                            self.pl += 1


                if self.pl >= 10:
                    # self.LimparTela()
                    self.pl = 0

                tf = time.time()
                delta_t = round(tf-ti, 1)
                if delta_t >= tempo:
                    duracao += tempo
                    duracao = round(duracao, 1)
                    print(
                        f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - time = {duracao}s')
                    ti = time.time()
                    tf = time.time()

    def Resultado(self):
        self.estrelas = self.seq[1]

        self.DefinirAtacantesEEstrelas()

        def OrdenarListadeClasses(lista, atributo, decrecente=False):
            return sorted(lista, key=attrgetter(atributo), reverse=decrecente)

        vilas_ordenadas = OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=True)

        listaj = self.lista_jogadores[:]
        for j, vila in enumerate(vilas_ordenadas):
            if vila.estrela == 3:
                listaj = OrdenarListadeClasses(
                    listaj, 'forca', decrecente=True)
                # print(listaj)
                for n, k in enumerate(listaj):
                    jogador = k
                    vila.recebe_ataque([jogador])
                    if vila.estrelas_l == vila.estrela:
                        vila.atacante = jogador.nome
                        del listaj[n]
                        break
                    # print(f'vila{vila.nome} << {vila.atacante}')

            else:
                listaj = OrdenarListadeClasses(listaj, 'forca', )
                for n, k in enumerate(listaj):
                    jogador = k
                    # print(k.nome)
                    vila.recebe_ataque([jogador])
                    if vila.estrelas_l == vila.estrela:
                        vila.atacante = jogador.nome
                        del listaj[n]
                        break
                    # print(f'vila{vila.nome} << {vila.atacante}')

        result = []
        for j, i in enumerate(self.lista_vilas):
            i.nome = int(i.nome)
            result.append([i.atacante, i.nome, i.estrela])
        newplan = pd.DataFrame(result, columns=['Jogador', 'Alvos', 'Estrelas']).sort_values(
            by=['Alvos'], ascending=True)
        total_de_estrelas = sum(self.estrelas)
        tt = pd.DataFrame({'Jogador': ['Total'], 'Alvos': [
            '  '], 'Estrelas': total_de_estrelas})
        fra = [newplan, tt]
        resu = pd.concat(fra).reset_index(drop=True)
        # resu.to_clipboard()
        self.df = resu
        return resu




    def Resultado2(self):
        if self.rodou:
            self.estrelas = self.seq[1]
            self.DefinirAtacantesEEstrelas()

            def ExibirAtributo(lista, atributo):
                for i in lista:
                    print(i.atributo)

            def OrdenarListadeClasses(lista, atributo, decrecente=False):
                return sorted(lista, key=attrgetter(atributo), reverse=decrecente)

            vilas_ordenadas = OrdenarListadeClasses(
                self.lista_vilas, 'forca', decrecente=True)

            listaj = self.lista_jogadores[:]
            listaj = OrdenarListadeClasses(listaj, 'forca', decrecente=True)

            # for i in vilas_ordenadas:
            #     i.atacante = ''
            def OrdenaJogadoresEstrelas(qtd_estrelas, listaj):
                Nnum_vila_velha = None  # nome da vila que estava sendo atacada pelo jogador anterior
                atacantes_3 = []
                for j, vila in enumerate(vilas_ordenadas):
                    if vila.estrela == qtd_estrelas:
                        # print(listaj)
                        atacante_anterior = vila.atacante
                        # encontra o antacante anterior
                        for i in listaj:
                            if atacante_anterior == i.nome:
                                atacante_anterior = i
                                break

                        for n, k in enumerate(listaj):
                            novo_atacante = k
                            vila.recebe_ataque([novo_atacante])
                            if vila.estrelas_l == vila.estrela:
                                # encontra a vila que estava sendo atacada pelo jogador anterior
                                for m, i in enumerate(vilas_ordenadas):
                                    if i.atacante == novo_atacante.nome:
                                        Nnum_vila_velha = m
                                        break

                                # testa se o anatacante anterior consegue a mesma quantidade de estrlas que o novo jogador conseguia naquela vila
                                vilas_ordenadas[m].recebe_ataque(
                                    [atacante_anterior])
                                if vilas_ordenadas[m].estrelas_l == vilas_ordenadas[m].estrela:
                                    vilas_ordenadas[m].atacante = atacante_anterior.nome
                                    vila.atacante = novo_atacante.nome
                                    atacantes_3.append(novo_atacante)
                                    del listaj[n]
                                    break

                return atacantes_3

            def ReordenaJogadores(qtd_estrelas, atacantes_3):
                for j, vila in enumerate(vilas_ordenadas):
                    if vila.estrela == qtd_estrelas:
                        # print(listaj)
                        atacante_anterior = vila.atacante
                        # print(vila.nome, atacante_anterior)
                        # encontra o antacante anterior
                        for i in atacantes_3:
                            if atacante_anterior == i.nome:
                                atacante_anterior = i
                                # print(atacante_anterior.nome)
                                break

                        for n, k in enumerate(atacantes_3):
                            novo_atacante = k
                            vila.recebe_ataque([novo_atacante])
                            if vila.estrelas_l == vila.estrela:
                                # encontra a vila que estava sendo atacada pelo jogador anterior
                                for m, i in enumerate(vilas_ordenadas):
                                    if i.atacante == novo_atacante.nome:
                                        Nnum_vila_velha = m
                                        break

                                # testa se o anatacante anterior consegue a mesma quantidade de estrlas que o novo jogador conseguia naquela vila
                                vilas_ordenadas[m].recebe_ataque(
                                    [atacante_anterior])
                                if vilas_ordenadas[m].estrelas_l == vilas_ordenadas[m].estrela:
                                    vilas_ordenadas[m].atacante = atacante_anterior.nome
                                    vila.atacante = novo_atacante.nome
                                    del atacantes_3[n]
                                    break

            atacantes_3 = OrdenaJogadoresEstrelas(qtd_estrelas=3, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=3, atacantes_3=atacantes_3)

            atacantes_2 = OrdenaJogadoresEstrelas(qtd_estrelas=2, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=2, atacantes_3=atacantes_2)

            atacantes_1 = OrdenaJogadoresEstrelas(qtd_estrelas=1, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=1, atacantes_3=atacantes_1)

            atacantes_0 = OrdenaJogadoresEstrelas(qtd_estrelas=0, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=0, atacantes_3=atacantes_0)

            result = []
            for j, i in enumerate(self.lista_vilas):
                i.nome = int(i.nome)
                result.append([i.atacante, i.nome, i.estrela, i.nivel_cv])





            chaves=['Jogador', 'Alvos', 'Estrelas', 'CV']
            dic = self.ConverterListadeListaParadiciomarioColunas(result, chaves)
            newplan = self.OrdenarDicionario(dic, 'Alvos')

            
            # newplan = pd.DataFrame(result, columns=['Jogador', 'Alvos', 'Estrelas', 'CV']).sort_values(
            #     by=['Alvos'], ascending=True)
            
            total_de_estrelas = sum(self.estrelas)

            newplan['Jogador'].append('Total')
            newplan['Alvos'].append('  ')
            newplan['Estrelas'].append(total_de_estrelas)
            newplan['CV'].append('')

            # tt = pd.DataFrame({'Jogador': ['Total'], 'Alvos': [
            #     '  '], 'Estrelas': total_de_estrelas,'CV':['']})
            # fra = [newplan, tt]
            # resu = pd.concat(fra).reset_index(drop=True)
            # resu.to_clipboard()
            self.dic = newplan
        else:
            print('Você ainda não rodou o programa (Rodar)')

    def ResultadoEspelho(self):
        if len(self.lista_jogadores) == len(self.lista_vilas):
            mapa = self.GerarMapaDeEstrelas()
            # mapa.index = mapa['Jogador']
            # print(mapa)
            estrelas = []
            alvos = []
            jogadores = []
            cv = []
            for i, j in enumerate(self.lista_vilas):
                jogadores.append(self.lista_jogadores[i].nome)
                cv.append(j.nivel_cv)
                alvos.append(int(j.nome))
                try:
                    index = mapa['Jogador'].index(str(self.lista_jogadores[i].nome))
                    estrelas.append(
                        # if vilas[str(i.nome)][index] == estrelas                        
                        # mapa.loc[str(self.lista_jogadores[i].nome), str(j.nome)]
                        
                        mapa[str(j.nome)][index]
                        )
                except:
                    index = mapa['Jogador'].index(str(self.lista_jogadores[i].nome))
                    estrelas.append(
                        mapa[str(j.nome)+'.0'][index]
                        # mapa.loc[str(self.lista_jogadores[i].nome), str(j.nome)+'.0']
                        )

            dic = {'Jogador': jogadores+['Total'],	'Alvos': alvos +
                [' '],	'Estrelas': estrelas+[sum(estrelas)], 'CV':cv+['']}

            # df_espelho = pd.DataFrame(dic)
            # df_espelho.to_clipboard()
            # print(df_espelho)
            self.dic = dic
        else:
            print(f'O número de jogadores ({len(self.lista_jogadores)}) deve ser igaula ao número de vilas ({len(self.lista_vilas)})')            

    def DefinirAtacantesEEstrelas(self):
        # alvos = [i.nome for i in self.lista_vilas]
        if len(self.seq[0]) >1:
            nomes_dos_jogadores = self.seq[0]
            estrelas = self.seq[1]
            # newplan = pd.DataFrame(
            # {'Jogador': nomes_dos_jogadores, 'Alvos': alvos, 'Estrelas': estrelas}).sort_values(by = ['Alvos'], ascending=True)
            # rl = newplan.values.tolist()
            # for i in rl:
            #     for j in g2.lista_vilas:
            #         if j.nome == i[1]:
            #             j.atacante == i[0]

            for j, i in enumerate(self.lista_vilas):
                i.atacante = nomes_dos_jogadores[j].nome
                # print(nomes_dos_jogadores[j].nome)
                i.estrela = estrelas[j]
        else:
            print('Você ainda não rodou o programa')


    # def SalvarDadosLocais(self, nome, valor):
    #     self.page.client_storage.set(nome, valor)
        

    # def LerDadosLocais(self, nome,  default=None):
    #     if self.page.client_storage.contains_key(nome):
    #         return self.page.client_storage.get(nome)
    #     else:
    #         return default


    def Escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def Ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.Escrever_json(default, filename)
            except:
                pass
            return default or {}
       
class LayoutGuerra(ft.Column):
    def __init__(self, page, vilas = None, equipe = None, jogadores = None):
        super().__init__()
        self.vilas = vilas
        self.equipe = equipe
        self.jogadores = jogadores
        self.page = page
        self.num_estrelas = False, False, False, True
        self.atualizou = False
        self.alignment=ft.MainAxisAlignment.START
        self.horizontal_alignment = 'center'
        self.g2 = None
        self.api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw 6Z2FtZWFwaSIsImp0aSI6ImYxMjM0OWViLTdjZTMtNGJlZi05N2YwLWVjNjJiZjcwODBiMSIsImlhdCI6MTcwMjY0NTA0Niwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYtNzM2Yy03YzIxL TE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3Ny4z OS41OS4zNyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.21xPvBHTivFI4Artdjns0l780mxVs5KPffY09j_LSEQ46eW1IEZDie1FdhQzHozMFOJLidqL6AsQsgjg_Zc3PA'
        self.link_clan = 'https://api.clashofclans.com/v1/clans/%23299GCJ8U'
        self.link_player = 'https://api.clashofclans.com/v1/players/%23'
        self.fase = 'Geral'
        self.n_ciclos = ft.TextField(value = 500000, dense = True, expand=True, label = 'Num cilcos', content_padding=7, border_width=0.5, col = 6)
        # self.config_equipes = Verificar_pasta('Guerra_clash').caminho('config_guerra.json')        
        # self.scroll  = ft.ScrollMode.ADAPTIVE
        self.height = self.page.window.height-100
        # self.width = self.page.window.width


                    
        def copiar_areaT(e):
            self.g2.df.to_clipboard()
            print('tabela copiada com sucesso!')


       

        self.inverter =  ft.Checkbox(label="Inverter", value=False, scale=0.8, col = 6, expand=True) 
        self.metodo = My_Dropdown('Método',None, 1,2,3,4)

        self.metodo.value = 4
        self.metodo.width = 70
        self.metodo.col = 6
        def Colu(x = 4):
            return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}        

        rodar = BotaoCT('Rodar', self.Rodar,bgcolor=ft.colors.GREEN_900,text_size=12, col = Colu(1))
        parar =BotaoCT('parar', on_click = self.Parar, bgcolor=ft.colors.BLUE_900,text_size=12, col = Colu(0.75))
        gerar_mapa =BotaoCT('mapa',on_click = self.Gerar_mapa, bgcolor=ft.colors.BLUE_800,text_size=12, col = Colu(0.75))
        resultado2 =BotaoCT('resultado2',on_click = self.Resultado2, bgcolor=ft.colors.BLUE_900,text_size=12, col = Colu(1.5))
        resultado_espelho = BotaoCT('espelho',on_click = self.Resultado_espelho,bgcolor=ft.colors.BLUE_800,text_size=12, col = Colu(1))
        botao_atualizar = BotaoCT('Atualizar', on_click=self.AtualizarDados,bgcolor=ft.colors.BLUE_700,text_size=12,  col = Colu(1))

        copiar = ft.IconButton(icon = ft.icons.COPY, tooltip = 'copiar tabela para área de transferência', on_click= copiar_areaT)
        
        self.saida = ft.Text('')
        
        dic = {'Jogador':list(range(15)), 'Vila':list(range(15)), 'Estrelas': list(range(15))}

        self.tabela = My_tabelaC(dic, larguras={'Jogador':100, 'Vilas':35, 'Estrelas': 60, 'CV':40})
        self.tabela.larguras = ('Jogador',100)

        self.controls = [
            ft.ResponsiveRow([rodar,parar, gerar_mapa, resultado2,resultado_espelho,], 

                expand=False, spacing=0, run_spacing=0, alignment='start', columns=5),
            ft.Row([ft.Column([self.tabela],scroll=ft.ScrollMode.ADAPTIVE,height = self.height-60,horizontal_alignment='center')],
                    scroll=ft.ScrollMode.ADAPTIVE,

                    )
        ]
        self.alignment = 'start'
    

    async def AtualizarDados(self,e):

        arquiv_equipes = await self.page.client_storage.get_async('equipes')
        if isinstance(arquiv_equipes, dict):
            equipe = arquiv_equipes["equipe A"]

        arquiv_vilas = await self.page.client_storage.get_async('vilas')
        if isinstance(arquiv_vilas, dict):
            lista_vilas = []
            for nome, nivel_cv, cv_exposto in zip(arquiv_vilas['nome'], arquiv_vilas['nivel_cv'], arquiv_vilas['cv_exposto']):
                lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, equipe=equipe, func=None,forca=(50 - nome) + 50 *nivel_cv))

        # arquiv_lista = await self.page.client_storage.get_async('lista')

        lista_jogadores = []
        arquiv_jogadores = await self.page.client_storage.get_async('jogadores')
        for i,j,k in zip(arquiv_jogadores['nome'],arquiv_jogadores['nivel_cv'],arquiv_jogadores['forca']):
            lista_jogadores.append(Jogador(nome = i,nivel_cv = j,forca = k))


        self.lista_vilas = lista_vilas
        self.listajogadores = lista_jogadores
        self.equipe = equipe
        # await self.equipe.CarregarEquipes(1)
        # equipe = self.equipe.arquiv["equipe A"]

        # await self.jogadores.Atualizar(1)
        # self.listajogadores = self.jogadores.lista_jogadores
        
        # await self.vilas.Gera_Lista_de_Vilas(equipe)
        # self.lista_vilas = self.vilas.lista_vilas



    async def AtualizarVilas(self,e):
        arquiv = await self.page.client_storage.get_async('vilas')
        dic = {'Vila':[], 'CV':[], 'cv_exposto': []}
        self.lista_vilas = []
        equipe = {
                   "Nome da Equipe": "equipe A",
                    "GRUPO MASTER": "1930",
                    "GRUPO ELITE": "1825",
                    "GRUPO A": "1794",
                    "GRUPO B": "1585",
                    "GRUPO C": "1444",
                    "GRUPO D": "1440",
                    "GRUPO E": "1430"
                }
      
        for nome, nivel_cv, cv_exposto in zip(arquiv['nome'], arquiv['nivel_cv'], arquiv['cv_exposto']):
                dic['Vila'].append(nome)
                dic['CV'].append(nivel_cv)
                dic['cv_exposto'].append(cv_exposto)
                self.lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=None, equipe=equipe,forca = (50 - nome) + 50 *nivel_cv,)) #forca = (50 - nome) + 50 *nivel_cv,

       

        self.tabela.dic = dic
        self.tabela.larguras = ('Vila',60)
        self.tabela.larguras = ('CV',40)
        self.tabela.larguras = ('cv_exposto',80)
        self.tabela.visible = True
        self.atualizou = True
        await self.update_async()

    def Config(self):
        def Valor(e):
            match e.data:
                case 'poucas_0_estrelas':
                    self.num_estrelas =  True, False, False, False                
                case  'poucas_1_estrelas':
                    self.num_estrelas =  False, True, False, False                  
                case 'poucas_2_estrelas':
                    self.num_estrelas =  False, False, True, False                  
                case  'poucas_3_estrelas':
                    self.num_estrelas =  False, False, False, True   
                   
        estrelas = My_Dropdown('estrelas',Valor,'poucas_0_estrelas', 'poucas_1_estrelas', 'poucas_2_estrelas', 'poucas_3_estrelas')
        estrelas.value = 'poucas_3_estrelas'    
        estrelas.col = 6  
        return ft.Column([
                ft.ResponsiveRow([estrelas, self.metodo,], width=self.width, spacing=0, run_spacing=0),
                ft.ResponsiveRow([self.inverter, self.n_ciclos, ], width=self.width, spacing=0, run_spacing=0),
        ])        


    async def Rodar1(self,e):
        self.atualizou = True
        if self.atualizou:
            # equipe = {
            #         "Nome da Equipe": "equipe A",
            #             "GRUPO MASTER": "1930",
            #             "GRUPO ELITE": "1825",
            #             "GRUPO A": "1794",
            #             "GRUPO B": "1585",
            #             "GRUPO C": "1444",
            #             "GRUPO D": "1440",
            #             "GRUPO E": "1430"
            #         }          
            # self.equipe.CarregarEquipes(1)
            # equipe = self.equipe.arquiv["equipe A"]
            # self.jogadores.Atualizar(1)
            # self.listajogadores = self.jogadores.lista_jogadores
            # self.vilas.Gera_Lista_de_Vilas(equipe)
            # self.lista_vilas = self.vilas.lista_vilas
            await self.AtualizarDados(1)

            pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas = self.num_estrelas
            # print(pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas)
            inverter = self.inverter.value
            metodo = int(self.metodo.value)
            # print(metodo)

            print('iniciando ...')
            # if not self.lista_vilas:
            self.g2 = Guerra2(metodo=metodo,  fase=self.fase,
                        arq_configuracoes='equipes', page = self.page,
                        listavilas=self.lista_vilas,
                        listajogadores=self.listajogadores,
                        equipe=self.equipe,
                        )
            if self.g2.rodou:
                # t1.join()
                self.g2.rodou = False
            # t1 = threading.Thread(target=self.g2.Rodar, args=(self.n_ciclos, pocucas_0_estrelas,
            #                                             poucas_1_estrelas, poucas_2_estrelas, poucas_3_estrelas, inverter), daemon=True)
            # t1.start()
            
            self.g2.Rodar(int(self.n_ciclos.value), pocucas_0_estrelas,poucas_1_estrelas, poucas_2_estrelas, poucas_3_estrelas, inverter)

            time.sleep(1)
            if metodo == 4:
                # t1.join()
                # time.sleep(10)
                dic = self.g2.dic
                # print(df)
                # print(dic)
                self.tabela.visible = True
                self.tabela.dic = dic# = My_tabela(df)
                self.tabela.larguras= ('Jogador',100)
                # self.tabela.df = self.g2.df
                await  self.update_async()
                # self.RedimensionarJanela(400)
            # print(self.g2.df)
            elif metodo == 2:
                await  self.Resultado2(1)
            self.atualizou = False
        else:
            self.tabela.dic = {'clique em atualizar     ':''}
            self.tabela.larguras= ('clique em atualizar     ',200)
            self.tabela.visible = True
            await  self.update_async()

          

    async def Rodar(self,e):
        self.atualizou = True
        if self.atualizou:
            equipe = {
                    "Nome da Equipe": "equipe A",
                        "GRUPO MASTER": "1930",
                        "GRUPO ELITE": "1825",
                        "GRUPO A": "1794",
                        "GRUPO B": "1585",
                        "GRUPO C": "1444",
                        "GRUPO D": "1440",
                        "GRUPO E": "1430"
                    }          
            self.equipe.CarregarEquipes(1)
            equipe = self.equipe.arquiv["equipe A"]
            self.jogadores.Atualizar(1)
            self.listajogadores = self.jogadores.lista_jogadores
            self.vilas.Gera_Lista_de_Vilas(equipe)
            self.lista_vilas = self.vilas.lista_vilas
            pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas = self.num_estrelas
            # print(pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas)
            inverter = self.inverter.value
            metodo = int(self.metodo.value)
            # print(metodo)

            print('iniciando ...')
            # if not self.lista_vilas:
            self.g2 = Guerra2(metodo=metodo,  fase=self.fase,
                        arq_configuracoes='equipes', page = self.page,
                        listavilas=self.lista_vilas,
                        listajogadores=self.listajogadores,
                        equipe=self.equipe,
                        )
            if self.g2.rodou:
                # t1.join()
                self.g2.rodou = False
            # t1 = threading.Thread(target=self.g2.Rodar, args=(self.n_ciclos, pocucas_0_estrelas,
            #                                             poucas_1_estrelas, poucas_2_estrelas, poucas_3_estrelas, inverter), daemon=True)
            # t1.start()
            
            self.g2.Rodar(int(self.n_ciclos.value), pocucas_0_estrelas,poucas_1_estrelas, poucas_2_estrelas, poucas_3_estrelas, inverter)

            time.sleep(1)
            if metodo == 4:
                # t1.join()
                # time.sleep(10)
                dic = self.g2.dic
                # print(df)
                # print(dic)
                self.tabela.visible = True
                self.tabela.dic = dic# = My_tabela(df)
                self.tabela.larguras= ('Jogador',100)
                # self.tabela.df = self.g2.df
                await self.update_async()
                # self.RedimensionarJanela(400)
            # print(self.g2.df)
            elif metodo == 2:
                await self.Resultado2(1)
            self.atualizou = False
        else:
            self.tabela.dic = {'clique em atualizar     ':''}
            self.tabela.larguras= ('clique em atualizar     ',200)
            self.tabela.visible = True
            await self.update_async()
                        


 
    async def Parar(self,e):
        try:
            if self.g2 != None:
                self.g2.parar = True
        except:
            pass

    def resultado(self,e):
        def pp():
            self.g2.Resultado()
            self.tabela.dic = self.g2.dic
            self.RedimensionarJanela(400)
            self.update()

        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value, page = self.page)
        # threading.Thread(target=pp, daemon=True).start()
        pp()

    async def Resultado2(self,e):
        def pp():
            if self.g2.rodou:
                self.g2.Resultado2()
                self.tabela.visible = True
                self.tabela.dic = self.g2.dic
                self.tabela.larguras= ('Jogador',100)

                # self.RedimensionarJanela(410)
                self.Atualizar()
            else:
                print('Você ainda não rodou o programa, usando metódo 2')

        await self.AtualizarDados(1)

        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value, page = self.page,
                        listavilas=self.lista_vilas,
                        listajogadores=self.listajogadores,
                        equipe=self.equipe,                              
                              )
        # threading.Thread(target=pp, daemon=True).start()
        pp()


    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    async def Atualizar_async(self):
        try:
            await self.update_async()
        except:
            pass    

    async def Resultado_espelho(self,e):
        def pp():
            self.g2.ResultadoEspelho()
            self.tabela.visible = True
            self.tabela.dic = self.g2.dic
            self.tabela.larguras= ('Jogador',100)

            # self.RedimensionarJanela(400)
            self.Atualizar()
        await self.AtualizarDados(1)

        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value, page = self.page,
                            listavilas=self.lista_vilas,
                        listajogadores=self.listajogadores,
                        equipe=self.equipe,
                              )

        # threading.Thread(target=pp, daemon=True).start()
        pp()


    async def Gerar_mapa(self,e):


        def pp():
            self.tabela.visible = True
            dic = self.g2.GerarMapaDeEstrelas()
            self.tabela.dic = dic
            self.tabela.larguras= (list(dic.keys())[0],80)

            for i in list(dic.keys())[1:]:
                self.tabela.larguras= (i,20)

            # self.RedimensionarJanela(700)
            self.Atualizar()
        # if self.g2 == None:
        # self.equipe.CarregarEquipes(1)
        # equipe = self.equipe.arquiv["equipe A"]
        # self.jogadores.Atualizar(1)
        # self.listajogadores = self.jogadores.lista_jogadores
        # self.vilas.Gera_Lista_de_Vilas(equipe)
        # self.lista_vilas = self.vilas.lista_vilas 
        await self.AtualizarDados(1)

        self.g2 = Guerra2(metodo=self.metodo.value, page = self.page,
                        listavilas=self.lista_vilas,
                        listajogadores=self.listajogadores,
                        equipe=self.equipe,                          
                          )
        # threading.Thread(target=pp, daemon=True).start()
        pp()
        
        

    def RedimensionarJanela(self, valor):       
        tamanho = 30*(len(self.g2.lista_jogadores)-4)+valor
        self.page.window.width = tamanho
        self.page.update()
        self.update()


class ConfirmarSaida:
    def __init__(self,page, funcao = None):
        super().__init__()
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

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self,page):
        self.page = page
        self.page.on_resized = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        self.page.overlay.append(self.pw)   

    def page_resize(self, e):
        self.pw.value = f"{self.page.window.width}*{self.page.window.height} px"
        self.pw.update()
  
class Saida(ft.Column):
    def __init__(self):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=150,  ),bgcolor='white,0.03' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.page.update()

class Tabe(ft.Tabs):
    def __init__(self,  funcao = None, *controls):
        super().__init__()
        self.selected_index=0
        self.animation_duration=3
        self.expand=1
        self.controls = list(controls)
        self.funcao = funcao
        self.on_change = self.func
        if isinstance(self.controls, list) and len(self.controls) >0:
            for i in self.controls: 
                if len(i) == 2:                
                    self.tabs.append(ft.Tab(icon=i[0],content=i[1] ))
                else:
                    self.tabs.append(ft.Tab(text=i[0],content=i[1] ))


    def Add(self, icone, janela):
        self.tabs.append(ft.Tab(icon=icone,content=janela ))
        try:
            self.update()
        except:
             pass

    def func(self,e):
        if self.funcao != None:
            self.funcao(e)
        # pass

    
class My_tabelaC(ft.Container):
    def __init__(self, dic,# dicionário
                 larguras = None, #dict
                 largura_default = 60
                    ):
        super().__init__()
        # self.spacing = 5
        # self.run_spacing = 5
        self._dic = dic 
        self.visible = False 
        self.largura_default = largura_default
        self._larguras = larguras
        if self._larguras is None:
            self._larguras = {}

        self.Iniciar()     
        self.Linhas()
        self.border=ft.border.all(1,'white,0.5')

    def Larg(self,coluna):
        if not self._larguras is None:
            return  self._larguras.get(coluna,self.largura_default)
        else:
            return self.largura_default

    def Iniciar(self):
        self.chaves = list(self._dic.keys())
        # if self._larguras is None:
        #     self._larguras = {i:60 for i in self.chaves}
        self.opcoes = self._dic[self.chaves[0]]


    def Colunas(self):
        self.controls = [ft.Container(ft.Row([ft.Text(self.chaves[0], width=self.Larg(self.chaves[0]), text_align='end', weight='BOLD')]+
                        [ft.Text(i, width=self.Larg(i), text_align='center', weight='BOLD') for i in self.chaves[1:]], tight=True),bgcolor='white,0.3')]

            
        
    def Linhas(self):
        self.Colunas()
        for i, k in enumerate(self._dic[self.chaves[0]]):     
            cor  = 'black' if i%2 == 0 else  'white,0.05'  
            self.controls.append(
                ft.Container(ft.Row([
                                Display(value = self._dic[self.chaves[0]][i],opitions=self.opcoes, width=self.Larg(self.chaves[0]),height=20,text_size = 12, 
                                        borda_width = 0,border_radius = 0, 
                                                text_align= ft.TextAlign.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END, bgcolor = 'white,0')
                ]+[ft.Text(self._dic[j][i],width=self.Larg(j), text_align='center') for j in self.chaves[1:]], tight=True),bgcolor=cor)
                
                )
        self.content = ft.Column(self.controls,spacing=2)
        
            
    def Atualizar(self):
        try:
            self.update()
        except:
            pass


    @property
    def dic(self):
        return self._dic
    
    @dic.setter
    def dic(self, dic):
        if isinstance(dic, dict):
            self._dic = dic
            # self._larguras = None
            self.Iniciar()
            self.Linhas()
        self.Atualizar()

    @property
    def larguras(self):
        return self._larguras
    
    @larguras.setter
    def larguras(self,  valor = ('chave','valor')):        
        if valor[0] in self.chaves and isinstance(valor[1], int):
            # self.Iniciar()
            self._larguras[valor[0]] = valor[1]
            # print('aceitou')
        else:
            print('chave ou valor inválido')
        self.Linhas()
        self.Atualizar()


class ClassName(ft.Column):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.vilas = LayoutVilas(printt=print,page = self.page)
        self.jogadores = layout_jogadores(printt=print, page=self.page)
        self.equipes = layout_equipes(page = page)
        self.layout = LayoutGuerra(page = self.page, vilas=self.vilas, equipe=self.equipes, jogadores=self.jogadores) 
        self.importar = layout_Importar(printt=print, page = self.page)
        self.config = ft.Column([ self.layout.Config(),self.importar.Configs() ]) #,                                          
        self.janela = ft.Container()
        self.janela.content = self.layout
        self.spacing = 1
        self.run_spacing = 1



        def Colu(x = 4):
            return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}
        co2 = {"xs":2,"sm": 1, "md": 1, "lg": 1, "xl": 1,"xxl": 1}
        self.menu = ft.Container(
            
            content = ft.ResponsiveRow([
                BotaoCT('Lista de Guerra',self.Escolher_janela,  text_size = 11, col = co2),
                BotaoCT('Vilas',self.Escolher_janela, col = co2),
                BotaoCT('Jogadores',self.Escolher_janela, col = co2),
                BotaoCT('Equipes',self.Escolher_janela, col = co2),
                BotaoCT('Importar',self.Escolher_janela, col = co2),
                BotaoCT('config',self.Escolher_janela, col = co2),
                ],spacing=0, run_spacing=0,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,columns=6), 
                    
            # padding=2,
            bgcolor=ft.colors.BROWN_500,
            border_radius=0,
            # width=page.window.width+20
        )

        self.controls = [self.menu,self.janela]



    def Escolher_janela(self, e):
        match e.control.content.value:
            case 'Lista de Guerra':
                # janela.content = ft.Row([layout], scroll=ft.ScrollMode.ALWAYS, width=page.window.width-10)
                self.janela.content = self.layout
            case 'Vilas':
                
                self.janela.content =  ft.Column([self.vilas], scroll=ft.ScrollMode.ALWAYS, height=self.page.window.height-10)
            case 'Jogadores':
                self.janela.content =  ft.Column([self.jogadores], scroll=ft.ScrollMode.ALWAYS, height=self.page.window.height-10)
            case 'Lista de Guerra':
                self.janela.content =  ft.Column([self.layout], scroll=ft.ScrollMode.ALWAYS, height=self.page.window.height-10)
            case 'Equipes':
                self.janela.content =  ft.Column([self.equipes], scroll=ft.ScrollMode.ALWAYS, height=self.page.window.height-100)
            case 'Importar':
                self.janela.content =    ft.Column([self.importar], scroll=ft.ScrollMode.ALWAYS, height=self.page.window.height-10) 
            case 'config':
                self.janela.content = self.config                                                                                               

        self.page.update()

    def Func(self,e):
        match e.data:
            case '4':
                self.page.window.width = 630
                self.page.window.height = 970
                self.page.update()             
            case '3':
                self.page.window.width = 700
                self.page.update() 
            case '2':
                self.page.window.width = 500
                self.page.update()  
            case '1':
                self.page.window.width = 510
                self.page.update()  
            case '0':
                self.page.window.width = 810
        self.page.update() 


def main(page: ft.Page):
    page.title = "Guerra de Clans - 015"
    page.window.width = 330  # Define a largura da janela como 800 pixels
    page.window.height = 600  #    
    # page.vertical_alignment = ft.MainAxisAlignment.START  
    # page.theme = ft.ThemeMode.DARK
    page.theme_mode = ft.ThemeMode.DARK
    page.spacing = 3
    page.expand = True
    page.vertical_alignment = 'start'
    page.theme = ft.Theme(visual_density = "comfortable")


    # ConfirmarSaida(page)
    # Resize(page) 
    #   
    # def resizer(e):
    #     page.clean()
    #     layout = LayoutGuerra(page = page) 
    #     janela = ft.Container()
    #     janela.content = layout
    #     menu = ft.Container(
    #         content = ft.ResponsiveRow([
    #             ft.Container(
    #                 content = ft.Column([
    #                     BotaoCT('Lista de Guerra',Escolher_janela,  text_size = 11),
    #                     BotaoCT('Vilas',Escolher_janela),
    #                 ],spacing=6, run_spacing=0,alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'),
    #                 border=ft.border.all(2,'white,0.4'),
    #                 height = 50,
    #                 col = Colu()
    #             ),

    #             ft.Container(
    #                 content = ft.Column([
    #                     BotaoCT('Jogadores',Escolher_janela),
    #                     BotaoCT('Equipes',Escolher_janela),
    #                 ],spacing=6, run_spacing=0,alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'),
    #                 border=ft.border.all(2,'white,0.4'),
    #                 height = 50,
    #                 col = Colu()
    #             ),

    #             ft.Container(
    #                 content = ft.Column([
    #                     BotaoCT('Importar',Escolher_janela),
    #                     BotaoCT('config',Escolher_janela),
    #                     ],spacing=6, run_spacing=0,alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'), 
    #                 border=ft.border.all(2,'white,0.4'),
    #                 height = 50,
    #                 col = Colu()
    #                 )
    #                 ],spacing=0, run_spacing=5),
                        
    #         # padding=2,
    #         bgcolor=ft.colors.BROWN_500,
    #         border_radius=0,
    #         width=page.window.width+20
    #     )


    #     page.add(menu,janela)
    #     menu.update()
    #     page.update()
    
    page.overlay.append(ft.Text('versão - 025',bottom=10, right=10, size=8 ))
    c = ClassName(page)

    page.add(c)

if __name__ == '__main__':  
   
    ft.app(main,
    #    view = ft.AppView.WEB_BROWSER
    # port = 8050
       )
