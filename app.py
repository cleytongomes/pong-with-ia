# Primeiro temos que importar os módulos que iremos usar:
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *


speed_per_SECOND_X = 80

speed_per_SECOND_Y = 80

janela=Window(800, 600)

janela.set_title("Pong com IA")
 
fundo = GameImage("sprites/fancy-court.png")  

paddle_left = Sprite("sprites/fancy-paddle-green.png")
paddle_left.set_position(20,300)

paddle_right = Sprite("sprites/fancy-paddle-blue.png")
paddle_right.set_position(780 - paddle_right.width,300)

ball = Sprite("sprites/fancy-ball.png")
ball.set_position(400,300)

while True:
    fundo.draw()

    paddle_left.move_key_y(speed_per_SECOND_X * janela.delta_time())

    ball.move_x(speed_per_SECOND_X * janela.delta_time())  # mesma coisa do exemplo 2.2
    ball.move_y(speed_per_SECOND_Y * janela.delta_time())

    if(ball.collided(paddle_left)):
        pass
    elif(ball.collided(paddle_right)):
        pass

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

    ball.draw()
    paddle_left.draw()
    paddle_right.draw()

    janela.update()  