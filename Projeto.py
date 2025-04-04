from util.cor import cor

import json
import time

# função para limpar o terminal/console :D
def clear():
    print("\n" * 30)
clear()

# opções para o menu principal
options = {
    "Saír da aplicação": 0,
    "Estudante": 1,
    "Disciplinas": 2,
    "Professores": 3,
    "Turmas": 4,
    "Matrículas": 5,
}

# função de saida das opções + menu principal
def title():
    print(f"{cor.blue}<==> Menu principal <==>\n")
    for i in options:
        print(f"{cor.yellow}{options[i]} - {i}")
title()


# função para operações
def selected(selec):
    clear()
    # função que recebe de match case que futuramente vai verificar e inserir dados nos campos escolhidos
    def manage(aba):
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
            print(f"\n\n{cor.blue}--> Menu de operações: {list(options)[selec]}")
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
                    print(f"{cor.red}escolha outra opção!")
                    call()

                clear()
                print(f"operação: {cor.blue}[{cor.green}{operations[choice]}{cor.blue}]\n\n")

            except ValueError:
                clear()
                print(f"{cor.red}selecione uma das opções!!")
                call()



                # decidi colocar em um json pq queria testar coisas novas :D
                # funções para gerenciamento CRUD do sistema
            jsonPath = "data.json"

            def printar():
                if data == []:
                    print(f"{cor.red}Não há estudantes cadastrados")
                for i in data:
                    print(i)


            def openFile():
                with open(jsonPath, "r") as file:
                    global data
                    data = json.load(file)


            def writeFile():
                try:
                    newUser = input("insira seu nome: ") #posso colocar idade no futuro...
                    openFile()
                    data.append(newUser)
                    with open(jsonPath, "w") as file:
                        json.dump(data, file, indent=4)

                except ValueError:
                    print(f"{cor.red}esse não é seu nome :[")
                    call()



            # match case para executar funções acima
            match choice:
                case 0:
                    title()
                    main()

                case 1:
                    openFile()
                    printar()

                case 2:
                    writeFile()


            time.sleep(.5)
            call()
        call()

        # == == == == == == == == == == == == == call == == == == == == == == == == == == #

        # verificar se arquivo json existe.. se n... crie
        # usando try except para tentar abrir arquivo json... se n tiver ent cria e escreve [] nele
        try:
            openFile()
        except FileNotFoundError:
            with open(jsonPath, "w") as file:
                json.dump([], file, indent=4)



    # estrutura de switch case, ou melhor, match case para python, pq achei mais simples
    match selec:
        case 0:
            print("\nVocê fechou o aplicativo :(")
            exit(0)

        case _:
            manage(selec)


# função para iniciar o código e verificar opções :P
# se der ValueError além de n executar o resto do código vai tmb reiniciar mostrar saida except ValueError e perguntar dnv
# se tiver interrupção do teclado com ctrl + c vai mostrar que fechou o sistema e tmb vai forçar sair sem nenhum erro
# se escolher um número entre as opções ent vai executar o resto do código
def main():
    while True:
        try:
            print(cor.lightblue)
            opt = int(input("\nSua opção: "))
            if opt > -1 and opt <= len(options) - 1:
                selected(opt)
                break
            print("Selecione outra opção :P")

        except ValueError:
            clear()
            print(f"\n{cor.red}Tente números!!")
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
