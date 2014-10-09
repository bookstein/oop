import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []



    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y -1)
        elif direction == "down":
            return (self.x, self.y +1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            self.move_character("up")
        elif symbol ==  key.DOWN:
            self.move_character("down")
        elif symbol == key.LEFT:
            self.move_character("left")
        elif symbol == key.RIGHT:
            self.move_character("right")

        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))
        
        # if direction:
        #     next_location = self.next_pos(direction)
        
        #     if next_location:
        #         next_x = next_location[0]
        #         next_y = next_location[1]
        #         self.board.del_el(self.x, self.y)
        #         self.board.set_el(next_x, next_y, self)


    def move_character(self, direction):
        if direction:
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                existing_el = self.board.get_el(next_x, next_y)
                if existing_el:
                    existing_el.interact(self)
                    
                if existing_el and existing_el.SOLID:
                    self.board.draw_msg("There's something in my way!")

                elif existing_el is None or not existing_el.SOLID:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)


class NewCat(GameElement):
    IMAGE = 'Cat'
    SOLID = True

    def __init__(self):
        self.inventory = []

    def interact(self, player):
        if len(player.inventory) > 0:
            gem = player.inventory.pop()
            self.inventory.append(gem)

            GAME_BOARD.draw_msg("The CAT just acquired a gem! The cat have %d items! CATITUDE"%(len(self.inventory)))
        else:
            GAME_BOARD.draw_msg("Ouch! The cat sratched you. Go away!")


class NewFriend (Character):
    IMAGE = 'Girl'

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.E:
            self.move_character("up")
        elif symbol ==  key.C:
            self.move_character("down")
        elif symbol == key.S:
            self.move_character("left")
        elif symbol == key.F:
            self.move_character("right")

        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))



class ShinyThings(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))


class OrangeGem(ShinyThings):
    IMAGE = "OrangeGem"
    SOLID = True

    def interact(self, player):
        player.board.del_el(player.x, player.y)
        player.board.set_el(0, 0, player)


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    gem = ShinyThings()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1, gem)

    orangegem = OrangeGem()
    GAME_BOARD.register(orangegem)
    GAME_BOARD.set_el(4,4, orangegem)

    newgirl = NewFriend()
    GAME_BOARD.register(newgirl)
    GAME_BOARD.set_el(3,3, newgirl)

    thecat = NewCat()
    GAME_BOARD.register(thecat)
    GAME_BOARD.set_el(7,5, thecat)

    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
    ]

    rocks = []

    for position in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(position[0], position[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    rocks[-1].SOLID = False

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2,2,player)
    print player

    GAME_BOARD.draw_msg("This game is wicked awesome.")


