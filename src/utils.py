import subprocess


def push_git(commit_message="data: atualiza estoque de remedios"):
  """Adiciona, comita e faz o push das alterações do repositório para o GitHub."""
  try:
    print("\n[GIT] Enviando alterações para o GitHub...")

    # Adiciona todos os arquivos alterados
    subprocess.run(["git", "add", "."], check=True)

    # Cria o commit
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Envia para a branch atual no GitHub
    subprocess.run(["git", "push"], check=True)

    print(" [SUCESSO] Repositório atualizado no GitHub com sucesso!")

  except subprocess.CalledProcessError as e:
    print(
        f"\n [ERRO] Falha ao executar o comando Git. Código de saída:"
        f" {e.returncode}"
    )
  except Exception as e:
    print(f"\n [ERRO] Ocorreu um erro inesperado: {e}")