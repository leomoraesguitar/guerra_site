import json
import flet as ft
import os



# class Verificar_pasta:
#     def __init__(self,pastalocal = 'Guerra_clash'):
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
            self.page.dialog = self.confirm_dialog
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

class Saida(ft.Column):
    def __init__(self,height = 50):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad], auto_scroll=True, height=height), bgcolor='white,0.03'))

    def pprint(self, *texto):
        for i in texto:
            self.saidad.value += f'{i}\n'
        self.page.update()

class LayoutEquipes(ft.Column):
    def __init__(self, printt=None, page=None):
        super().__init__()
        self.printt = printt
        self.page = page
        cp = 5
        wd = 50
        self.equipe_fields = {
            "GRUPO MASTER": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO ELITE": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO A": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO B": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO C": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO D": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO E": ft.TextField(width=wd, dense=True, content_padding=cp, bgcolor='white,0.08', on_change=self.salvar),
        }
        self.controls = [
            ft.Container(ft.Column([ft.Row([ft.Text(name, weight='BOLD', size=12), field ],
                alignment=ft.MainAxisAlignment.CENTER),ft.Text(details, size=13, color='white,0.6', text_align='center')], horizontal_alignment='center', spacing=0),
                bgcolor='blue,0.05'
                )
            for name, field, details in [
                ("GRUPO MASTER", self.equipe_fields["GRUPO MASTER"], '3 em cv15-, 2 em cv14+'),
                ("GRUPO ELITE", self.equipe_fields["GRUPO ELITE"], '3 em cv14-, 2 em cv15+'),
                ("GRUPO A", self.equipe_fields["GRUPO A"], '3 em cv13-, 2 em cv13+'),
                ("GRUPO B", self.equipe_fields["GRUPO B"], '3 em cv12-, 2 em cv12+'),
                ("GRUPO C", self.equipe_fields["GRUPO C"], '3 em cv11-, 2 em cv12 e cv13, 1 + cv expoto em cv14+'),
                ("GRUPO D", self.equipe_fields["GRUPO D"], '3 em cv10-, 2 em cv11 e cv12, 1 + cv expoto em cv13, 1 em cv14 se cv exposto'),
                ("GRUPO E", self.equipe_fields["GRUPO E"], '3 em cv9-, 2 em cv10, 1 + cv expoto em cv11, 1 em cv12, 1 em cv13 se cv exposto'),
            ]
        ]
        self.saida = Saida()
        self.printt = self.saida.pprint
        self.controls.append(self.saida)
        self.iniciar()
    
    # def did_mount(self):

    def iniciar(self):
        # self.config_equipes = Verificar_pasta('Guerra_clash').caminho('config_guerra.json')        
        # self.arquiv = self.ler_json(self.config_equipes, default={
        #     "equipe A": {
        #             "Nome da Equipe": "equipe A",
        #             "GRUPO MASTER": "1930",
        #             "GRUPO ELITE": "1825",
        #             "GRUPO A": "1794",
        #             "GRUPO B": "1585",
        #             "GRUPO C": "1444",
        #             "GRUPO D": "1440",
        #             "GRUPO E": "1430"
        #         }
        # })   
        
        # self.SalvarDadosLocais('equipes', self.arquiv)     
        self.arquiv = self.LerDadosLocais('equipes', default={
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
        for key in self.equipe_fields:
            self.equipe_fields[key].value = self.arquiv["equipe A"].get(key, "")

    def salvar(self, e):
        # self.arquiv = self.ler_json(self.config_equipes)
        self.arquiv = self.LerDadosLocais('equipes')
        for key, field in self.equipe_fields.items():
            self.arquiv["equipe A"][key] = field.value
        # self.escrever_json(self.arquiv, self.config_equipes)
        self.SalvarDadosLocais('equipes',self.arquiv)
        self.printt('Configurações salvas com sucesso')

    def SalvarDadosLocais(self, nome, valor):
        self.page.client_storage.set(nome, valor)
      

    def LerDadosLocais(self, nome,  default=None):
        if self.page.client_storage.contains_key(nome):
            return self.page.client_storage.get(nome)
        else:
            return default

        



    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}

def main(page: ft.Page):
    page.window.width = 320
    page.window.height = 600
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START
    ConfirmarSaida(page)
    saida = Saida()
    Resize(page)
    layout = LayoutEquipes(printt=saida.pprint, page=page)
    page.add(layout)

if __name__ == '__main__':
    ft.app(main)
