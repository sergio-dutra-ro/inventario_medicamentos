# scripts_options.py

from pathlib import Path
from typing import Callable

import pandas as pd
import src.utils as utils

def input_script_option() -> str:
    '''
    Presents the options of available scripts.

    :return: string with the key for the script function.
    :rtype: str
    '''

    script_options = {
        '0' : 'Exit',
        '1' : 'Atualizar Estoque',
        '2' : 'Restaurar Backup',
        '3' : 'Incrementar/Decrementar Medicamento',
        }
    
    while True:
        print("Choose one option:")

        for option in script_options.items():
            print(f"\t{option[0]}: {option[1]}")

        choice = input("Choice: ")
        choice = choice.strip().lower()

        if choice in script_options:
            return choice

        print(f"\n-->ERROR: Option '{choice}' is not available\n")

def script_choice() -> Callable | None:
    '''
    Options to choose which script to run.

    :return: function for the script
    :rtype: Callable
    '''

    title = "Inventário de Medicamentos"
    title_bar= len(title) + 6
    print(f"\n{title_bar * '='}")
    print(f"   {title}   ")
    print(f"{title_bar * '='}\n")

    scripts_available = {
        '1' : update_invetory,
        '2' : restore_bak,
        '3' : update_med,
    }
    
    choice = input_script_option()
    if choice == '0' or choice not in scripts_available:
        return None
    
    return scripts_available[choice]

def update_invetory():
    csv_name = "data/inventario_remedios.csv"
    csv_path = Path(__file__).parent.parent / csv_name

    df_meds = pd.DataFrame()
    if csv_path.is_file():
      df_meds = pd.read_csv(csv_path)

    if df_meds.empty:
      print(f"[ERRO] Arquivo {csv_name} não encontrado ou vazio.")
      exit()


    title = "Atualizar Inventário"
    title_bar= len(title) + 6
    print(f"\n{title_bar * '-'}")
    print(f"   {title}   ")
    print(f"{title_bar * '-'}\n")

    print("=== Estoque atual ===")
    print(df_meds)

    print("\nAtualizando quantidade de remédios (digite -1 para cancelar)")
    stock_list = []
    for i, row in df_meds.iterrows():
      new_stock = int(
          input(f"[ATUALIZAR QUANTIDADE] {row['nome']}, {row['medicamento']} {row['dosagem']}: ")
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
            Path(__file__).parent.parent / "data/inventario_remedios_bak.csv",
            index=False,
            encoding="utf-8",
        )
        new_csv.to_csv(csv_path, index=False, encoding="utf-8")
        print("\n [SUCESSO] Estoque atualizado e backup criado com sucesso!")

        utils.push_git(commit_message="data: atualiza estoque de remedios")

    else:
      print("\n Operação cancelada.")

def restore_bak():
    base_path = Path(__file__).parent.parent
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

def update_med():
    csv_name = "data/inventario_remedios.csv"
    csv_path = Path(__file__).parent.parent / csv_name

    df_meds = pd.DataFrame()
    if csv_path.is_file():
      df_meds = pd.read_csv(csv_path)

    if df_meds.empty:
      print(f"[ERRO] Arquivo {csv_name} não encontrado ou vazio.")
      exit()

    # User Interaction
    title = "Incrementar/Decrementar Medicamento"
    title_bar= len(title) + 6
    print(f"\n{title_bar * '-'}")
    print(f"   {title}   ")
    print(f"{title_bar * '-'}\n")

    print("=== Estoque atual ===")
    print(df_meds)

    med_ID = input("\nDigite o ID do medicamento que deseja modificar: ").strip()
    print("Digite a quantidade a ser acrescentada ou subtraída:")
    print("Exemplo:")
    print("  13 => Aumenta em 13 unidades")
    print("  -7 => Diminui em 7 unidades")
    increment = input("\nDigite a quantidade (digite 'x' para cancelar): ").strip().lower()
    
    if increment == 'x':
        print("Operação cancelada.")
        return

    try:
        increment = int(increment)
    except ValueError:
        print(" [ERRO] Valor digitado inválido (deve ser um número inteiro ou 'x'). Operação Cancelada")
        return

    id_mask = df_meds['id'] == med_ID
    if not id_mask.any():
        print(f" [ERRO] Medicamento com ID '{med_ID}' não encontrado. Operação Cancelada")
        return

    # Altering DataFrame
    medicamento = df_meds.loc[id_mask, 'medicamento'].values[0]
    dosagem = df_meds.loc[id_mask, 'dosagem'].values[0]
    qtd_atual = df_meds.loc[id_mask, 'qtd_atual'].values[0]
    novo_valor = qtd_atual + increment
    
    print("\n\nConfira a quantidade a ser alterada.")
    print(f"{medicamento} {dosagem}: {qtd_atual} => {novo_valor}")

    new_csv = pd.DataFrame()
    while True:
      confirmation = input("Confirma? (S/N) ").strip().upper()

      if confirmation == "S":
        new_csv = df_meds.copy()
        new_csv.loc[id_mask, 'qtd_atual'] = novo_valor
        print("== Novo Estoque ==")
        print(new_csv)
        break
      elif confirmation == "N":
        break


    # Save File
    if not new_csv.empty:
        df_meds.to_csv(
            Path(__file__).parent.parent / "data/inventario_remedios_bak.csv",
            index=False,
            encoding="utf-8",
        )
        new_csv.to_csv(csv_path, index=False, encoding="utf-8")
        print("\n [SUCESSO] Estoque atualizado e backup criado com sucesso!")

        utils.push_git(commit_message="data: atualiza estoque de remedios")

    else:
      print("\n Operação cancelada.") 