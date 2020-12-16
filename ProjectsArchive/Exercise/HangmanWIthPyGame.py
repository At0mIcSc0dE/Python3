import pygame
import Alphabet as alpha
import collections

pygame.init()
win = pygame.display.set_mode((900, 600))
win.fill((255, 255, 255))

class Button:
    def __init__(self, r, g, b, x, y, width, height, text=''):
        self.r = r
        self.g = g
        self.b = b
        self.color = (r, g, b)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def drawRectBtn(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            pygame.font.init()
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def getWord():
    import random
    word = random.choice(open('C:/Temp/WordBank.txt').read().splitlines()).upper()
    if ' ' not in word : return word


def redrawWindow(btn_list):
    win.fill((255, 255, 255))
    for btn in btn_list:
        btn.drawRectBtn(win)


def getBtns():
    x_coord = 10
    iteration = 0
    btn_lst = []
    for itr, char in enumerate(alpha.getUpper()):
        if itr < 13:
            btn = Button(0, 255, 0, x_coord, 10, 40, 40, char)
            btn_lst.append(btn)
            x_coord += 70
        if itr > 12:
            if iteration == 0:
                x_coord = 10
                iteration = 1
            btn = Button(0, 255, 0, x_coord, 80, 40, 40, char)
            btn_lst.append(btn)
            x_coord += 70
    return btn_lst    # return lbl_list


font = pygame.font.Font('freesansbold.ttf', 32)
def getLbl(msg, x, y):
    text = font.render(msg, True, (0, 0, 0))
    win.blit(text, [x, y])


def isInWord(txt):
    if txt in word:
        return True
    return False


def isSameWord():
    if collections.Counter(word) == collections.Counter(correct_letters):
        return True
    return False


def drawGuessedInput(btn):
    gen_indcs = []
    for itr, letter in enumerate(word):
        if letter == btn.text:
            gen_indcs.append(itr)

    for indx, char in zip(gen_indcs, word):
        if indx == 0:
            getLbl(word[0], 0, 450)
        elif indx == 1:
            getLbl(word[1], 50, 450)
        elif indx == 2:
            getLbl(word[2], 100, 450)
        elif indx == 3:
            getLbl(word[3], 150, 450)
        elif indx == 4:
            getLbl(word[4], 200, 450)
        elif indx == 5:
            getLbl(word[5], 250, 450)
        elif indx == 6:
            getLbl(word[6], 300, 450)
        elif indx == 7:
            getLbl(word[7], 350, 450)
        elif indx == 8:
            getLbl(word[8], 400, 450)
        elif indx == 9:
            getLbl(word[9], 450, 450)
        elif indx == 10:
            getLbl(word[10], 500, 450)
        elif indx == 11:
            getLbl(word[11], 550, 450)
        elif indx == 12:
            getLbl(word[12], 600, 450)
        elif indx == 13:
            getLbl(word[13], 750, 450)
        elif indx == 14:
            getLbl(word[14], 800, 450)
        elif indx == 15:
            getLbl(word[15], 850, 450)


def onClick(btn):
    global tries
    btn_list.remove(btn)
    if isInWord(btn.text):
        for i in range(word.count(btn.text)):
            correct_letters.append(btn.text)
            drawGuessedInput(btn)
            if isSameWord():
                pygame.quit()
                print(f'Done, word {word}')
                exit()
    else:
        tries -= 1
    redrawWindow(btn_list)


run = True
correct_letters = []
tries = 6
btn_list = getBtns()
word = getWord()
print(word)



while run:

    if tries != 0:
        redrawWindow(btn_list)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btn_list:
                    if btn.isOver(pos):
                        onClick(btn)

    else:
        pygame.quit()
        print('Failed')
        quit()


