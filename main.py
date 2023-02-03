# Mario style level creator
# makes a 2D array 256x16, which has an int value associated
#   // 0 = NOTHING (BG)
# 	// 1 = FLOOR
# 	// 2 = block - type and texture assigned (oop blocks)
# 	// 3 = tp - an invisible block.
# 	// 4 = invis wall/world borders - could combine with block, we will see how this goess
# 	// 5 = Decorative
#   // 6 = Entities - Goomba, Koopa, Flag,
#
# Level editor needs to be a pygame window, and a scrollable 0-256 grid or the ability to zoom.
# Pygame window should have:
#       - A grid    ===
#       - Mouse or keyboard selection
#       - Brush tool, which cycles through the above values to represent on or off
#       - Export/save as into a text file
#       - load text level data
#
# TODO:
#
import copy
import random
import sys
import pygame
import Export  # tkinter Dialogue box
import ImportLvl  # same as above but for imports

blockTypeColors = (
    (199, 176, 76),  # Floor
    (112, 57, 9),  # Block
    (166, 58, 137),  # TP
    (204, 204, 204),  # Invis Barrier
    (3, 87, 161),  # Decoration
    (150, 2, 24),  # Entity Spawns
)

greys = (
    (24, 43, 30),  # Darkest
    (24, 34, 43),
    (33, 24, 43),
    (43, 34, 24),
    (97, 80, 61)
)

Grey = (43, 41, 43)  # Dark Grey
SelectColor = (194, 14, 14)
WIDTH, HEIGHT = 960, 720


def IncrementTowards(a, b):
    if (a < b):
        return a + 1
    if (a > b):
        return a - 1
    return a


# If the selection is at the edges, we do nothing and leave the camera
# If the selection is within the range 15, to (256-15) 241, Center the camera
# Not smoothing, just jump to positions
# This will work by shifting all y positions of every grid cell
class Camera:
    def __init__(self):
        # should go from 0 - 240
        self.posy = 0

    def CamMove(self, selectionY):
        self.posy = selectionY - 15
        if selectionY > 241:
            self.posy = 241 - 15
        if selectionY < 15:
            self.posy = 0


