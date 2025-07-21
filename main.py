from fastapi import FastAPI, HTTPException, Query, Request
from models import Cliente, ClienteEndereco
import httpx
import logging
from httpx import ConnectTimeout, HTTPStatusError
import time
from dotenv import load_dotenv
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
load_dotenv()

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
    strcep=str(cliente.cep)
    t=len(strcep)
    if t<8:
        for _ in range(8-t):
            strcep='0'+strcep

    url = f"https://brasilapi.com.br/api/cep/v1/{strcep}"

    try:
        proxy_usu=os.getenv("PROXY")
        async with httpx.AsyncClient(verify=False, proxy=proxy_usu) as client:
            response = await client.get(url)
        response.raise_for_status()
        data = response.json()
    except ConnectTimeout:
        logger.error("Timeout ao conectar com a BrasilAPI")
        raise HTTPException(status_code=504, detail="Timeout ao conectar com a BrasilAPI")
    except HTTPStatusError:
        logger.error(f"CEP inválido: {strcep}")
        raise HTTPException(status_code=400, detail="CEP inválido")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    
    return ClienteEndereco(
        cpf=cliente.cpf,
        cep=strcep,
        state=data.get("state", ""),
        city=data.get("city", ""),
        neighborhood=data.get("neighborhood", ""),
        street=data.get("street", ""),
        service=data.get("service", "")
    )
