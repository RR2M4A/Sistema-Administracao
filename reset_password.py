import subprocess
import os


def main():
    print("=" * 50)
    print("RECUPERAÇÃO DE SENHA DO SISTEMA")
    print("=" * 50)

    # Pergunta qual usuário deseja alterar (assume 'admin' se o usuário apenas apertar Enter)
    username = input(
        "\nDigite o nome do usuário (ou aperte Enter para 'admin'): "
    ).strip()
    if not username:
        username = "admin"

    print(f"\n[+] Iniciando redefinição para o usuário: {username}")
    print("Aviso: Por segurança, a senha NÃO aparecerá na tela enquanto você digita.\n")

    # Localiza o Python dentro da venv criada pelo script de setup
    venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

    # Verifica se o Python da venv existe antes de prosseguir
    if not os.path.exists(venv_python):
        print(f"Erro: Ambiente virtual (venv) não encontrado em {venv_python}")
        print("Certifique-se de que o script de setup foi executado primeiro.")
        input("\nPressione Enter para sair...")
        return

    # Comando nativo do Django para trocar senha
    cmd = f'"{venv_python}" manage.py changepassword {username}'

    try:
        # Passa o controle do terminal para o Django gerenciar a troca de senha
        subprocess.run(cmd, shell=True, check=True)
        print("\n✅ Senha alterada com sucesso!")
    except subprocess.CalledProcessError:
        print(
            "\n❌ Falha ao alterar a senha. Verifique se o usuário realmente existe no banco."
        )

    print("\n" + "=" * 50)
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
