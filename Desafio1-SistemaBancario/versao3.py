from abc import ABC, abstractmethod

class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

class Historico:
    def __init__(self):
        self.transacoes = []
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Cliente:
    def __init__(self, endereco, contas=[]):
        self.endereco = endereco
        self.contas = contas

    def realizar_transacao(self, conta, transacao):
        if conta not in self.contas:
            print("Conta não encontrada.")
            return

        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)
        print("Transação realizada com sucesso.")
        if conta not in self.contas:
            print("Conta não encontrada.")
            return

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, **kwargs):
        super().__init__(**kwargs)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    limite = 500
    limite_saques = 3

    def __init__(self, numero, agencia, cliente, historico,  saldo=0):
        self._saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo += valor
    
    def nova_conta(self, cliente, numero):
        return Conta(saldo=0, numero=numero, agencia="0001", cliente=cliente, historico=Historico())
    
    def sacar(self, valor):
        if(valor > self.limite):
            print("Valor acima do limite. Saque não realizado.")
            return False

        if(numero_saques >= self.limite_saques):
            print("Limite de saques atingido. Saque não realizado.")
            return False
        
        if(valor > self.saldo):
            print("Saldo insuficiente. Saque não realizado.")
            return False

        self.saldo(-valor)
        numero_saques += 1
        self.historico.adicionar_transacao(f"Saque de R$ {valor}")
        print(f"Saque de R$ {valor} realizado com suceso.")
        return True

    def depositar(self, valor):
        if(valor <= 0):
            print("Valor inválido. Depósito não realizado.")
            return False

        self.saldo(valor)
        self.historico.adicionar_transacao(f"Depósito de R$ {valor}")
        print(f"Depósito de R$ {valor} realizado com sucesso.")
        return True

class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, **kwargs):
        super().__init__(**kwargs)
        self.limite = limite
        self.limite_saques = limite_saques

def menu():
    menu = """\n
    === Menu ===
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """

    print(menu)
    return input("Digite a opção desejada: ").lower()


def exibir_extrato(conta):
    print("\n=== Extrato ===")
    for transacao in conta.historico.transacoes:
        print(transacao)
    print(f"\nSaldo: R$ {conta.saldo}")
    print("=========================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço: ")

    usuario = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
    usuarios.append(usuario)
    print("=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)

    if usuario:
        conta = ContaCorrente(numero=numero_conta, agencia=agencia, cliente=usuario, historico=Historico(), limite=Conta.limite, limite_saques=Conta.limite_saques)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta

    print("\nERRO: Usuário não encontrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
              C/C:\t\t{conta.numero}

          """
        print("=" * 100)
        print(linha)

        print("\n")


def main():
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            usuario = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            valor = float(input("Informe o valor do depósito: "))
            conta = usuario.contas[0]  # Considerando que o usuário tem apenas uma conta
            usuario.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            usuario = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            valor = float(input("Informe o valor do saque: "))
            conta = usuario.contas[0]  # Considerando que o usuário tem apenas uma conta
            usuario.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            usuario = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            conta = usuario.contas[0]  # Considerando que o usuário tem apenas uma conta
            exibir_extrato(conta)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()