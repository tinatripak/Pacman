import pdb
import pygame
from pygame import *
from const import black_colour, violet_colour, white_colour, DirectionState, SCREEN_SIZE, path_pacman_img, font
from player import Player
from walls import Walls
from ghosts import Ghosts
from dots import Dots

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Pac-Man')
board = pygame.image.load("pacman_startgame.png")
board1 = board.get_rect(
    bottomright=(800, 500))
screen.blit(board, board1)
pygame.display.update()


def start_music():
    pygame.init()
    mixer.music.load('pacman_beginning.wav')
    mixer.music.play()
    key_pressed = False
    while not key_pressed:
        for event_ in pygame.event.get():
            if event_.type == KEYDOWN and event_.key == K_RETURN:
                key_pressed = True


start_music()


def notepad_to_array(path, array):
    with open(path) as f:
        content = f.read().splitlines()
        for s in content:
            temp = []
            for t in s.split(','):
                temp.append(int(t))
            array.append(temp)


directions_of_pinky = directions_of_blinky = directions_of_inky = directions_of_clyde = []
notepad_to_array("Pinky_directions.txt", directions_of_pinky)
notepad_to_array("Blinky_directions.txt", directions_of_blinky)
notepad_to_array("Inky_directions.txt", directions_of_inky)
notepad_to_array("Clyde_directions.txt", directions_of_clyde)


def first_map(sprites_list):
    wall_list = pygame.sprite.RenderPlain()
    walls = []
    # x, y, width, height
    notepad_to_array("Map.txt", walls)
    for i in walls:
        wall = Walls(i[0], i[1], i[2], i[3], violet_colour)
        wall_list.add(wall)
        sprites_list.add(wall)
    return wall_list


def spawn_setup(sprites_list):
    spawn = pygame.sprite.RenderPlain()
    spawn.add(Walls(281, 242, 44, 3, white_colour))
    sprites_list.add(spawn)
    return spawn


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
pacman_img = pygame.image.load(path_pacman_img)


