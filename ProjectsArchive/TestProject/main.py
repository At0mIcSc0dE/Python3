import pygame


pygame.init()

(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

running = True
if pygame.joystick.get_count() < 1:
    print("No Joysticks Found, Exiting!")
    running = False


while running:
    for event in pygame.event.get():

        print("EVENT")

        # if event.type == pygame.JOYBUTTONDOWN:
        #     print("Joystick pressed!")
        # else:
        #     print("No")
