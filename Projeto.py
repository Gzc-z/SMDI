# Gabriel Zaiac
# Superior em tecnologia de análise e desenvolvimento de sistemas
# fiz esse programinha para ser executado em terminal  (espeficicamente linux), não me responsabiliso por não funcionamento em outros ambientes ;-;

# não leia o código :[

# importações :D
import json
import random
import os
import shutil
import datetime


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
    reyellow = '\033[0;0m\033[93m'

# função para limpar o terminal/console dependendo do SO :D
def clear():
    os.system('cls' if os.name == 'nt' else'clear')
clear()

# dict para opções para o menu principal + função de saida das opções + menu principal
def title():
    global options
    options = {
        1: "Estudante",
        2: "Professor",
        3: "Disciplinas",
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

            # verificar se arquivo existe e criar um backup (do arquivo atual) se estiver com erro de sintaxe resscrevendo o arquivo atual
            def bkup(e):
                log = datetime.datetime.now().strftime("%d%m%y_%X")
                os.makedirs("backups", exist_ok=True)
                backup = f"backups/backupError_{log}.json"
                shutil.copy("data.json", backup)
                clear()
                print(f"{cor.red}erro: {e}{cor.cyan}\nbackup feito em {backup}{cor.red}")
                sendData([[],[],[],[],[]])
                exit(1)

            # função para abrir o arquivo e escrevendo as informações em data. escrever [[],[]] se n existir
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

            # função de input de informações. Usada por write e update
            def groupInput(send) -> dict:
                def verify():
                    if data:
                        for i in data:
                            if aba in (0, 1):
                                if codigo == i["id"]:                                           # vou mexer aqui depois verificação para ver se o id ja existe
                                    raise ValueError(f"O id já existe")
                            if aba == 2:
                                if idDisciplina == i["codigo"]:
                                    raise ValueError(f"O id já existe")
                try:
                    match aba:
                        case 0 | 1:
                            codigo = input(f"{cor.blue}digite o código do {options[aba + 1]} (max: 5): {cor.white}")[:5]
                            codigo = int(codigo)
                            nome = input(f"{cor.blue}insira o nome do {options[aba + 1]} (max. 45): {cor.white}")[:45].title()
                            cpf = int(input(f"{cor.blue}insira o CPF do {options[aba + 1]} (apenas números{cor.reset}{cor.blue}): {cor.white}"))
                            cpf = str(cpf)
                            if len(cpf) != 11:
                                clear()
                                print(f"{cor.red}cpf inválido: cpf apenas 11 digitos{cor.reset}")
                                call()
                            info = {"id": codigo, "nome": nome, "cpf": cpf}

                        case 2:
                            idDisciplina = int(input(f"{cor.blue}Informe o código da disciplina (max: 6): {cor.white}"))
                            nomeDisciplina = input(f"{cor.blue}Nome da disciplina: {cor.white}")
                            info = {"codigo": int(str(idDisciplina)[:6]), "disciplina": nomeDisciplina}

                        case 3:
                            idClass = int(input(f"{cor.blue}código da turma: {cor.white}"))
                            idProf = int(input(f"{cor.blue}código do professor: {cor.white}"))
                            idDisciplina = int(input(f"{cor.blue}Informe o código da disciplina: {cor.white}"))
                            info = {"idTurma": idClass, "idProf": idProf, "idDisciplina": idDisciplina}

                        case 4:
                            idClass = int(input(f"{cor.blue}código da turma: {cor.white}"))
                            idEstudante = int(input(f"{cor.blue}código do estudante: {cor.white}"))
                            info = {"idTurma": idClass, "idEstudante": idEstudante}

                    # if recebido de write para verificar os ids :D
                    if send == None:
                        verify()
                    return info
                except ValueError as e:
                    clear()
                    print(f"{cor.red}informações inválidas :[\n{cor.red}{e}")
                    call()


            # ler os dados do json
            # misericórdia
            non = ""
            def readFile():
                openFile()
                if data[aba] == []:
                    print(f"{cor.bold}{cor.red}lista vazia\n")
                    call()
                dataRedirect()
                match aba:
                    case 1 | 0:
                        print(cor.faint, "-> {0:<3}|{1:^8}|{2:>4}".format("id","nome","cpf"), end=f"\n\n{cor.yellow}")
                        for i in data:
                            cpf = i["cpf"]
                            viewCpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
                            conta = 45 - len(i["nome"])
                            print(f"{cor.reset}{cor.yellow}> {i["id"]:<6}{i["nome"]}{cor.faint}{non:.>{conta}}{cor.reset}{cor.yellow}{viewCpf}")
                    case 2:
                        print(cor.faint, f"-> código -- disciplina{cor.reset}\n")
                        for i in data:
                            print(f"{cor.yellow}>", i["codigo"], f"{cor.faint}{'':.>{13 - len(str(i['codigo']))}}{cor.reyellow}{i['disciplina']}")

                    case 3:
                        print(cor.faint, f"códigos: -> turma | professor | disciplina{cor.reset}\n")
                        for i in data:
                            print(f"{cor.yellow}> {cor.faint}turma:{cor.reyellow}{i['idTurma']:<8} {cor.faint}professor:{cor.reyellow}{i['idProf']:<8} {cor.faint}disciplina:{cor.reyellow}{i['idDisciplina']:<8}")

                    case 4:
                        print(cor.faint, f"códigos: -> turma | estudante{cor.reset}\n")
                        for i in data:
                            print(f"{cor.yellow}> {cor.faint}turma: {cor.reyellow}{i['idTurma']:<10}{cor.faint}estudante: {cor.reyellow}{i['idEstudante']}")

                print(cor.reset)
                print(f"{cor.faint}{cor.cyan}{" end of list ":-^62}{cor.reset}\n")

            # função para inserir info no arquivo json
            def writeFile():
                openFile()
                dataRedirect()
                info = groupInput(None)

                openFile()
                data[aba].append(info)
                sendData(data)
                print(f"\n{cor.green}adicionado!")

            # função para atualizar lista do json :|
            # verifica no meio da função se ja existe um id desse tipo                   # acho q talvez eu mexa aqui também
            def updateInfo():
                try:
                    readFile()
                    openFile()
                    dataRedirect()
                    update = int(input(f"{cor.blue}digite o id que deseja alterar (primeiro id): {cor.white}"))
                    for i in range(len(data)):
                        verId = list(data[i].values())[0]
                        if update == verId:
                            print(f"{cor.green}novos dados:\n")
                            info = groupInput("upt")
                            count = 0
                            for a in range(len(data)):
                                if list(data[a].values())[0] == list(info.values())[0]:
                                    count += 1
                            if list(data[i].values())[0] == list(info.values())[0]:
                                count -= 1
                            if count != 0:
                                clear()
                                print(f"{cor.red}esse id ja existe!\n")
                                call()
                            data[i] = info
                            newInfo = data
                            openFile()
                            data[aba] = newInfo
                            sendData(data)
                            clear()
                            print(f"{cor.green}alterado!\n")
                            call()
                    print(f"\n{cor.red}Esse id não existe")
                except ValueError:
                    print(f"\n{cor.red}coloque corretamente as informações")

            # função para excluir info da lista em json
            # pede o primeiro id para excluí-lo
            def excludeInfo():
                try:
                    readFile()
                    pop = int(input(f"{cor.blue}id de quem deseja remover: {cor.white}"))
                    openFile()
                    dataRedirect()
                    for i in range(len(data)):
                        verId = list(data[i].values())[0]
                        if pop == verId:
                            del data[i]
                            newInfo = data
                            openFile()
                            data[aba] = newInfo
                            sendData(data)
                            clear()
                            print(f"\n{cor.green}excluido!")
                            call()
                    print(f"\n {cor.red}esse id não exite")
                except ValueError:
                    print(f"{cor.red}escolha um valor válido")

            # função para procurar pelo primeiro id
            # ele printa de um jeito legal e espaçoso
            def searchInfo():
                info = input(f"pesquisar por: {cor.white}")
                openFile()
                dataRedirect()
                print("")
                for i in data:
                    for j in i.values():
                        if info in str(j):
                            vals = list(i.values())
                            print(f"{cor.yellow}> ", *[f"{j:<32}" for j in vals])
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

    # except Exception as e:
    #     print(f"\nOcorreu um erro inesperado :[ entre em contato conosco\n\n{cor.red}erro: ", e, cor.reset)
    #     exit(0)

main()
