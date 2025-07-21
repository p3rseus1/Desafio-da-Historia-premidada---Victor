from fastapi import FastAPI, HTTPException, Query, Request
from models import Cliente, ClienteEndereco
import httpx
import logging
from httpx import ConnectTimeout, HTTPStatusError
import time


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Tempo: {process_time:.2f}ms - "
        f"Query: {dict(request.query_params)}"
    )

    return response


@app.get("/cliente-endereco", response_model=ClienteEndereco)
async def get_cliente_endereco(cpf: str = Query(...), nome: str = Query(...), cep: int = Query(...)):
    cliente = Cliente(cpf=cpf, nome=nome, cep=cep)
    teste=str(cliente.cep)
    t=len(teste)
    if t<8:
        for _ in range(8-t):
            teste='0'+teste

    url = f"https://brasilapi.com.br/api/cep/v1/{teste}"

    try:
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            response = await client.get(url)
        response.raise_for_status()
        data = response.json()
    except ConnectTimeout:
        logger.error("Timeout ao conectar com a BrasilAPI")
        raise HTTPException(status_code=504, detail="Timeout ao conectar com a BrasilAPI")
    except HTTPStatusError:
        logger.error(f"CEP inválido: {cliente.cep}")
        raise HTTPException(status_code=400, detail="CEP inválido")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    
    return ClienteEndereco(
        cpf=cliente.cpf,
        cep=teste,
        state=data.get("state", ""),
        city=data.get("city", ""),
        neighborhood=data.get("neighborhood", ""),
        street=data.get("street", ""),
        service=data.get("service", "")
    )
