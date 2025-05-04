# Gabriel Zaiac
# Superior em tecnologia de análise e desenvolvimento de sistemas

# não leia o código :[
# ta feio

# importações :D
from util.TextColor import Cor as c, Text as text
from Operations import Operations as op
import os

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
    op(options)
    text.title("<==> Menu principal <==>\n")
    for i in options:
        print(f"{c.yellow}{i}. {options[i]}")

# função para iniciar o código e verificar opções :P
# vai dar ValueError se n selecionar uma opção listada. e o código vai reiniciar
# se tiver interrupção do teclado com ctrl + c ou ctrl + d mostra que fechou o sistema e forçar saida sem erro
def main():
    try:
        title()
        opt = int(input(text.ask("Sua opção")))
        if opt > -1 and opt <= len(options) - 1:
            op.selected(opt)
            clear()
            main()
        clear()
        print(f"{c.red}Selecione outra opção :P\n")
        main()

    except ValueError:
        clear()
        print(f"{c.red}Tente números!!\n")
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
