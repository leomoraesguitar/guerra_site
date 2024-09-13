

import os
import json
import flet as ft



# class Verificar_pasta:
#     def __init__(self,pastalocal = 'tabelamandadostjse'):
#         self.pastalocal = pastalocal
#         self.verificar_pasta()

#     def verificar_pasta(self):
#         user_profile = os.environ.get('USERPROFILE')
#         # print(user_profile)
#         if not user_profile:
#             # return False  # USERPROFILE não está definido
#             self.local = None

#         # caminho = os.path.join(user_profile, self.pastalocal)
#         caminho = self.pastalocal

        
#         if os.path.exists(caminho):
#             self.local = caminho
#             # return self.caminho
#         else:
#             os.mkdir(caminho)
#             # print(caminho)
#             if os.path.exists(caminho):
#                 self.local = caminho
#                 # return self.caminho
#             # else:
#                 # return None
    

#     def caminho(self, nome):
#         # self.verificar_pasta()
#         return os.path.join(self.local, nome)


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
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=50,  ),bgcolor='white,0.03' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.page.update()



class Jogador(ft.Row):
    def __init__(self, nome, nivel_cv, forca):
        super().__init__()
        self.peso = 0
        nomes = ('Cristiano',
                'lulmor',
                'lllll',
                'leoclash10',
                "cacauesntos",
                "rochaleo",
                "lolop",
                "Diogo SvS",
                "SR.ALEXANDRE",
                "GOKU BL4CKSE",
                "xXBPCBXx",
                'Letícia',
                'MaggieMelT',
                'GERIEL CAOS',
                'br')
        
        # self._nome = ft.Dropdown(value = nome, options=[ft.dropdown.Option(i) for i in nomes],dense=True, content_padding=5, width=130)
        self._nome = ft.Text(value = nome,  width=130)
        # self._nivel_cv = ft.Dropdown(focused_bgcolor = None, bgcolor = None,filled = True,value = nivel_cv, options=[ft.dropdown.Option(i) for i in range(20)],dense=True, content_padding=5, width=60,  text_style = ft.TextStyle(weight = ft.FontWeight.BOLD) )
        self._nivel_cv = ft.Text(value = nivel_cv,  width=60, )
        # self._forca = ft.TextField(value = forca, dense=True, content_padding=5, width=60)
        self._forca = ft.Text(value = forca,  width=60)
        # self._estrelas = None
        self.controls = [self._nome,self._nivel_cv, self._forca ]
    
    @property
    def nome(self):
        return self._nome.value
    @nome.setter
    def nome(self,nome):
        self._nome.value = nome

    @property
    def nivel_cv(self):
        return int(self._nivel_cv.value)
    @nivel_cv.setter
    def nivel_cv(self, nivel):
        self._nivel_cv.value = int(nivel)

    @property
    def forca(self):
        return int(self._forca.value)
    @forca.setter
    def forca(self, forca):
        self._forca.value = int(forca)


