# database.py

"""
Adapter Supabase -> UI (Perfect Acqua).

Tabelas esperadas:

- aluno (
    id_aluno, nome_completo, data_nascimento, cpf, telefone, email, endereco,
    id_plano, valor_mensalidade, nome_responsavel, telefone_responsavel,
    cpf_responsavel, status, client_id, created_at, updated_at
  )

- instrutor (id_instrutor, nome_completo, cref, telefone, email, created_at, updated_at)

- aula (id_aula, id_instrutor, data, horario, observacoes, vagas, created_at, updated_at)

- ponto (id_registro, id_instrutor, data, hora_entrada, hora_saida, observacoes, created_at)

- despesas (id_despesa, data, descricao, categoria, valor)

- mensalidades (id_mensalidade, id_aluno, mes_referencia, valor_praticado,
                data_vencimento, data_pagamento, status, valor_pago, client_id)

- condicao_aluno (opcional) — se não existir, retornamos {}.
"""

from datetime import date, datetime
import uuid
import traceback
from typing import Any, Dict, List, Optional

# Tentativa de importar helper que expõe 'supabase' client
try:
    import supabase_helpers as _sb
    SUPABASE_AVAILABLE = getattr(_sb, "supabase", None) is not None
except Exception:
    _sb = None
    SUPABASE_AVAILABLE = False


def _log(msg: str):
    ts = datetime.utcnow().isoformat()
    print(f"[database {ts}] {msg}")


def _ensure_client():
    if not SUPABASE_AVAILABLE or _sb is None or getattr(_sb, "supabase", None) is None:
        raise RuntimeError(
            "Supabase client não configurado. Verifique supabase_helpers.supabase e variáveis de ambiente."
        )


def _get_client():
    _ensure_client()
    return _sb.supabase


# SAFE SELECT wrapper — returns list or [] on error
def _safe_select(
    table: str,
    select: str = "*",
    eq_filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
):
    try:
        _ensure_client()
        client = _get_client()
        qb = client.table(table).select(select)
        if eq_filters:
            for k, v in eq_filters.items():
                if v is None:
                    continue
                qb = qb.eq(k, v)
        if limit:
            qb = qb.limit(limit)

        resp = qb.execute()
        data = getattr(resp, "data", None)

        if data is None:
            return []

        # se ainda vier dict com error
        if isinstance(data, dict) and data.get("error"):
            _log(f"_safe_select: api error for table {table}: {data.get('error')}")
            return []

        return data
    except Exception as e:
        _log(f"_safe_select error on table {table}: {e}")
        return []



# -----------------------
# ALUNOS
# -----------------------

def buscar_alunos(limit: int = 1000) -> List[Dict[str, Any]]:
    rows = _safe_select("aluno", select="*", limit=limit) or []
    out: List[Dict[str, Any]] = []

    for r in rows:
        # aceitável que r seja dict; normalizamos nomes para as UIs
        try:
            id_val = r.get("id_aluno") or r.get("id")  # supabase pode retornar id ou id_aluno
            nome = r.get("nome_completo") or r.get("nome") or r.get("full_name") or ""
            out.append(
                {
                    "id_aluno": id_val,
                    "id": id_val,
                    "nome_completo": nome,
                    "nome": nome,
                    "cpf": r.get("cpf"),
                    "data_nasc": r.get("data_nascimento")
                    or r.get("data_ingresso")
                    or r.get("data_nasc"),
                    "telefone": r.get("telefone"),
                    "email": r.get("email"),
                    "endereco": r.get("endereco"),
                    "id_plano": r.get("id_plano"),
                    "valor_mensalidade": r.get("valor_mensalidade")
                    or r.get("valor_praticado")
                    or None,
                    "nome_responsavel": r.get("nome_responsavel"),
                    "telefone_responsavel": r.get("telefone_responsavel"),
                    "cpf_responsavel": r.get("cpf_responsavel"),
                    "status": r.get("status") or "",
                    "client_id": r.get("client_id"),
                    "created_at": r.get("created_at"),
                    "updated_at": r.get("updated_at"),
                }
            )
        except Exception:
            continue
    return out

