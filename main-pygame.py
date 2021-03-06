# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:37:13 2019
Gui for Dog ceo

@author: Naveen 
"""

# Intialising Logger
import logging
import os
import time
from sys import exit as quit

import pygame

logger = logging.getLogger("dog-ceo-NaveenMK")
logging.basicConfig(filename="log.log", level=logging.INFO)

pygame.init()

displayinfo = pygame.display.Info()


pygame.display.set_caption("Dog ceo-Pygame By Naveen M K")
font = pygame.font.Font("Fonts/octin.ttf", 50)

anim_running = False

# The code underneath is related to anything that has to do to the game's size.
gameDisplay = pygame.display.set_mode(flags=pygame.FULLSCREEN)  # Noframe window
x, y = gameDisplay.get_size()
display_width_height = [x, y]
gameDisplay = pygame.display.set_mode(display_width_height, flags=pygame.RESIZABLE)
pygame.display.update()

# Variable for getting screen location
fullscreen = False
help_con = False
main_screen = False

# The code below initializes and plays audio!!
pygame.mixer.init()  # Initializes the Mixer/Player.
pygame.mixer.music.load("Sounds/dog_bark.mp3")  # Loads the audio file
pygame.mixer.music.play(-1)  # Plays the audio file and loops it forever.

# Internal Variables that will not change whether the game runs:
url = "https://dog.ceo/api/breeds/image/random"
path = os.path.join(os.path.abspath(os.curdir), "Images", "dog")

# The code underneath sets variables for colours:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
brightGreen = (3, 254, 1)
snakeGreen = (120, 154, 19)
poisonblue = (25, 25, 77)
grey = (37, 37, 37)

# blocks begins


def StartScreen():  # Defines the Code for the Start Screen
    pygame.mouse.set_visible(False)
    waiting = font.render("Please wait Loading...", 1, black)
    gameDisplay.fill(white)
    pygame.display.update()
    gameDisplay.blit(waiting, (0, 0))
    pygame.display.update()
    init_dog_loc = os.path.join(os.path.abspath(os.curdir), "Images", "logo", "dog.jpg")
    shrink_imgto_fit(init_dog_loc)
    # StartImage = pygame.image.load('Images/dog.jpg').convert() #Sets "StartImage" To the specified image
    StartImage = pygame.image.load(
        init_dog_loc
    )  # .convert() doesn't allow to set icon So removed.
    pygame.display.set_icon(StartImage)
    gameDisplay.blit(StartImage, (50, 50))
    pygame.display.update()
    DogRequest()


def DogRequest():
    global loading_screen
    import requests
    import json
    import random
    import os
    from PIL import Image
    from io import BytesIO

    no_random = random.randint(1, 100)
    filename = "dog" + str(no_random)
    try:
        result = requests.get(url)
        a = json.loads(result.text)
        img_url = a["message"]
        img1 = requests.get(img_url)
    except requests.exceptions.RequestException as e:
        while anim_running == True:
            pass
        else:
            print(e)
            logger.error("This is the error message: %s" % e)
            loading_screen = False
            loading_picture()
    img = Image.open(BytesIO(img1.content))
    if not os.path.exists(path):
        os.makedirs(path)
    while os.path.exists(path + filename + "." + img.format):
        filename = filename + str(no_random + 1)
    open(os.path.join(path, filename + "." + img.format), "wb").write(img1.content)
    stored_img = os.path.join(path, filename + "." + img.format)
    shrink_imgto_fit(stored_img)
    loading_screen = False
    openimg(stored_img)


def openimg(stored_img):
    global display_width_height
    global main_screen
    # filesave=font.render("Status: "+str(stored_img),1,black)
    final_loding_fill()
    filesave = font.render("Sucessfully Loaded a Picture OF Dog", 1, black)
    logging.info("File sucessfully saved at:::" + str(stored_img))
    gameDisplay.fill(white)
    pygame.display.update()
    gameDisplay.blit(filesave, (0, 0))
    pygame.display.update()
    Dogimg = pygame.image.load(stored_img).convert()
    # gameDisplay.blit(Dogimg, (int(display_width_height[0]/4),int(display_width_height[1]/4)))
    gameDisplay.blit(Dogimg, (10, int(display_width_height[1] / 8)))
    # pygame.display.set_icon(Dogimg)
    pygame.mouse.set_visible(True)
    pygame.display.toggle_fullscreen()
    pygame.display.update()
    user_help = font.render("Press H for HELP", 1, black)
    gameDisplay.blit(user_help, (0, 40))
    pygame.display.update()
    display_logo()
    main_screen = True
    show_reload_button()
    # endscreen()


def endscreen():
    for event in pygame.event.get():  # If a key is pressed or the mouse is moved.
        if event.type == pygame.QUIT:  # If the event is the quit button being clicked
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                quit()
            else:
                waiting = font.render("Please wait Loading...", 1, white)
                gameDisplay.fill(black)
                pygame.display.update()
                gameDisplay.blit(waiting, (0, 0))
                pygame.display.update()
                DogRequest()


def loading(msg):
    main_screen = False
    gameDisplay.fill(grey)
    waiting = font.render(msg, 1, white)
    pygame.display.update()
    gameDisplay.blit(waiting, (0, 0))
    pygame.display.update()
    loading_picture()


def loading_picture():
    global loading_screen
    global anim_running
    display_logo()
    if loading_screen == True:
        anim_running = True
        for i in range(0, 253):
            asurf = pygame.image.load(
                os.path.join("images", "loading", str(i) + ".gif")
            ).convert()
            gameDisplay.blit(
                asurf,
                (int(display_width_height[0] / 3), int(display_width_height[1] / 3)),
            )
            pygame.display.update()
            time.sleep(0.03)
        else:
            time.sleep(0.03)
            anim_running = False
    else:
        gameDisplay.fill(white)
        waiting = font.render("Connectivity Error Please try Later", 1, black)
        asurf = pygame.image.load(os.path.join("images", "error-internet.png"))
        gameDisplay.blit(
            asurf, (display_width_height[0] / 4, display_width_height[1] / 4)
        )
        gameDisplay.blit(waiting, (0, 0))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        quit()


def final_loding_fill():
    """Loading screen"""
    gameDisplay.fill(white)
    pygame.display.update()
    time.sleep(0.3)
    gameDisplay.fill(grey)
    pygame.display.update()
    time.sleep(0.3)
    gameDisplay.fill(white)
    pygame.display.update()
    time.sleep(0.3)


def shrink_imgto_fit(store_path):
    """Pillow utility to make it fit in screen"""
    global display_width_height
    from PIL import Image

    img = Image.open(store_path)
    while True:
        if img.size[0] > display_width_height[0]:
            basewidth = display_width_height[0] - 30
            hsize = img.size[1]
            img = img.resize((basewidth, hsize), Image.LANCZOS)
            img.save(store_path)
        elif img.size[1] > display_width_height[1]:
            basewidth = img.size[0]
            hsize = display_width_height[1] - int(display_width_height[1] / 8) - 60
            img = img.resize((basewidth, hsize), Image.LANCZOS)
            img.save(store_path)
        else:
            break


def display_logo():
    """This shows my logo"""
    global help_con
    logo = pygame.image.load(
        os.path.join(os.path.abspath(os.curdir), "Images", "logo", "Naveen M K.png")
    )
    if fullscreen == True:
        if help_con == True:
            gameDisplay.blit(
                logo,
                (
                    (int(display_width_height[0] / 2)) - 219,
                    int(display_width_height[1] - 219),
                ),
            )
        else:
            gameDisplay.blit(
                logo,
                (
                    int(display_width_height[0] - 401),
                    int(display_width_height[1] - 219),
                ),
            )
    else:
        if help_con == True:
            gameDisplay.blit(
                logo,
                (
                    (int(display_width_height[0] / 2)) - 401,
                    int(display_width_height[1] - 250),
                ),
            )
        else:
            gameDisplay.blit(
                logo,
                (
                    int(display_width_height[0]) - 401,
                    int(display_width_height[1] - 250),
                ),
            )
    pygame.display.update()


def help_screen():
    """This loads the help screen from `help.doghelp` file."""
    import random

    global help_con
    help_con = True
    final_loding_fill()
    gameDisplay.fill(white)
    font_list = pygame.font.get_fonts()
    rand = random.randint(0, len(font_list) - 1)
    font = pygame.font.SysFont(font_list[rand], 40)
    with open("help.doghelp", "r") as helpper:
        lines = helpper.readlines()
        height = 20
        for words in lines:
            blit_word = font.render(words[0:-1], 1, black)
            gameDisplay.blit(blit_word, (10, height))
            pygame.display.update()
            height += 40
    display_logo()
    help_con = False


def show_reload_button():
    """This shows the reload button"""
    if fullscreen == True:
        pygame.draw.rect(
            gameDisplay,
            red,
            pygame.Rect((display_width_height[0] - 220, 0), (200, 50)),
            5,
        )
        font = pygame.font.Font("Fonts/octin.ttf", 40)
        blit_word = font.render("Reload", 1, black)
        gameDisplay.blit(blit_word, (display_width_height[0] - 200, 0))
        # Rect(left, top, width, height)
        pygame.display.update()


StartScreen()  # Calls StartScreen
# print(pygame.mouse.get_focused())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the event is the quit button being clicked
            loading_screen = True
            loading("Bye Bye!  By Naveen M K")
            # loading_picture()
            loading_screen = False
            time.sleep(3)
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                loading_screen = True
                loading("Please wait Loading...")
                # loading_picture()
                DogRequest()
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                loading_screen = True
                loading("Bye Bye! By Naveen M K")
                # loading_picture()
                time.sleep(3)
                loading_screen = False
                pygame.quit()
                quit()
            elif event.key == pygame.K_f or event.key == pygame.K_F5:
                # logging.info('pygame.display.toggle_fullscreen()='+str(pygame.display.toggle_fullscreen()))
                if fullscreen == False:
                    loading_screen = True
                    loading("Full Screen Loading")
                    pygame.display.set_mode(flags=pygame.FULLSCREEN)
                    # logging.info('pygame.display.toggle_fullscreen()='+str(pygame.display.toggle_fullscreen()))
                    logging.info("Full Screen:" + str(fullscreen))
                    pygame.display.update()
                    time.sleep(2)
                    fullscreen = True
                    # loading_picture()
                    DogRequest()
                else:
                    final_loding_fill()
                    pygame.display.set_mode(flags=pygame.RESIZABLE)
                    pygame.display.update()
                    fullscreen = False
                    DogRequest()
            elif event.key == pygame.K_h:
                help_screen()
            else:
                loading_screen = True
                loading("Please wait Loading...")
                # loading_picture()
                DogRequest()
        elif pygame.mouse.get_pressed() == (1, 0, 0):
            print("hi")
            if main_screen == True and fullscreen == True:
                postion = pygame.mouse.get_pos()
                if postion[0] > display_width_height[0] - 220 and postion[1] < 50:
                    DogRequest()
