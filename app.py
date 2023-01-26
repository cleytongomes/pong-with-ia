# Primeiro temos que importar os módulos que iremos usar:
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from variaveis import *
from PPlay.keyboard import *
import random
import time

from ia import Ia

# Cria a janela
janela=Window(MAPA_WIDTH, MAPA_HEIGHT)

# Título do Jogo
janela.set_title("Pong com IA")

# Teclado
teclado = Window.get_keyboard()

# Paddle esquerda
paddle_esquerda = Sprite("paddle.png")
paddle_esquerda.set_position(20,(MAPA_HEIGHT / 2) - (paddle_esquerda.height / 2))

# Paddle direira
paddle_direita = Sprite("paddle.png")
paddle_direita.set_position(780 - paddle_direita.width,(MAPA_HEIGHT / 2) - (paddle_direita.height / 2))

# Bola
bola = Sprite("bola.png")
bola.set_position((MAPA_WIDTH / 2) - (bola.width / 2),(MAPA_HEIGHT / 2) - (bola.height / 2))

# Direções da bola
bola_direcao_vertical   = random.choice([ESQUERDA, DIREITA])
bola_direcao_horizontal = random.choice([ESQUERDA, DIREITA])

# Instância a Ia do Paddle
paddle_Ia = Ia()

# Pontucao
pontos_paddle_esquerda = 0
pontos_paddle_direita = 0

# Incrementador de Velocidade (Altera o ângulo)
incre_velocidade_lateral_bola = 0

# Aguarda uns segundos para o jogo iniciar
time.sleep(1)

# Game loop
while True:

    # Decisão de movimentação
    escolha_paddle_esquerda = 'P'
    escolha_paddle_direita = 'P'

    # Movimentação Usuário (Teclado)
    if(teclado.key_pressed("W")):
        escolha_paddle_esquerda = 'S'
        paddle_esquerda.move_y(VELOCIDADE_PADDLE * -1 * janela.delta_time())
    elif(teclado.key_pressed("S")):
        escolha_paddle_esquerda = 'D'
        paddle_esquerda.move_y(VELOCIDADE_PADDLE * janela.delta_time())

    # Movimentação Automática (Lógica)
    if( bola.y < paddle_esquerda.y ):
        escolha_paddle_esquerda = 'S'
        paddle_esquerda.move_y(VELOCIDADE_PADDLE * -1 * janela.delta_time())
    elif( bola.y > paddle_esquerda.y + paddle_esquerda.height ):
        escolha_paddle_esquerda = 'D'
        paddle_esquerda.move_y(VELOCIDADE_PADDLE * janela.delta_time())

    # Move o Paddle (IA)
    escolha_paddle_direita = paddle_Ia.move(bola, paddle_direita, VELOCIDADE_PADDLE * janela.delta_time())

    # Move a Bola
    bola.move_x((VELOCICADE_BOLA_X) * bola_direcao_vertical * janela.delta_time())
    bola.move_y((VELOCIDADE_BOLA_Y + incre_velocidade_lateral_bola) * bola_direcao_horizontal * janela.delta_time())

    # Verifica colisão da bola com o Paddle da Esquerda
    if(bola.collided(paddle_esquerda)):
        bola.x = paddle_esquerda.x + paddle_esquerda.width
        bola_direcao_vertical *= -1
        paddle_Ia.grava_posicoes("ESQUERDA")

    # Verifica colisão da bola com o Paddle da Direita
    elif(bola.collided(paddle_direita)):
        bola.x = paddle_direita.x - bola.width
        bola_direcao_vertical *= -1
        paddle_Ia.grava_posicoes("DIREITA")

    # Verifica se o paddle da esquerda passou do topo ou fundo
    if paddle_esquerda.y < 0:
        paddle_esquerda.y = 0
    elif paddle_esquerda.y + paddle_esquerda.height > 600:
        paddle_esquerda.y = 600 - paddle_esquerda.height

    # Verifica se o paddle da direira passou do topo ou fundo
    if paddle_direita.y < 0:
        paddle_direita.y = 0
    elif paddle_direita.y + paddle_direita.height > 600:
        paddle_direita.y = 600 - paddle_direita.height

    # Verifica se a posição da bola passou do topo e fundo
    if bola.y < 0:
        bola.y = 0
        bola_direcao_horizontal *= -1

    elif bola.y + bola.height > 600:
        bola.y = 600 - bola.height
        bola_direcao_horizontal *= -1

    # Verifica se a posição da bola passou das laterais (Pontuacao)
    if bola.x < 0:
        bola.set_position(400,300)
        bola_direcao_vertical *= -1
        pontos_paddle_direita +=1
        
        paddle_esquerda.y = (MAPA_HEIGHT / 2) - (paddle_esquerda.height / 2)
        paddle_direita.y = (MAPA_HEIGHT / 2) - (paddle_direita.height / 2)
        
        incre_velocidade_lateral_bola = random.choice([-1, 1]) * random.randint(30,60)
        paddle_Ia.reseta_posicoes()
        paddle_Ia.re_treinar()
    elif bola.x + bola.width > 800:
        bola.set_position(400,300)
        bola_direcao_vertical *= -1
        pontos_paddle_esquerda += 1

        paddle_esquerda.y = (MAPA_HEIGHT / 2) - (paddle_esquerda.height / 2)
        paddle_direita.y = (MAPA_HEIGHT / 2) - (paddle_direita.height / 2)

        incre_velocidade_lateral_bola = random.choice([-1, 1]) * random.randint(30,60)
        paddle_Ia.reseta_posicoes()
        paddle_Ia.re_treinar()

    # Salva as posições do paddle
    paddle_Ia.salva_posicoes(bola, paddle_esquerda, paddle_direita, escolha_paddle_esquerda, escolha_paddle_direita)

    # Pinta o fundo
    janela.set_background_color((0,0,0))  # Vermelho

    # Desenha os objetos
    bola.draw()
    paddle_esquerda.draw()
    paddle_direita.draw()

    # Atualiza a janela
    janela.update()  