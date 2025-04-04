from util.cor import cor, fundo

import json
import time

# função para limpar o terminal/console :D
def clear():
    print("\n" * 30)
clear()

# opções para o menu principal
options = {
    1: "Estudante",
    2: "Disciplinas",
    3: "Professores",
    4: "Turmas",
    5: "Matrículas",
    0: "Saír da aplicação"
}

# função de saida das opções + menu principal
def title():
    print(f"{cor.blue}<==> Menu principal <==>{cor.reset}\n")
    for i in options:
        print(f"{cor.yellow}{i}. {options[i]}")
title()


# função para operações
def selected(selec):
    # função que recebe de match case que futuramente vai verificar e inserir dados nos campos escolhidos
    def manage(aba):
        clear()
        # print(aba)

        #dicionário para operações
        operations = {
            1: "Listar",
            2: "Incluir",
            3: "Atualizar",
            4: "Excluir",
            0: "menu principal"
        }


        # printar menu de operações + área escolhida
        def menu2():
            print(f"\n{cor.blue}--> Menu de operações: {cor.green}{cor.underline}{options[selec]}{cor.reset}")
            print(cor.pink)
            for i in operations:
                print(f"{i} - {operations[i]}")


        # == == == == == == == == == == == == == call == == == == == == == == == == == == #
        # função para selecionar opção para gerenciamento
        def call():
            try:
                menu2()
                print(cor.blue)
                choice = int(input(f"\nselecione uma opção: "))
                if choice not in operations:
                    clear()
                    print(f"{cor.red}selecione uma das opções!!")
                    call()
                clear()
                print(f"operação: {cor.blue}[{cor.underline}{cor.green}{operations[choice]}{cor.reset}{cor.blue}]\n")
            except ValueError:
                clear()
                print(f"{cor.red}escolha números!")
                call()



            # funções para gerenciamento CRUD do sistema
            jsonPath = "data.json"


            def openFile():
                with open(jsonPath, "r") as file:
                    global data
                    data = json.load(file)

            def readFile():
                if data == []:
                    print(f"{cor.bold}{cor.red}Não há estudantes cadastrados")
                for i in data:
                    print(f"{cor.yellow} > {i}{cor.reset}")
                print(f"\n{cor.faint}{cor.cyan}==============================={cor.reset}")



            def writeFile():
                try:
                    newUser = input(f"{cor.blue}insira seu nome: {cor.white}") #posso colocar idade no futuro...
                    openFile()
                    data.append(newUser)
                    with open(jsonPath, "w") as file:
                        json.dump(data, file, indent=4)

                except ValueError:
                    print(f"{cor.red}esse não é seu nome :[")
                    call()


            # verificar se arquivo existe.
            try:
                openFile()
            except FileNotFoundError:
                with open(jsonPath, "w") as file:
                    json.dump([], file, indent=4)

            # match case para executar funções acima
            match choice:
                case 0:
                    init()

                case 1:
                    openFile()
                    readFile()

                case 2:
                    writeFile()


            time.sleep(.3)
            call()
        call()

        # == == == == == == == == == == == == == call == == == == == == == == == == == == #



    # estrutura de switch case, ou melhor, match case para python, pq achei mais simples
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


# função para iniciar o código e verificar opções :P
# se der ValueError além de n executar o resto do código vai tmb reiniciar mostrar saida except ValueError e perguntar dnv
# se tiver interrupção do teclado com ctrl + c vai mostrar que fechou o sistema e tmb vai forçar sair sem nenhum erro
# se escolher um número entre as opções ent vai executar o resto do código
def init():
    title()
    main()

def main():
    while True:
        try:
            print(cor.lightblue)
            opt = int(input(f"\nSua opção: {cor.white}"))
            if opt > -1 and opt <= len(options) - 1:
                selected(opt)
                break
            clear()
            print(f"{cor.red}Selecione outra opção :P\n")
            init()

        except ValueError:
            clear()
            print(f"\n{cor.red}Tente números!!\n")
            title()

        except KeyboardInterrupt:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        except SystemExit:
            raise

        # except:
        #     print("\nOcorreu um erro inesperado :[ entre em contato conosco")
        #     exit(0)

main()
