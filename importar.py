import json
import pickle
import flet as ft
import re
import webbrowser
import requests
from operator import attrgetter
import os
# from pandas import DataFrame


class Verificar_pasta:
    def __init__(self,pastalocal = 'Guerra_clash'):
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
    def __init__(self,height = 50):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=height,  ),bgcolor='white,0.03' ))
    def Atualizar(self):
        try:
            self.update()
        except:
            pass


    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.Atualizar()
class Players(ft.ResponsiveRow):
    def __init__(self, 
                 guerra = None,
                 jogador = None, 
                 tag = None,
                 nivel_cv = None, 
                 forca = None, 
                 atenuador = None,
                 forca_final = None,
                 func = None,
                #  page  = None            
                                  
                 ):
        super().__init__() 
        # self.page = page         
        self.func = func
        self._guerra = ft.Checkbox(value = guerra, data = 'guerra', on_change=self.Chenge_guerra, col = self.Colu(1))
        self._jogador = ft.Text(jogador,text_align='center',selectable = True,)
        self._tag = ft.Text(tag,text_align='center',selectable = True,  visible=False, col = self.Colu(1))
        self._nivel_cv = ft.Text(nivel_cv,text_align='center',selectable = True,  col = self.Colu(1))
        self._forca = ft.Text(forca,text_align='center',selectable = True,  visible=False, col = self.Colu(1))
        self._atenuador = ft.TextField(value = atenuador,   bgcolor= 'white,0.08',dense=True, 
                            data = 'atenuador',content_padding=5,  on_change=self.Chenge_atenuador, col = self.Colu(3))
        
        self._forca_final = ft.Text(forca,text_align='center',selectable = True, width=80, col = self.Colu(3))
        self._forca_final.value = forca
        try:
            self._forca_final.value -= int(atenuador)
        except:
            pass

        self.controls = [self._guerra,
                         ft.Container(self._jogador, bgcolor='white,0.1',  col = self.Colu(4), ),
                         self._tag,
                         self._nivel_cv,
                         self._forca,
                         self._atenuador,
                         self._forca_final

        ]


        # self.tight = True
        self.spacing = 0
        self.run_spacing = 0


    def Colu(self, x = 4):
        return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}

    @property
    def forca_final(self):
        return self._forca_final.value
    

    @property
    def jogador(self):
        return self._jogador.value



    @property
    def guerra(self):
        return self._guerra.value

    @property
    def jogador(self):
        return self._jogador.value

    @property
    def tag(self):
        return self._tag.value

    @property
    def nivel_cv(self):
        return self._nivel_cv.value

    @property
    def forca(self):
        return self._forca.value

    @property
    def atenuador(self):
        return self._atenuador.value   

    def Chenge_guerra(self, e):
        if self.func(e) != None:
            self.func(e)
            self.update()        

    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    def Chenge_atenuador(self, e):
        valor = self._atenuador.value
        forca = self._forca.value
        try:
            forca_final = int(forca) - int(valor)
            self._forca_final.value = forca_final
        except:
            try:
                self._forca_final.value = int(forca)
            except:
                pass   
        # self._forca_final.update()           
        self.Atualizar()
        if self.func(e) != None:
            self.func(e)




class BotaoCT(ft.Container):
    def __init__(self,nome,on_click = None, bgcolor = None, scale = 0.8, text_size = None, col = None, data =None ):
        super().__init__()
        self.on_click=on_click
        self.border_radius = 0
        self.bgcolor = bgcolor
        self.scale = scale
        self.data = data
        self.col = col
        self.text_size = text_size
        self.expand = True
        self.padding = ft.Padding(0,0,0,0)
        # self.border=ft.Border(right=ft.BorderSide(2,'white,0.4'))
        self.nome = nome
        # self.content = ft.Row([ft.VerticalDivider(color='blue', width=2), ft.Text(nome, weight='BOLD', text_align='center'),ft.VerticalDivider(color='blue', width=2),],alignment='center')
        self.content = ft.Text(nome, weight='BOLD', text_align='center', size = self.text_size )
                                                      