class layout_jogadores(ft.Column):
    def __init__(self, num_jogadores = 15, printt = None, page = None):
        super().__init__()
        self.page = page
        self.spacing = 0
        self.run_spacing = 0


        self.num_jogadores = ft.Dropdown(label = 'Número de Jogadores',value = num_jogadores, 
                options=[ft.dropdown.Option(i) for i in range(5,51)],dense=True, 
                content_padding=5, width=180, on_change=self.Chenge_num_jogadores)
        self.botao_salvar = ft.ElevatedButton('Salvar', on_click=self.Salvar, width=100)
        self.botao_atualizar = ft.ElevatedButton('Atualizar', on_click=self.Atualizar, width=105)
        self.controls.append(ft.Row([self.num_jogadores,self.botao_atualizar]))
        self.controls.append(ft.Text(height=0))
        self.controls.append(ft.Container(ft.Row([ft.Text('           Nome           '),ft.Text(' CV         '),ft.Text('forca')]),border=ft.border.all(1,'white,0.5'),width=300))
        cp = 165+(36*int(num_jogadores))
        if self.page is None:
            pw = 500
        else:
            pw = self.page.window.height
        if cp > pw:
            cumprimento_coluna = pw - 180
        else:
            cumprimento_coluna = cp
        self.controls.append(ft.Column(height=cumprimento_coluna, scroll=ft.ScrollMode.ADAPTIVE))
        self.saida = Saida()
        self.printt = self.saida.pprint
        self.controls.append(self.saida)        

        
        self.lista_jogadores = []
        # self.config_jogadores = Verificar_pasta('Guerra_clash').caminho('jogadores_config')
        try:
            # self.arquiv = self.Ler_json(self.config_jogadores,
            #     default={
            #             "nome": [
            #                 "Diogo SvS",
            #                 "Cristiano",
            #                 "lulmor",
            #                 "Let\u00edcia",
            #                 "lllll",
            #                 "leoclash10",
            #                 "lolop",
            #                 "cacauesntos",
            #                 "rochaleo",
            #                 "Maxwell",
            #                 "GOKU BL4CK-SE",
            #                 "SR. ALEXANDRE",
            #                 "xXBPCBXx",
            #                 "GERIEL CAOS",
            #                 "br"
            #             ],
            #             "nivel_cv": [
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 15,
            #                 15,
            #                 15,
            #                 13,
            #                 13
            #             ],
            #             "forca": [
            #                 1950,
            #                 1945,
            #                 1940,
            #                 1930,
            #                 1925,
            #                 1920,
            #                 1905,
            #                 1895,
            #                 1890,
            #                 1875,
            #                 1840,
            #                 1830,
            #                 1825,
            #                 1585,
            #                 1560
            #             ]
            #         }
            #     )
            # self.SalvarDadosLocais('jogadores',self.arquiv)
            self.arquiv = self.LerDadosLocais('jogadores',
                default={
                        "nome": [
                            "Diogo SvS",
                            "Cristiano",
                            "lulmor",
                            "Let\u00edcia",
                            "lllll",
                            "leoclash10",
                            "lolop",
                            "cacauesntos",
                            "rochaleo",
                            "Maxwell",
                            "GOKU BL4CK-SE",
                            "SR. ALEXANDRE",
                            "xXBPCBXx",
                            "GERIEL CAOS",
                            "br"
                        ],
                        "nivel_cv": [
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            15,
                            15,
                            15,
                            13,
                            13
                        ],
                        "forca": [
                            1950,
                            1945,
                            1940,
                            1930,
                            1925,
                            1920,
                            1905,
                            1895,
                            1890,
                            1875,
                            1840,
                            1830,
                            1825,
                            1585,
                            1560
                        ]
                    }
                )            
            for i,j,k in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['forca']):
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = j,forca = k))

        except:
            self.printt('deu erro na importação dos jogadores')
            nomes = ('Cristiano',
                    'lulmor',
                    'lllll',
                    'leoclash10',
                    "cacauesntos",
                    "rochaleo",
                    "lolop",
                    "Diogo SvS",
                    "SR.ALEXANDRE",
                    "GOKU BL4CKSE",
                    "xXBPCBXx",
                    'Letícia',
                    'MaggieMelT',
                    'GERIEL CAOS',
                    'br')            
            for i in nomes:
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = 15,forca = 800))

        self.controls[3].controls = self.lista_jogadores

    def Atualizar(self,e):
        self.lista_jogadores = []
        try:
            # self.arquiv = self.Ler_json(self.config_jogadores,
            #     default={
            #             "nome": [
            #                 "Diogo SvS",
            #                 "Cristiano",
            #                 "lulmor",
            #                 "Let\u00edcia",
            #                 "lllll",
            #                 "leoclash10",
            #                 "lolop",
            #                 "cacauesntos",
            #                 "rochaleo",
            #                 "Maxwell",
            #                 "GOKU BL4CK-SE",
            #                 "SR. ALEXANDRE",
            #                 "xXBPCBXx",
            #                 "GERIEL CAOS",
            #                 "br"
            #             ],
            #             "nivel_cv": [
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 16,
            #                 15,
            #                 15,
            #                 15,
            #                 13,
            #                 13
            #             ],
            #             "forca": [
            #                 1950,
            #                 1945,
            #                 1940,
            #                 1930,
            #                 1925,
            #                 1920,
            #                 1905,
            #                 1895,
            #                 1890,
            #                 1875,
            #                 1840,
            #                 1830,
            #                 1825,
            #                 1585,
            #                 1560
            #             ]
            #         }
            #     )
            # self.SalvarDadosLocais('jogadores',self.arquiv )
            self.arquiv = self.LerDadosLocais('jogadores',
                default={
                        "nome": [
                            "Diogo SvS",
                            "Cristiano",
                            "lulmor",
                            "Let\u00edcia",
                            "lllll",
                            "leoclash10",
                            "lolop",
                            "cacauesntos",
                            "rochaleo",
                            "Maxwell",
                            "GOKU BL4CK-SE",
                            "SR. ALEXANDRE",
                            "xXBPCBXx",
                            "GERIEL CAOS",
                            "br"
                        ],
                        "nivel_cv": [
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            16,
                            15,
                            15,
                            15,
                            13,
                            13
                        ],
                        "forca": [
                            1950,
                            1945,
                            1940,
                            1930,
                            1925,
                            1920,
                            1905,
                            1895,
                            1890,
                            1875,
                            1840,
                            1830,
                            1825,
                            1585,
                            1560
                        ]
                    }
                )
                        
            for i,j,k in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['forca']):
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = j,forca = k))

        except:
            self.printt('deu erro na importação dos jogadores')
            nomes = ('Cristiano',
                    'lulmor',
                    'lllll',
                    'leoclash10',
                    "cacauesntos",
                    "rochaleo",
                    "lolop",
                    "Diogo SvS",
                    "SR.ALEXANDRE",
                    "GOKU BL4CKSE",
                    "xXBPCBXx",
                    'Letícia',
                    'MaggieMelT',
                    'GERIEL CAOS',
                    'br')            
            for i in nomes:
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = 15,forca = 800))

        self.controls[3].controls = self.lista_jogadores
        self.update()

    def Gera_Lista_de_jogadores(self):
        return self.lista_jogadores


    def Chenge_num_jogadores(self, e):  
        pass   
    def Salvar(self,e):
        dic = {'nome':[],'nivel_cv':[],'forca':[] }
        for i in self.controls[3].controls:
            dic['nome'].append(i.nome)
            dic['nivel_cv'].append(i.nivel_cv)
            dic['forca'].append(i.forca)
        
        # self.Escrever_json(dic, self.config_jogadores)
        self.SalvarDadosLocais('jogadores',dic)
        self.printt('Vilas salvas com sucesso')



    def SalvarDadosLocais(self, nome, valor):
        self.page.client_storage.set(nome, valor)
        

    def LerDadosLocais(self, nome,  default=None):
        if self.page.client_storage.contains_key(nome):
            return self.page.client_storage.get(nome)
        else:
            return default


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

def main(page: ft.Page):
    page.window.width = 330  # Define a largura da janela como 800 pixels
    page.window.height = 500  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    j =  layout_jogadores(15, printt = saida.pprint, page = page)    
    page.add(j)

if __name__ == '__main__':    
    ft.app(main)        
