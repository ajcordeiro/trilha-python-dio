import sys
from abc import ABC, abstractmethod
from datetime import datetime
import os


# --- Utilidades ---
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def painel_inicial():
    titulo = " Seja bem vindo ao Banco Dio "
    largura = len(titulo) + 60
    print("╔" + "═" * largura + "╗")
    print("║" + titulo.center(largura) + "║")
    print("╚" + "═" * largura + "╝")


def desenhar_menu_principal(menu_str: str, titulo, largura_minima=40):
    """Desenha um menu com moldura, título e largura mínima"""
    linhas = [linha for linha in menu_str.splitlines() if linha.strip() != ""]
    largura = max(len(l) for l in linhas)
    largura = max(largura, largura_minima)
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


def prosseguir():
    input("\nPrecione qualquer tecla para prosseguir... ")
    limpar_tela()
    painel_inicial()


# --- Menus ---
menu_principal = """ 
[nc] Novo Cliente
[d]  Depositar 
[s]  Sacar 
[e]  Extrato
[l]  Listar Clientes
[nc] Nova Conta
[lc] Listar Contas 
[s]  Sair
"""

menu_continuar = """ 
[s] Sim 
[n] Não 
"""


# --- Classes ---
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def listar_transacoes(self):
        if not self.transacoes:
            print("\n@@@ Nenhuma transação realizada. @@@")
        else:
            print("\n=== Histórico de Transações ===\n")
            for t in self.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===\n")
            return True
        else:
            print("\n@@@ Valor inválido para depósito! @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# --- Funções de negócio ---
def listar_todos_os_clientes(clientes):
    if not clientes:
        print("\n@@@ Nenhum cliente cadastrado! @@@")
        return

    print("\n=== Lista de Clientes ===")
    for cliente in clientes:
        print(f"\n Nome: {cliente.nome}")
        print(f" CPF: {cliente.cpf}")
        print(f" Endereço: {cliente.endereco}")
        print(f" Nascimento: {cliente.data_nascimento}")

        if cliente.contas:
            print("\n Contas:")
            for conta in cliente.contas:
                print(
                    f" Agência: {conta.agencia} | Número: {conta.numero} | Saldo: R$ {conta.saldo:.2f}\n"
                )
        else:
            print("Nenhuma conta cadastrada.")

    prosseguir()


def listar_cliente_por_cpf(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return  # volta pro menu inicial

    print("\n=== Dados do Cliente ===")
    print(f" Nome: {cliente.nome}")
    print(f" CPF: {cliente.cpf}")
    print(f" Endereço: {cliente.endereco}")
    print(f" Nascimento: {cliente.data_nascimento}")

    if cliente.contas:
        print("\n Contas:")
        for conta in cliente.contas:
            print(
                f" Agência: {conta.agencia} | Número: {conta.numero} | Saldo: R$ {conta.saldo:.2f}"
            )
    else:
        print(" Nenhuma conta cadastrada.")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)

    return cliente

    prosseguir()


def criar_conta(cliente, contas):
    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"\n=== CLIENTE E CONTA CRIADO COM SUCESSO ===")
    print(f"\nCliente: {cliente.nome}")
    print(f"Conta Número: {numero_conta}")
    print(f"Agência: {conta.agencia}")

    prosseguir()


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]  # por enquanto, pega a primeira conta


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito R$: "))
    transacao = Deposito(valor)
    transacao.registrar(conta)


def extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    conta.historico.listar_transacoes()
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")


# --- Programa Principal ---
def main():
    painel_inicial()
    clientes = []
    contas = []

    # Menu principal do cliente
    while True:
        opcao = desenhar_menu_principal(
            menu_principal, titulo=" MENU PRINCIPAL "
        ).lower()

        if opcao == "nc":
            cliente = criar_cliente(clientes)
            if cliente:
                criar_conta(cliente, contas)

        elif opcao == "l":
            clientes_opcao = input(
                "Deseja listar todos os clientes ou buscar por CPF? [todos/cpf]: "
            ).lower()
            if clientes_opcao == "todos":
                listar_todos_os_clientes(clientes)
            else:
                listar_cliente_por_cpf(clientes)
            # continue

        elif opcao == "d":
            depositar(clientes)

        elif opcao == "e":
            extrato(clientes)

        elif opcao == "s":
            print("\nSaindo do sistema...")
            sys.exit()

        else:
            print("\n@@@ Opção inválida! @@@")


if __name__ == "__main__":
    main()
