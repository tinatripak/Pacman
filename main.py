import pygame
from pygame import *
black_colour = (0, 0, 0)
white_colour = (255, 255, 255)
violet_colour = (66, 49, 137)
red_colour = (255, 0, 0)
yellow_colour = (255, 255, 0)

screen = pygame.display.set_mode((900, 604))
pygame.display.set_caption('Pac-Man')


def notepad_to_array(path, array):
    with open(path) as f:
        content = f.read().splitlines()
        for str in content:
            temp = []
            for t in str.split(','):
                temp.append(int(t))
            array.append(temp)


def first_map(sprites_list):
    wall_list = pygame.sprite.RenderPlain()
    walls = []
    # x, y, width, height
    notepad_to_array("C:/Users/Кристина/Desktop/Map.txt", walls)
    for i in walls:
        wall = Walls(i[0], i[1], i[2], i[3], violet_colour)
        wall_list.add(wall)
        sprites_list.add(wall)
    return wall_list


# TODO Create walls
class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


def spawn_setup(sprites_list):
    spawn = pygame.sprite.RenderPlain()
    spawn.add(Walls(281, 242, 44, 3, white_colour))
    sprites_list.add(spawn)
    return spawn


# TODO Create dots
class Dots(pygame.sprite.Sprite):
    def __init__(self, width, height, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def previous_direction(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:

            self.rect.top = new_y

            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


class Ghost(Player):
    def change_speed(self, list, ghost, turn, steps, l):
        try:
            if steps < list[turn][2]:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


directions_of_pinky = []
notepad_to_array("C:/Users/Кристина/Desktop/Pinky_directions.txt", directions_of_pinky)
directions_of_blinky = []
notepad_to_array("C:/Users/Кристина/Desktop/Blinky_directions.txt", directions_of_blinky)
directions_of_inky = []
notepad_to_array("C:/Users/Кристина/Desktop/Inky_directions.txt", directions_of_inky)
directions_of_clyde = []
notepad_to_array("C:/Users/Кристина/Desktop/Clyde_directions.txt", directions_of_clyde)

pygame.init()
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)


def start_game():
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    ghost_list = pygame.sprite.RenderPlain()
    pacman_list = pygame.sprite.RenderPlain()
    wall_list = first_map(all_sprites_list)
    gate = spawn_setup(all_sprites_list)

    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_turn = 0
    c_steps = 0

    pacman = Player(287, 439, "C:/Users/Кристина/Desktop/Pacman.png")
    blinky = Ghost(287, 199, "C:/Users/Кристина/Desktop/2469740-blinky.png")
    pinky = Ghost(287, 259, "C:/Users/Кристина/Desktop/2469744-pinky.png")
    inky = Ghost(255, 259, "C:/Users/Кристина/Desktop/2469741-inky.png")
    clyde = Ghost(319, 259, "C:/Users/Кристина/Desktop/2469743-clyde.png")

    all_sprites_list.add(pacman)
    pacman_list.add(pacman)
    ghost_list.add(blinky)
    all_sprites_list.add(blinky)
    ghost_list.add(pinky)
    all_sprites_list.add(pinky)
    ghost_list.add(inky)
    all_sprites_list.add(inky)
    ghost_list.add(clyde)
    all_sprites_list.add(clyde)

    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Dots(4, 4, yellow_colour, )

                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_list, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)
    score = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.change_speed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.change_speed(30, 0)
                if event.key == pygame.K_UP:
                    pacman.change_speed(0, -30)
                if event.key == pygame.K_DOWN:
                    pacman.change_speed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pacman.change_speed(30, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.change_speed(-30, 0)
                if event.key == pygame.K_UP:
                    pacman.change_speed(0, 30)
                if event.key == pygame.K_DOWN:
                    pacman.change_speed(0, -30)

        pacman.update(wall_list, gate)

        returned = pinky.change_speed(directions_of_pinky, False, p_turn, p_steps, len(directions_of_pinky) - 1)
        p_turn = returned[0]
        p_steps = returned[1]
        pinky.change_speed(directions_of_pinky, False, p_turn, p_steps, len(directions_of_pinky) - 1)
        pinky.update(wall_list, False)

        returned = blinky.change_speed(directions_of_blinky, False, b_turn, b_steps, len(directions_of_blinky) - 1)
        b_turn = returned[0]
        b_steps = returned[1]
        blinky.change_speed(directions_of_blinky, False, b_turn, b_steps, len(directions_of_blinky) - 1)
        blinky.update(wall_list, False)

        returned = inky.change_speed(directions_of_inky, False, i_turn, i_steps, len(directions_of_inky) - 1)
        i_turn = returned[0]
        i_steps = returned[1]
        inky.change_speed(directions_of_inky, False, i_turn, i_steps, len(directions_of_inky) - 1)
        inky.update(wall_list, False)

        returned = clyde.change_speed(directions_of_clyde, "clyde", c_turn, c_steps, len(directions_of_clyde) - 1)
        c_turn = returned[0]
        c_steps = returned[1]
        clyde.change_speed(directions_of_clyde, "clyde", c_turn, c_steps, len(directions_of_clyde) - 1)
        clyde.update(wall_list, False)

        blocks_hit_list = pygame.sprite.spritecollide(pacman, block_list, True)

        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        screen.fill(black_colour)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        ghost_list.draw(screen)

        text = font.render("Score", True, (255, 255, 0))
        screen.blit(text, [718, 10])
        text1 = font.render(str(score) + "/" + str(bll), True, (255, 255, 0))
        screen.blit(text1, [720, 40])

        if score == bll:
            doNext("You won!", 145, all_sprites_list, block_list, ghost_list, pacman_list,
                   wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(pacman, ghost_list, False)

        if monsta_hit_list:
            doNext("You lose!", 235, all_sprites_list, block_list, ghost_list, pacman_list, wall_list, gate)

        pygame.display.flip()
        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_list, wall_list, gate):
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_list
                    del wall_list
                    del gate
                    start_game()

        window = pygame.Surface((300, 150))
        window.set_alpha(10)
        window.fill((255, 0, 0))
        screen.blit(window, (140, 220))

        text1 = font.render(message, True, white_colour)
        screen.blit(text1, [left, 233])
        text2 = font.render("ENTER to PLAY again", True, white_colour)
        screen.blit(text2, [142, 303])
        text3 = font.render("ESC to FINISH this game", True, white_colour)
        screen.blit(text3, [142, 333])

        pygame.display.flip()
        clock.tick(10)


start_game()
pygame.quit()
