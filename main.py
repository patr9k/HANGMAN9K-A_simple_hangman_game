import pygame 
import os
import math
import random

#DISPLAY
pygame.init()
WIDTH, HEIGHT = 800, 500 #DISPLAY RESOLUTION VALUES
win = pygame.display.set_mode((WIDTH, HEIGHT)) #CREATED THE WINDOW WITH THE GIVEN RESOLUTION
pygame.display.set_caption("HANGMAN9K! ~by @patr9k") #THE WINDOW'S NAME (OR GAME NAME)

#BUTTON VARIABLES
RADIUS = 20 #RADIUS OF THE LETTER BUTTONS (IN PIXELS)
GAP = 15 #GAP BETWEEN BUTTONS (IN PIXELS)
letters = [] #CREATED A LIST FOR LETTERS
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2) #THE STARTING POSITION OF THE BUTTONS AT THE x SCALE
starty = 400                                          #THE STARTING POSITION OF THE BUTTONS AT THE y SCALE
A = 65
for i in range(26): #26 LETTERS / ENGLISH ABC
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13)) 
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

#FONTS
LETTER_FONT = pygame.font.SysFont('Caviar Dreams', 40) #LETTERS ON THE BUTTONS - FONT
WORD_FONT = pygame.font.SysFont('Caviar Dreams', 60) #WORDS FONT
TITLE_FONT = pygame.font.SysFont('Caviar Dreams', 70) #TITLE FONT

#LOAD IMAGES

images = [] #CREATED A LIST FOR THE IMAGES
for i in range(7):  #LOADING THE IMAGES IN (FROM THE HANGMAN9K FOLDER) WITH A FOR LOOP("HANGMAN" + CONVERTING THE CURRENT I VALUE INTO A STRING + ".PNG")
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

#GAME VARIABLES
hangman_status = 0 #HANGMAN'S STATUS, THAT VALUE WILL DETERMINE THAT WHICH IMAGE IS DRAWN CURRENTLY ON THE SCREEN
words = ["EMPLOYER","EMPLOYEE","SOFTWARE","ENGINEER","POLITICIAN","DRUGDEALER","DEVELOPER","FACEBOOK","MICROSOFT","GOOGLE"] #THE LIST OF THE WORDS THAT ARE USED TO PLAY {YOU CAN CHANGE IT IF YOU WANT TO PLAY WITH CUSTOM WORDS, JUST USE CAPITAL LETTERS}
word = random.choice(words) #THE WORD VALUE CHOOSES A RANDOM ONE FROM THE WORDS LIST (USING THE RANDOM IMPORT)
guessed = [] #CREATED A LIST FOR THE GUESSED LETTERS

#COLORS - USING RGB VALUES
WHITE = (255,255,255) 
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,128,0)


#DRAWING TO THE SCREEN
def draw():
    win.fill(BLACK)

    #DRAWS THE TITLE
    text = TITLE_FONT.render("HANGMAN9K.EXE", 1, RED)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    #DRAW THE WORD
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, WHITE)
    win.blit(text, (400, 200))

    #DRAWS LETTERS
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, WHITE, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100)) #PUTS THE IMAGE TO 150,100
    pygame.display.update() #!!! - UPDATES THE SCREEN

#DISPLAY THE MESSAGE - THE FIRST ONE IS GREEN, THE SECOND IS RED
def display_message1(message):
    pygame.time.delay(1000)
    win.fill(BLACK)
    text = WORD_FONT.render(message, 1, GREEN)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def display_message2(message):
    pygame.time.delay(1000)
    win.fill(BLACK)
    text = WORD_FONT.render(message, 1, RED)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

#MAIN GAME METHOD
def main():
    global hangman_status #GETS THE HANGMAN_STATUS (USING GLOBAL)

    FPS = 60                #FRAMES PER SECOND SET TO 60 (MAXIMAL FRAMES PER SECOND) 
    clock = pygame.time.Clock()    #PYGAME CLOCK
    run = True                      #TRUE VALUE in RUN

    while run:                       #A WHILE STATEMENT INSIDE THE MAIN
        clock.tick(FPS)                 #MAKES THE CLOCK TICKING AT 60 FPS

        for event in pygame.event.get():    #QUITTING THE GAME
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #GETTING THE MOUSE BUTTON'S POSITION
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter  #4 TYPES OF VALUES IN LETTER (LETTER IS A LIST)
                    if visible: #IF VISIBLE'S VALUE IS TRUE
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2) #GETS THE POS DISTANCE BETWEEN THE CLICK AND LETTER
                        if dis < RADIUS: #IF THAT DISTANCE IS SMALLER THAN THE RADIUS(20)
                            letter[3] = False   #SETS THE VISIBILITY (LETTER'S 3TH INDEX) TO FALSE
                            guessed.append(ltr) #THE LTR GETS INTO THE LIST NAMED GUESSED
                            if ltr not in word: #IF THE LTR WE HAVE CLICKED IS NOT IN THE WORD:
                                hangman_status += 1   #HANGMAN_STATUS GROWS BY 1 -----> THE IMAGE CHANGES WITH THAT FOR SURE
        
        draw()  #WE ARE USING OUR DRAW FUNCTION

        won = True    #WE SET WON TRUE BY DEFAULT
        for letter in word: #WE LOOP THROUGH THE LETTERS IN THE GIVEN WORD
            if letter not in guessed: #IF ITS NOT IN THE GUESSED LIST
                won = False                 #WON BECOMES FALSE
                break                           #WE BREAK THE LOOP
        
        if won: #IF WE HAVE WON THE GAME BY GUESSING THE WORD
            display_message1("CONGRATS, you WON! :)")  #WE GET THE MESSAGE WITH THE MESSAGE1 FUNCTION
            break #WE BREAK IT TO DONT GET THE MESSAGE MORE TIMES, AND THE PROGRAM CAN CLOSE ITSELF

        if hangman_status == 6: #IF WE LOSE(HANGMAN_STATUS REACHES 6), WE GET THE MESSAGE WITH THE MESSAGE2 FUNCTION
            display_message2("SORRY, but you LOST! :(")
            break #WE BREAK IT TO DONT GET THE MESSAGE MORE TIMES, AND THE PROGRAM CAN CLOSE ITSELF
    

    
main() #WE RUN THE MAIN FUNCTION
pygame.quit() #AFTER THE MAIN FUNCTION'S ENDING THE GAME CLOSES ITSELF