class Manager:
    def __init__(self, grid, screen, Clock):
        self.textFont = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.grid = grid
        self.gridsize = 32
        self.screen = screen
        self.clock = Clock

        # Selection
        self.size = 1
        self.drawMode = 1  # 0 = Circle, 1 = Square, 2 = Line, 3 = Fill
        self.blockType = 0

        self.xbound = 255
        self.ybound = 15
        self.Selection = [0, 0]
        self.movespeed = 1

        # Pause stuff
        self.paused = False

        # Dynamic BG stuff
        self.BGTiemr = 0
        self.BGTimeLimit = 10
        self.bgSelection = random.randint(0, 3)
        self.bg = greys[self.bgSelection]

        # camera
        self.Cam = Camera()

    def Text(self, screen, Text, pox, posy):
        selectText = self.textFont.render(Text, False, (255, 255, 255))
        selectTextPos = selectText.get_rect(x=pox, y=posy)
        screen.blit(selectText, selectTextPos)

    def UpdateGrid(self, newGrid):
        self.grid = newGrid

    def DrawBlocks(self):

        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if y != 0:
                    ypos = i - self.Cam.posy

                    ItemRect = pygame.rect.Rect(ypos * self.gridsize, j * self.gridsize, self.gridsize, self.gridsize)
                    pygame.draw.rect(self.screen, blockTypeColors[y], ItemRect)

    def DrawGrid(self):
        self.UpdateBg()
        self.DrawBlocks()

        # BG drawing grid based on item indexes
        # item y - camera y
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                ypos = i - self.Cam.posy
                ItemRect = pygame.rect.Rect(ypos * self.gridsize, j * self.gridsize, self.gridsize, self.gridsize)
                if i % 30 == 0:
                    pygame.draw.rect(self.screen, (20, 201, 74), ItemRect, 2)
                elif i % 15 == 0:
                    pygame.draw.rect(self.screen, (147, 161, 116), ItemRect, 2)
                else:
                    pygame.draw.rect(self.screen, Grey, ItemRect, 2)

        selectY = self.Selection[0] - self.Cam.posy
        SelectionRect = pygame.rect.Rect(selectY * self.gridsize, self.Selection[1] * self.gridsize, self.gridsize,
                                         self.gridsize)
        pygame.draw.rect(self.screen, SelectColor, SelectionRect, 4)

    def DrawText(self):
        # Position
        self.Text(self.screen, f"Pos: {self.Selection}", 0, 512)

        # step distance
        self.Text(self.screen, f"step Distance: {self.movespeed}", 0, 544)

        # Brush: Type, Size, Shape
        self.Text(self.screen, f"Type: {self.blockType}", 0, 576)

    def pauseOverlay(self):
        overlayDisplay = pygame.Surface((WIDTH, HEIGHT))
        overlayDisplay.set_alpha(128)
        overlayDisplay.fill((0, 0, 0))
        self.screen.blit(overlayDisplay, (0, 0))
        pygame.display.update()

    def Paused(self):
        # overlay
        self.pauseOverlay()

        while self.paused:
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_p]:
                    self.paused = False

    def MainLoop(self):
        self.screen.fill(self.bg)
        self.DrawGrid()
        self.DrawText()
        pygame.display.flip()


        if not self.paused:
            # enables fast movement
            if pygame.key.get_mods() == pygame.KMOD_LALT:
                self.FastMove()
                fastmove = True
            else:
                fastmove = False
            for event in pygame.event.get():
                # stuff that isnt movement
                self.OptionInput(event)
                # Regular movement
                if not fastmove:
                    self.GetInput(event)
                if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.CollisionCheck()
            # Move the camera
            self.Cam.CamMove(self.Selection[0])
        else:
            self.Paused()
        self.clock.tick(60)

    def UpdateBg(self):

        self.BGTiemr += 1
        # only update when timer reaches limit
        if self.BGTiemr == self.BGTimeLimit:
            self.BGTiemr = 0
            # Update Selection
            if (self.bg == greys[self.bgSelection]):
                if self.bgSelection == len(greys) - 1:
                    self.bgSelection = 0
                else:
                    self.bgSelection += 1
            else:
                # Makes dynamic bg, and moves linearly towards the next color in the list
                newColor = list(self.bg)
                newColor[0] = IncrementTowards(newColor[0], greys[self.bgSelection][0])
                newColor[1] = IncrementTowards(newColor[1], greys[self.bgSelection][1])
                newColor[2] = IncrementTowards(newColor[2], greys[self.bgSelection][2])
                self.bg = tuple(newColor)

    # While import/exporting, game is paused, so you cant be a dastardly devil and accidently kill the editor

    def export(self):
        self.paused = True
        self.pauseOverlay()
        Export.main(self.grid)
        self.paused = False

    def importLevel(self):
        self.paused = True
        self.pauseOverlay()
        self.UpdateGrid(ImportLvl.main(self.grid))
        self.paused = False

    def CollisionCheck(self):
        if self.Selection[0] > self.xbound:
            self.Selection[0] = self.xbound
        if self.Selection[0] < 0:
            self.Selection[0] = 0

        if self.Selection[1] > self.ybound:
            self.Selection[1] = self.ybound
        if self.Selection[1] < 0:
            self.Selection[1] = 0

    def FastMove(self):
        movespeed = self.movespeed


        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.SetSquare()

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            movespeed += 5
        # Left - Right
        if pygame.key.get_pressed()[pygame.K_a]:
            self.Selection[0] -= movespeed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.Selection[0] += movespeed

        # Up - Down
        if pygame.key.get_pressed()[pygame.K_s]:
            self.Selection[1] += movespeed
        if pygame.key.get_pressed()[pygame.K_w]:
            self.Selection[1] -= movespeed

    def OptionInput(self,keyboardEvent):


        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.SetSquare()

        if keyboardEvent.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_p]:
                self.paused = True
            # Increase Step
            if pygame.key.get_pressed()[pygame.K_EQUALS]:
                self.movespeed += 1
            if pygame.key.get_pressed()[pygame.K_MINUS]:
                self.movespeed -= 1

            # Skip to ends
            if pygame.key.get_pressed()[pygame.K_END]:
                self.Selection[0] = self.xbound
            if pygame.key.get_pressed()[pygame.K_HOME]:
                self.Selection[0] = 0

            if pygame.key.get_pressed()[pygame.K_TAB]:
                if pygame.key.get_mods() == pygame.KMOD_LSHIFT:
                    self.Selection[0] -= 30
                else:
                    self.Selection[0] += 30


            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                self.blockType += 1
                if self.blockType > len(blockTypeColors) - 1:
                    self.blockType = 0

            if pygame.key.get_pressed()[pygame.K_COMMA]:
                self.blockType -= 1
                if self.blockType < 0:
                    self.blockType = len(blockTypeColors) - 1


            if pygame.key.get_pressed()[pygame.K_F1]:
                self.export()

            if pygame.key.get_pressed()[pygame.K_F2]:
                self.importLevel()


    def GetInput(self, keyboardEvent):
        movespeed = self.movespeed
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            movespeed += 5

        if keyboardEvent.type == pygame.KEYDOWN:

            if pygame.key.get_pressed()[pygame.K_p]:
                self.paused = True
            # Increase Step
            if pygame.key.get_pressed()[pygame.K_EQUALS]:
                self.movespeed += 1
            if pygame.key.get_pressed()[pygame.K_MINUS]:
                self.movespeed -= 1

            # Left - Right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.Selection[0] -= movespeed
            if pygame.key.get_pressed()[pygame.K_d]:
                self.Selection[0] += movespeed

            # Up - Down
            if pygame.key.get_pressed()[pygame.K_s]:
                self.Selection[1] += movespeed
            if pygame.key.get_pressed()[pygame.K_w]:
                self.Selection[1] -= movespeed

        return

    # Turn current squarespace on, based on drawmode Value
    def SetSquare(self):
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                if i == self.Selection[0] and j == self.Selection[1]:
                    self.grid[i][j] = self.blockType



def main(Grid):
    icon = pygame.image.load("EditorLogo.png")
    grid = Grid
    pygame.init()
    Screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0, 0, 0)
    pygame.display.set_caption("Level Editor")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    gm = Manager(grid, Screen, clock)
    gaming = True
    while gaming:
        gm.MainLoop()


if __name__ == "__main__":
    x = 256
    y = [0] * 16
    grid = []
    for item in range(x):
        grid.append(copy.deepcopy(y))
    main(grid)
