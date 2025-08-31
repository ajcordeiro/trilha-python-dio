import sys
from datetime import datetime

def desenhar_menu(menu_str: str, titulo, largura_minima=40):
    """Desenha um menu com moldura, título e largura mínima"""
    linhas = [linha for linha in menu_str.splitlines() if linha.strip() != ""]
    largura = max(len(l) for l in linhas)

    # garante largura mínima
    largura = max(largura, largura_minima)

    # topo com título centralizado
    titulo = f" {titulo} "
    largura_total = largura + 2
    meio = largura_total - len(titulo)
    esquerda = meio // 2
    direita = meio - esquerda

    print("\n╔" + "═" * esquerda + titulo + "═" * direita + "╗")

    for l in linhas:
        print("║ " + l.ljust(largura) + " ║")

    print("╚" + "═" * (largura + 2) + "╝")

    return input("=> Escolha uma opção: ")

def menu_deseja_continuar():

    while True:
        escolha = desenhar_menu(menu_continuar, titulo="DESEJA REALIZAR NOVAS OPERAÇÕES?").lower()
        if escolha == "s":
            return True
        elif escolha == "n":
            print("\nSaindo do sistema...")
            sys.exit()
        else:
            print("\nOpção inválida. Digite 's' para continuar ou 'n' para sair.")

def desenhar_extrato(extrato_lista, titulo, largura_minima=40):

    linhas = [linha for linha in extrato_lista.splitlines() if linha.strip() != ""]
    largura = max(len(l) for l in linhas)

    # garante largura mínima
    largura = max(largura, largura_minima)

    # topo com título centralizado
    titulo = f" {titulo} "
    largura_total = largura + 2
    meio = largura_total - len(titulo)
    esquerda = meio // 2
    direita = meio - esquerda

    print("\n╔" + "═" * esquerda + titulo + "═" * direita + "╗")

    for l in linhas:
        print("║ " + l.ljust(largura) + " ║")

    print("╚" + "═" * (largura + 2) + "╝")

# --- Menu ---
menu_principal = """ 
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""

menu_continuar = """ 
[s] Sim
[n] Não
"""
# --- Fim Menu ---


# --- Sistema Bancário ---

saldo = 0
limite = 500
extrato = ""
numero_saques = 0

LIMITE_SAQUES = 3

while True:

    opcao = desenhar_menu(menu_principal, titulo=" MENU PRINCIPAL ").lower()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!\n")
            data_deposito = datetime.now().strftime("%d/%m/%Y %H:%M")
            extrato += f"\n[{data_deposito}] - Depósito: R$ {valor:.2f}\n"
            menu_deseja_continuar()
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            data_saque = datetime.now().strftime("%d/%m/%Y %H:%M")
            extrato += f"\n[{data_saque}] - Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!\n")
            menu_deseja_continuar()
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        conteudo = extrato if extrato else "Não foram realizadas movimentações.\n"

        conteudo += f"\nSaldo: R$ {saldo:.2f}\n"

        desenhar_extrato(conteudo, titulo=" EXTRATO ", largura_minima=60) 
        menu_deseja_continuar()
               
    elif opcao == "q":
        print("\nSaindo do sistema...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
