from player import Player


class Ghosts(Player):
    def change_speed_ghost(self, list_, ghost, turn, steps, l):
        try:
            if steps < list_[turn][2]:
                self.change_x = list_[turn][0]
                self.change_y = list_[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list_[turn][0]
                self.change_y = list_[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]
