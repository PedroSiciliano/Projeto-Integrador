# teste_database.py
import database, json
from datetime import date

print("is_supabase_available:", database.is_supabase_available())
try:
    al = database.buscar_alunos(50)
    print("alunos sample (len):", len(al))
    for i, a in enumerate(al[:5]):
        print(" aluno", i, type(a), a)
except Exception as e:
    print("Erro buscar_alunos:", e)

try:
    ins = database.buscar_instrutores(50)
    print("instrutores sample (len):", len(ins))
    for i, it in enumerate(ins[:5]):
        print(" instrutor", i, type(it), it)
except Exception as e:
    print("Erro buscar_instrutores:", e)

try:
    hoje = date.today().isoformat()
    aulas = database.buscar_aulas_com_id_por_data(hoje)
    print(f"aulas hoje ({hoje}) len:", len(aulas))
    for i, a in enumerate(aulas[:5]):
        print(" aula", i, a)
except Exception as e:
    print("Erro buscar_aulas_com_id_por_data:", e)

try:
    pontos = database.buscar_registros_ponto()
    print("pontos len:", len(pontos))
    for i, p in enumerate(pontos[:5]):
        print(" ponto", i, p)
except Exception as e:
    print("Erro buscar_registros_ponto:", e)

try:
    print("contar_alunos_ativos():", database.contar_alunos_ativos())
    print("calcular_receita_mes_atual():", database.calcular_receita_mes_atual())
    print("calcular_despesas_mes_atual():", database.calcular_despesas_mes_atual())
except Exception as e:
    print("Erro metrics:", e)