def contar_alunos_ativos() -> int:
    """
    Conta alunos com status = 'Ativo' (ou sem status definido).
    """
    rows = _safe_select("aluno", select="status", limit=100000) or []
    total = 0
    for r in rows:
        st = str(r.get("status") or "").strip().lower()
        if st in ("", "ativo", "active"):
            total += 1
    return total


def buscar_aluno_por_id(id_aluno: Any) -> Optional[Dict[str, Any]]:
    """
    Busca aluno pelo ID (id_aluno ou id).
    """
    if not id_aluno:
        return None
    try:
        # tenta pelas colunas mais comuns
        for col in ("id_aluno", "id", "client_id", "cpf"):
            rows = _safe_select(
                "aluno",
                select="*",
                eq_filters={col: id_aluno},
                limit=1,
            )
            if isinstance(rows, list) and rows:
                r = rows[0]
                r["id"] = r.get("id_aluno") or r.get("id")
                return r

        # fallback: varre a lista toda
        rows = buscar_alunos(10000)
        for r in rows:
            if str(r.get("id")) == str(id_aluno) or str(r.get("id_aluno")) == str(id_aluno):
                return r
    except Exception as e:
        _log(f"buscar_aluno_por_id error: {e}\n{traceback.format_exc()}")
    return None


def buscar_condicao_aluno(id_aluno: Any) -> Dict[str, Any]:
    if not id_aluno:
        return {}
    try:
        rows = _safe_select(
            "condicao_aluno", select="*", eq_filters={"id_aluno": id_aluno}, limit=1
        )
        if isinstance(rows, list) and rows:
            return rows[0]
    except Exception as e:
        _log(f"buscar_condicao_aluno: tabela não existe ou erro: {e}")
    return {}




def adicionar_aluno(
    nome_completo: str,
    data_nascimento: str,
    cpf: str,
    telefone: Optional[str] = None,
    email: Optional[str] = None,
    endereco: Optional[str] = None,
    id_plano: Optional[int] = None,
    valor_mensalidade: Optional[float] = None,
    nome_responsavel: Optional[str] = None,
    telefone_responsavel: Optional[str] = None,
    cpf_responsavel: Optional[str] = None,
    status: str = "Ativo",
):
    _ensure_client()
    payload = {
        "nome_completo": nome_completo,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "endereco": endereco,
        "id_plano": id_plano,
        "valor_mensalidade": float(valor_mensalidade)
        if valor_mensalidade is not None
        else None,
        "nome_responsavel": nome_responsavel,
        "telefone_responsavel": telefone_responsavel,
        "cpf_responsavel": cpf_responsavel,
        "status": status,
        "client_id": str(uuid.uuid4()),
    }
    resp = _get_client().table("aluno").insert(payload).execute()
    return getattr(resp, "data", None) or resp


def criar_mensalidade_inicial_para_aluno(
    id_aluno: Any,
    valor_praticado: float,
    tipo_plano: str = "Mensal",
):
    """
    Cria uma mensalidade Pendente para o aluno recém cadastrado.
    tipo_plano: 'Mensal', 'Trimestral', 'Anual' (apenas texto em mes_referencia).
    """
    hoje = date.today()
    mes_ref = hoje.strftime("%Y-%m")
    data_venc = hoje.isoformat()

    payload = {
        "id_aluno": id_aluno,
        "mes_referencia": f"{tipo_plano} {mes_ref}",
        "valor_praticado": float(valor_praticado),
        "data_vencimento": data_venc,
        "status": "Pendente",
        "client_id": str(uuid.uuid4()),
    }
    _ensure_client()
    resp = _get_client().table("mensalidades").insert(payload).execute()
    return getattr(resp, "data", None) or resp


# -----------------------
# INSTRUTORES
# -----------------------

