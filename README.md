# Atividade-em-Sala---Dos-Requisitos-ao-Prot-tipo-Inicial-
Eng de software

Main: integra o sistema de Login (sessão persistente) com o
Controle de vagas de estacionamento em tempo real.

Fluxo:
    1. Ao abrir o app, verifica se já existe uma sessão válida salva
       (login.py -> sessao_valida). Se existir, o usuário entra direto,
       sem precisar digitar usuário/senha novamente.
    2. Se não houver sessão válida, pede usuário e senha, autentica e
       salva a sessão para os próximos acessos.
    3. Após autenticado, inicia o monitoramento das vagas
       (controle_vagas.py) e exibe o painel em tempo real.
