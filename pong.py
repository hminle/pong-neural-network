import pygame
import random

# define variables for game
FPS = 60

# size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# size of our paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 30

# size of our ball
BALL_WIDTH = 10
BALL_HEIGHT = 10

# distance from the edge of the window
PADDLE_BUFFER = 10
#Speed of our paddle & ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

# RGB Colors paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# initialize our screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def drawBall(ballXpos, ballYpos):
    ball = pygame.Rect(ballXpos, ballYpos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)

def drawPaddle1(paddle1YPos):
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle1)

def drawPaddle2(paddle2YPos):
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle2)

def updateBall(paddle1YPos, paddle2YPos, ballXpos, ballYpos, ballXDirection, ballYDirection):

    #update x and y position
    ballXPos = ballXpos + ballXDirection * BALL_X_SPEED
    ballYPos = ballYpos + ballYDirection * BALL_Y_SPEED
    score = 0

    #check for a collision, if the ball
    # hits the left side
    #then switch direction
    if(ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH 
            and ballYPos + BALL_HEIGHT >= paddle1YPos 
            and ballYPos - BALL_HEIGHT <= paddle1YPos + PADDLE_HEIGHT):
        ballXDirection = 1
    elif(ballXPos <= 0):
        ballXDirection = 1
        score = -1
        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    #hits the other side
    if(ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER 
            and ballYPos + BALL_HEIGHT >= paddle2YPos 
            and ballYPos - BALL_HEIGHT <= paddle2YPos + PADDLE_HEIGHT):
        ballXDirection = -1
    elif(ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        ballXDirection = -1
        score = 1
        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    # ball hits
    if(ballYPos <= 0):
        ballYPos = 0
        ballYDirection = 1
    elif(ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

#update the paddle position
def updatePaddle1(action, paddle1YPos):
    # action is an array of where it moves, up down left right
    # move up
    if(action[1] == 1):
        paddle1YPos = paddle1YPos - PADDLE_SPEED

    #move down
    if(action[2] == 1):
        paddle1YPos = paddle1YPos + PADDLE_SPEED

    # don't let it moves off the screen
    if(paddle1YPos < 0):
        paddle1YPos = 0
    if(paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle1YPos

def updatePaddle2(paddle2YPos, ballYPos):
    # move down if ball is in upper half
    if(paddle2YPos + PADDLE_HEIGHT/2 < ballYPos + BALL_HEIGHT/2):
        paddle2YPos = paddle2YPos + PADDLE_SPEED

    #move up if ball is in lower half
    if(paddle2YPos + PADDLE_HEIGHT/2 > ballYPos + BALL_HEIGHT/2):
        paddle2YPos = paddle2YPos - PADDLE_SPEED

    #don't let it hit top
    if(paddle2YPos < 0):
        paddle2YPos = 0
    #dont let it hit bottom
    if(paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle2YPos


class PongGame:
    def __init__(self):
        #random number for initial direction of ball
        num = random.randint(0,9)
        #keep score
        self.tally = 0
        #initialize position of our paddle
        self.paddle1YPos = WINDOW_HEIGHT /2 - PADDLE_HEIGHT / 2
        self.paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        #and ball direction
        self.ballXDirection = 1
        self.ballYDirection = 1
        #starting point
        self.ballXPos = WINDOW_WIDTH / 2 - BALL_WIDTH/2

        #randomly decide where the ball will move
        if(0<num<3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if(3 <= num < 5):
            self.balllXDirection = -1
            self.ballYDirection = 1
        if(5<= num <8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if(8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1
        #new random number
        num = random.randint(0,9)
        #where it will start, y part
        self.ballYPos = num*(WINDOW_HEIGHT - BALL_HEIGHT)/9

    def getPresentFrame(self):
        #for each frame call the event queue
        pygame.event.pump()
        #make background black
        screen.fill(BLACK)
        #draw our paddles
        drawPaddle1(self.paddle1YPos)
        drawPaddle2(self.paddle2YPos)
        #draw ball
        drawBall(self.ballXPos, self.ballYPos)
        # get pixels 
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #return screen data
        return image_data

    def getNextFrame(self,action):
        pygame.event.pump() # call event queue
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.paddle1YPos = updatePaddle1(action, self.paddle1YPos)
        drawPaddle1(self.paddle1YPos)
        #update AI paddle
        self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos)
        drawPaddle2(self.paddle2YPos)
        #update our vars by updating ball position
        [score, self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, 
                self.ballXDirection, self.ballYDirection] = updateBall(self.paddle1YPos, self.paddle2YPos,
                        self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection)
        #draw the ball        
        drawBall(self.ballXPos, self.ballYPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score
        print("Tally is " + str(self.tally))
        #return score and the surface data
        return [score, image_data]