def buscar_instrutores(limit: int = 1000) -> List[Dict[str, Any]]:
    rows = _safe_select("instrutor", select="*", limit=limit) or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        try:
            id_val = r.get("id_instrutor") or r.get("id")
            nome = r.get("nome_completo") or r.get("nome") or ""
            out.append(
                {
                    "id_instrutor": id_val,
                    "id": id_val,
                    "nome_completo": nome,
                    "nome": nome,
                    "cref": r.get("cref"),
                    "telefone": r.get("telefone"),
                    "email": r.get("email"),
                    "cpf": r.get("cpf"),
                    "especialidade": r.get("especialidade"),
                    "created_at": r.get("created_at"),
                    "updated_at": r.get("updated_at"),
                }
            )
        except Exception:
            continue
    return out


def adicionar_instrutor(
    nome_completo: str,
    cref: str,
    telefone: Optional[str] = None,
    email: Optional[str] = None,
    especialidade: Optional[str] = None,
    cpf: Optional[str] = None,
):
    if not cref or str(cref).strip() == "":
        raise ValueError("CREF é obrigatório")
    _ensure_client()
    payload = {
        "nome_completo": nome_completo,
        "cref": cref,
        "telefone": telefone,
        "email": email,
        "cpf": cpf,
        "especialidade": especialidade,
        # nada de client_id aqui
    }
    resp = _get_client().table("instrutor").insert(payload).execute()
    return getattr(resp, "data", None) or resp



# -----------------------
# AULAS / AGENDA
# -----------------------

def buscar_aulas_com_id_por_data(data_str: str) -> List[Dict[str, Any]]:
    rows = _safe_select("aula", select="*", eq_filters={"data": data_str}) or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        try:
            id_aula = r.get("id_aula") or r.get("id")
            inicio = r.get("horario") or r.get("inicio") or ""
            nivel = r.get("observacoes") or r.get("descricao") or ""
            id_instr = r.get("id_instrutor") or r.get("instrutor_id")
            instrutor_nome = ""
            if id_instr:
                ins = None
                try:
                    ins = buscar_instrutor_por_id(id_instr)
                except Exception:
                    ins = None
                if ins:
                    instrutor_nome = (
                        ins.get("nome_completo")
                        or ins.get("nome")
                        or str(id_instr)
                    )
                else:
                    instrutor_nome = str(id_instr)
            vagas = r.get("vagas") or r.get("capacidade") or ""
            out.append(
                {
                    "id_aula": id_aula,
                    "data": data_str,
                    "horario": inicio,
                    "nivel": nivel,
                    "id_instrutor": id_instr,
                    "nome_instrutor": instrutor_nome,
                    "vagas": vagas,
                    "raw": r,
                }
            )
        except Exception:
            continue
    return out


def adicionar_aula(
    data_val: str,
    horario: str,
    id_instrutor: Any,
    duracao_minutes: int = 60,
    sala: Optional[str] = None,
    descricao: Optional[str] = None,
):
    _ensure_client()
    payload = {
        "data": data_val,          # date
        "horario": horario,        # timestamptz
        "id_instrutor": id_instrutor,
        "observacoes": descricao or "",  # texto
        # NÃO enviar nome_completo, client_id, duracao_minutes, sala etc.
    }
    resp = _get_client().table("aula").insert(payload).execute()
    return getattr(resp, "data", None) or resp




