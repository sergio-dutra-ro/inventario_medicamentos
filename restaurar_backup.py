from pathlib import Path
import pandas as pd
import src.utils as utils

base_path = Path(__file__).parent
csv_main = base_path / "data/inventario_remedios.csv"
csv_bak = base_path / "data/inventario_remedios_bak.csv"

if not csv_bak.is_file():
    print("[ERRO] Nenhum arquivo de backup (data/inventario_remedios_bak.csv) encontrado.")
    exit()

df_bak = pd.read_csv(csv_bak)

if df_bak.empty:
    print("[ERRO] O arquivo de backup está vazio. Restauração cancelada.")
    exit()

print("--- RESTAURAÇÃO DE BACKUP ---")
print("Dados encontrados no arquivo de backup:\n")
for _, row in df_bak.iterrows():
    print(f"• {row['nome']}, {row['medicamento']} {row['dosagem']}: Estoque {row['qtd_atual']}")

while True:
    confirmation = input("\nTem certeza que deseja restaurar este backup? (S/N): ").strip().upper()
    if confirmation == "S":
        df_bak.to_csv(csv_main, index=False, encoding="utf-8")
        print("\n [SUCESSO] O inventário principal foi restaurado a partir do backup!")
        
        utils.push_git(commit_message="fix: restaura inventario a partir do backup")
        break

    elif confirmation == "N":
        print("\n Restauração cancelada.")
        break