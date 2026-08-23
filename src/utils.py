import subprocess
from pathlib import Path

def push_git(commit_message="data: atualiza estoque de remedios"):
  """Adiciona, comita e faz o push das alterações do repositório para o GitHub."""
  repo_root = Path(__file__).parent.parent

  try:
    print("\n[GIT] Enviando alterações para o GitHub...")

    subprocess.run(["git", "add", "."], check=True, cwd=repo_root)

    subprocess.run(
        ["git", "commit", "-m", commit_message], check=True, cwd=repo_root
    )

    subprocess.run(["git", "push"], check=True, cwd=repo_root)

    print(" [SUCESSO] Repositório atualizado no GitHub com sucesso!")

  except subprocess.CalledProcessError as e:
    print(
        f"\n [ERRO] Falha ao executar o comando Git. Código de saída:"
        f" {e.returncode}"
    )
  except Exception as e:
    print(f"\n [ERRO] Ocorreu um erro inesperado: {e}")