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

        # print(aba)

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

                print(f"{cor.blue}--> Menu de operações: {cor.green}{cor.underline}{options[selec]}{cor.reset}\n")
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
                    backup = f"backups/backupError_{log}.json" # seria interessante ver o histórico de mudanças que houve no arquivo.. tipo undo do vim
                    shutil.copy("data.json", backup)
                    clear()
                    print(f"{cor.red}erro: {e}{cor.cyan}\nbackup feito em {backup}{cor.reset}")
                    sendData([])
                    exit(1)


            # ler os dados do arquivo, futuramente vou adicionar uma array para diferentes listas das opções do menu
            def readFile():
                openFile()
                if data == []:
                    print(f"{cor.bold}{cor.red}{data}")
                print(cor.faint, end="")
                print("-> {0:<3}|{1:^6}|{2:>4}".format("id","nome","cpf"))
                print(cor.reset, end="")
                print(cor.yellow)
                for i in data:
                    items = list(i.values())
                    print("> {0:<4} {1}\t{2}".format(items[0], items[1], items[2]))
                print(cor.reset)
                print(f"{cor.faint}{cor.cyan}==============================={cor.reset}\n")



            # função para inserir info no arquivo json
            # eu fiz para que o id sempre fosse maior que o ultimo id da lista, e mesmo se apagar qualquer valor o id vai ser diferente
            def writeFile():
                try:
                    nome = input(f"{cor.blue}insira seu nome: {cor.white}")
                    cpf = int(input(f"{cor.blue}insira o CPF do estudante ({cor.green}{cor.underline}apenas números{cor.reset}{cor.blue}): {cor.white}"))

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

            def searchInfo():
                info = input(f"id, nome ou cpf: {cor.white}")
                openFile()
                for i in data: # poderia usar 2 for, mas dae teria que fazer a mesma coisa em readFile :|
                    pid = i["id"]
                    nome = i["nome"]
                    cpf = i["cpf"]
                    if info in str((pid, nome, cpf)):
                        print(f"\n{cor.yellow}> {pid} {nome} {cpf}{cor.reset}\n")
                        break
                    print(f"\n{cor.lightred}não foi possivel encontrar o estudante\n") #aqui também posso colocar!!
                    break

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


    # estrutura match case para verificar e executar as funcionalidades.
    match selec:
        case 0:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        case 1:
            manage(selec)

        case 2 | 3 | 4 | 5:
            clear()
            print(f"{cor.red}EM DESENVOLVIMENTO\n")
            main()

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