class layout_Importar(ft.Column):
    def __init__(self, printt = None, page = None):
        super().__init__()
        self.page = page
        # self.config_jogadores = Verificar_pasta('Guerra_clash').caminho('jogadores_config.json')
        self.config_tabela = Verificar_pasta('Guerra_clash').caminho('tabela.plk')

        self.link_clan = 'https://api.clashofclans.com/v1/clans/%23299GCJ8U'
        self.link_player = 'https://api.clashofclans.com/v1/players/%23'        
        self.Tokken = ft.TextField(label='Tokken', width=400,dense=True, content_padding=10, bgcolor='white,0.08',)
        self.Tokken.value ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjgwZTdmZTkzLTM5ZDAtNGFmYi1hZjA0LTc1YzgzMmJiNmY0MiIsImlhdCI6MTcyNTM1NTE4OSwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYt NzM2Yy03YzIxLTE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS40Mi44NS4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.h27D7KDVBmpHMEwMcF-pC_fSwXNueXtaOy7dozOF_3J6Y43NZaxlqABJgIGKa0_1xc0vw-qWgm09pXibtZUdBQ'
        # self.tag = ft.TextField(label='tag do clan', width=400,dense=True, content_padding=10, bgcolor='white,0.08',)
        self.tag = ft.Dropdown(label = 'escolha a tag do clan:', 
        options=[ft.dropdown.Option("Aracaju"),ft.dropdown.Option("SkyWarrios"),ft.dropdown.Option("Outro") ], 
        value = "Aracaju",content_padding=10,filled=True, bgcolor='white,0.08'
                )
        # dica = ft.Text('gere o token no site: https://developer.clashofclans.com/#/key/e7ff0da5-5d92-42b7-990f-d7431f5ab41c', color = 'white,0.6',selectable = True)
        self.gerar_token = ft.IconButton(tooltip='gerar Token',icon = ft.icons.GENERATING_TOKENS, on_click=self.GerarToken, icon_size=20)
        self.botao_importar = ft.ElevatedButton('Importar dados',on_click=self.Importar_players)
        
        self.botao_ordenar_forca = ft.TextButton('Força',data = 'forca',on_click=self.Ordenar_por, col = self.Colu(2))
        self.botao_ordenar_tag = ft.TextButton('Tag',data = 'tag',on_click=self.Ordenar_por,  col = self.Colu(2))

        self.botao_ordenar_guerra = ft.IconButton(icon = ft.icons.ACCESSIBILITY_NEW_ROUNDED,data = 'guerra',on_click=self.Ordenar_por, col = self.Colu(0.7), scale=0.8)
        self.botao_ordenar_jogador = BotaoCT('Jogador',data = 'jogador',on_click=self.Ordenar_por,  col = self.Colu(4.3))
        self.botao_ordenar_cv = BotaoCT('CV',data = 'nivel_cv',on_click=self.Ordenar_por, col = self.Colu(0.8))
        self.botao_ordenar_atenuador = BotaoCT('Atenuador',data = 'atenuador',on_click=self.Ordenar_por, col = self.Colu(3), scale=0.8)
        self.botao_ordenar_forca_final = BotaoCT('Força Final',data = 'forca_final',on_click=self.Ordenar_por, col = self.Colu(3), scale=0.8)

        self.controls = [
                         
                         ft.ResponsiveRow([
                             self.botao_ordenar_guerra,
                             self.botao_ordenar_jogador,
                            #  self.botao_ordenar_tag,
                             self.botao_ordenar_cv,
                            #  self.botao_ordenar_forca,
                             self.botao_ordenar_atenuador,
                             self.botao_ordenar_forca_final,

                                 
                                 
                        ], spacing=0, run_spacing=0, ),
                         
                ]
    
        try:
            # self.lista = self.LerPickle(self.config_tabela)
            # self.SalvarDadosLocais('lista', self.lista)
            defal = self.Ler_json('lista_import')
            self.lista = self.LerDadosLocais('lista', default=defal)
            self.tabela = [Players(*i,func = self.Salvar)  for i in self.lista]
            self.tabela = self.OrdenarListadeClasses(self.tabela, 'forca_final')
            self.controls.append(ft.Column(self.tabela,scroll=ft.ScrollMode.ADAPTIVE, height=600))
        except:
            pass
        self.run_spacing = 0
        self.spacing = 0
        self.saida = Saida()
        self.printt = printt
        self.controls.append(self.saida)        


    def Configs(self):
        return  ft.Column([self.tag,self.Tokken,ft.Row([self.botao_importar,self.gerar_token])])


    def Colu(self, x = 4):
        return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}


