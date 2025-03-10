# CRUD:

from sqlalchemy.orm import Session
from src.model.db import Tarefa  # Importe o modelo de Tarefa do arquivo db.py

# Função para criar uma nova tarefa
def cadastrar_tarefa(db: Session, descricao: str, situacao: bool = False):
    # Criar uma nova tarefa
    tarefa = Tarefa(DESCRICAO=descricao, SITUACAO=situacao)
    
    # Adicionar e commitar no banco
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)  # Para obter a instância completa com o ID
    return tarefa

# Função para editar uma tarefa
def editar_tarefa(db: Session, task_id: int, descricao: str, situacao: bool):
    # Buscar a tarefa pelo ID
    tarefa = db.query(Tarefa).filter(Tarefa.ID == task_id).first()
    
    if tarefa:
        tarefa.DESCRICAO = descricao
        tarefa.SITUACAO = situacao
        
        db.commit()
        db.refresh(tarefa)  # Atualiza a instância após o commit
        return tarefa
    return None  # Caso a tarefa não seja encontrada

# Função para excluir uma tarefa
def excluir_tarefa(db: Session, task_id: int):
    # Buscar a tarefa pelo ID
    tarefa = db.query(Tarefa).filter(Tarefa.ID == task_id).first()
    
    if tarefa:
        db.delete(tarefa)  # Excluir a tarefa
        db.commit()
        return True
    return False  # Retorna False se a tarefa não for encontrada

# Função para listar todas as tarefas
def listar_tarefa(db: Session):
    # Retorna todas as tarefas no banco de dados
    return db.query(Tarefa).all()

# Função para listar uma tarefa por ID
def listar_tarefa_id(db: Session, task_id: int):
    # Retorna a tarefa com o ID específico
    return db.query(Tarefa).filter(Tarefa.ID == task_id).first()