from typing import TypedDict

from bson.objectid import ObjectId
from decouple import config
from pymongo import MongoClient

from ..presentation.viewmodels import Tarefa


class TarefaMongo(TypedDict):
    _id: ObjectId
    nome: str
    genero: str
    ano: int
    duracao: int


class TarefaMongoDBRepository():

    def __init__(self):
        # Connect to MongoDB
        # uri = 'mongodb://localhost:27017'
        uri = config('MONGODB_URL')
        client = MongoClient(uri)
        db = client['tarefasapp']
        self.tarefas = db['tarefas']
        

    def todos(self, skip=0, take=0):
        tarefas = self.tarefas.find().skip(skip).limit(take)
        return list(map(Tarefa.fromDict, tarefas))

    def salvar(self, tarefa):
        _id = self.tareafas.insert_one(tarefa.toDict()).inserted_id
        tarefa.id = str(_id)
        return tarefa

    def obter_um(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        tarefa_encontrado = self.tarefas.find_one(filtro)
        return Tarefa.fromDict(tarefa_encontrado) if tarefa_encontrado else None

    def remover(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tarefas.delete_one(filtro)

    def atualizar(self, tarefa_id, tarefa):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tarefas.update_one(filtro, {'$set': filme.toDict()})
        tarefa.id = tarefa_id
        return tarefa