# i.Tokken.value = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03 ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw 6Z2FtZWFwaSIsImp0aSI6IjI2ODk2ZTg4LTZmYmMtNDU3NS1iYjhkLTI1NWVmM2QzNTMxOSIsI mlhdCI6MTcxNzMzNTIxMiwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYtNzM2Yy03YzI xLTE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE 3Ny4zOS41OS4xNiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.0uaDqGBq6ayrNLsuaHUTY98uq5AllD5vitRCLlssnl5Ol9rmT_qPleO87kDaGwNF8FEEXNWJ6t7rCElh6A-0EA'
    def OrdenarListadeClasses(self, lista, atributo, decrecente=True):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)    

    def Ordenar_por(self, e):
        atr = e.control.data
        self.controls[-2].controls = self.OrdenarListadeClasses(self.controls[-2].controls, atr)

        self.update()     
        self.printt(f'ordenando por {atr}')
        self.page.update()

    def OrdenarDicionario(self, dic, col):
        coluna_old = dic[col]
        ord = sorted(dic[col], reverse = True)
        novo_index = [coluna_old.index(i) for i in ord]
        for i in dic.keys():
            dic[i]= [dic[i][k] for k in novo_index ]
        return dic

    def Salvar(self,e):
        dic = {'nome':[],'nivel_cv':[],'forca':[] }
        lista = []

        # for i in self.tabela:
        for i in self.controls[-2].controls:
            if i.guerra:
                dic['nome'].append(i.jogador)
                dic['nivel_cv'].append(i.nivel_cv)
                dic['forca'].append(i.forca_final)
                # dic['atenuador'].append(i.atenuador)

            lista.append([i.guerra,i.jogador,i.tag,i.nivel_cv, i.forca,i.atenuador, i.forca_final])
        

        dic2 = self.OrdenarDicionario(dic, 'forca')



        # self.SalvarPickle(lista, self.config_tabela)
        # self.Escrever_json(dic2, self.config_jogadores)
        self.SalvarDadosLocais('jogadores',dic2)
        self.SalvarDadosLocais('lista',lista)
        self.printt('Dados dos players salvo com sucesso') 
        self.Atualizar()       


    def SalvarDadosLocais(self, nome, valor):
        self.page.client_storage.set(nome, valor)
        

    def LerDadosLocais(self, nome,  default=None):
        if self.page.client_storage.contains_key(nome):
            return self.page.client_storage.get(nome)
        else:
            return default


    def GerarToken(self,e):
        webbrowser.open('https://developer.clashofclans.com/#/key/e7ff0da5-5d92-42b7-990f-d7431f5ab41c')

    def _ImportarDadosAPI(self, api_key1, url):
        api_key = re.sub(r'\s+', '', api_key1)
        headers = {'Authorization': f'Bearer {api_key}'}
        # try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # A solicitação foi bem-sucedida, você pode continuar a trabalhar com os dados da API
            # Converte a resposta JSON em um dicionário Python ou uma lista, dependendo do formato dos dados da API
            dados = response.json()
            # Agora, você pode acessar os dados como faria com qualquer outro dicionário ou lista em Python
            return dados
        else:
            # A solicitação não foi bem-sucedida, lide com isso de acordo com os requisitos do seu aplicativo
            return f'Erro ao buscar dados da API. Código de status: {response.status_code}'
    # except:
        #     print('Tokken inválido!')

    def _Import(self, api_key):
        players = self._ImportarDadosAPI(api_key, self.link_clan)
        if isinstance(players, dict):
            tags_nomes = [[i['tag'], i['name']] for i in players['memberList']]

            dic_jogadores = {}
            for i in tags_nomes:
                dic_jogadores[f'{i[1]}-{i[0]}'] = self._ImportarDadosAPI(
                    api_key, url=str(self.link_player+f'{i[0][1:]}'))

            dic_jogadores_esp1 = {}

            chaves_desejadas = ['name', 'townHallLevel',
                                'troops', 'heroes',  'spells']

            dic_jogadores_esp1['nome'] = list(dic_jogadores.keys())

            dic_jogadores_esp1['cv'] = [dic_jogadores[chave]['townHallLevel']
                                        for chave in dic_jogadores_esp1['nome']]

            nomes_herois = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['heroes']]
            
            herois = {chave: dic_jogadores[chave]['heroes']
                    for chave in dic_jogadores_esp1['nome']}
            
            herois2 = {}
            for chave, valor in herois.items():
                herois2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_herois:
                dic_jogadores_esp1[i] = []
                for chave, valor in herois2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            # Valores dos níveis das tropas
            nomes_tropas = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['troops']]
            tropas = {chave: dic_jogadores[chave]['troops']
                    for chave in dic_jogadores_esp1['nome']}
            tropas2 = {}
            for chave, valor in tropas.items():
                tropas2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_tropas:
                dic_jogadores_esp1[i] = []
                for chave, valor in tropas2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            # Valores dos níveis dos spells
            nomes_spells = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['spells']]
            spells = {chave: dic_jogadores[chave]['spells']
                    for chave in dic_jogadores_esp1['nome']}
            spells2 = {}
            for chave, valor in spells.items():
                spells2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_spells:
                dic_jogadores_esp1[i] = []
                for chave, valor in spells2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            dic_jogadores_esp1['nome'] = [
                i[:-10].replace("-", "") for i in dic_jogadores_esp1['nome']]


            return dic_jogadores_esp1
        else:
            self.printt(f'Tokken inválido!')

    def Importar_dados(self,e):
        api_key = re.sub(r'\s+', '', self.Tokken.value)
        if isinstance(api_key, str) and api_key not in ['', None]:
            self.printt('Importando dados...')
            return self._Import(api_key)
        else:
            self.printt('Você não inseriu uma api_key válida, ou o IP está incorreto. \nVerifique o IP e adicione uma nova api_key no site: \nhttps://developer.clashofclans.com/#/')




    def Importar_players(self,e):
        if self.Tokken.value not in ['', None]:
            self.printt('Importando dados...')
            players1 = self._ImportarDadosAPI(self.Tokken.value, self.link_clan)
            if isinstance(players1, dict):
                self.printt('Nomes dos players importados')

                tags_nomes = [[i['tag'], i['name']] for i in players1['memberList']]

                self.printt('Importando dados de cada um dos players...')

                dic_jogadores = {}
                for j in tags_nomes:
                    dic_jogadores[f'{j[1]}-{j[0]}'] = self._ImportarDadosAPI(self.Tokken.value, url=str(self.link_player+f'{j[0][1:]}'))
                
                def Calcular_forcaT(jogador):
                    cv = jogador['townHallLevel']
                    tropas = jogador['troops']
                    tropas_desejadasT = list((



                        # 'Root Rider', 'L.A.S.S.I', 'Mighty Yak', 'Electro Owl', 'Unicorn',
                        # 'Phoenix', 'Poison Lizard', 'Diggy', 'Frosty', 'Spirit Fox', 'Angry Jelly',

                'Barbarian',
                'Archer',
                'Goblin',
                'Giant',
                'Wall Breaker',
                'Balloon',
                'Wizard',
                'Healer',
                'Dragon',
                'P.E.K.K.A',
                'Minion',
                'Hog Rider',
                'Valkyrie',
                'Golem',
                'Witch',
                'Lava Hound',
                'Bowler',
                'Baby Dragon',
                'Miner',



                'Wall Wrecker',
                'Battle Blimp',
                'Yeti',
                'Sneaky Goblin',
                'Rocket Balloon',
                'Ice Golem',
                'Electro Dragon',
                'Stone Slammer',
                'Inferno Dragon',

                'Dragon Rider',

                'Siege Barracks',
                'Ice Hound',
                'Log Launcher',
                'Flame Flinger',

                'Electro Titan',
                'Apprentice Warden',
                'Super Hog Rider',
                'Root Rider',
                'L.A.S.S.I',
                'Mighty Yak',
                'Electro Owl',
                'Unicorn',
                'Phoenix',
                'Poison Lizard',
                'Diggy',
                'Frosty',
                'Spirit Fox',
                'Angry Jelly'        


                    ))
                
                    forca = []

                    for k in tropas:
                        if k['name'] in tropas_desejadasT:
                            forca.append(5)

                    forca.append(100*cv)
                    return cv, sum(forca)

                def Calcular_forcaH(jogador):
                    heroes = jogador['heroes']
                    tropas_desejadas = list((

                        'Barbarian King', 'Archer Queen', 'Grand Warden', 'Royal Champion',

                    ))

                    forca = []

                    for k in heroes:
                        if k['name'] in tropas_desejadas:
                            forca.append(10)

                    return sum(forca)

                def Calcular_forcaS(jogador):
                    spells = dic_jogadores[j]['spells']

                    tropas_desejadas = list((
                        'Lightning Spell',
                        'Healing Spell',
                        'Rage Spell',
                        'Jump Spell',
                        'Freeze Spell',
                        'Poison Spell',
                        'Earthquake Spell',
                        'Haste Spell',
                        'Clone Spell',
                        'Skeleton Spell',
                        'Bat Spell',
                        'Invisibility Spell',
                        'Recall Spell',
                        'Overgrowth Spell'
                    ))

                    forca = []

                    for k in spells:
                        if k['name'] in tropas_desejadas:
                            forca.append(5)
                    return sum(forca)

                self.lista = []
                for j in list(dic_jogadores.keys()):
                    nome = dic_jogadores[j]['name']
                    tag = dic_jogadores[j]['tag']
                    cv, forcaT = Calcular_forcaT(dic_jogadores[j])
                    forcaH = Calcular_forcaH(dic_jogadores[j])
                    forcaS = Calcular_forcaS(dic_jogadores[j])
                    forca = forcaT+forcaH+forcaS

                    self.lista.append([0,nome,tag,cv,forca, '',''])


                self.tabela = [Players(*i,self.Salvar)  for i in self.lista]


                self.tabela = self.OrdenarListadeClasses(self.tabela, 'forca_final')

                self.Salvar(1)


                self.printt('Dados importados com sucesso!')
                self.update()
                
                
            else:
                self.printt('Erro na importação dos dados')

        else:
            self.printt('Insira o token')
            print('Insira o token')



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
                
    def SalvarPickle(self, var, nome):
        if not nome.endswith('.plk'):
            nome += '.plk'        
        with open(nome, 'wb') as arquivo:
            pickle.dump(var, arquivo)

    def LerPickle(self,nome):
        if not nome.endswith('.plk'):
            nome += '.plk'
        if os.path.isfile(nome):
            with open(nome, 'rb') as arquivo:
                return pickle.load(arquivo)
        else:
            return None   

    def Atualizar(self):
        try:
            self.update()
        except:
            pass

def main(page: ft.Page):
    page.window.width = 330  # Define a largura da janela como 800 pixels
    page.window.height = 600  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    i =  layout_Importar( printt = saida.pprint, page = page)    
    page.add(i, saida)




if __name__ == '__main__':    
    ft.app(main) 