def buscar_proximas_aulas(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retorna lista de dicts: id_aula, data, horario, observacoes,
    id_instrutor, nome_instrutor, vagas
    """
    out: List[Dict[str, Any]] = []
    try:
        hoje = date.today().isoformat()
        rows = _safe_select("aula", select="*", limit=100) or []
        # filtra localmente por data >= hoje
        for r in rows:
            try:
                data_field = r.get("data") or ""
                if not data_field:
                    continue
                if str(data_field) >= hoje:
                    id_aula = r.get("id_aula") or r.get("id")
                    horario = r.get("horario") or ""
                    obs = r.get("observacoes") or r.get("descricao") or ""
                    id_instr = r.get("id_instrutor") or r.get("instrutor_id")
                    nome_instr = ""
                    if id_instr:
                        try:
                            ins = buscar_instrutor_por_id(id_instr)
                            if ins:
                                nome_instr = (
                                    ins.get("nome_completo")
                                    or ins.get("nome")
                                    or str(id_instr)
                                )
                        except Exception:
                            nome_instr = str(id_instr)
                    vagas = r.get("vagas") or ""
                    out.append(
                        {
                            "id_aula": id_aula,
                            "data": data_field,
                            "horario": horario,
                            "observacoes": obs,
                            "id_instrutor": id_instr,
                            "nome_instrutor": nome_instr,
                            "vagas": vagas,
                        }
                    )
            except Exception:
                continue
        out_sorted = sorted(out, key=lambda x: x.get("data") or "")[:limit]
        return out_sorted
    except Exception as e:
        _log(
            f"buscar_proximas_aulas direct supabase query failed, using fallback: {e}\n{traceback.format_exc()}"
        )
        return out



def buscar_alunos_da_aula(id_aula: Any) -> List[Dict[str, Any]]:
    rows = _safe_select(
        "aluno_aula", select="id_aluno", eq_filters={"id_aula": id_aula}
    ) or []
    ids = [r.get("id_aluno") for r in rows if r.get("id_aluno") is not None]
    if not ids:
        return []
    alunos = _safe_select("aluno", select="id_aluno,nome_completo", eq_filters=None) or []
    out = []
    for a in alunos:
        if a.get("id_aluno") in ids:
            out.append(
                {
                    "id_aluno": a.get("id_aluno"),
                    "nome_completo": a.get("nome_completo"),
                }
            )
    return out


def buscar_alunos_fora_da_aula(id_aula: Any) -> List[Dict[str, Any]]:
    rows = _safe_select(
        "aluno_aula", select="id_aluno", eq_filters={"id_aula": id_aula}
    ) or []
    ids_ocupados = {r.get("id_aluno") for r in rows if r.get("id_aluno") is not None}
    alunos = _safe_select("aluno", select="id_aluno,nome_completo", eq_filters=None) or []
    out = []
    for a in alunos:
        if a.get("id_aluno") not in ids_ocupados:
            out.append(
                {
                    "id_aluno": a.get("id_aluno"),
                    "nome_completo": a.get("nome_completo"),
                }
            )
    return out


def atualizar_alunos_na_aula(id_aula: Any, ids_alunos: List[Any]):
    _ensure_client()
    client = _get_client()
    # remove todos e insere de novo (simples)
    client.table("aluno_aula").delete().eq("id_aula", id_aula).execute()
    payload = [
        {"id_aula": id_aula, "id_aluno": int(i)}
        for i in ids_alunos
        if i is not None
    ]
    if payload:
        client.table("aluno_aula").insert(payload).execute()
    return True

# -----------------------
# PONTO
# -----------------------

def registrar_ponto(
    id_instrutor: Any,
    hora_entrada: Optional[str] = None,
    hora_saida: Optional[str] = None,
    observacoes: Optional[str] = None,
):
    _ensure_client()
    payload = {
        "id_instrutor": id_instrutor,
        "hora_entrada": hora_entrada,   # formato "HH:MM" ou "HH:MM:SS"
        "hora_saida": hora_saida,       # idem
        "observacoes": observacoes,
        "data": date.today().isoformat(),  # "YYYY-MM-DD" vai para a coluna date
        "client_id": str(uuid.uuid4()),
    }
    resp = _get_client().table("ponto").insert(payload).execute()
    return getattr(resp, "data", None) or resp


def buscar_registros_ponto(
    limit: int = 1000,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
) -> List[Dict[str, Any]]:
    rows = _safe_select("ponto", select="*", limit=limit) or []
    instrs = buscar_instrutores(2000)
    instr_map: Dict[str, str] = {}
    for ins in instrs:
        key = str(ins.get("id_instrutor") or ins.get("id") or "")
        instr_map[key] = ins.get("nome_completo") or ins.get("nome") or ""
        cref = ins.get("cref")
        if cref:
            instr_map[str(cref)] = ins.get("nome_completo") or ins.get("nome") or ""
    out: List[Dict[str, Any]] = []
    for r in rows:
        try:
            id_reg = r.get("id_registro") or r.get("id")
            id_instr = r.get("id_instrutor")
            nome_instr = instr_map.get(str(id_instr or ""), "")
            out.append(
                {
                    "id_registro": id_reg,
                    "id_instrutor": id_instr,
                    "nome_instrutor": nome_instr,
                    "data": r.get("data"),
                    "hora_entrada": r.get("hora_entrada") or r.get("entrada"),
                    "hora_saida": r.get("hora_saida") or r.get("saida"),
                    "observacoes": r.get("observacoes") or r.get("obs") or "",
                }
            )
        except Exception:
            continue
    return out


# -----------------------
# DESPESAS / FINANCEIRO
# -----------------------

def listar_despesas(limit: int = 200):
    rows = _safe_select("despesas", select="*", limit=limit) or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        try:
            out.append(
                {
                    "id_despesa": r.get("id_despesa") or r.get("id"),
                    "data": r.get("data"),
                    "descricao": r.get("descricao"),
                    "categoria": r.get("categoria"),
                    "valor": float(r.get("valor") or 0),
                    "client_id": r.get("client_id"),
                    "created_at": r.get("created_at"),
                    "updated_at": r.get("updated_at"),
                }
            )
        except Exception:
            continue
    return out


def adicionar_despesa(data_val: str, descricao: str, categoria: str, valor: float):
    _ensure_client()
    payload = {
        "data": data_val,
        "descricao": descricao,
        "categoria": categoria,
        "valor": float(valor),
        "client_id": str(uuid.uuid4()),
    }
    resp = _get_client().table("despesas").insert(payload).execute()
    return getattr(resp, "data", None) or resp


# -----------------------
# MENSALIDADES
# -----------------------

def listar_mensalidades(limit: int = 200):
    rows = _safe_select("mensalidades", select="*", limit=limit) or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        try:
            out.append(
                {
                    "id_mensalidade": r.get("id_mensalidade") or r.get("id"),
                    "id_aluno": r.get("id_aluno"),
                    "mes_referencia": r.get("mes_referencia"),
                    "valor_praticado": float(r.get("valor_praticado") or 0),
                    "valor_pago": float(r.get("valor_pago") or 0)
                    if r.get("valor_pago") not in (None, "")
                    else None,
                    "data_vencimento": r.get("data_vencimento"),
                    "data_pagamento": r.get("data_pagamento"),
                    "status": r.get("status"),
                    "client_id": r.get("client_id"),
                    "created_at": r.get("created_at"),
                    "updated_at": r.get("updated_at"),
                }
            )
        except Exception:
            continue
    return out


def adicionar_mensalidade(
    id_aluno: Any, mes_referencia: str, valor_praticado: float, data_vencimento: str
):
    _ensure_client()
    payload = {
        "id_aluno": id_aluno,
        "mes_referencia": mes_referencia,
        "valor_praticado": float(valor_praticado),
        "data_vencimento": data_vencimento,
        "status": "Pendente",
        "client_id": str(uuid.uuid4()),
    }
    resp = _get_client().table("mensalidades").insert(payload).execute()
    return getattr(resp, "data", None) or resp


def marcar_mensalidade_paga(
    id_mensalidade: Any,
    data_pagamento: Optional[str] = None,
    valor_pago: Optional[float] = None,
):
    try:
        _ensure_client()
        client = _get_client()
        payload: Dict[str, Any] = {"status": "Pago"}
        if data_pagamento:
            payload["data_pagamento"] = data_pagamento
        if valor_pago is not None:
            payload["valor_pago"] = float(valor_pago)
        resp = (
            client.table("mensalidades")
            .update(payload)
            .eq("id_mensalidade", id_mensalidade)
            .execute()
        )
        return getattr(resp, "data", None) or resp
    except Exception as e:
        _log(f"marcar_mensalidade_paga error: {e}\n{traceback.format_exc()}")
        return {"ok": False, "error": str(e)}


def calcular_receita_mes_atual() -> float:
    rows = _safe_select(
        "mensalidades",
        select="status,valor_praticado,valor_pago,data_vencimento",
        limit=10000,
    ) or []
    total = 0.0
    for r in rows:
        st = str(r.get("status") or "").lower()
        if st == "pago" or st == "paid":
            v = (
                r.get("valor_pago")
                if r.get("valor_pago") not in (None, "")
                else r.get("valor_praticado")
                or 0
            )
            try:
                total += float(v)
            except Exception:
                continue
    return float(total)


def calcular_despesas_mes_atual() -> float:
    rows = _safe_select("despesas", select="valor,data", limit=10000) or []
    total = 0.0
    for r in rows:
        try:
            total += float(r.get("valor") or 0)
        except Exception:
            continue
    return float(total)


# -----------------------
# CONDICAO FISICA / FICHA
# -----------------------

def buscar_condicao_aluno(id_aluno: Any) -> Dict[str, Any]:
    """
    Busca em 'condicao_aluno' por id_aluno.
    Se não existir, retorna {}.
    """
    try:
        if not id_aluno:
            return {}

        rows = _safe_select(
            "condicao_aluno",
            select="*",
            eq_filters={"id_aluno": id_aluno},
            limit=1,
        )

        if isinstance(rows, list) and rows:
            return rows[0]
    except Exception as e:
        _log(f"buscar_condicao_aluno: tabela não existe ou erro: {e}")
    return {}



def salvar_ou_atualizar_condicao(id_aluno: Any, dados: Dict[str, Any]):
    """
    Insere ou atualiza registro de condicao_aluno para o id_aluno.
    Usa select + update/insert (não depende de UNIQUE).
    """
    _ensure_client()
    client = _get_client()

    payload = {
        "id_aluno": id_aluno,
        "condicoes": dados.get("condicoes"),
        "alergias": dados.get("alergias"),
        "medicamentos": dados.get("medicamentos"),
        "restricoes": dados.get("restricoes"),
        "contato": dados.get("contato"),
        "telefone": dados.get("telefone"),
    }

    existentes = _safe_select(
        "condicao_aluno",
        select="id_condicao",
        eq_filters={"id_aluno": id_aluno},
        limit=1,
    ) or []

    if isinstance(existentes, list) and existentes:
        id_cond = existentes[0].get("id_condicao") or existentes[0].get("id")
        resp = (
            client.table("condicao_aluno")
            .update(payload)
            .eq("id_condicao", id_cond)
            .execute()
        )
    else:
        resp = client.table("condicao_aluno").insert(payload).execute()

    return getattr(resp, "data", None) or resp



# -----------------------
# UTIL
# -----------------------

__all__ = [
    "buscar_alunos",
    "adicionar_aluno",
    "buscar_aluno_por_id",
    "contar_alunos_ativos",
    "criar_mensalidade_inicial_para_aluno",
    "buscar_instrutores",
    "adicionar_instrutor",
    "buscar_instrutor_por_id",
    "buscar_aulas_com_id_por_data",
    "adicionar_aula",
    "buscar_proximas_aulas",
    "registrar_ponto",
    "buscar_registros_ponto",
    "listar_despesas",
    "adicionar_despesa",
    "listar_mensalidades",
    "adicionar_mensalidade",
    "marcar_mensalidade_paga",
    "calcular_receita_mes_atual",
    "calcular_despesas_mes_atual",
    "buscar_condicao_aluno",
    "salvar_ou_atualizar_condicao",
    "buscar_alunos_da_aula",
    "buscar_alunos_fora_da_aula",
    "atualizar_alunos_na_aula",
]
