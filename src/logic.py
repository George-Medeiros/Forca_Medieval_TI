# src/logic.py
import random

class HangmanSession:
    def __init__(self):
        # Lista embutida para evitar erro de arquivo não encontrado
        self.banco_palavras = [
            {"palavra": "PYTHON", "dica": "Linguagem de programacao versatil"},
            {"palavra": "ALGORITMO", "dica": "Sequencia de passos para resolver um problema"},
            {"palavra": "VARIAVEL", "dica": "Espaco na memoria para armazenar dados"},
            {"palavra": "HARDWARE", "dica": "Parte fisica do computador"},
            {"palavra": "SOFTWARE", "dica": "Parte logica do computador"},
            {"palavra": "FIREWALL", "dica": "Dispositivo de seguranca de rede"},
            {"palavra": "DATABASE", "dica": "Conjunto estruturado de dados"},
            {"palavra": "BACKUP", "dica": "Copia de seguranca de dados"}
        ]
        self.iniciar_nova_partida()

    def iniciar_nova_partida(self):
        selecionada = random.choice(self.banco_palavras)
        self.palavra_completa = selecionada["palavra"].upper()
        self.dica = selecionada["dica"]
        self.letras_adivinhadas = set()
        self.letras_erradas = set()
        self.tentativas_restantes = 6
        self.venceu = False
        self.perdeu = False

    def tentar_letra(self, letra):
        letra = letra.upper()
        if letra in self.letras_adivinhadas or letra in self.letras_erradas or self.venceu or self.perdeu:
            return

        if letra in self.palavra_completa:
            self.letras_adivinhadas.add(letra)
            if all(l in self.letras_adivinhadas for l in self.palavra_completa):
                self.venceu = True
        else:
            self.letras_erradas.add(letra)
            self.tentativas_restantes -= 1
            if self.tentativas_restantes <= 0:
                self.perdeu = True

    def get_palavra_oculta(self):
        return " ".join([l if l in self.letras_adivinhadas else "_" for l in self.palavra_completa])

        