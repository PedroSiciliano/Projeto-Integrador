# verifica_database_source.py
import database, inspect, io, os, sys

print("database module file:", getattr(database, "__file__", "UNKNOWN"))

def safe_getsource(fn):
    try:
        s = inspect.getsource(fn)
        # limit to first 80 lines (enough pra inspecionar)
        return "\n".join(s.splitlines()[:80])
    except Exception as e:
        return f"could not get source by inspect: {e}"

print("\n--- contar_alunos_ativos (source preview) ---")
print(safe_getsource(database.contar_alunos_ativos))

print("\n--- buscar_registros_ponto (source preview) ---")
print(safe_getsource(database.buscar_registros_ponto))

# count occurrences of function names in file on disk
path = getattr(database, "__file__", None)
if path and os.path.exists(path):
    text = open(path, "r", encoding="utf-8").read()
    def count_occ(name):
        return text.count(f"def {name}(")
    names = ["contar_alunos_ativos", "calcular_receita_mes_atual", "buscar_registros_ponto", "buscar_alunos"]
    print("\n--- occurrences in file on disk ---")
    for n in names:
        print(f"{n}: {count_occ(n)}")
    print("\n--- first 120 lines of file on disk ---")
    print("\n".join(text.splitlines()[:120]))
else:
    print("\nCould not locate file on disk to inspect.")
