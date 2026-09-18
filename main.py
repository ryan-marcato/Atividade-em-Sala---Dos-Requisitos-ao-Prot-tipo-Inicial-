

import time
import getpass

from login import Login
from controle_vagas import Estacionamento


# Simula uma "base de usuários" cadastrados no sistema.
# Em um cenário real, isso viria de um banco de dados.
USUARIOS_CADASTRADOS = {
    "admin": "1234",
    "operador": "senha123",
}

MAX_TENTATIVAS = 3


def verificar_sessao_ativa():
    """
    Percorre os usuários cadastrados e verifica se algum deles possui
    uma sessão salva e válida (login persistente entre aberturas do app).
    """
    for usuario, senha in USUARIOS_CADASTRADOS.items():
        login = Login(usuario, senha)
        if login.sessao_valida():
            return login
    return None


def realizar_login():
    """Solicita usuário e senha no terminal e tenta autenticar."""
    usuario_input = input("Usuário: ").strip()
    senha_input = getpass.getpass("Senha: ")

    if usuario_input not in USUARIOS_CADASTRADOS:
        print("Usuário não encontrado.\n")
        return None

    login = Login(usuario_input, USUARIOS_CADASTRADOS[usuario_input])

    if login.autenticar(usuario_input, senha_input):
        login.salvar_sessao()
        return login

    print("Usuário ou senha incorretos.\n")
    return None


def autenticar_usuario():
    """
    Retorna um objeto Login autenticado, ou None se o usuário
    esgotar as tentativas.
    """
    login = verificar_sessao_ativa()
    if login:
        print(f"Sessão ativa encontrada. Bem-vindo de volta, {login.usuario}!\n")
        return login

    tentativas_restantes = MAX_TENTATIVAS
    while tentativas_restantes > 0:
        login = realizar_login()
        if login:
            print(f"Login realizado com sucesso! Bem-vindo, {login.usuario}.\n")
            return login
        tentativas_restantes -= 1
        if tentativas_restantes > 0:
            print(f"Tentativas restantes: {tentativas_restantes}\n")

    print("Número máximo de tentativas excedido. Encerrando.")
    return None


def iniciar_painel_vagas(total_vagas=10, intervalo_sensores=1.5, intervalo_painel=5):
    """Inicia o monitoramento em tempo real e exibe o painel periodicamente."""
    estacionamento = Estacionamento(total_vagas=total_vagas)
    estacionamento.iniciar_monitoramento(intervalo_segundos=intervalo_sensores)

    try:
        while True:
            time.sleep(intervalo_painel)
            estacionamento.exibir_painel()
    except KeyboardInterrupt:
        estacionamento.parar_monitoramento()
        print("\nMonitoramento encerrado.")


def main():
    print("=" * 46)
    print("  SISTEMA DE CONTROLE DE ESTACIONAMENTO")
    print("=" * 46 + "\n")

    login = autenticar_usuario()
    if login is None:
        return

    iniciar_painel_vagas()


if __name__ == "__main__":
    main()
