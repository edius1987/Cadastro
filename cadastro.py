import flet as ft
import os
import datetime
import sqlite3
import xml.etree.ElementTree as ET
import xml.parsers.expat
import xml.sax.saxutils

class PatientApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cadastro de Pacientes"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = False
        self.page.padding = 20
        self.page.bgcolor = "#541e35"  # Cor de fundo escura
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.filename = os.path.join(os.path.dirname(__file__), "patients.sdb")
        self.db = self.connect(self.filename)

        self.images_path = os.path.join(os.path.dirname(__file__), "images")
        self.icon = os.path.join(self.images_path, "bookmark.gif")

        # Estilo padrão para os campos
        field_border_color = "#6bb38e"
        field_color = "#ffb43e"
        text_color = "white"
        label_style = ft.TextStyle(
            color=text_color,
            weight=ft.FontWeight.BOLD,
        )
        
        self.name = ft.TextField(
            label="Nome", 
            width=400,
            border_color=field_border_color,
            color=text_color,
            bgcolor="#df5d2e15",
            label_style=label_style,
            focused_border_color="#ffb43e",
            border_radius=10,
            text_size=16,
        )
        
        self.gender = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Masculino", label="Masculino", fill_color="#ffb43e", label_style=label_style),
                ft.Radio(value="Feminino", label="Feminino", fill_color="#ffb43e", label_style=label_style)
            ]),
        )
        
        self.health_plan = ft.Dropdown(
            label="Plano de Saúde",
            width=200,
            border_color=field_border_color,
            color=text_color,
            bgcolor="#df5d2e15",
            label_style=label_style,
            focused_border_color="#ffb43e",
            border_radius=10,
        )
        
        self.card_number = ft.TextField(label="Número do Cartão", width=200)
        self.birth_date = ft.TextField(label="Data de Nascimento", width=200)
        self.age = ft.TextField(label="Idade", width=120, read_only=True)
        self.address = ft.TextField(label="Endereço", width=400)
        self.city = ft.TextField(label="Cidade", width=200)
        self.state = ft.Dropdown(label="Estado", width=100, options=[
            ft.dropdown.Option(state) for state in (
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
                'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            )
        ])
        self.zip_code = ft.TextField(label="CEP", width=100)
        self.phone = ft.TextField(label="Telefone", width=150)
        self.cellphone = ft.TextField(label="Celular", width=150)
        self.record = ft.Dropdown(label="Registro", width=100)

        # Barra de ferramentas com ícones
        self.toolbar = ft.Row([
            ft.IconButton(
                icon=ft.icons.ADD_CIRCLE,
                on_click=self.new_patient,
                icon_color="#ffb43e",
                icon_size=30,
            ),
            ft.IconButton(
                icon=ft.icons.FOLDER_OPEN,
                on_click=self.open_patient,
                icon_color="#ffb43e",
                icon_size=30,
            ),
            ft.IconButton(
                icon=ft.icons.DELETE,
                on_click=self.delete_patient,
                icon_color="#ffb43e",
                icon_size=30,
            ),
            ft.IconButton(
                icon=ft.icons.SAVE,
                on_click=self.save_patient,
                icon_color="#ffb43e",
                icon_size=30,
            ),
            ft.IconButton(
                icon=ft.icons.EXIT_TO_APP,
                on_click=self.exit_app,
                icon_color="#ffb43e",
                icon_size=30,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Container principal
        main_container = ft.Container(
            content=ft.Column([
                ft.Container(  # Container para a toolbar
                    content=self.toolbar,
                    bgcolor="#df5d2e",
                    padding=10,
                    border_radius=10,
                ),
                ft.Container(  # Container para o formulário
                    content=ft.Column([
                        self.name,
                        self.gender,
                        ft.Row([
                            self.health_plan,
                            self.card_number,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            self.birth_date,
                            self.age
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        self.address,
                        ft.Row([
                            self.city,
                            self.state,
                            self.zip_code
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            self.phone,
                            self.cellphone
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        self.record,
                    ], spacing=20),
                    bgcolor="#a4c97215",
                    padding=30,
                    border_radius=10,
                )
            ], spacing=20),
            padding=20,
        )

        # Aplicar estilo aos demais campos
        for field in [self.card_number, self.birth_date, self.age, self.address,
                     self.city, self.state, self.zip_code, self.phone, 
                     self.cellphone, self.record]:
            if isinstance(field, (ft.TextField, ft.Dropdown)):
                field.border_color = field_border_color
                field.color = text_color
                field.bgcolor = "#df5d2e15"
                field.label_style = label_style
                field.focused_border_color = "#ffb43e"
                field.border_radius = 10
                if isinstance(field, ft.TextField):
                    field.text_size = 16

        self.page.add(main_container)

        self.load_health_plans()
        self.load_records()

    def connect(self, filename):
        create = not os.path.exists(filename)
        db = sqlite3.connect(filename)
        if create:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE planos ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                           "nome TEXT UNIQUE NOT NULL)")
            cursor.execute("CREATE TABLE pacientes ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                           "nome TEXT NOT NULL, "
                           "sexo TEXT, "
                           "cartao TEXT, "
                           "dia_nasc TEXT, "
                           "mes_nasc TEXT, "
                           "ano_nasc TEXT, "
                           "endereco TEXT, "
                           "cidade TEXT, "
                           "estado TEXT, "
                           "cep TEXT, "
                           "telefone TEXT NOT NULL, "
                           "celular TEXT, "
                           "plano_id INTEGER NOT NULL, "
                           "FOREIGN KEY (plano_id) REFERENCES planos)")
            db.commit()
        return db

    def load_health_plans(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT nome FROM planos ORDER BY nome")
        self.health_plan.options = [ft.dropdown.Option(plan[0]) for plan in cursor.fetchall()]
        self.page.update()

    def load_records(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM pacientes ORDER BY id")
        self.record.options = [ft.dropdown.Option(str(record[0])) for record in cursor.fetchall()]
        self.page.update()

    def new_patient(self, e):
        self.clear_fields()

    def open_patient(self, e):
        pass  # Implementar a lógica para abrir um paciente existente

    def delete_patient(self, e):
        pass  # Implementar a lógica para deletar um paciente

    def save_patient(self, e):
        pass  # Implementar a lógica para salvar um paciente

    def exit_app(self, e):
        self.page.window_close()

    def clear_fields(self):
        self.name.value = ""
        self.gender.value = None
        self.health_plan.value = ""
        self.card_number.value = ""
        self.birth_date.value = ""
        self.age.value = ""
        self.address.value = ""
        self.city.value = ""
        self.state.value = ""
        self.zip_code.value = ""
        self.phone.value = ""
        self.cellphone.value = ""
        self.record.value = ""
        self.page.update()

if __name__ == "__main__":
    ft.app(target=PatientApp)
