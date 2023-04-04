from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

class Tarefa(BaseModel):
    id: int | None
    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str | None
    prioridade: int


tarefas: list[Tarefa] = []


@app.get('/tarefas')
def listar_tarefas(skip: int | None = None, take: int | None = None):
    inicio = skip

    if skip and take:
        fim = skip + take
    else:
        fim = None
    
    return tarefas[inicio:fim]


@app.get('/tarefas/{tarefa_id}')
def detalhar_tarefas(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa.id == tarefa_id:
            return tarefa
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.get('/tarefas/nivel/{pesquisar_nivel}')
def listar_nivel(pesquisar_nivel: int):
    tarefas_nivel = []
    for tarefa in tarefas:
        if tarefa.nivel == pesquisar_nivel:
            tarefas_nivel.append(tarefa)
    
    if len(tarefas_nivel) > 0:
        return tarefas_nivel
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.get('/tarefas/prioridade/{pesquisar_prioridade}')
def listar_prioridade(pesquisar_prioridade: int):
    tarefas_prioridade = []
    for tarefa in tarefas:
        if tarefa.prioridade == pesquisar_prioridade:
            tarefas_prioridade.append(tarefa)
    
    if len(tarefas_prioridade) > 0:
        return tarefas_prioridade
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.get('/tarefas/situacao/{pesquisar_situacao}')
def listar_situacao(pesquisar_situacao: int):
    tarefas_situacao = []
    for tarefa in tarefas:
        if tarefa.situacao == pesquisar_situacao:
            tarefas_situacao.append(tarefa)
    
    if len(tarefas_situacao) > 0:
        return tarefas_situacao
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.post('/tarefas/criar', status_code=status.HTTP_201_CREATED)
def nova_tarefa(tarefa: Tarefa):
    tarefa.id = len(tarefas) + 1
    tarefa.situacao = "Nova"
    tarefas.append(tarefa)

    return tarefa


@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa.id == tarefa_id:
            tarefas.remove(tarefa)
            return "tarefa deletada"
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.put('/tarefas/{tarefa_id}/cancelar')
def cancelar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            tarefa_atual.situacao = "Cancelada"
            tarefas[index] = tarefa_atual
            return tarefa_atual
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.put('/tarefas/{tarefa_id}/completar')
def completar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "Em andamento":
                tarefa_atual.situacao = "Completo"
                tarefas[index] = tarefa_atual
                return tarefa_atual
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.put('/tarefas/{tarefa_id}/em_andamento')
def tarefa_em_andamento(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "Nova" or tarefa_atual.situacao == "Pendente":
                tarefa_atual.situacao = "Em andamento"
                tarefas[index] = tarefa_atual
                return tarefa_atual
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")


@app.put('/tarefas/{tarefa_id}/pendente')
def tarefa_pendente(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "Nova" or tarefa_atual.situacao == "Em andamento":
                tarefa_atual.situacao = "Pendente"
                tarefas[index] = tarefa_atual
                return tarefa_atual
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
