# Primeiro temos que importar os módulos que iremos usar:
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import random

from ia import Ia


speed_per_SECOND_X = (80 + random.random() * 20) * random.choice([1, -1])

speed_per_SECOND_Y = (80 + random.random() * 20) * random.choice([1, -1])

speed_peddle = 120

janela=Window(800, 600)

janela.set_title("Pong com IA")
 
fundo = GameImage("sprites/fancy-court.png")  

paddle_left = Sprite("sprites/fancy-paddle-green.png")
paddle_left.set_position(20,300)

paddle_right = Sprite("sprites/fancy-paddle-blue.png")
paddle_right.set_position(780 - paddle_right.width,300)

ball = Sprite("sprites/fancy-ball.png")
ball.set_position(400,300)

paddle_Ia = Ia()

while True:
    fundo.draw()

    paddle_left.move_key_y(speed_peddle * janela.delta_time())

    paddle_Ia.move(ball, paddle_right, speed_peddle * janela.delta_time())

    ball.move_x(speed_per_SECOND_X * janela.delta_time())
    ball.move_y(speed_per_SECOND_Y * janela.delta_time())

    if(ball.collided(paddle_left)):

        print(ball.x, paddle_left.x, paddle_left.width)
        if( ball.x > paddle_left.x + paddle_left.width - 10):
            speed_per_SECOND_X *= -1

    elif(ball.collided(paddle_right)):
        speed_per_SECOND_X *= -1

    if ball.y < 0:
        ball.y = 0
        speed_per_SECOND_Y *= -1
    elif ball.y + ball.height > 600:
        ball.y = 600 - ball.height
        speed_per_SECOND_Y *= -1

    if ball.x < 0:
        ball.set_position(400,300)
    elif ball.x + ball.width > 800:
        ball.set_position(400,300)

    if paddle_left.y < 0:
        paddle_left.y = 0
    elif paddle_left.y + paddle_left.height > 600:
        paddle_left.y = 600 - paddle_left.height

    if paddle_right.y < 0:
        paddle_right.y = 0
    elif paddle_right.y + paddle_right.height > 600:
        paddle_right.y = 600 - paddle_right.height

    ball.draw()
    paddle_left.draw()
    paddle_right.draw()

    janela.update()  