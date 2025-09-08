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
    input("\nPressione enter para prosseguir... ")
    limpar_tela()
    painel_inicial()


# --- Menus ---
menu_principal = """ 
[n]  Novo Cliente
[d]  Depositar 
[s]  Sacar 
[e]  Extrato
[l]  Listar Clientes
[nc] Nova Conta
[lc] Listar Contas 
[q]  Sair
"""


# --- Classes ---
class Historico:
    def __init__(self):
        self.transacoes = []
        self.eventos = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def adicionar_evento(self, descricao, conta):
        self.eventos.append(
            {
                "descricao": descricao,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "conta_numero": conta.numero,
                "conta_agencia": conta.agencia,
            }
        )

    def listar_transacoes(self):
        if not self.transacoes:
            print("\n@@@ Nenhuma transação realizada. @@@")
        else:
            print("\n=== Histórico de Transações ===\n")
            for t in self.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

    def listar_eventos(self):
        if not self.eventos:
            print("\n@@@ Nenhum evento registrado. @@@")
        else:
            print("\n=== Histórico de Eventos ===\n")
            for e in self.eventos:
                print(
                    f"Agencia: {e['conta_agencia']}\tConta: {e['conta_numero']} - "
                    f"{e['data']}\t{e['descricao']}"
                )


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
    def __init__(self, numero, cliente, data_criacao):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._data_criacao = data_criacao
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero, data_criacao):
        return cls(numero, cliente, data_criacao)

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

    @property
    def data_criacao(self):
        return self._data_criacao

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(
                f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===\n")
            return True
        else:
            print("\n@@@ Valor inválido para depósito! @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, data_criacao, limite=500, limite_saques=3):
        super().__init__(numero, cliente, data_criacao)
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


# --- Funções de negócio cliente ---
def listar_todos_os_clientes(clientes):
    if not clientes:
        print("\n@@@ Nenhum cliente cadastrado. @@@")
        return

    print("\n=== Lista de Clientes ===")
    for cliente in clientes:
        print(f"\nCliente: {cliente.nome} \t CPF: {cliente.cpf}")
        if not cliente.contas:
            print("Nenhuma conta vinculada.")
        else:
            for conta in cliente.contas:
                print("\nContas:")
                print(
                    f" Criada em: {conta.data_criacao}"
                    f"\n Agência: {conta.agencia} \t Conta: {conta.numero}"
                    f"\n Saldo: R$ {conta.saldo:.2f}"
                )
                conta.historico.listar_eventos()

    prosseguir()


def listar_cliente_por_cpf(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return  # volta pro menu inicial

    print("\n=== Dados do Cliente ===")
    print(
        f"\n Nome: {cliente.nome} \t CPF: {cliente.cpf}"
        f"\n Endereço: {cliente.endereco}"
        f"\n Nascimento: {cliente.data_nascimento}"
    )

    if cliente.contas:
        for conta in cliente.contas:
            print("\nContas:")
            print(
                f" Criada em: {conta.data_criacao}"
                f"\n Agência: {conta.agencia} \tConta: {conta.numero}"
                f"\n Saldo: R$ {conta.saldo:.2f}"
            )
    else:
        print("Nenhuma conta cadastrada.")

    prosseguir()


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
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


# --- Funções de negócio conta ---
def criar_conta(cliente, contas):
    numero_conta = len(contas) + 1
    data_criacao = datetime.now().strftime("%d-%m-%Y %H:%M")
    conta = ContaCorrente.nova_conta(cliente, numero_conta, data_criacao)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    conta.historico.adicionar_evento("Conta criada", conta)

    print(f"\n=== CLIENTE E CONTA CRIADO COM SUCESSO ==="
          f"\n Registro criado em {conta.data_criacao}\n"
          f"\n Cliente: {cliente.nome} \t CPF: {cliente.cpf}\n"
          f"\n ================= CONTA ================="
          f"\n Conta Número: {numero_conta} \tAgência: {conta.agencia}"
          )

    prosseguir()


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    print("\n=== Lista de Contas ===")
    for conta in contas:
        print(
            f"\nCriada em: {conta.data_criacao}"
            f"\nTitular: {conta.cliente.nome}"
            f"\nAgência: {conta.agencia} \tConta: {conta.numero}"
            f"\nSaldo: R$ {conta.saldo:.2f}")

    # conta.historico.listar_eventos()
    prosseguir()


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]  # por enquanto, pega a primeira conta


# --- Funções de negócio transação ---
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

        if opcao == "n":
            cliente = criar_cliente(clientes)
            if cliente:
                criar_conta(cliente, contas)

        elif opcao == "l":
            clientes_opcao = input(
                "Deseja listar todos os clientes ou buscar por CPF? [todos/cpf]: "
            ).lower()

            if clientes_opcao not in ("todos", "cpf"):
                print("\n@@@ Opção inválida! @@@")
                prosseguir()
                continue

            if clientes_opcao == "todos":
                listar_todos_os_clientes(clientes)
            elif clientes_opcao == "cpf":
                listar_cliente_por_cpf(clientes)

        elif opcao == "d":
            depositar(clientes)

        elif opcao == "e":
            extrato(clientes)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nSaindo do sistema...")
            sys.exit()

        else:
            print("\n@@@ Opção inválida! @@@")
            prosseguir()


if __name__ == "__main__":
    main()
