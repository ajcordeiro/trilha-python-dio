import textwrap
import sys
from datetime import datetime

menu = """\n
================ MENU =================
| [d]\tDepositar                     |
| [s]\tSacar                         |
| [e]\tExtrato                       |
| [q]\tSair                          |
=======================================
=> """

def menu_continuar():
    while True:
        menu = """\n
        ===== Deseja realizar novas operações? =====
        | [s]\tSim                                |
        | [n]\tNão                                |
        ============================================    
        => """
        escolha = input(textwrap.dedent(menu)).lower()

        if escolha == "s":
            return True   
        elif escolha == "n":
            print("Saindo do sistema...")
            sys.exit()   
        else:
            print("Opção inválida. Digite 's' para continuar ou 'n' para sair.")

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu).lower()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            print (f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
            extrato += f" Data Depósito: {datetime.now()}\n Valor: R$ {valor:.2f}\n\n"
           
            menu_continuar()  
            
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
            extrato += f" Data Saque: {datetime.now()} \n Valor: R$ {valor:.2f}\n\n"

            numero_saques += 1
            print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
            menu_continuar()  

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
       

        print("\n=================== EXTRATO =================== ")
        print(" Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n Saldo Total: R$ {saldo:.2f}")
        print("===============================================")

    elif opcao == "q":
        print("\nSaindo do sistema...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
