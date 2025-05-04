# classe para cores de texto
class Cor:
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
    italic = '\033[3m'
    underline = '\033[4m'
    faint = '\033[2m'
    crossed = '\033[9m'
    blink = '\033[5m'
    negative = '\033[7m'
    end = '\033[0m'
    invert = '\033[;7m'
    reset = '\033[0;0m'
    reyellow = '\033[0;0m\033[93m'

class Text:
    def title(text):
        print(f"{Cor.underline}{Cor.blue}{text}{Cor.reset}")

    def menu(text):
        text = text.split()
        lastWord = text.pop()
        operation = f"{Cor.blue}[", Cor.underline, Cor.green, lastWord, Cor.reset,f"{Cor.blue}]", Cor.reset
        print(Cor.blue, " ".join(text), "".join(operation), "\n")

    def ask(text):
        return f"\n{Cor.blue}{text}: {Cor.reset}"

    def cpf(text):
        return f"{text[:3]}.{text[3:6]}.{text[6:9]}-{text[9:11]}"

    def readS(text):
        print(f"{Cor.yellow}{text}")
