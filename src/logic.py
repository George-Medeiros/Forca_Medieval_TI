# src/logic.py
import json
import random
import os

class HangmanSession:
    def __init__(self):
        """
        Inicia o objeto de lógica e carrega o banco de dados JSON uma vez só.
        """
        # Configuração Profissional de Caminhos (os.path)
        base_path = os.path.dirname(__file__) # Pasta src
        # Volta uma pasta (..) e entra em data/palavras.json
        file_path = os.path.join(base_path, "..", "data", "palavras.json")
        
        # Carrega o banco de dados
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.banco_palavras = json.load(f) # Transforma JSON em lista Python
        except FileNotFoundError:
            print("Erro Crítico: arquivo palavras.json não encontrado na pasta data/.")
            # Rede de segurança (PLANO B) se o JSON sumir
            self.banco_palavras = [{"palavra": "ERRO", "dica": "Arquivo JSON não encontrado."}]

        # Atributos do Estado da Partida (vazios até iniciar)
        self.palavra_completa = ""
        self.dica = ""
        # Usamos sets (conjuntos) para garantir que letras não se repitam
        self.letras_corretas = set() 
        self.letras_erradas = set()
        self.tentativas_restantes = 6 # Começamos com 6 vidas (cabeça, corpo, 2 braços, 2 pernas)
        self.venceu = False
        self.perdeu = False

    def iniciar_nova_partida(self):
        """
        Sorteia uma palavra e reseta todo o estado para uma nova partida.
        """
        # Sorteia um dicionário aleatório {"palavra": X, "dica": Y}
        selecionada = random.choice(self.banco_palavras)
        self.palavra_completa = selecionada["palavra"].upper() # Garante maiúsculas
        self.dica = selecionada["dica"]
        
        # Reseta os contadores e conjuntos
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas_restantes = 6
        self.venceu = False
        self.perdeu = False
        
        # print("Nova partida iniciada. Palavra:", self.palavra_completa) # Apenas para debug

    def get_palavra_oculta(self):
        """
        Retorna a palavra formatada para exibição (ex: 'P _ T H _ N').
        """
        exibicao = ""
        for letra in self.palavra_completa:
            # Se a letra já foi adivinhada, mostra a letra
            if letra in self.letras_corretas:
                exibicao += letra + " "
            # Se não, mostra o traço (_)
            else:
                exibicao += "_ "
        return exibicao.strip() # Remove o espaço extra no final da string

    def tentar_letra(self, letra):
        """
        Processa a tentativa de uma letra. Retorna True se acertou.
        Esta é a função mais importante da lógica.
        """
        letra = letra.upper() # Garante maiúsculas
        
        # Segurança Profissional: Ignora se a letra já foi tentada ou o jogo acabou
        if letra in self.letras_corretas or letra in self.letras_erradas or self.venceu or self.perdeu:
            # print(f"Letra '{letra}' já tentada ou jogo encerrado.") # Debug
            return False

        # ACERTOU: A letra existe na palavra
        if letra in self.palavra_completa:
            self.letras_corretas.add(letra)
            # Verifica Vitória: Todas as letras únicas da palavra foram adivinhadas
            if all(char in self.letras_corretas for char in set(self.palavra_completa)):
                self.venceu = True
                # print("VITÓRIA!") # Debug
            return True # Retorna True para acerto

        # ERROU: A letra NÃO existe na palavra
        else:
            self.letras_erradas.add(letra)
            self.tentativas_restantes -= 1
            # Verifica Derrota
            if self.tentativas_restantes <= 0:
                self.perdeu = True
                # print("DERROTA!") # Debug
            return False # Retorna False para erro