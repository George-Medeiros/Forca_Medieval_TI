# src/main.py
import pygame
import sys
import os
from logic import HangmanSession 

# Configurações de Tela
WIDTH, HEIGHT = 1280, 720
FPS = 60
GAME_TITLE = "Medieval TI - Acerte ou Forca"

# Paleta de Cores para Máxima Nitidez
COLOR_TEXT = (245, 235, 200)   # Creme Medieval
COLOR_DICA = (255, 215, 0)     # Dourado (Contraste para a dica)
COLOR_ALERT = (255, 80, 80)    # Vermelho Alerta
COLOR_FORCA = (80, 50, 20)     # Marrom Madeira
COLOR_CORPO = (200, 200, 150)  # Cor do Boneco

# Estados do Jogo
STATE_MENU = 0
STATE_PLAYING = 1
current_state = STATE_MENU

def main():
    global current_state 
    
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    sessao_jogo = HangmanSession()
    base_path = os.path.dirname(__file__)
    
    # --- Carregamento de Assets ---
    try:
        bg_path = os.path.join(base_path, "..", "assets", "images", "background.png")
        background_img = pygame.image.load(bg_path).convert()
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        
        music_path = os.path.join(base_path, "..", "assets", "sound", "music.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) 
    except:
        background_img = pygame.Surface((WIDTH, HEIGHT))
        background_img.fill((40, 40, 45)) 

    # --- Fontes ---
    try:
        font_path = os.path.join(base_path, "..", "assets", "fonts", "medieval.ttf")
        title_font = pygame.font.Font(font_path, 50) 
        credits_font = pygame.font.Font(font_path, 25) 
        button_theme_font = pygame.font.Font(font_path, 35) 
        command_theme_font = pygame.font.Font(font_path, 25) 
        word_font = pygame.font.Font(font_path, 70)  
        button_font = pygame.font.Font(font_path, 40) 
        dica_font = pygame.font.Font(None, 38) # Fonte padrão do sistema para dicas (mais legível)
    except:
        print("Erro: medieval.ttf não encontrada.")
        return 

    # Retângulo base do botão (Y será calculado dinamicamente)
    button_jogar_rect = pygame.Rect(WIDTH // 2 - 110, 0, 220, 60)

    # --- Loop Principal ---
    while True:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if current_state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_jogar_rect.collidepoint((mx, my)):
                        sessao_jogo.iniciar_nova_partida()
                        current_state = STATE_PLAYING 
            
            elif current_state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                    letter = event.unicode.upper()
                    if letter.isalpha() and len(letter) == 1:
                        sessao_jogo.tentar_letra(letter)

        # 1. Desenha o Fundo
        screen.blit(background_img, (0, 0))
        
        if current_state == STATE_MENU:
            # --- 2. Título Principal e Sombra ---
            pos_x, pos_y = WIDTH // 2, 85
            t_surf = title_font.render(GAME_TITLE, True, COLOR_TEXT)
            t_shad = title_font.render(GAME_TITLE, True, (0, 0, 0))
            screen.blit(t_shad, (pos_x - t_surf.get_width()//2 + 3, pos_y - t_surf.get_height()//2 + 3))
            screen.blit(t_surf, t_surf.get_rect(center=(pos_x, pos_y)))

            # --- 3. Créditos Sombreados (George Medeiros) ---
            cred_txt = "by George Medeiros, RU 5117806"
            c_s = credits_font.render(cred_txt, True, COLOR_TEXT)
            c_sh = credits_font.render(cred_txt, True, (0, 0, 0))
            c_rect = c_s.get_rect(center=(pos_x, pos_y + 45))
            screen.blit(c_sh, (c_rect.x + 2, c_rect.y + 2)) # Sombra
            screen.blit(c_s, c_rect)

            # --- 4. Bloco de Comandos de Controle ---
            y_base_cmds = HEIGHT - 150
            cmds = [
                "Comandos de Controle:",
                "[MOU] - Clicar em JOGAR",
                "[A-Z] - Escolher Letra (na forca)",
                "[ESC] - Voltar ao Menu / Sair"
            ]
            for i, txt in enumerate(cmds):
                y_p = y_base_cmds + (i * 32)
                txt_s = command_theme_font.render(txt, True, COLOR_TEXT)
                txt_sh = command_theme_font.render(txt, True, (0, 0, 0))
                screen.blit(txt_sh, txt_sh.get_rect(center=(WIDTH//2 + 2, y_p + 2))) # Sombra
                screen.blit(txt_s, txt_s.get_rect(center=(WIDTH//2, y_p)))

            # --- 5. Botão JOGAR com Simetria Perfeita ---
            # Posicionado exatamente entre o fim dos créditos e o início dos comandos
            espaco_total = y_base_cmds - c_rect.bottom
            button_jogar_rect.centery = c_rect.bottom + (espaco_total // 2)
            
            b_color = (80, 80, 100) if button_jogar_rect.collidepoint((mx, my)) else (50, 50, 60)
            pygame.draw.rect(screen, b_color, button_jogar_rect, border_radius=10)
            b_s = button_theme_font.render("JOGAR", True, COLOR_TEXT)
            b_sh = button_theme_font.render("JOGAR", True, (0, 0, 0))
            screen.blit(b_sh, b_sh.get_rect(center=(button_jogar_rect.centerx+2, button_jogar_rect.centery+2)))
            screen.blit(b_s, b_s.get_rect(center=button_jogar_rect.center))

        elif current_state == STATE_PLAYING:
            # --- 6. Tela de Jogo: Dica de TI (Dourada e Sombreada) ---
            d_str = f"CONCEITO TI: {sessao_jogo.dica}"
            d_s = dica_font.render(d_str, True, COLOR_DICA)
            d_sh = dica_font.render(d_str, True, (0, 0, 0))
            d_rect = d_s.get_rect(center=(WIDTH // 2, 80))
            screen.blit(d_sh, (d_rect.x + 2, d_rect.y + 2)) # Sombra da dica
            screen.blit(d_s, d_rect)

            # --- 7. Palavra Oculta ---
            p_s = word_font.render(sessao_jogo.get_palavra_oculta(), True, COLOR_TEXT)
            screen.blit(p_s, p_s.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            # --- 8. Desenho da Forca e Personagem ---
            erros = 6 - sessao_jogo.tentativas_restantes
            f_x, f_y = WIDTH * 0.75, HEIGHT * 0.55
            # Estrutura
            pygame.draw.rect(screen, COLOR_FORCA, (f_x-100, f_y+150, 200, 20)) # Base
            pygame.draw.rect(screen, COLOR_FORCA, (f_x-70, f_y-180, 20, 330))  # Poste
            pygame.draw.rect(screen, COLOR_FORCA, (f_x-70, f_y-180, 150, 20)) # Topo
            pygame.draw.line(screen, (150,100,50), (f_x+50, f_y-160), (f_x+50, f_y-110), 4) # Corda
            # Boneco
            if erros >= 1: pygame.draw.circle(screen, COLOR_CORPO, (int(f_x+50), int(f_y-85)), 25)
            if erros >= 2: pygame.draw.line(screen, COLOR_CORPO, (f_x+50, f_y-60), (f_x+50, f_y+20), 8)
            if erros >= 3: pygame.draw.line(screen, COLOR_CORPO, (f_x+50, f_y-40), (f_x+10, f_y-10), 6)
            if erros >= 4: pygame.draw.line(screen, COLOR_CORPO, (f_x+50, f_y-40), (f_x+90, f_y-10), 6)
            if erros >= 5: pygame.draw.line(screen, COLOR_CORPO, (f_x+50, f_y+20), (f_x+20, f_y+80), 6)
            if erros >= 6: pygame.draw.line(screen, COLOR_CORPO, (f_x+50, f_y+20), (f_x+80, f_y+80), 6)

            # --- 9. Status da Partida ---
            v_s = button_font.render(f"Vidas: {sessao_jogo.tentativas_restantes}", True, COLOR_TEXT)
            screen.blit(v_s, (50, HEIGHT - 100))
            e_s = dica_font.render(f"Erros: {' '.join(sorted(sessao_jogo.letras_erradas))}", True, COLOR_ALERT)
            screen.blit(e_s, (WIDTH - 450, HEIGHT - 100))

            # --- 10. Telas de Vitória / Derrota ---
            if sessao_jogo.venceu or sessao_jogo.perdeu:
                ov = pygame.Surface((WIDTH, HEIGHT)); ov.set_alpha(190); ov.fill((0,0,0))
                screen.blit(ov, (0,0))
                
                texto_fim = "CONCEITO DOMINADO!" if sessao_jogo.venceu else "ENFORCADO!"
                cor_fim = (100, 255, 100) if sessao_jogo.venceu else COLOR_ALERT
                msg = title_font.render(texto_fim, True, cor_fim)
                screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
                
                if sessao_jogo.perdeu:
                    revelar = dica_font.render(f"A palavra era: {sessao_jogo.palavra_completa}", True, COLOR_TEXT)
                    screen.blit(revelar, revelar.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
                
                rst = button_font.render("Pressione ESC para o Menu", True, COLOR_TEXT)
                screen.blit(rst, rst.get_rect(center=(WIDTH//2, HEIGHT//2 + 100)))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

    