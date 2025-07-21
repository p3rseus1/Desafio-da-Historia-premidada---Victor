# Desafio-da-Historia-premidada

## Historia
 
Criar backend que dado um objeto ele consulte uma api externa para completar os dados do correntista.
 
 
### Descrição
 
**COMO UM** novo correntista
**QUERO** passar o CEP
**PARA QUE** eu possa fazer meu cadastro
 
### Critério de Aceitação
 
* Código fonte deve esta salvo no github.
* Funcionar em container.
* Funcionar no formato openAPI.
* Ter swagger para acessar as funcoes.
* Ter log INFO falando das consultas.
* Ter log ERROR para Ceps invalidos.
* Ter log CRITICAL quando não tiver acesso a api.
* Deve ter uma esteira onde ao versionar (tag) no codigo ele disponibilize uma imagem no docker hub.
* Rodar na maquina local baixando a imagem no docker hub.(docker.binarios.bb.com.br/user-docker/imagem:versao)
* Consulta o CEP na api externa https://brasilapi.com.br/docs#tag/CEP
 
 
### Cenário de teste
 
**DADO QUE** mande o objeto *cliente* por metodo GET
**QUANDO** receber a requisição com cep valido.
**ENTÃO** devolver o objeto *clienteEndereço*
 
**DADO QUE** mande o objeto *cliente* por metodo GET
**QUANDO** receber a requisição com cep invalido.
**ENTÃO** devolver o erro de cep invalido, e logar como ERROR
 
Objetos:
```json
**cliente**
{
    "cpf": "string (required)",
    "nome": "string (required)",
    "cep": "integer <int64> (required)"
}
```
*clienteEndereço*
```json
{
    "cpf": "string (required)",    
    "cep": "integer <int64> (required)",
    "state": "string",
    "city": "string",
    "neighborhood": "string",
    "street": "string",
    "service": "viacep"
}
```
