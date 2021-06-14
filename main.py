import pygame
from pygame.locals import *
import random
import json
from poker import Hand
import time

# initialise pygame
pygame.init()

# create screen/window and set size
width = 953
height = 657
screen = pygame.display.set_mode((width, height))
# title & icon
pygame.display.set_caption("FuckYou")
icon = pygame.image.load("cards.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("table.jpeg")

FPS = 60  # frames per sec

# defining a font
smallfont = pygame.font.SysFont('Calibri', 20)


def main():
    global sb_chart     # push/fold chart for small blind
    global bb_chart     # same for big blind

    with open('pusher.txt') as p:
        pusher = p.read()

    sb_chart = json.loads(pusher)

    with open('caller.txt') as c:
        caller = c.read()

    bb_chart = json.loads(caller)

    clock = pygame.time.Clock()

    run = True

    while run:
        screen.blit(background, (0, 0))  # background image
        clock.tick(FPS)  # controls loop speed 60/sec

        click = False

        mx, my = pygame.mouse.get_pos()     # x and y cord of mouse pos

        button1 = pygame.Rect(210, 555, 120, 30)        # new hand button
        button2 = pygame.Rect(620, 555, 120, 30)        # shove button
        button3 = pygame.Rect(750, 555, 120, 30)        # fold button
        button4 = pygame.Rect(456.5, 500, 40, 30)       # hero blind button
        button5 = pygame.Rect(456.5, 34, 40, 30)        # villain blind button
        button6 = pygame.Rect(525, 500, 75, 30)        # hero stack size
        button7 = pygame.Rect(525, 34, 75, 30)        # villain stack size

        # rendering a texts written in this font
        text1 = smallfont.render('New Hand', True, (0, 0, 0))
        text2 = smallfont.render('Shove', True, (0, 0, 0))
        text3 = smallfont.render('Fold', True, (0, 0, 0))

        # drawing up buttons on board
        pygame.draw.rect(screen, (51, 153, 255), button1)  # b lue new hand
        pygame.draw.rect(screen, (120, 204, 0), button2)  # green shove
        pygame.draw.rect(screen, (230, 13, 13), button3)   # red fold
        pygame.draw.rect(screen, (255, 167, 13), button4)   # dark gold hero blind
        pygame.draw.rect(screen, (255, 167, 13), button5)   # dark gold vil blind
        pygame.draw.rect(screen, (255, 206, 40), button6)    # light gold hero stacks
        pygame.draw.rect(screen, (255, 206, 40), button7)    # light gold villain stacks

        # superimposing the text onto our buttons
        screen.blit(text1, (230, 560))
        screen.blit(text2, (655, 560))
        screen.blit(text3, (790, 560))

        for event in pygame.event.get():
            # stops program when quit is hit
            if event.type == pygame.QUIT:
                run = False
            # This block is executed once for each MOUSEBUTTONDOWN event.
            if event.type == MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    click = True

        if button1.collidepoint((mx, my)):
            if click:
                start_quiz()        # starts quiz, gives new hand when pressed

                screen.blit(card1Img, (416, 370))
                screen.blit(card2Img, (476, 370))

                if is_bb:
                    text4 = smallfont.render('BB', True, (0, 0, 0))
                    text5 = smallfont.render('SB', True, (0, 0, 0))
                else:
                    text4 = smallfont.render('SB', True, (0, 0, 0))
                    text5 = smallfont.render('BB', True, (0, 0, 0))

                text6 = smallfont.render(str(hero_stack) + " bb", True, (0, 0, 0))
                text7 = smallfont.render(str(villain_stack) + " bb", True, (0, 0, 0))

                screen.blit(text4, (465.5, 505))  # blinds
                screen.blit(text5, (465.5, 38))
                screen.blit(text6, (530, 505))  # stacks
                screen.blit(text7, (530, 40))

                time.sleep(8)

        if button2.collidepoint((mx, my)):
            if click:
                answer = "shove"
                if evaluate_hand(hero_hand, is_bb, eff_stack, answer):
                    text = smallfont.render('Correct!', True, (255, 255, 255))
                else:
                    text = smallfont.render('Incorrect!', True, (255, 255, 255))
                screen.blit(text, (420, 150))
                time.sleep(3)

        if button3.collidepoint((mx, my)):
            if click:
                answer = "fold"
                if evaluate_hand(hero_hand, is_bb, eff_stack, answer):
                    text = smallfont.render('Correct! :D', True, (255, 255, 255))
                else:
                    text = smallfont.render('Incorrect! :(', True, (255, 255, 255))
                screen.blit(text, (420, 150))
                time.sleep(3)

        pygame.display.update()     # updates board

    pygame.quit()       # quits program


# creates a random hand for the player, prints up the images of the approx cards when called
# assigns random stacks and a hand for the player and the blind sizes
# displays hand, returns values that will be needed in the main thanks
def start_quiz():
    hero_stack = round(random.uniform(0.5, 20), 2)
    villain_stack = round(random.uniform(0.5, 20), 2)

    eff_stack = min(hero_stack, villain_stack)

    hero_hand = str(Hand.make_random())

    card1 = hero_hand[0]
    card2 = hero_hand[1]
    suits = ["c", "h", "d", "s"]

# gives the cards an appropriate random suit
    if len(hero_hand) == 2:
        card1 += suits.pop(random.randint(0, 3))
        card2 += suits.pop(random.randint(0, 2))
    elif hero_hand[2] == "o":
        card1 += suits.pop(random.randint(0, 3))
        card2 += suits.pop(random.randint(0, 2))
    elif hero_hand[2] == "s":
        card1 += suits.pop(random.randint(0, 3))
        card2 += card1[1]

    card1Img = pygame.image.load('deck/' + card1 + '.png')
    card2Img = pygame.image.load('deck/' + card2 + '.png')

    if random.random() > 0.5:
        is_bb = True
    else:
        is_bb = False

    return is_bb, eff_stack, hero_stack, villain_stack, hero_hand, card1Img, card2Img


# create a function that will return all the return variables
is_bb, eff_stack, hero_stack, villain_stack, hero_hand, card1Img, card2Img = start_quiz()


# checks is player made the correct choice, return true/false
def evaluate_hand(hero_hand, is_bb, eff_stack, answer):

    if is_bb:
        stack_needed = bb_chart[hero_hand]
    else:
        stack_needed = sb_chart[hero_hand]

    if (eff_stack <= stack_needed and answer == "shove") or (eff_stack > stack_needed and answer == "fold"):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
