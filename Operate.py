# imports :)
from util.TextColor import Cor as c, Text as text
import json
import random
import os
import shutil
import datetime

# class Operate para fazer operações
class Operate:
    def __init__(self, aba, fields):
        self.jsonPath = "data.json"
        self.aba = aba
        self.fields = fields

    def clear():
        os.system('cls' if os.name == 'nt' else'clear')

    # funções para gerenciamento CRUD do sistema
    # função para mandar info pro json
    def sendData(self, dado):
        with open(self.jsonPath, "w", encoding="utf-8") as file:
            json.dump(dado, file, indent=4)

    # verificar se arquivo existe e criar um backup (do arquivo atual) se estiver com erro de sintaxe resscrevendo o arquivo atual
    def bkup(self, e):
        Operate.clear()
        log = datetime.datetime.now().strftime("%d%m%y_%X")
        os.makedirs("backups", exist_ok=True)
        backup = f"backups/backupError_{log}.json"
        shutil.copy("data.json", backup)
        print(f"{c.red}erro: {e}{c.cyan}\nbackup feito em {backup}{c.red}")
        self.sendData([[],[],[],[],[]])

    # função para abrir o arquivo e escrevendo as informações em data. escrever [[],[]] se n existir
    def openFile(self):
        try:
            with open(self.jsonPath, "r") as file:
                global __data
                __data = json.load(file)
        except FileNotFoundError:
            self.sendData([[],[],[],[],[]])
            self.openFile()
        except json.JSONDecodeError as e:
            self.bkup(e)

    # apenas transformanda data de: [[n1],[n2]...] para [nx]
    def dataRedirect(self):
        try:
            self.openFile()
            global __data
            __data = list(__data[self.aba])
        except IndexError as e:
            self.bkup(e)

    # ler os dados do json
    # misericórdia
    non = ""
    def readFile(self):
        self.openFile()
        if __data[self.aba] == []:
            print(f"{c.bold}{c.red}lista vazia\n")
            return
        self.dataRedirect()
        match self.aba:
            case 1 | 0:
                print(c.faint, c.blue, "-> {0:<3}|{1:^8}|{2:>4}".format("id","nome","cpf"), end=f"\n\n{c.reyellow}")
                for i in __data:
                    cpf = i["cpf"]
                    cpf = text.cpf(cpf)
                    conta = 45 - len(i["nome"])
                    text.readS(f"> {i["id"]:<6}{i["nome"]}{self.non:.>{conta}}{cpf}")
            case 2:
                print(c.faint, c.blue, f"-> código -- disciplina{c.reyellow}\n")
                for i in __data:
                    text.readS(f"> {i["codigo"]}{'':.>{13 - len(str(i['codigo']))}}{i['disciplina']}")

            case 3:
                print(c.faint, c.blue, f"códigos: -> turma | professor | disciplina{c.reset}\n")
                for i in __data:
                    print(f"{c.yellow}> turma: {i['idTurma']:<10}id_professor: {i['idProf']:<10}id_disciplina: {i['idDisciplina']:<8}")

            case 4:
                print(c.faint, c.blue, f"códigos: -> id matrícula | estudante | turma{c.reset}\n")
                for i in __data:
                    text.readS(f"> id: {i['codigo']:<10}estudante: {i['idEstudante']:<10}turma: {i['idTurma']}")

        print(c.reset)
        print(f"{c.faint}{c.cyan}{" end of list ":-^62}{c.reset}\n")


    # função de input de informações. Usada por write e update
    def groupInput(self, send, data) -> dict:
        def verify():
            if data:
                error = 0
                for i in data:
                    if self.aba in (0, 1):
                        if codigo == i["id"]:
                            error += 1
                    elif self.aba == 2:
                        if idDisciplina == i["codigo"]:
                            error += 1
                    elif self.aba == 3:
                        if idClass == i["idTurma"]:
                            error += 1
                    elif self.aba == 4:
                        if idEstudante == i["idEstudante"]:
                            text.readS("\nesse estudante ja existe no sistema:")
                            while True:
                                error = 0
                                rewrite = input("adicionar novo dado: y|n? ").lower()
                                if rewrite == 'y':
                                    break
                                elif rewrite == 'n':
                                    error += 1
                                    break
                                else:
                                    print("é y ou n :^")
                            break

                # if else para verificar erro
                if error == 0:
                    pass
                else:
                    raise ValueError(f"O id já existe")
        try:
            match self.aba:
                case 0 | 1:
                    codigo = input(text.ask(f"Digite o código do {self.fields[self.aba + 1]} (max: 5)"))[:5]
                    codigo = int(codigo)
                    nome = input(text.ask(f"Insira o nome do {self.fields[self.aba + 1]} (max. 45)"))[:45].title()
                    cpf = int(input(text.ask(f"Insira o CPF do {self.fields[self.aba + 1]} (apenas números)")))
                    cpf = str(cpf)
                    if len(cpf) != 11:
                        Operate.clear()
                        print(f"{c.red}cpf inválido: cpf apenas 11 digitos{c.reset}")
                        raise ValueError(f"Cpf inválido")
                    info = {"id": codigo, "nome": nome, "cpf": cpf}

                case 2:
                    idDisciplina = int(input(text.ask(f"Informe o código da disciplina (max: 6)")))
                    nomeDisciplina = input(text.ask(f"Nome da disciplina"))
                    info = {"codigo": int(str(idDisciplina)[:6]), "disciplina": nomeDisciplina}

                case 3:
                    idClass = int(input(text.ask(f"Código da turma")))
                    idProf = int(input(text.ask(f"Código do professor")))
                    idDisciplina = int(input(text.ask(f"Informe o código da disciplina")))
                    info = {"idTurma": idClass, "idProf": idProf, "idDisciplina": idDisciplina}

                case 4:
                    idEstudante = int(input(text.ask(f"Código do estudante")))
                    idClass = int(input(text.ask(f"Código da turma")))
                    codigo = len(__data)
                    if len(__data) == 0:
                        codigo = 0
                    else:
                        codigo = __data[-1]["codigo"] + 1
                    info = {"codigo": codigo, "idEstudante": idEstudante, "idTurma": idClass}

            # if recebido de write para verificar os ids :D
            if send == None:
                verify()
            return info
        except ValueError as e:
            Operate.clear()
            print(f"{c.red}Informações inválidas :[\n{e}")
            return e

    # função para inserir info no arquivo json
    def writeFile(self):
        self.dataRedirect()
        info = self.groupInput(None, __data)
        # verificar o tipo de erro e retornar para o menu de operações caso for erro no valor
        if type(info) == ValueError:
            return

        self.openFile()
        __data[self.aba].append(info)
        self.sendData(__data)
        Operate.clear()
        print(f"{c.green}adicionado!\n")

    # função para atualizar lista do json :|
    def updateInfo(self):
        try:
            self.readFile()
            self.dataRedirect()
            update = int(input(f"{c.blue}digite o id que deseja alterar (primeiro id): {c.white}"))
            for i in range(len(__data)):
                verId = list(__data[i].values())[0]
                if update == verId:
                    print(f"{c.green}novos dados:\n")
                    info = self.groupInput("upt", __data)
                    count = 0
                    for a in range(len(__data)):
                        if list(__data[a].values())[0] == list(info.values())[0]:
                            count += 1
                    if list(__data[i].values())[0] == list(info.values())[0]:
                        count -= 1
                    if count != 0:
                        clear()
                        print(f"{c.red}esse id ja existe!\n")
                        exit()
                    __data[i] = info
                    newInfo = __data
                    self.openFile()
                    __data[self.aba] = newInfo
                    self.sendData(__data)
                    Operate.clear()
                    print(f"{c.green}alterado!\n")
                    return
            print(f"\n{c.red}Esse id não existe")
        except ValueError:
            print(f"{c.red}insira as informações corretamente")
        except AttributeError:
            print(f"\n{c.red}coloque os dados corretos")

    # função para excluir info da lista em json
    # pede o primeiro id para excluí-lo
    def excludeInfo(self):
        try:
            self.readFile()
            pop = int(input(f"{c.blue}id de quem deseja remover: {c.white}"))
            self.dataRedirect()
            for i in range(len(__data)):
                verId = list(__data[i].values())[0]
                if pop == verId:
                    del __data[i]
                    newInfo = __data
                    self.openFile()
                    __data[self.aba] = newInfo
                    self.sendData(__data)
                    Operate.clear()
                    print(f"{c.green}excluido!\n")
                    return
            print(f"\n {c.red}esse id não exite")
        except ValueError:
            print(f"{c.red}escolha um valor válido")

    # função para procurar pelo primeiro id
    def searchInfo(self):
        info = input(text.ask("procurar por"))
        self.openFile()
        self.dataRedirect()
        print("")
        for i in __data:
            for j in i.values():
                if info in str(j):
                    vals = list(i.values())
                    print(f"{c.yellow}> ", *[f"- {j:<15}" for j in vals], end="\n")
                    break

