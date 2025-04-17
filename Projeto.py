# Gabriel Zaiac
# Superior em tecnologia de análise e desenvolvimento de sistemas
# fiz esse programinha para ser executado em terminal  (espeficicamente linux), não me responsabiliso por não funcionamento em outros  lugares ou plataformas (como IDE's)

# importações :D
import json
import random
import os
import shutil
import time


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

# função para limpar o terminal/console dependendo do SO :D
def clear():
    os.system('cls' if os.name == 'nt' else'clear')
clear()

# dict para opções para o menu principal + função de saida das opções + menu principal
def title():
    global options
    options = {
        1: "Estudante",
        2: "Disciplinas",
        3: "Professores",
        4: "Turmas",
        5: "Matrículas",
        0: "Saír da aplicação"
    }

    print(f"{cor.blue}<==> Menu principal <==>{cor.reset}\n")
    for i in options:
        print(f"{cor.yellow}{i}. {options[i]}")

def selected(selec):
    def manage(aba):
        clear()
        aba -= 1

        # printar menu de operações + área escolhida + função para selecionar opção para gerenciamento
        def call():
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

                print(f"{cor.blue}--> Menu de operações: {cor.bold}{cor.green}{cor.underline}{options[selec]}{cor.reset}\n")
                for i in operations:
                    print(f"{cor.pink}{i} - {operations[i]}")
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

            # abrir arquivo para gerenciar + verificar se arquivo existe. + se não, ent crie um e escreva [] nele
            # se o arquivo for alterado por fora, de um jeito fora da sintaxe, então ele gera um arquivo de backup(do erro), coloca em backups e reescreve o json atual
            #usei um numero 'aleatório' pq fiquei com preguiça de usar datetime
            def bkup(e):
                log = random.randint(100, 1000000)
                os.makedirs("backups", exist_ok=True)
                backup = f"backups/backupError_{log}.json" # seria interessante ver o histórico de mudanças que houve no arquivo.. tipo undo do vim
                shutil.copy("data.json", backup)
                clear()
                print(f"{cor.red}erro: {e}{cor.cyan}\nbackup feito em {backup}{cor.red}")
                sendData([[],[],[],[],[]])
                exit(1)

            def openFile():
                try:
                    with open(jsonPath, "r") as file:
                        global data
                        data = json.load(file)
                except FileNotFoundError:
                    sendData([[],[],[],[],[]])
                    openFile()
                except json.JSONDecodeError as e:
                    bkup(e)

            # apenas transformanda data de: [[n1],[n2]...] para [nx]
            def dataRedirect():
                try:
                    global data
                    data = list(data[aba])
                except IndexError as e:
                    bkup(e)


            # ler os dados do arquivo, futuramente vou adicionar uma array para diferentes listas das opções do menu
            # eu poderia fzr mais simples.. porém eu não teria mais controle do espaçamento entre os elementos ent deixei assim mesmo
            def readFile():
                openFile()
                dataRedirect()
                if data == []:
                    print(f"{cor.bold}{cor.red}lista vazia\n")
                    call()
                print(cor.faint, end="")
                print("-> {0:<3}|{1:^8}|{2:>4}".format("id","nome","cpf"))
                print(cor.reset, end="")
                print(cor.yellow)
                lenName = []
                for i in data:
                    lenName.append(len(i["nome"]))
                maxName =  max(lenName)
                for i in data:
                    itens = list(i.values())
                    conta = 45 - len(i["nome"])
                    non = ""
                    print(f"{cor.yellow}> {itens[0]:<4}{itens[1]}{cor.faint}{non:.>{conta}}{cor.reset}{cor.yellow}{itens[2]}")
                print(cor.reset)
                print(f"{cor.faint}{cor.cyan}{" end of list ":-^62}{cor.reset}\n")

            # função para inserir info no arquivo json
            # eu fiz para que o id sempre fosse maior que o ultimo id da lista, e mesmo se apagar qualquer valor o id vai ser diferente
            def writeFile():
                try:
                    nome = input(f"{cor.blue}insira seu nome (max. 45): {cor.white}")[:45].lower()
                    cpf = int(input(f"{cor.blue}insira o CPF do estudante ({cor.green}{cor.underline}apenas números{cor.reset}{cor.blue}): {cor.white}"))
                    if len(str(cpf)) != 11:
                        clear()
                        print(f"{cor.red}cpf inválido: 11 digitos{cor.reset}")
                        call()
                    clear()
                    print(f"{cor.green}adicionado!")
                    openFile()
                    dataRedirect()
                    codigo = len(data)
                    if data:
                        codigo -= 1
                        pid = data[codigo]["id"]
                        codigo = pid + 1
                    info = {"id": codigo, "nome": nome, "cpf": cpf}
                    openFile()
                    data[aba].append(info)
                    sendData(data)
                except ValueError:
                    print(f"{cor.red}informações inválidas :[")
                    call()

            # função para atualizar lista do json :|
            def updateInfo():
                try:
                    readFile()
                    update = int(input(f"{cor.blue}digite o id de quem deseja alterar: {cor.white}"))
                    openFile()
                    dataRedirect()
                    for i in range(len(data)):
                        if update == data[i]["id"]:
                            newName = input(f"\n{cor.blue}coloque um novo nome: {cor.white}").lower()
                            newCpf = int(input(f"{cor.blue}escolha seu nove cpf: {cor.white}"))
                            if len(str(newCpf)) != 11:
                                clear()
                                print(f"{cor.red}cpf inválido: 11 digitos{cor.reset}\n{cor.blue}")
                                updateInfo()
                            data[i]["nome"] = newName
                            data[i]["cpf"] = newCpf
                            newInfo = data[i]
                            openFile()
                            data[aba][i] = newInfo
                            sendData(data)
                            clear()
                            print(f"{cor.green}alterado!")
                            call()
                    print(f"\n{cor.red}Esse id não existe")
                except ValueError:
                    print(f"\n{cor.red}coloque corretamente as informações")

            # função para excluir info da lista em json
            def excludeInfo():
                try:
                    readFile()
                    pop = int(input(f"{cor.blue}id de quem deseja remover: {cor.white}"))
                    openFile()
                    dataRedirect()
                    for i in range(len(data)):
                        verId = data[i].get("id")
                        if pop == verId:
                            del data[i]
                            newInfo = data
                            openFile()
                            data[aba] = newInfo
                            sendData(data)
                            clear()
                            print(f"\n{cor.green}estudante excluido!")
                            call()
                    print(f"\n {cor.red}esse estudante não exite") # posso fazer no futuro para escolher a quem dizer que está sendo feito a execução ex: Estudante, Disciplinas
                except ValueError:
                    print(f"{cor.red}escolha um valor válido")

            def searchInfo():
                info = input(f"procurar por: {cor.white}")
                openFile()
                dataRedirect()
                for i in data: # poderia usar 2 for, mas dae teria que fazer a mesma coisa em readFile :|
                    pid = i["id"]
                    nome = i["nome"]
                    cpf = i["cpf"]
                    if info in str((pid, nome, cpf)):
                        print(f"{cor.yellow}> {pid} {nome} {cpf}{cor.reset}")

            # match case para executar funções acima
            # no futuro posso fazer para mandar um valor para info da área.. ex: 1: estudante 2: disciplina, para verificar em qual array colocar as informações
            match choice:
                case 0:
                    main()

                case 1:
                    readFile()

                case 2:
                    writeFile()

                case 3:
                    updateInfo()

                case 4:
                    excludeInfo()

                case 5:
                    searchInfo()

            call()
        call()


    # função para verificar e executar as funcionalidades.
    def selection(aba):
        if selec >= 1 and selec <= 5:
            manage(aba)

        elif selec == 0:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        else:
            print(f"{cor.red}acho q vc não escolher a opção correta!")
            exit(1)
    selection(selec)


# função para iniciar o código e verificar opções :P
# vai dar ValueError se n selecionar uma opção listada. e o código vai reiniciar
# se tiver interrupção do teclado com ctrl + c ou ctrl + d mostra que fechou o sistema e forçar saida sem erro
def main():
    try:
        title()
        opt = int(input(f"\n\n{cor.lightblue}Sua opção: {cor.white}"))
        if opt > -1 and opt <= len(options) - 1:
            selected(opt)
        clear()
        print(f"{cor.red}Selecione outra opção :P\n")
        main()

    except ValueError:
        clear()
        print(f"{cor.red}Tente números!!\n")
        main()

    except (KeyboardInterrupt, EOFError):
        print("\nVocê fechou o aplicativo :(")
        exit(0)

    except SystemExit:
        raise

    except Exception as e:
        print(f"\nOcorreu um erro inesperado :[ entre em contato conosco\n\n{cor.red}erro: ", e, cor.reset)
        exit(0)

main()
