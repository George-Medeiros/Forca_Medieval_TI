# src/main.py
import pygame
import sys
import os
# Importamos a Classe de lógica (HangmanSession)
from logic import HangmanSession 

# --- Configurações Profissionais ---
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Cores RGB - Mantemos o padrão medieval/TI
COLOR_TEXT = (245, 235, 200) # Bege claro (medieval)
COLOR_DICA = (180, 210, 245) # Azul claro para destacar o CONCEITO TI
COLOR_ALERT = (255, 80, 80)  # Vermelho para erros

# Título do seu jogo
GAME_TITLE = " Medieval Debbuger.exe "

# --- Estados do Jogo (Game States) ---
STATE_MENU = 0
STATE_PLAYING = 1
current_state = STATE_MENU

def main():
    global current_state # Permite alterar a variável fora da função main
    
    # --- Inicialização ---
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # --- Instancia a Sessão de Lógica ---
    sessao_jogo = HangmanSession()

    # --- Carregamento de Assets Base (Caminhos Seguros) ---
    base_path = os.path.dirname(__file__)
    
    try:
        # Imagem de Fundo (Praça medieval)
        bg_path = os.path.join(base_path, "..", "assets", "images", "background.png")
        background_img = pygame.image.load(bg_path).convert()
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        
        # Música (Mantenha o som melancólico!)
        music_path = os.path.join(base_path, "..", "assets", "sound", "music.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Loop infinito
        
    except FileNotFoundError as e:
        print(f"Alerta: Asset base não encontrado ({e}). Iniciando em modo genérico.")
        # Plano B: Fundo sólido
        background_img = pygame.Surface((WIDTH, HEIGHT))
        background_img.fill((40, 40, 45)) # Cinza escuro sombrio
        pygame.mixer.music.stop()

    # --- NOVO BLOCO (SUBSTITUIÇÃO): Geração de Placeholder em Código ---
    # Como não temos as imagens em arquivo, vamos criar 'Surfaces' em branco
    # e desenhar formas geométricas nelas professionalmente.
    forca_images = []
    for i in range(7): # Gera 7 surfaces (0 a 6 erros)
        # Cria uma superfície transparente de 300x400
        surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        
        # --- Definição de Cores e Posições Comuns ---
        COLOR_FORCA = (80, 50, 20) # Marrom madeira escura
        COLOR_CORPO = (200, 200, 150) # Amarelo palha/pele clara
        
        # 1. Desenha a Forca (Sempre presente, de 0 a 6 erros)
        # Base
        pygame.draw.rect(surface, COLOR_FORCA, (50, 380, 200, 20), border_radius=5)
        # Poste Vertical
        pygame.draw.rect(surface, COLOR_FORCA, (80, 50, 20, 330), border_radius=5)
        # Trave Horizontal
        pygame.draw.rect(surface, COLOR_FORCA, (80, 50, 150, 20), border_radius=5)
        # Corda
        pygame.draw.line(surface, COLOR_TEXT, (200, 70), (200, 120), 5)
        # Estrutura de Apoio
        pygame.draw.line(surface, COLOR_FORCA, (80, 120), (130, 50), 10)

        # 2. Desenha o Boneco (Baseado no número de erros 'i')
        # 1 erro: Cabeça
        if i >= 1:
            pygame.draw.circle(surface, COLOR_CORPO, (200, 145), 25)
        # 2 erros: Corpo
        if i >= 2:
            pygame.draw.line(surface, COLOR_CORPO, (200, 170), (200, 250), 10)
        # 3 erros: Braço Esquerdo
        if i >= 3:
            pygame.draw.line(surface, COLOR_CORPO, (200, 190), (160, 220), 8)
        # 4 erros: Braço Direito
        if i >= 4:
            pygame.draw.line(surface, COLOR_CORPO, (200, 190), (240, 220), 8)
        # 5 erros: Perna Esquerda
        if i >= 5:
            pygame.draw.line(surface, COLOR_CORPO, (200, 250), (170, 310), 8)
        # 6 erros: Perna Direita (ENFORCADO)
        if i >= 6:
            pygame.draw.line(surface, COLOR_CORPO, (200, 250), (230, 310), 8)
        
        # Adiciona a surface gerada à nossa lista de imagens
        forca_images.append(surface)
    # -------------------------------------------------------------------

    # --- Carregamento de Fontes ---
    try:
        font_path = os.path.join(base_path, "..", "assets", "fonts", "medieval.ttf")
        title_font = pygame.font.Font(font_path, 80) # Título enorme
        word_font = pygame.font.Font(font_path, 70)  # Palavra oculta grande
        button_font = pygame.font.Font(font_path, 40) # Botões médios
        
        # Fonte padrão para dicas e INSTRUÇÕES (legibilidade)
        dica_font = pygame.font.Font(None, 36) 
        
    except FileNotFoundError as e:
        print(f"Erro Crítico: Fonte medieval.ttf não encontrada ({e}). O jogo não pode rodar.")
        return # Encerra se a fonte falhar

    # --- Definição do Botão JOGAR do Menu ---
    button_jogar_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 80)

    # --- Loop Principal do Jogo ---
    game_running = True
    while game_running:
        # Obtém a posição do mouse a cada quadro
        mx, my = pygame.mouse.get_pos() 
        
        # --- 1. Entrada de Eventos (Event Loop) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            
            # --- Eventos: MENU ---
            if current_state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Clique esquerdo
                    if button_jogar_rect.collidepoint((mx, my)):
                        sessao_jogo.iniciar_nova_partida()
                        current_state = STATE_PLAYING # Transição de Estado
            
            # --- Eventos: PLAYING (JOGANDO) ---
            elif current_state == STATE_PLAYING:
                # Detecta pressionamento de Teclas
                if event.type == pygame.KEYDOWN:
                    # Se pressionar ESC, volta pro menu
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                    
                    # Se pressionar uma tecla de letra (A-Z)
                    letter = event.unicode.upper()
                    if letter.isalpha() and len(letter) == 1:
                        # Passa a letra para a lógica processar
                        sessao_jogo.tentar_letra(letter)

        # --- 2. Desenho e Atualização (Rendering Loop) ---
        screen.blit(background_img, (0, 0))
        
        # Renderização: MENU
        if current_state == STATE_MENU:
            # Título e Sombra (Centralizado)
            title_text = title_font.render(GAME_TITLE, True, COLOR_TEXT)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            shadow_text = title_font.render(GAME_TITLE, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 3))
            screen.blit(shadow_text, shadow_rect)
            screen.blit(title_text, title_rect)

            # Botão JOGAR com efeito Hover
            b_color = (80, 80, 100) if button_jogar_rect.collidepoint((mx, my)) else (50, 50, 60)
            pygame.draw.rect(screen, b_color, button_jogar_rect, border_radius=10)
            
            # Texto do Botão
            b_text = button_font.render("JOGAR", True, COLOR_TEXT)
            b_text_rect = b_text.get_rect(center=button_jogar_rect.center)
            screen.blit(b_text, b_text_rect)

            # SEÇÃO DE COMANDOS DE CONTROLE (na parte inferior)
            comandos = [
                "Comandos de Controle:",
                "[MOU] - Clicar em JOGAR",
                "[A-Z] - Escolher Letra (na forca)",
                "[ESC] - Voltar ao Menu / Sair"
            ]

            y_start = HEIGHT - 140
            line_height = 32

            for i, linha in enumerate(comandos):
                cmd_surface = dica_font.render(linha, True, COLOR_TEXT)
                cmd_rect = cmd_surface.get_rect(center=(WIDTH // 2, y_start + (i * line_height)))
                screen.blit(cmd_surface, cmd_rect)

        # --- Renderização: PLAYING (JOGANDO) ---
        elif current_state == STATE_PLAYING:
            # DICA (O Conceito TI - Destaque no Topo)
            dica_str = f"CONCEITO TI: {sessao_jogo.dica}"
            dica_surface = dica_font.render(dica_str, True, COLOR_DICA)
            dica_rect = dica_surface.get_rect(center=(WIDTH // 2, 80)) 
            screen.blit(dica_surface, dica_rect)

            # PALAVRA OCULTA (Centralizada)
            palavra_oculta = sessao_jogo.get_palavra_oculta()
            p_surface = word_font.render(palavra_oculta, True, COLOR_TEXT)
            p_rect = p_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(p_surface, p_rect)

            # --- NOVO BLOCO (DO MÓDULO 4): Desenho Dinâmico da Forca Gerada ---
            # Pegamos a imagem correspondente ao número de erros (que é 6 - tentativas_restantes)
            erros_atuais = 6 - sessao_jogo.tentativas_restantes
            # Pega a surface que geramos no Módulo 2
            forca_surface = forca_images[erros_atuais]
            
            # Centralizamos a forca no meio do tablado da imagem de fundo
            forca_rect = forca_surface.get_rect(center=(WIDTH * 0.70, HEIGHT * 0.60))
            
            # Desenha a forca sobre o tablado
            screen.blit(forca_surface, forca_rect)
            # -------------------------------------------------------------

            # STATUS (Vidas e Letras Erradas nas Laterais Inferiores)
            vidas_text = button_font.render(f"Vidas: {sessao_jogo.tentativas_restantes}", True, COLOR_TEXT)
            screen.blit(vidas_text, (50, HEIGHT - 100)) 

            # Letras Erradas
            erradas_str = " ".join(sorted(list(sessao_jogo.letras_erradas)))
            erradas_text = dica_font.render(f"Erros: {erradas_str}", True, COLOR_ALERT)
            screen.blit(erradas_text, (WIDTH - 400, HEIGHT - 100)) 

            # TELA FINAL (Vitória/Derrota Overlay)
            if sessao_jogo.venceu or sessao_jogo.perdeu:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180) # Transparência
                overlay.fill((0, 0, 0)) # Preto
                screen.blit(overlay, (0, 0))

                # Mensagem Final Centralizada
                if sessao_jogo.venceu:
                    end_text = title_font.render("CONCEITO DOMINADO!", True, (100, 255, 100)) # Verde
                else:
                    end_text = title_font.render("ENFORCADO!", True, COLOR_ALERT) # Vermelho
                    # Revelar a palavra oculta
                    revelar_text = dica_font.render(f"A palavra era: {sessao_jogo.palavra_completa}", True, COLOR_TEXT)
                    revelar_rect = revelar_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                    screen.blit(revelar_text, revelar_rect)

                # Instrução para reiniciar/voltar
                restart_text = button_font.render("Pressione ESC para o Menu", True, COLOR_TEXT)

                end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
                
                screen.blit(end_text, end_rect)
                screen.blit(restart_text, restart_rect)

        # Atualiza o display e segura o FPS
        pygame.display.flip()
        clock.tick(FPS)

    # Encerramento Limpo
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()