#Requisito Quando abrir o aplicativo pela primeira vez, trocado a senha ou reinstalado o app.
#Entao apos realizar o login o usuario deve permanecer logado toda vez que reabrir o app.
import hashlib
import json
import os


ARQUIVO_SESSAO = "sessao.json"

class Login:
    def __init__(self, usuario, senha):
        self.__usuario = usuario
        self.__senha = senha
        
    def __gerar_token(self):
        """Gera um token simples a partir do usuário e senha."""
        dados = f"{self.__usuario}:{self.__senha}"
        return hashlib.sha256(dados.encode()).hexdigest()
    
    def autenticar(self, usuario, senha):
        """Valida se o usuario e senha estao corretos"""
        return usuario == self.__usuario and senha == self.__senha
    
    def salvar_sessao(self):
        """Salva o token de sessao localmente para manter o usuario logado."""
        token = self.__gerar_token()
        with open(ARQUIVO_SESSAO, "w") as f:
            json.dump({"usuario": self.__usuario, "token": token}, f)
    
    @staticmethod
    def sessao_existe(path):
        """Verifica se ja existe"""
        os.path.exists(path)
    
    def sessao_valida(self):
        """Confere se o token salvo corresponde ao usuario/senha atuais."""
        if not self.sessao_existe():
            return False
        with open(ARQUIVO_SESSAO, "r") as f:
            dados = json.load(f)
        token_atual = self.__gerar_token()
        return dados.get("usuario") == self.__usuario and dados.get("token") == token_atual

    @staticmethod
    def encerrar_sessao():
        """Remove a sessão salva (logout, troca de senha ou reinstalação)."""
        if os.path.exists(ARQUIVO_SESSAO):
            os.remove(ARQUIVO_SESSAO)