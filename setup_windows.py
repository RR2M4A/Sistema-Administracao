import os
import subprocess
import ctypes
import sys
import shutil
from django.core.management.utils import get_random_secret_key

indentation = '    '

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command, description):
    """Runs a command in the terminal and displays its status."""
    print(f"\n[+] {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"{indentation}-> Sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"{indentation}-> Erro ao executar: {command}")
        print(f"{indentation}-> Detalhes: {e}")
        sys.exit(1)

def setup_env():
    """Creates or overwrites the .env file unconditionally."""
    print("\n[+] Criando/Recriando arquivo .env e gerando nova SECRET_KEY...")

    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={get_random_secret_key()}\n")
        f.write("DEBUG=False\n")

    print(f"{indentation}-> Arquivo .env gerado com sucesso!")

def open_firewall(port=5000):
    """Opens the port on the firewall."""
    rule_name = f"Recepcao_{port}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'

    print(f"\n[+] Configurando Firewall do Windows para a porta {port}...")
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
        print(f"{indentation}-> Porta liberada com sucesso no Firewall!")
    except subprocess.CalledProcessError:
        print(f"{indentation}-> Aviso: Falha ao liberar o firewall. Tem certeza que executou como Administrador?")

def setup_nssm_service():
    """Instala e configura o serviço do Windows usando o NSSM."""
    service_name = "RecepcaoGDF"

    nssm_path = shutil.which("nssm") or os.path.join(os.getcwd(), "nssm.exe")

    if not os.path.exists(nssm_path):
        print("\n[!] ERRO CRÍTICO: nssm.exe não foi encontrado!")
        print(f"{indentation}Baixe o nssm.exe e coloque-o na mesma pasta deste script.")
        sys.exit(1)

    print("\n[+] Configurando o serviço do Windows com NSSM...")

    python_exe = sys.executable
    project_dir = os.getcwd()

    # Parada e remoção silenciosa caso o serviço já exista
    subprocess.run(f'"{nssm_path}" stop {service_name}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(f'"{nssm_path}" remove {service_name} confirm', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Configuração via NSSM usando a sua função estrita
    run_command(f'"{nssm_path}" install {service_name} "{python_exe}"', "Instalando serviço base")
    run_command(f'"{nssm_path}" set {service_name} AppParameters "-m waitress --port=5000 config.wsgi:application"', "Configurando o Waitress como servidor")
    run_command(f'"{nssm_path}" set {service_name} AppDirectory "{project_dir}"', "Definindo diretório de trabalho")
    run_command(f'"{nssm_path}" set {service_name} DisplayName "Servidor Django - Recepção"', "Configurando nome de exibição")
    run_command(f'"{nssm_path}" set {service_name} Description "Backend do sistema de recepção rodando na porta 5000"', "Configurando descrição")
    run_command(f'"{nssm_path}" start {service_name}', "Iniciando o serviço no Windows")

def main():
    if not is_admin():
        print("="*60)
        print("⚠️  ATENÇÃO: Este script precisa ser executado com privilégios de Administrador.")
        print("Por favor, feche, abra o terminal como Administrador e rode novamente.")
        print("="*60)
        sys.exit(1)

    print("=== Iniciando configuração do sistema ===")

    run_command("pip install -r requirements.txt", "Instalando dependências do Python")
    setup_env()
    open_firewall(5000)
    run_command("python manage.py migrate", "Aplicando migrações do banco de dados")
    run_command("python manage.py collectstatic --noinput", "Coletando arquivos estáticos (CSS, JS, Imagens)")
    setup_nssm_service()

    print("\n" + "="*60)
    print("✅ Configuração concluída com sucesso!")
    print("O sistema está rodando em segundo plano como um Serviço do Windows.")
    print("Mesmo se o PC reiniciar, o sistema subirá sozinho.")
    print("\nPara acessar, abra o navegador e digite:")
    print("http://<IP_DESTA_MAQUINA>:5000/system/")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()