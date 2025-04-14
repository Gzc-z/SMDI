# Gabriel Zaiac
# Superior em tecnologia de análise e desenvolvimento de sistemas
# fiz esse programinha para ser executado em terminal  (espeficicamente linux), não me responsabiliso por não funcionamento em outros  lugares ou plataformas (como IDE's)

# importações :D
import json
import random
import os
import shutil

# classe para cores de texto
class cor:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    white = '\033[0m'
    bold = '\033[;1m'
    italic = "\033[3m"
    underline = "\033[4m"
    faint = "\033[2m"
    crossed = "\033[9m"
    blink = "\033[5m"
    negative = "\033[7m"
    end = "\033[0m"
    invert = '\033[;7m'
    reset = '\033[0;0m'


# função para limpar o terminal/console :D
def clear():
    os.system('cls' if os.name == 'nt' else'clear')
clear()

# dict para opções para o menu principal
def options():
    global options
    options = {
        1: "Estudante",
        2: "Disciplinas",
        3: "Professores",
        4: "Turmas",
        5: "Matrículas",
        0: "Saír da aplicação"
    }
options()

# função de saida das opções + menu principal
def title():
    print(f"{cor.blue}<==> Menu principal <==>{cor.reset}\n")
    for i in options:
        print(f"{cor.yellow}{i}. {options[i]}")

title()


