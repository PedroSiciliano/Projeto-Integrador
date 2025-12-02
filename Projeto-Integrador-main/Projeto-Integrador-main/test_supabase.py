# test_supabase_robusto.py
from dotenv import load_dotenv
import os, traceback

load_dotenv()

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL =", SUPABASE_URL)
print("KEY =", ("<present>" if SUPABASE_KEY else "<missing>"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Env vars SUPABASE_URL / SUPABASE_KEY não configuradas")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    resp = supabase.table("plano").select("*").limit(5).execute()
except Exception:
    print("Erro ao executar a query:")
    traceback.print_exc()
    raise SystemExit(1)

print("\n--- RESP OBJECT INSPECTION ---")
print("repr(resp):", repr(resp))
print("type(resp):", type(resp))
print("dir(resp):", [a for a in dir(resp) if not a.startswith("_")])

# tentativas seguras de extrair dados/status/erro
data = None
status = None
error = None

# common attrs
if hasattr(resp, "data"):
    data = resp.data
if hasattr(resp, "status_code"):
    status = resp.status_code
elif hasattr(resp, "status"):
    status = resp.status

# some versions may pack error inside .data or .json()
if hasattr(resp, "error"):
    error = resp.error
else:
    # try resp.json() if available
    try:
        j = resp.json() if hasattr(resp, "json") else None
    except Exception:
        j = None
    # if json looks like dict and has 'error'
    if isinstance(j, dict) and "error" in j:
        error = j.get("error")
    # if data is dict-like and has 'error'
    if isinstance(data, dict) and "error" in data:
        error = data.get("error")

print("\n--- PARSED OUTPUT ---")
print("status:", status)
print("error:", error)
print("data (type={}):".format(type(data)))
print(data)
