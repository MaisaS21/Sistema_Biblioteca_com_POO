#========================================================================================
# Funções auxiliares (carrega dados, salva dados, converte data para string e vice versa, lê strings, lê numeros inteiros, lê numero de telefone padrão e verifica senha do adm para pagar multas)
# =======================================================================================
# Bibliotecas
from rich import inspect
from rich import print 
import os 
import json
from datetime import datetime
# =======================================================================================
ARQUIVO = 'biblioteca.json'
# =======================================================================================

def carregar_dados(arquivo):
    """
    Verifica se o arquivo já existe no disco, se sim ele lê o conteúdo, se não, retorna um dicionário vazio (para não quebrar)
    """

    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

# =======================================================================================
def salvar_dados(dados, arquivo):
    """
    Recebe os dados(dicionário), o nome do arquivo e salva em JSON;
    Se o arrquivo não existir ele cria, se existir, sobrescreve.
    """

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# =======================================================================================
def data_para_string(data):
    """
    Converte um objeto date em uma string no  formato 'AAAA-MM-DD'
    """
    return data.strftime('%Y-%m-%d')

# =======================================================================================
def string_para_data(texto):
    """
    Converte uma string no formato 'AAAA-MM-DD'
    """

    return datetime.strptime(texto, '%Y-%m-%d').date()

# =======================================================================================
def leiaint(msg, tentativas=3):
    """Lê números inteiros com até 3 tentativas com marcação de quantas restam, após, retorna ao menu"""

    for tentativa in range(1, tentativas + 1):
        try:
            return int(input(msg))
        except (ValueError, TypeError):
            restantes = tentativas - tentativa
            if restantes > 0:
                print(f'\n[red]Valor inválido! Tentativas restantes: {restantes}[/]')
            else:
                print(f'\n[red]Limite de {tentativas} tentativas excedido![/]')
                return None
        except KeyboardInterrupt:
            print('\n[red]Operação cancelada.[/]')
            return None

# =======================================================================================
def leia_string(msg, tentativas=2):
    """Lê strings não vazias com até 2 tentativas, mostra quantas ainda faltam também"""

    for tentativa in range(1, tentativas + 1):
        valor = input(msg).strip().title()
        if valor != "":
            return valor
        else:
            restantes = tentativas - tentativa
            if restantes > 0:
                print(f'\n[red]Valor não pode ficar vazio! Tentativas restantes: {restantes}[/]')
            else:
                print(f'\n[red]Limite de {tentativas} tentativas excedido![/]')
                return None

# =======================================================================================
def leia_telefone(msg, tentativas=2):
    """Lê telefone de exatamente 11 dígitos com até 2 tentativas, percorre cada caractere do telefone e só adiciona se for numero (0-9)"""

    for tentativa in range(1, tentativas + 1):
        telefone = input(msg).strip()
        
        telefone_limpo = ""
        for caractere in telefone:
            if caractere.isdigit():
                telefone_limpo = telefone_limpo + caractere
        
        if len(telefone_limpo) == 11:
            return telefone_limpo
        else:
            restantes = tentativas - tentativa
            if restantes > 0:
                print(f'[red][bold]---------> [/]Telefone deve ter 11 dígitos! Tentativas restantes: {restantes}[/]\n[deep_pink1]TELEFONE:[/] ', end=' ')
            else:
                print(f'\n[red]Limite de {tentativas} tentativas excedido![/]')
                return None

# =======================================================================================
SENHA_ADMIN = "admin123"  

def verificar_senha(tentativas=3):
    """Verifica a senha do administrador com até 3 tentativas, mostra quantas faltam até retornar ao menu ou estar correta"""
    
    for tentativa in range(1, tentativas + 1):
        print('🔐[bold] Senha do administrador:[/] ',end=' ')
        senha = input(" ").strip()
        if senha == SENHA_ADMIN:
            return True
        else:
            restantes = tentativas - tentativa
            if restantes > 0:
                print(f"[red]❌ Senha incorreta! Tentativas restantes: {restantes}[/]")
            else:
                print(f"\n[red]❌ Limite de tentativas excedido!\n              [red][bold]======> Operação cancelada <======[/][/]\n")
                return False
    return False
#========================================================================================