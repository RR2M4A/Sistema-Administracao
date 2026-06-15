import os
import subprocess
import ctypes
import sys
import shutil
import socket

INDENTATION = '    '
SYSTEM_PORT = 9130 

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
        print(f"{INDENTATION}-> Sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"{INDENTATION}-> Erro ao executar: {command}")
        print(f"{INDENTATION}-> Detalhes: {e}")
        sys.exit(1)

def check_port_in_use(port):
    """Checks if the port is already in use. Returns True if occupied."""
    print(f"\n[+] Verificando disponibilidade da porta {port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # If connect_ex returns 0, the port is occupied
        if s.connect_ex(('127.0.0.1', port)) == 0:
            print(f"{INDENTATION}-> A porta {port} já está em uso. Assumindo que é o nosso próprio serviço.")
            return True
        else:
            print(f"{INDENTATION}-> A porta {port} está livre!")
            return False

def setup_venv():
    """Creates the virtual environment if it doesn't exist and returns the isolated Python path."""
    venv_dir = os.path.join(os.getcwd(), "venv")
    python_exe = os.path.join(venv_dir, "Scripts", "python.exe")

    if not os.path.exists(venv_dir):
        print("\n[+] Criando Ambiente Virtual (venv)...")
        subprocess.run(f'"{sys.executable}" -m venv venv', shell=True, check=True)
        print(f"{INDENTATION}-> Venv criada com sucesso na pasta /venv/")
    else:
        print("\n[+] Ambiente Virtual (venv) já existe. Pulando criação.")

    return python_exe

def setup_env():
    """Creates or overwrites the .env file unconditionally."""
    print("\n[+] Criando/Recriando arquivo .env e gerando nova SECRET_KEY...")

    import secrets
    new_key = secrets.token_urlsafe(50)

    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={new_key}\n")
        f.write("DEBUG=False\n")

    print(f"{INDENTATION}-> Arquivo .env gerado com sucesso!")

def open_firewall(port):
    """Opens the specified port on the Windows firewall."""
    rule_name = f"Recepcao_{port}"
    
    # 1. Silently deletes the old rule (if it exists) to avoid duplicates
    cmd_delete = f'netsh advfirewall firewall delete rule name="{rule_name}"'
    subprocess.run(cmd_delete, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Creates the new rule
    cmd_add = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'

    print(f"\n[+] Configurando Firewall do Windows para a porta {port}...")
    try:
        subprocess.run(cmd_add, shell=True, check=True, stdout=subprocess.DEVNULL)
        print(f"{INDENTATION}-> Porta liberada com sucesso no Firewall!")
    except subprocess.CalledProcessError:
        print(f"{INDENTATION}-> Aviso: Falha ao liberar o firewall. Tem certeza que executou como Administrador?")

def create_superuser(python_exe, username="admin", password="admin"):
    """Creates a default administrator user using the venv's Python."""
    print(f"\n[+] Criando usuário administrador padrão ({username})...")
    
    # Temporarily injects the password into the environment for this command only
    env = os.environ.copy()
    env["DJANGO_SUPERUSER_PASSWORD"] = password
    
    cmd = f'"{python_exe}" manage.py createsuperuser --noinput --username {username} --email {username}@gdf.df.gov.br'
    
    # capture_output prevents ugly errors from polluting the terminal if the user already exists
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{INDENTATION}-> Sucesso! (Usuário: {username} | Senha: {password})")
        print(f"{INDENTATION}-> RECOMENDAÇÃO: Troque esta senha no painel administrativo depois.")
    elif "already exists" in result.stderr or "já existe" in result.stderr:
        print(f"{INDENTATION}-> O usuário '{username}' já existe no banco de dados. Pulando criação.")
    else:
        print(f"{INDENTATION}-> Aviso: Não foi possível criar o administrador automaticamente.")
        print(f"{INDENTATION}-> Detalhe: {result.stderr.strip() or result.stdout.strip()}")

def setup_nssm_service(python_exe, port):
    """Installs and configures the Windows service using NSSM and the venv's Python."""
    service_name = "RecepcaoGDF"
    nssm_path = shutil.which("nssm") or os.path.join(os.getcwd(), "nssm.exe")

    if not os.path.exists(nssm_path):
        print("\n[!] ERRO CRÍTICO: nssm.exe não foi encontrado!")
        print(f"{INDENTATION}Baixe o nssm.exe e coloque-o na mesma pasta deste script.")
        sys.exit(1)

    print("\n[+] Configurando o serviço do Windows com NSSM...")
    project_dir = os.getcwd()

    # Silent stop and removal in case the service already exists
    subprocess.run(f'"{nssm_path}" stop {service_name}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(f'"{nssm_path}" remove {service_name} confirm', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # NSSM configuration parameters
    run_command(f'"{nssm_path}" install {service_name} "{python_exe}"', "Instalando serviço base")
    run_command(f'"{nssm_path}" set {service_name} AppParameters "-m waitress --port={port} config.wsgi:application"', "Configurando o Waitress como servidor")
    run_command(f'"{nssm_path}" set {service_name} AppDirectory "{project_dir}"', "Definindo diretório de trabalho")
    run_command(f'"{nssm_path}" set {service_name} DisplayName "Servidor Django - Recepção"', "Configurando nome de exibição")
    run_command(f'"{nssm_path}" set {service_name} Description "Backend do sistema de recepção rodando na porta {port}"', "Configurando descrição")
    run_command(f'"{nssm_path}" start {service_name}', "Iniciando o serviço no Windows")

def main():
    if not is_admin():
        print("="*60)
        print("⚠️  ATENÇÃO: Este script precisa ser executado com privilégios de Administrador.")
        print("Por favor, feche, abra o terminal como Administrador e rode novamente.")
        print("="*60)
        sys.exit(1)

    print("=== Iniciando configuração do sistema ===")

    # Checks the port and stores the status
    port_in_use = check_port_in_use(SYSTEM_PORT)

    python_exe = setup_venv()

    run_command(f'"{python_exe}" -m pip install -r requirements.txt', "Instalando dependências na venv")
    
    setup_env()
    
    # Only configures the firewall if the port is free
    if not port_in_use:
        open_firewall(SYSTEM_PORT)
    else:
        print(f"\n[+] Pulando configuração de Firewall (porta {SYSTEM_PORT} assumida como já configurada).")
    
    run_command(f'"{python_exe}" manage.py migrate', "Aplicando migrações do banco de dados")
    
    create_superuser(python_exe)
    
    run_command(f'"{python_exe}" manage.py collectstatic --noinput', "Coletando arquivos estáticos")
    
    # NSSM will stop the service (freeing the port) and start it again, updated!
    setup_nssm_service(python_exe, SYSTEM_PORT)

    print("\n" + "="*60)
    print("✅ Configuração concluída com sucesso!")
    print("O sistema está rodando em segundo plano como um Serviço do Windows isolado.")
    print("\nPara acessar, abra o navegador e digite:")
    print(f"http://<IP_DESTA_MAQUINA>:{SYSTEM_PORT}/system/")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
