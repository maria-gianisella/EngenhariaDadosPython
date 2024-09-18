menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0.00
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(valor):
    global saldo
    global extrato

    if(valor <= 0):
        print("Valor inválido.")
        return

    saldo += valor
    extrato += f"Depósito de R$ {valor}\n"
    print(f"Depósito de R$ {valor} realizado com sucesso.")

def sacar(valor):
    global saldo
    global extrato
    global numero_saques

    if(valor > limite):
        print("Valor acima do limite. Saque não realizado.")
        return

    if(numero_saques >= LIMITE_SAQUES):
        print("Limite de saques atingido. Saque não realizado.")
        return
    
    if(valor > saldo):
        print("Saldo insuficiente. Saque não realizado.")
        return
    
    saldo -= valor
    extrato += f"Saque de R$ {valor}\n"
    numero_saques += 1
    print(f"Saque de R$ {valor} realizado com sucesso.")

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Deposito")
        valor = float(input("Digite o valor a ser depositado: "))
        depositar(valor)

    elif opcao == "s":
        print("Saque")
        valor = float(input("Digite o valor a ser sacado: "))
        sacar(valor)
       
    elif opcao == "e":
        print("Extrato")
        print(f"Saldo: R$ {saldo}")
        print(extrato)

    elif opcao == "q":
        print("Encerrando excucao...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

