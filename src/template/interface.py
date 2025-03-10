import sys
import os

# Adiciona o diretório raiz ao sys.path para importar corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft  # Importando a biblioteca flet para criar a interface gráfica
from src.service import crud  # Importando as funções de CRUD do arquivo crud.py
from src.model.db import SessionLocal  # Importando a sessão do banco de dados

# Lista global para armazenar as tarefas
lista_tarefas = []

def main(page=ft.Page):  # Função principal que é chamada para renderizar a página
    page.title = 'aula 3'  # Definindo o título da página no navegador
    page.window.height = 700
    page.window.width = 700
    page.window.center()

    def adicionar(e):  # Função para adicionar uma nova tarefa
        if not nova_tarefa.value:  # Verificando se o campo de texto para adicionar tarefa está vazio
            nova_tarefa.error_text = 'Digite algo para adicionar'  # Definindo um erro de validação
            page.update()  # Atualizando a página para mostrar a mensagem de erro
        else:
            nova_tarefa.error_text = None  # Se o campo não está vazio, removendo a mensagem de erro

            # Criando a tarefa no banco de dados
            tarefa_criada = crud.cadastrar_tarefa(SessionLocal(), nova_tarefa.value, False)  # Situação inicial como False

            # Criando um container de linha (Row) para a tarefa
            tarefa = ft.Row([])

            # Criando um Checkbox com o texto da nova tarefa
            checkbox = ft.Checkbox(label=nova_tarefa.value, on_change=lambda e: atualizar_situacao(tarefa_criada.ID, checkbox.checked))

            # Criando o botão de editar com ícone de "editar"
            btn_editar = ft.IconButton(
                icon=ft.icons.EDIT,  # Definindo o ícone de editar
                tooltip='Editar tarefa',  # Tooltip que aparece quando o mouse passa por cima
                on_click=lambda e: editar_tarefa(tarefa, checkbox, btn_editar, botao_remover, tarefa_criada)  # Chamando a função de edição da tarefa
            )

            # Criando o botão de remover com ícone de "remover"
            botao_remover = ft.IconButton(
                icon=ft.icons.DELETE_OUTLINED,  # Ícone de remover
                tooltip="Remover tarefa",  # Tooltip que aparece quando o mouse passa por cima
                on_click=lambda e: remover_tarefa(tarefa, tarefa_criada)  # Chamando a função para remover a tarefa
            )

            tarefa.controls.extend([checkbox, botao_remover, btn_editar])  # Adicionando os componentes à tarefa

            page.add(tarefa)  # Adicionando a tarefa à página
            lista_tarefas.append(tarefa)  # Adicionando a tarefa à lista de tarefas
            nova_tarefa.value = ''  # Limpando o campo de entrada
            nova_tarefa.focus()  # Focando no campo para o usuário digitar uma nova tarefa
            nova_tarefa.update()  # Atualizando a página

    def atualizar_situacao(task_id, situacao):  # Função para atualizar a situação da tarefa no banco
        # Aqui vamos chamar a função para atualizar a situação da tarefa no banco de dados sempre que o checkbox for alterado
        crud.editar_tarefa(SessionLocal(), task_id, None, situacao)  # Atualiza o campo 'SITUACAO' no banco automaticamente

    def editar_tarefa(tarefa, checkbox, btn_editar, botao_remover, tarefa_criada):  # Função para editar a tarefa
        # Esconde os componentes de texto e checkbox
        checkbox.visible = False
        btn_editar.visible = False
        botao_remover.visible = False
        page.update()

        # Criando o campo de edição com o valor atual da tarefa
        campo_edicao = ft.TextField(label='Editar tarefa', value=checkbox.label, width=300)

        # Criando o botão para salvar a edição
        def salvar_edicao(e):
            # Atualizando a tarefa no banco de dados com o novo texto e a situação da checkbox
            updated_task = crud.editar_tarefa(
                SessionLocal(), tarefa_criada.ID, campo_edicao.value, checkbox.value  # Agora passando checkbox.value corretamente
            )
    
            if updated_task:
                # Atualizando o texto do checkbox com o novo valor
                checkbox.label = campo_edicao.value
                checkbox.value = updated_task.SITUACAO  # Atualizando a checkbox com o valor de situação
                page.update()  # Atualizando a página para refletir a mudança

            # Mostrando novamente o checkbox e o botão de editar
            checkbox.visible = True
            btn_editar.visible = True
            botao_remover.visible = True

            # Esconde o campo de edição e o botão de salvar
            campo_edicao.visible = False
            btn_salvar.visible = False
            page.update()  # Atualizando a página para refletir a mudança

        # Criando o ícone de salvar
        btn_salvar = ft.IconButton(
            icon=ft.icons.SAVE_OUTLINED,  # Ícone de salvar
            tooltip='Salvar tarefa',  # Tooltip que aparece quando o mouse passa por cima
            on_click=salvar_edicao,  # Ação ao clicar no botão
        )

        # Adicionando a TextField e o botão de salvar
        tarefa.controls.append(campo_edicao)
        tarefa.controls.append(btn_salvar)
        page.update()  # Atualizando a página

    def remover_tarefa(tarefa, tarefa_criada):  # Função para remover a tarefa
        crud.excluir_tarefa(SessionLocal(), tarefa_criada.ID)  # Remove do banco de dados
        page.controls.remove(tarefa)  # Removendo a tarefa da página
        lista_tarefas.remove(tarefa)  # Removendo a tarefa da lista
        page.update()  # Atualizando a página para refletir as mudanças

    # Definindo o campo de texto para inserir nova tarefa
    nova_tarefa = ft.TextField(label='Nome da tarefa', width=300,)

    def listar_tarefa(e):
        # Mostra as tarefas na lista
        for tarefa in lista_tarefas:
            tarefa.visible = True
        page.update()

    # Criando o layout para adicionar novas tarefas
    page.add(ft.Column([  
        nova_tarefa, 
        ft.ElevatedButton('Adicionar', on_click=adicionar, color=ft.colors.WHITE, bgcolor=ft.colors.GREEN_500, width=200, height=50)
    ]))  

    page.theme_mode = ft.ThemeMode.DARK  # Definindo o tema inicial como escuro
    page.update()  # Atualizando a página

# Iniciando o app
ft.app(main)
