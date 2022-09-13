import pygame as pg

pg.init()

pg.display.set_caption("Pong")

#monitor_size = [pg.display.Info().current_w, pg.display.Info().current_h]
monitor_size = [800, 600]
screen = pg.display.set_mode((monitor_size[0], monitor_size[1]))
fullscreen = False

frame = pg.time.Clock()

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WINNING_SCORE = 7

class Paddle:
    color = (255, 255, 255)
    velocity = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, dsp):
        pg.draw.rect(
            dsp, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    max_velocity = 5
    color = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.max_velocity
        self.y_velocity = 0

    def draw(self, dsp):
        pg.draw.circle(dsp, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1

def draw(dsp, paddles, ball, left_score, right_score):
    dsp.fill((0, 0, 0))

    left_score_text = pg.font.SysFont("consolas", 50).render(f"{left_score}", 1, (255, 255, 255))
    right_score_text = pg.font.SysFont("consolas", 50).render(f"{right_score}", 1, (255, 255, 255))
    dsp.blit(left_score_text, (monitor_size[0]//4 - left_score_text.get_width()//2, 20))
    dsp.blit(right_score_text, (monitor_size[0] * (3/4) -
                                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(dsp)

    for i in range(10, monitor_size[1], monitor_size[1]//20):
        if i % 2 == 1:
            continue
        pg.draw.rect(dsp, (255, 255, 255), (monitor_size[0]//2 - 5, i, 10, monitor_size[1]//20))

    ball.draw(dsp)
    pg.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= monitor_size[1]:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.max_velocity
                y_velocity = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_velocity
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.max_velocity
                y_velocity = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_velocity

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pg.K_w] and left_paddle.y - left_paddle.velocity >= 0:
        left_paddle.move(up=True)
    if keys[pg.K_s] and left_paddle.y + left_paddle.velocity + left_paddle.height <= monitor_size[1]:
        left_paddle.move(up=False)

    if keys[pg.K_UP] and right_paddle.y - right_paddle.velocity >= 0:
        right_paddle.move(up=True)
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.velocity + right_paddle.height <= monitor_size[1]:
        right_paddle.move(up=False)


left_paddle = Paddle(10, monitor_size[1]//2 - PADDLE_HEIGHT //
                        2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = Paddle(monitor_size[0] - 10 - PADDLE_WIDTH, monitor_size[1] //
                        2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = Ball(monitor_size[0] // 2, monitor_size[1] // 2, BALL_RADIUS)

left_score = 0
right_score = 0

while True:
    screen.fill((0, 0, 0))
    draw(screen, [left_paddle, right_paddle], ball, left_score, right_score)

    #pg.draw.rect(
    # screen, (255, 255, 255), pg.Rect(screen.get_width() - 5 - (screen.get_width() / 5), 50, screen.get_width() / 5, 50))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

            if event.key == pg.K_f:
                if fullscreen:
                    screen = pg.display.set_mode((monitor_size[0], monitor_size[1]))
                    fullscreen = False
                else:
                    screen = pg.display.set_mode((monitor_size[0], monitor_size[1]), pg.FULLSCREEN)
                    fullscreen = True

    keys = pg.key.get_pressed()
    handle_paddle_movement(keys, left_paddle, right_paddle)

    ball.move()
    handle_collision(ball, left_paddle, right_paddle)

    if ball.x < 0:
        right_score += 1
        ball.reset()
    elif ball.x > monitor_size[0]:
        left_score += 1
        ball.reset()

    won = False
    if left_score >= WINNING_SCORE:
        won = True
        win_text = "left player wins"
    elif right_score >= WINNING_SCORE:
        won = True
        win_text = "right player wins"

    if won:
        text = winner_font = pg.font.SysFont("arial", 50).render(win_text.upper(), 1, (255, 255, 255))
        screen.blit(text, (monitor_size[0]//2 - text.get_width() //
                        2, monitor_size[1]//2 - text.get_height()//2))
        pg.display.update()
        pg.time.delay(5000)
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        left_score = 0
        right_score = 0

    pg.display.update()
    frame.tick(60)