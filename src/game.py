from pygame import Overlay
import renderer
import random

EMPTY = -1
BOMB = 10
OPEN = 11
FLAG = 12


class Minesweeper:

    def __init__(self, height: int, width: int, nbombs: int) -> None:
        self.height = height
        self.width = width
        self.nbombs = nbombs
        self.renderer = renderer.Renderer(width, height)
        self.reset_game()
        self.highlighted = (-1, -1)

    def main_loop(self) -> None:
        while (self.render()):
            clicks = self.renderer.get_clicked()
            for click in clicks[0]:
                if not self.make_play(click[0], click[1]) or self.check_finished():
                    #self.quit_game()
                    self.reset_game()
                    continue
            for click in clicks[1]:
                self.put_flag(click[0], click[1])
            self.update_highlight()

    def update_highlight(self):
        mouse_pos = self.renderer.get_mouse_pos()
        if mouse_pos == (-1, -1):
            self.highlighted = (-1, -1)
            return
        x = mouse_pos[0]//renderer.RECT_SIZE
        y = mouse_pos[1]//renderer.RECT_SIZE
        if self.visible_rects[x][y] in (EMPTY, FLAG):
            self.highlighted = (x, y)
        else:
            self.highlighted = (-1, -1)

    def put_flag(self, left: int, top: int) -> None:
        x = left//renderer.RECT_SIZE 
        y = top//renderer.RECT_SIZE 
        print(f"{x}, {y}: {left}, {top}")
        if self.visible_rects[x][y] == EMPTY:
            self.visible_rects[x][y] = FLAG
        elif self.visible_rects[x][y] == FLAG:
            self.visible_rects[x][y] = EMPTY

    def check_finished(self) -> bool:
        for x in range(self.width):
            for y in range(self.height):
                if self.rects[x][y] == BOMB:
                    continue
                elif self.visible_rects[x][y] == EMPTY:
                    return False
        print("YOU WON")
        return True

    def open_zeros(self, rect_x: int, rect_y: int):
        zeros = [(rect_x, rect_y)]
        self.visible_rects[rect_x][rect_y] = OPEN

        z = 0
        while z < len(zeros):
            left = zeros[z][0]
            top = zeros[z][1]
            x = left - 1 if left - 1 >= 0 else left
            y = top - 1 if top - 1 >= 0 else top
            x_end = left + 1 if left + 1 < self.width else left
            y_end = top + 1 if top + 1 < self.height else top

            for i in range(x, x_end + 1):
                for k in range(y, y_end + 1):
                    if i == left and k == top:
                        continue
                    if self.rects[i][k] == 0 and (i,k) not in zeros:
                        zeros += [(i, k)]
                        self.visible_rects[i][k] = OPEN
                    elif self.rects[i][k] != BOMB:
                        self.visible_rects[i][k] = self.rects[i][k]
            z += 1

    def make_play(self, left: int, top: int) -> bool:
        x = left//renderer.RECT_SIZE 
        y = top//renderer.RECT_SIZE 
        print(f"{x}, {y}: {left}, {top}")
        if self.rects[x][y] == BOMB:
            print("YOU LOST")
            return False
        elif self.rects[x][y] == 0:
            self.open_zeros(x, y)
        elif self.rects[x][y] != FLAG:
            self.visible_rects[x][y] = self.rects[x][y]
        return True

    def render(self) -> bool:
        self.renderer.clear()
        
        curr_color = renderer.LIGHT_GREEN
        curr_color_filled = renderer.WHITE
        for x in range(self.width):
            for y in range(self.height):
                if self.visible_rects[x][y] == BOMB:
                    self.renderer.draw_rect(x, y, renderer.BLACK)
                if self.visible_rects[x][y] not in (EMPTY, FLAG):
                    self.renderer.draw_rect(x, y, curr_color_filled)
                else:
                    if curr_color == renderer.DARK_GREEN:
                        color = renderer.LIGHTER_DARK_GREEN if self.highlighted == (x, y) else renderer.DARK_GREEN
                    else:
                        color = renderer.LIGHTER_GREEN if self.highlighted == (x, y) else renderer.LIGHT_GREEN
                    self.renderer.draw_rect(x, y, color)

                # draw number
                if self.visible_rects[x][y] not in (EMPTY, OPEN, 0, FLAG):
                    self.renderer.draw_str(x, y, str(self.visible_rects[x][y]))
                elif self.visible_rects[x][y] == FLAG:
                    self.renderer.draw_str(x, y, "!")

                # switch color
                curr_color = renderer.DARK_GREEN if curr_color == renderer.LIGHT_GREEN else renderer.LIGHT_GREEN
                curr_color_filled = renderer.GREY if curr_color_filled == renderer.WHITE else renderer.WHITE
            # switch color
            curr_color = renderer.DARK_GREEN if curr_color == renderer.LIGHT_GREEN else renderer.LIGHT_GREEN
            curr_color_filled = renderer.GREY if curr_color_filled == renderer.WHITE else renderer.WHITE
        return self.renderer.tick()

    def generate_game(self):
        self.generate_bombs()
        self.generate_nums()

    def get_rect_num(self, left: int, top: int) -> int:
        x = left - 1 if left - 1 >= 0 else left
        y = top - 1 if top - 1 >= 0 else top
        x_end = left + 1 if left + 1 < self.width else left
        y_end = top + 1 if top + 1 < self.height else top

        total = 0
        for i in range(x, x_end + 1):
            for k in range(y, y_end + 1):
                if i == left and k == top:
                    continue
                if self.rects[i][k] == BOMB:
                    total += 1
        return total

    def generate_nums(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.rects[x][y] != BOMB:
                    self.rects[x][y] = self.get_rect_num(x, y)

    def generate_bombs(self) -> None:
        nrects = self.width * self.height
        generated = []
        
        while len(generated) < self.nbombs:
            rnd = random.randint(0, nrects-1)
            if rnd in generated:
                continue
            generated += [rnd]
            
            # fill self.rects
            y = rnd // self.width 
            x = rnd - y*self.width
            self.rects[x][y] = BOMB

    def start_game(self) -> None:
        self.generate_game()
        self.main_loop()

    def reset_game(self) -> None:
        self.rects = [ [EMPTY]*self.height for _ in range(self.width) ]
        self.visible_rects = [ [EMPTY]*self.height for _ in range(self.width) ]
        self.generate_game()

    def quit_game(self) -> None:
        self.renderer.quit()
        exit(0)

