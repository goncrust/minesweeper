import pygame

RECT_SIZE = 60
LIGHT_GREEN = (134, 168, 64)
LIGHTER_GREEN = (184, 218, 114)
DARK_GREEN = (128, 164, 58)
LIGHTER_DARK_GREEN = (178, 214, 108)
BLACK = (0, 0, 0)
WHITE = (180, 152, 124)
GREY = (168, 144, 120)
LEFT = 1
RIGHT = 3

class Renderer:

    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width*RECT_SIZE, height*RECT_SIZE))
        self.clock = pygame.time.Clock()

    def tick(self) -> bool:
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                return False

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def clear(self) -> None:
        self.screen.fill("black")

    def draw_rect(self, left: int, top: int, color: tuple) -> None:
        rect = pygame.Rect(left*RECT_SIZE, top*RECT_SIZE, RECT_SIZE, RECT_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_str(self, left: int, top: int, number: str) -> None:
        font = pygame.font.SysFont('arial', 50)
        text = font.render(str(number), True, (0, 0, 0))
        self.screen.blit(text, ((left + 0.25)*RECT_SIZE, (top + 0.05)*RECT_SIZE))

    def get_clicked(self) -> tuple:
        clicks = []
        flags = []
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicks += [pygame.mouse.get_pos()]
                elif event.button == 3:
                    flags += [pygame.mouse.get_pos()]
        return (clicks, flags)

    def get_mouse_pos(self) -> tuple:
        return pygame.mouse.get_pos() if pygame.mouse.get_focused() == 1 else (-1, -1)

    def quit(self) -> None:
        pygame.quit()
