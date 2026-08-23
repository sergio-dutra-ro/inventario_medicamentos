from pathlib import Path
import pandas as pd
import src.utils as utils

csv_name = "data/inventario_remedios.csv"
csv_path = Path(__file__).parent / csv_name

df_meds = pd.DataFrame()
if csv_path.is_file():
  df_meds = pd.read_csv(csv_path)

if df_meds.empty:
  print(f"[ERRO] Arquivo {csv_name} não encontrado ou vazio.")
  exit()

print("Atualizando quantidade de remédios (digite -1 para cancelar)")
stock_list = []
for i, row in df_meds.iterrows():
  # Aspas simples nas f-strings corrigidas
  new_stock = int(
      input(f"[ATUALIZAR QUANTIDADE] {row['nome']}, {row['medicamento']}: ")
  )
  if new_stock == -1:
    print("Operação cancelada.")
    exit()

  stock_list.append(new_stock)

print("\n\nConfira as quantidades a serem alteradas.")
for i, row in df_meds.iterrows():
  print(f"{row['nome']}, {row['medicamento']}: {stock_list[i]}")

new_csv = pd.DataFrame()
while True:
  confirmation = input("Confirma? (S/N) ").strip().upper()
  if confirmation == "S":
    new_csv = df_meds.copy()
    new_csv["qtd_atual"] = stock_list
    print(new_csv)
    break
  elif confirmation == "N":
    break


# Salvar o arquivo
if not new_csv.empty:
  df_meds.to_csv(
      Path(__file__).parent / "data/inventario_remedios_bak.csv",
      index=False,
      encoding="utf-8",
  )
  new_csv.to_csv(csv_path, index=False, encoding="utf-8")
  print("\n [SUCESSO] Estoque atualizado e backup criado com sucesso!")

  utils.push_git(commit_message="data: atualiza estoque de remedios")

else:
  print("\n Operação cancelada.")