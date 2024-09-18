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


def depositar(saldo, valor, extrato, /):
    if(valor <= 0):
        print("Valor inválido.")
        return saldo, extrato
    
    saldo += valor
    extrato += f"Depósito de R$ {valor}\n"
    print(f"Depósito de R$ {valor} realizado com sucesso.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if(valor > limite):
        print("Valor acima do limite. Saque não realizado.")
        return saldo, extrato

    if(numero_saques >= limite_saques):
        print("Limite de saques atingido. Saque não realizado.")
        return saldo, extrato
    
    if(valor > saldo):
        print("Saldo insuficiente. Saque não realizado.")
        return saldo, extrato

    saldo -= valor
    extrato += f"Saque de R$ {valor}\n"
    numero_saques += 1
    print(f"Saque de R$ {valor} realizado com suceso.")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n=== Extrato ===")
    if extrato:
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")

    print(f"Saldo: R$ {saldo}")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")

    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("\nERRO: Usuário já cadastrado!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nERRO: Usuário não encontrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)
        print("\n")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

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