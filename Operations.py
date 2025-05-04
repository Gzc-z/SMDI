from util.TextColor import Cor as c, Text as text
from Operate import Operate
import os

def clear():
    os.system('cls' if os.name == 'nt' else'clear')
clear()

# misericórdia, me ajuda senhor
class Operations:
    def __init__(self, *options):
        global __dados
        __dados = options
        __dados = __dados[0]

    def selected(aba):
        if aba >= 1 and aba <= 5:
            pass

        elif aba == 0:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        else:
            print(f"{c.red}Selecione a opção correta")
            exit(1)

        clear()
        aba -= 1

        # printar menu de operações + área escolhida + função para selecionar opção para gerenciamento
        while True:
            try:
                # dicionário para operações
                operations = {
                    1: "Listar",
                    2: "Adicionar",
                    3: "Atualizar",
                    4: "Excluir",
                    5: "procurar",
                    0: "Menu principal"
                }
                text.menu(f"--> Menu de operações - {__dados[aba + 1]}")
                for i in operations:
                    print(f"{c.pink}{i} - {operations[i]}")

                choice = int(input(text.ask(f"selecione uma opção")))
                if choice not in operations.keys():
                    clear()
                    print(f"{c.red}selecione uma das opções!!\n")
                    break
                clear()
                text.menu(f"operação: {operations[choice]}")
            except ValueError:
                clear()
                print(f"{c.red}escolha números!\n")
                break

            # match case para executar as funções instanciadas
            op = Operate(aba, __dados)
            try:
                match choice:
                    case 0:
                        break
                    case 1:
                        op.readFile()

                    case 2:
                        op.writeFile()

                    case 3:
                        op.updateInfo()

                    case 4:
                        op.excludeInfo()

                    case 5:
                        op.searchInfo()
            except KeyError as e:
                op.bkup(e)
                print(f"{c.red}arquivo json obstuído")
                exit(1)
