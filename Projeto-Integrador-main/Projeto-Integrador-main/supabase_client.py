# supabase_client.py
# Wrapper do cliente Supabase + normalizador de respostas
# Versão ajustada: NÃO chama resp.raise_when_api_error() diretamente
# — usa inspeção segura do objeto de resposta para detectar erros.

from dotenv import load_dotenv
load_dotenv()  # carrega automaticamente .env sempre que este módulo é importado

import os
from supabase import create_client
from typing import List, Dict, Any

# Carrega variáveis do ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL / SUPABASE_KEY não configuradas. "
        "Crie um arquivo .env ou defina no ambiente."
    )

# Inicializa o cliente
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def _unwrap_resp(resp) -> List[Dict[str, Any]]:
    """
    Normaliza respostas da API do Supabase/PostgREST:
    - Retorna lista de dicionários quando possível.
    - Lança RuntimeError com mensagem legível quando detectar erro.
    Compatível com diferentes versões do postgrest/supabase-py.
    """
    # 1) Se tiver .data -> normalmente é a lista de linhas
    try:
        if hasattr(resp, "data"):
            data = resp.data
            # Algumas respostas retornam um dicionário com 'error'
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(f"Supabase API error: {data.get('error')}")
            return data or []
    except Exception as e:
        # se ocorrer algo ao acessar .data, transforme em erro legível
        raise RuntimeError(f"Erro ao ler resp.data: {e}") from e

    # 2) Tenta extrair via json() / model_dump_json / model_dump
    try:
        # prefer model_dump_json (Pydantic v2) -> parse to dict if possible
        if hasattr(resp, "model_dump_json"):
            jtxt = resp.model_dump_json()
            import json as _json
            j = _json.loads(jtxt) if isinstance(jtxt, str) else jtxt
            if isinstance(j, dict):
                if "error" in j:
                    raise RuntimeError(f"Supabase API error: {j.get('error')}")
                if "data" in j:
                    return j.get("data") or []
        # fallback para json()
        if hasattr(resp, "json") and callable(resp.json):
            j = resp.json()
            if isinstance(j, dict):
                if "error" in j:
                    raise RuntimeError(f"Supabase API error: {j.get('error')}")
                if "data" in j:
                    return j.get("data") or []
    except Exception:
        # ignore parsing errors here; vamos tentar outros caminhos a seguir
        pass

    # 3) Se houver status code e indicar falha, reprovar
    try:
        status = None
        if hasattr(resp, "status_code"):
            status = resp.status_code
        elif hasattr(resp, "status"):
            status = resp.status
        if status is not None and (status < 200 or status >= 300):
            # tenta extrair mensagem de erro
            msg = None
            try:
                j = resp.json() if hasattr(resp, "json") else None
                if isinstance(j, dict) and "error" in j:
                    msg = j.get("error")
            except Exception:
                pass
            raise RuntimeError(f"Supabase API returned status {status}: {msg or 'sem mensagem'}")
    except Exception:
        # se deu problema ao checar status, ignoramos e deixamos o fallback
        pass

    # 4) Se for lista já, devolve
    if isinstance(resp, list):
        return resp

    # 5) Se ainda não conseguimos extrair nada razoável, lança erro genérico
    raise RuntimeError("Resposta inesperada do Supabase: formato desconhecido")