def selected(selec):
    # função manage() que recebe para verificar qual área escolhida
    # ex: estudante, turmas, professores, matrículas
    # futuramente vai ler qual opção escolhida e interpretar em uma lista diferente as opções adicionadas
    # ex: adicionar em professores vai adicionar em uma lista diferente de adicionar em aluno
    def manage(aba):
        clear()
        # print(aba)

        #dicionário para operações
        operations = {
            1: "Listar",
            2: "Adicionar",
            3: "Atualizar",
            4: "Excluir",
            0: "Menu principal"
        }


        # printar menu de operações + área escolhida
        def menu2():
            print(f"\n{cor.blue}--> Menu de operações: {cor.green}{cor.underline}{options[selec]}{cor.reset}")
            print(cor.pink)
            for i in operations:
                print(f"{i} - {operations[i]}")


        # função para selecionar opção para gerenciamento
        def call():
            # try case para escolher opção do segundo menu
            try:
                menu2()
                print(cor.blue)
                choice = int(input(f"\nselecione uma opção: {cor.white}"))
                if choice not in operations:
                    clear()
                    print(f"{cor.red}selecione uma das opções!!")
                    call()
                clear()
                print(f"{cor.blue}operação: [{cor.underline}{cor.green}{operations[choice]}{cor.reset}{cor.blue}]\n")
            except ValueError:
                clear()
                print(f"{cor.red}escolha números!")
                call()



            # funções para gerenciamento CRUD do sistema
            jsonPath = "data.json"

            # função para mandar info pro json
            def sendData(dado):
                with open(jsonPath, "w", encoding="utf-8") as file:
                    json.dump(dado, file, indent=4)


            # abrir arquivo para gerenciar
            # verificar se arquivo existe.
            # se não, ent crie um e escreva [] nele
            # se o arquivo for alterado por fora, de um jeito fora da sintaxe, então ele gera um arquivo de backup(do erro), coloca em backups e apaga o json atual
            def openFile():
                try:
                    with open(jsonPath, "r") as file:
                        global data
                        data = json.load(file)
                except FileNotFoundError:
                    sendData([])
                    openFile()
                except json.JSONDecodeError as e:
                    #usei um numero 'aleatório' pq fiquei com preguiça de usar datetime
                    log = random.randint(100, 1000000)
                    os.makedirs("backups", exist_ok=True)
                    backup = f"backups/backupError_{log}.json"
                    shutil.copy("data.json", backup)
                    clear()
                    print(f"{cor.red}erro: {e}{cor.cyan}\nbackup feito em {backup}{cor.reset}")
                    os.remove("data.json")
                    exit(1)


            # ler os dados do arquivo, futuramente vou adicionar uma array para diferentes listas das opções do menu
            def readFile():
                openFile()
                if data == []:
                    print(f"{cor.bold}{cor.red}Não há estudantes inseridos")
                print("-> {0:<3}|{1:^6}|{2:>4}".format("id","nome","cpf"))
                print(cor.yellow)
                for i in data:
                    items = list(i.values())
                    print("> {0:<4}{1}\t {2}".format(items[0], items[1], items[2]))
                print(cor.reset)
                print(f"\n{cor.faint}{cor.cyan}==============================={cor.reset}")



            # função para inserir info no arquivo json
            # eu fiz para que o id sempre fosse maior que o ultimo id da lista, e mesmo se apagar qualquer valor o id vai ser diferente
            def writeFile():
                try:
                    nome = input(f"{cor.blue}insira seu nome: {cor.white}")
                    cpf = int(input(f"{cor.blue}insira o CPF do estudante: {cor.white}"))

                    openFile()
                    codigo = len(data)
                    if data:
                        codigo = len(data) - 1
                        pid = data[codigo]["id"]
                        codigo = pid + 1
                    info = {"id": codigo, "nome": nome, "cpf": cpf}
                    data.append(info)
                    sendData(data)
                except ValueError:
                    print(f"{cor.red}informações inválidas :[")
                    call()


            # função para excluir info da lista em json
            def excludeInfo():
                try:
                    pop = int(input(f"código de quem deseja remover: {cor.white}"))
                    openFile()
                    for i in range(len(data)):
                        verId = data[i].get("id")
                        if pop == verId:
                            del data[i]
                            sendData(data)
                            print(f"\n{cor.green}estudante excluido!")
                            call()
                    print(f"\n {cor.red}esse estudante não exite") # posso fazer no futuro para escolher a quem dizer que está sendo feito a execução ex: Estudante, Disciplinas
                except ValueError:
                    print(f"{cor.red}escolha um valor válido")

            # função para atualizar lista do json :|
            def updateInfo():
                try:
                    update = int(input(f"digite o id do aluno que deseja alterar: {cor.white}"))
                    openFile()
                    for i in range(len(data)):
                        if update == data[i]["id"]:
                            newName = input(f"\n{cor.blue}coloque um novo nome: {cor.white}")
                            newCpf = int(input(f"{cor.blue}escolha seu nove cpf: {cor.white}"))
                            data[i]["nome"] = newName
                            data[i]["cpf"] = newCpf
                            sendData(data)
                            print(f"{cor.green}estudante alterado com sucesso!")
                            call()
                    print(f"\n{cor.red}Esse estudante não existe")
                except ValueError:
                    print(f"\n{cor.red}coloque corretamente as informações")



            # match case para executar funções acima
            # no futuro posso fazer para mandar um valor para info da área.. ex: 1: estudante 2: disciplina, para verificar em qual array colocar as informações
            match choice:
                case 0:
                    init()

                case 1:
                    readFile()

                case 2:
                    writeFile()

                case 3:
                    updateInfo()

                case 4:
                    excludeInfo()
                case 5:
                    openFile()

            call()
        call()


    # estrutura match case para verificar e executar as funcionalidades.
    match selec:
        case 0:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        case 1:
            manage(selec)

        case 2 | 3 | 4 | 5:
            clear()
            print(f"{cor.red}EM DESENVOLVIMENTO")
            init()


# função de inicialização.. para mostrar o titulo (menu principal) e o primeiro menu
def init():
    title()
    main()

# função para iniciar o código e verificar opções :P
# vai dar ValueError se n selecionar uma opção listada. e o código vai reiniciar
# se tiver interrupção do teclado com ctrl + c ou ctrl + d mostra que fechou o sistema e forçar saida sem erro
def main():
    try:
        print(cor.lightblue)
        opt = int(input(f"\nSua opção: {cor.white}"))
        if opt > -1 and opt <= len(options) - 1:
            selected(opt)
        clear()
        print(f"{cor.red}Selecione outra opção :P\n")
        init()

    except ValueError as e:
        clear()
        print(f"\n{cor.red}Tente números!!\n", e)
        title()

    except (KeyboardInterrupt, EOFError):
        print("\nVocê fechou o aplicativo :(")
        exit(0)

    except SystemExit:
        raise

    except Exception as e:
        print(f"\nOcorreu um erro inesperado :[ entre em contato conosco\n\n{cor.red}erro: ", e, cor.reset)
        exit(0)

main()