def start_game():
    sprites_list = pygame.sprite.RenderPlain()
    walls_list = first_map(sprites_list)
    dots_list = pygame.sprite.RenderPlain()
    spawn = spawn_setup(sprites_list)
    ghosts_list = pygame.sprite.RenderPlain()
    pacman_list = pygame.sprite.RenderPlain()

    pink_turn = blinky_turn = inky_turn = clyde_turn = 0
    pink_steps = blinky_steps = inky_steps = clyde_steps = 0

    pacman = Player(287, 439, path_pacman_img)
    blinky = Ghosts(287, 199, "ghosts/2469740-blinky.png")
    pinky = Ghosts(287, 259, "ghosts/2469744-pinky.png")
    inky = Ghosts(255, 259, "ghosts/2469741-inky.png")
    clyde = Ghosts(319, 259, "ghosts/2469743-clyde.png")

    sprites_list.add(pacman)
    pacman_list.add(pacman)
    ghosts_list.add(blinky)
    sprites_list.add(blinky)
    ghosts_list.add(pinky)
    sprites_list.add(pinky)
    ghosts_list.add(inky)
    sprites_list.add(inky)
    ghosts_list.add(clyde)
    sprites_list.add(clyde)

    # TODO Locations for dots
    for row in range(19):
        for column in range(19):
            if (6 < row < 9) and (7 < column < 11):
                continue
            else:
                dots = Dots(4, 4)

            dots.rect.x = 30 * column + 32
            dots.rect.y = 30 * row + 32

            blinky_collide = pygame.sprite.spritecollide(dots, walls_list, False)
            pinky_collide = pygame.sprite.spritecollide(dots, pacman_list, False)
            if blinky_collide:
                continue
            elif pinky_collide:
                continue
            else:
                dots_list.add(dots)
                sprites_list.add(dots)

    score = 0
    done = False

    win_score = len(dots_list)

    while not done:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                done = True

            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_UP:
                    pacman.image = set_direction(DirectionState.up.name)
                    pacman.change_speed_player(0, -30)
                if event_.key == pygame.K_DOWN:
                    pacman.image = set_direction(DirectionState.down.name)
                    pacman.change_speed_player(0, 30)
                if event_.key == pygame.K_LEFT:
                    pacman.image = set_direction(DirectionState.left.name)
                    pacman.change_speed_player(-30, 0)
                if event_.key == pygame.K_RIGHT:
                    pacman.image = set_direction(DirectionState.right.name)
                    pacman.change_speed_player(30, 0)

            if event_.type == pygame.KEYUP:
                if event_.key == pygame.K_UP:
                    pacman.image = set_direction(DirectionState.up.name)
                    pacman.change_speed_player(0, 30)
                if event_.key == pygame.K_DOWN:
                    pacman.image = set_direction(DirectionState.down.name)
                    pacman.change_speed_player(0, -30)
                if event_.key == pygame.K_LEFT:
                    pacman.image = set_direction(DirectionState.left.name)
                    pacman.change_speed_player(30, 0)
                if event_.key == pygame.K_RIGHT:
                    pacman.image = set_direction(DirectionState.right.name)

                    pacman.change_speed_player(-30, 0)

        pacman.new_position_player(walls_list, spawn)

        changed_speed_inky = inky.change_speed_ghost(directions_of_inky, False, inky_turn, inky_steps,
                                                     len(directions_of_inky) - 1)
        inky_turn = changed_speed_inky[0]
        inky_steps = changed_speed_inky[1]
        inky.change_speed_ghost(directions_of_inky, False, inky_turn, inky_steps, len(directions_of_inky) - 1)
        inky.new_position_player(walls_list, False)

        changed_speed_clyde = clyde.change_speed_ghost(directions_of_clyde, "clyde", clyde_turn, clyde_steps,
                                                       len(directions_of_clyde) - 1)
        clyde_turn = changed_speed_clyde[0]
        clyde_steps = changed_speed_clyde[1]
        clyde.change_speed_ghost(directions_of_clyde, "clyde", clyde_turn, clyde_steps, len(directions_of_clyde) - 1)
        clyde.new_position_player(walls_list, False)

        changed_speed_pinky = pinky.change_speed_ghost(directions_of_pinky, False, pink_turn, pink_steps,
                                                       len(directions_of_pinky) - 1)
        pink_turn = changed_speed_pinky[0]
        pink_steps = changed_speed_pinky[1]
        pinky.change_speed_ghost(directions_of_pinky, False, pink_turn, pink_steps, len(directions_of_pinky) - 1)
        pinky.new_position_player(walls_list, False)

        changed_speed_blinky = blinky.change_speed_ghost(directions_of_blinky, False, blinky_turn, blinky_steps,
                                                         len(directions_of_blinky) - 1)
        blinky_turn = changed_speed_blinky[0]
        blinky_steps = changed_speed_blinky[1]
        blinky.change_speed_ghost(directions_of_blinky, False, blinky_turn, blinky_steps, len(directions_of_blinky) - 1)
        blinky.new_position_player(walls_list, False)

        check_location(pacman)

        check_location(inky)

        check_location(clyde)

        check_location(pinky)

        check_location(blinky)

        sprite_collides_dots = pygame.sprite.spritecollide(pacman, dots_list, True)

        if sprite_collides_dots:

            if len(sprite_collides_dots) > 0:
                score += len(sprite_collides_dots)
            mixer.music.load('pacman_chomp.wav')
            mixer.music.play()

        # TODO Clean
        screen.fill(black_colour)
        # TODO Draw
        walls_list.draw(screen)
        spawn.draw(screen)
        sprites_list.draw(screen)
        ghosts_list.draw(screen)
        # TODO Write Score Of Player
        text = font.render("High Score", True, (255, 255, 0))
        screen.blit(text, [690, 10])
        text1 = font.render(str(score) + "/" + str(win_score), True, (255, 255, 0))
        screen.blit(text1, [690, 40])

        text = font.render("Location", True, (255, 255, 0))
        screen.blit(text, [690, 70])
        text1 = font.render("X: " + str(pacman.rect.x) + " Y: " + str(pacman.rect.y), True, (255, 255, 0))
        screen.blit(text1, [690, 100])

        if pygame.sprite.spritecollide(pacman, ghosts_list, False):
            mixer.music.load('pacman_death.wav')
            mixer.music.play()
            finish_game(f"You lose!", 235, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)
        if score == win_score:
            finish_game("You won!", 145, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)

        pygame.display.flip()
        clock.tick(10)


def set_direction(direction):
    if direction == "right":
        return pacman_img
    if direction == "up":
        return pygame.transform.rotate(pacman_img, 90)
    if direction == "left":
        return pygame.transform.rotate(pacman_img, 180)
    if direction == "down":
        return pygame.transform.rotate(pacman_img, 270)


def check_location(player):
    if (player.rect.x < 17) and (259 <= player.rect.y <= 319):
        player.rect.x = 587

    if (player.rect.x > 587) and (259 <= player.rect.y <= 319):
        player.rect.x = 17


def finish_game(message, left, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn):
    while True:

        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                pdb.set_trace()
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_ESCAPE:
                    pygame.quit()
                    pdb.set_trace()
                if event_.key == pygame.K_RETURN:
                    del sprites_list
                    del dots_list
                    del ghosts_list
                    del pacman_list
                    del walls_list
                    del spawn
                    start_game()

        # TODO Window output: win or loss
        window = pygame.Surface((300, 170))
        window.set_alpha(10)
        window.fill((255, 0, 0))
        screen.blit(window, (160, 220))

        text1 = font.render(message, True, (255, 246, 212))
        screen.blit(text1, [left, 233])
        text2 = font.render("ENTER to PLAY again", True, (255, 246, 212))
        screen.blit(text2, [180, 303])
        text3 = font.render("ESC to FINISH this game", True, (255, 246, 212))
        screen.blit(text3, [180, 333])

        pygame.display.flip()
        clock.tick(10)


start_game()
pygame.quit()
pdb.set_trace()
