# main.py

from pathlib import Path
import src.scripts_options as scripts

def main():

    task = scripts.script_choice()
    if task:
        task()
    
    title = "Finalizando: Inventário de Medicamentos"
    title_bar= len(title) + 6
    print(f"\n{title_bar * '='}")
    print(f"   {title}   ")
    print(f"{title_bar * '='}\n")

if __name__ == "__main__":
    main()