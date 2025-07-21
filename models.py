from pydantic import BaseModel

class Cliente(BaseModel):
    cpf: str
    nome: str
    cep: int

class ClienteEndereco(BaseModel):
    cpf: str
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    service: str
