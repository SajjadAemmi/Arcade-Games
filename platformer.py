import arcade
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Move with Walls Example"

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5
JUMP_SPEED = 14
GRAVITY = 0.5


class Wall(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/grass.png")
        self.speed = 4
        self.width = 48
        self.height = 48
        self.center_x = x
        self.center_y = y

    def move(self):
        self.center_y -= self.speed


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

        self.idle_texture_pair = arcade.load_texture(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)


        self.speed = 4
        self.width = 48
        self.height = 48
        self.center_x = 50
        self.center_y = 64
        self.cur_texture = 0

    
    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME

        self.texture = self.walk_textures[frame]


    def move(self):
        self.center_y -= self.speed


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Sprite lists
        self.coin_list = None
        self.moving_wall_list = None
        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

        self.player = Player()
        self.moving_wall_list = arcade.SpriteList()

        for x in range(0, 650, 48):
            self.moving_wall_list.append(Wall(x, 0))

        for y in range(273, 500, 64):
            self.moving_wall_list.append(Wall(465, y))

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.moving_wall_list, gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()

        # Draw all the sprites.
        self.moving_wall_list.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):

        self.player.update_animation()
        self.physics_engine.update()


if __name__ == "__main__":
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
