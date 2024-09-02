from threading import Thread
import time
import random
import pygame
import customtkinter as tk
from customtkinter import CTkFrame as Frame
from customtkinter import CTkEntry as Entry
from customtkinter import CTkButton as _Button
from customtkinter import StringVar, END
import asset_loader

# pygame setup
tk.set_appearance_mode("dark")
tk.set_default_color_theme("green")
pygame.init()
width, height = 1024, 720
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
pygame.display.set_caption('FroggieWarfare')
icon = pygame.image.load("frog_icon.ico")
pygame.display.set_icon(icon)
background = pygame.image.load("./Froggie/maps/background.png").convert_alpha()
frog_up = pygame.image.load("./Froggie/frog/Frog_up.png").convert_alpha()
frog_down = pygame.image.load("./Froggie/frog/Frog_down.png").convert_alpha()
frog_right = pygame.image.load("./Froggie/frog/Frog_right.png").convert_alpha()
frog_left = pygame.image.load("./Froggie/frog/Frog_Left.png").convert_alpha()
frog_tongue_up = pygame.image.load("./Froggie/frog/Frog_tongue_up.png").convert_alpha()
frog_tongue_right = pygame.image.load("./Froggie/frog/Frog_tongue_right.png").convert_alpha()
frog_tongue_left = pygame.image.load("./Froggie/frog/Frog_tongue_left.png").convert_alpha()
frog_tongue_down = pygame.image.load("./Froggie/frog/Frog_tongue_down.png").convert_alpha()
in_game_background = pygame.image.load("./Froggie/maps/map2.png").convert_alpha()
bullet_up = pygame.image.load("./Froggie/weapons/slime.png").convert_alpha()
bullet_down = pygame.image.load("./Froggie/weapons/bullet_down.png").convert_alpha()
bullet_left = pygame.image.load("./Froggie/weapons/bullet_left.png").convert_alpha()
bullet_right = pygame.image.load("./Froggie/weapons/bullet_right.png").convert_alpha()
bullet2_up = pygame.image.load("./Froggie/weapons/bullet3_up.png").convert_alpha()
bullet2_down = pygame.image.load("./Froggie/weapons/bullet3_down.png").convert_alpha()
bullet2_left = pygame.image.load("./Froggie/weapons/bullet3_left.png").convert_alpha()
bullet2_right = pygame.image.load("./Froggie/weapons/bullet3_right.png").convert_alpha()
bullet3_up = pygame.image.load("./Froggie/weapons/bullet4_up.png").convert_alpha()
bullet3_down = pygame.image.load("./Froggie/weapons/bullet4_down.png").convert_alpha()
bullet3_right = pygame.image.load("./Froggie/weapons/bullet4_right.png").convert_alpha()
bullet3_left = pygame.image.load("./Froggie/weapons/bullet4_left.png").convert_alpha()
snake = pygame.image.load("./Froggie/enemies/snake.png").convert_alpha()
snake_shot = pygame.image.load("./Froggie/enemies/snake_shot.png").convert_alpha()
menu = pygame.image.load("./Froggie/frog/menu.png").convert_alpha()
start_button = pygame.image.load("./Froggie/start_button.png").convert_alpha()
croc = pygame.image.load("./Froggie/enemies/croc.png").convert_alpha()
frog_icon = pygame.image.load("./Froggie/frog/frog_icon.png").convert_alpha()
weapon_selectBG = pygame.image.load("./Froggie/maps/weapon_select.png").convert_alpha()
map2 = pygame.image.load("./Froggie/maps/map3.png")
maps = [in_game_background, map2]
# sounds
menu_sound = pygame.mixer.Sound("./Froggie/sfx/menu_audio.wav")
switch_sound = pygame.mixer.Sound("./Froggie/sfx/switch.wav")
shoot_sound = pygame.mixer.Sound("./Froggie/sfx/shoot.wav")
hit_sound = pygame.mixer.Sound("./Froggie/sfx/hit.mp3")
killed_sound = pygame.mixer.Sound("./Froggie/sfx/killed.wav")
reloading_sound = pygame.mixer.Sound("./Froggie/sfx/reloading.wav")

start_game = False
running = True
dt = 0
center = pygame.Vector2((screen.get_width() / 2) - 20, screen.get_height() / 2)

frog_view = frog_up

weapons = {}

spawned = False
worm_positions = [[200, 300], [400, 350], [600, 700]]
worms = []
spawned_enemies = 0
score = 0
multiplier = 1
text_color = "#FEDD00FF"

font = pygame.font.Font('freesansbold.ttf', 15)


# Ammo
def show_ammo(ammo_type):
    global remaining_ammo
    _font = pygame.font.Font('freesansbold.ttf', 10)
    _text = _font.render(f"{remaining_ammo}", True, text_color)
    screen.blit(ammo_type, (750, 10))
    screen.blit(_text, (770, 15))


# Score
def show_score():
    text = font.render(f'Score: {score}', True, text_color)
    screen.blit(text, (920, 10))


class HealthBar:
    def __init__(self, x, y, _w, h, max_hp):
        self.x = x
        self.y = y
        self._w = _w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, _surface, color="green"):
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(_surface, "red", (self.x, self.y, self._w, self.h))
        pygame.draw.rect(_surface, color, (self.x, self.y, self._w * ratio, self.h))


class Weapon:
    def __init__(self, damage, _bullet_up, _bullet_down, _bullet_right, _bullet_left, max_ammo, _reload_time, name):
        self.damage = damage
        self.bullet_up_ = _bullet_up
        self.bullet_down_ = _bullet_down
        self.bullet_right_ = _bullet_right
        self.bullet_left_ = _bullet_left
        self.max_ammo = max_ammo
        self.reload_time_ = _reload_time
        self.name = name


weapon1 = Weapon(15, bullet_up, bullet_down, bullet_right, bullet_left, 30, 3, "GreenFireBall")

# weapons.append(weapon1)
# weapons.append(weapon2)
selected_weapon = weapon1
ammo_round = selected_weapon.max_ammo
remaining_ammo = ammo_round


class Button:
    def __init__(self, x, y, image, text=""):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.text = text

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        _font = pygame.font.Font('freesansbold.ttf', 10)
        _text = font.render(self.text, True, text_color)
        screen.blit(_text, (self.rect.x, self.rect.y + 120))
        return action


class Player:
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    health = 100
    health_bar = HealthBar(850, 10, 60, 10, health)
    _font = pygame.font.Font('freesansbold.ttf', 10)
    score = 0

    def keep_on_screen(self):
        if self.player_pos.x > 1040:
            self.player_pos.x = 1040

        elif self.player_pos.x < 0:
            self.player_pos.x = 0

        elif self.player_pos.y > 670:
            self.player_pos.y = 670

        elif self.player_pos.y < 0:
            self.player_pos.y = 0

    def update_hp(self):
        self.health_bar.hp = self.health
        self.health_bar.draw(screen, color="blue")
        text = self._font.render(f'{self.health}', True, text_color)
        screen.blit(text, (850, 10))
        screen.blit(frog_icon, (820, 10))

    def move_up(self):
        self.player_pos.y -= 300 * dt

    def move_down(self):
        self.player_pos.y += 300 * dt

    def move_right(self):
        self.player_pos.x += 300 * dt

    def move_left(self):
        self.player_pos.x -= 300 * dt

    def shoot_up(self):
        new_bullet = Bullet(selected_weapon.damage, selected_weapon.bullet_up_, "up", self.player_pos.x + 23,
                            self.player_pos.y - 20)
        # new_bullet.x_pos = self.player_pos.x + 23
        # new_bullet.y_pos = self.player_pos.y - 20
        # new_bullet.direction = "up"
        new_bullet.show()
        bullets.append(new_bullet)

    def shoot_down(self):
        new_bullet = Bullet(selected_weapon.damage, selected_weapon.bullet_down_, "down", self.player_pos.x + 23,
                            self.player_pos.y + 20)
        # new_bullet.x_pos = self.player_pos.x + 23
        # new_bullet.y_pos = self.player_pos.y + 20
        # new_bullet.direction = "down"
        new_bullet.show()
        bullets.append(new_bullet)

    def shoot_right(self):
        new_bullet = Bullet(selected_weapon.damage, selected_weapon.bullet_right_, "right", self.player_pos.x + 22,
                            self.player_pos.y + 24)
        # new_bullet.x_pos = self.player_pos.x + 22
        # new_bullet.y_pos = self.player_pos.y + 24
        # new_bullet.direction = "right"
        new_bullet.show()
        bullets.append(new_bullet)

    def shoot_left(self):
        new_bullet = Bullet(selected_weapon.damage, selected_weapon.bullet_left_, "left", self.player_pos.x + 22,
                            self.player_pos.y + 24)
        # new_bullet.x_pos = self.player_pos.x + 22
        # new_bullet.y_pos = self.player_pos.y + 24
        # new_bullet.direction = "left"
        new_bullet.show()
        bullets.append(new_bullet)

    @staticmethod
    def die():
        global center, start_game
        _font = pygame.font.Font('freesansbold.ttf', 20)
        _text = font.render(f'GAME OVER!', True, text_color)
        screen.blit(_text, center)
        pygame.display.flip()
        time.sleep(1)
        start_game = False


reloading = False
gun_type = 1
blink = True
reload_time = selected_weapon.reload_time_


def reload():
    global blink, reloading, remaining_ammo, reload_time, ammo_round
    ammo_increment = int(selected_weapon.max_ammo / (reload_time / 0.1))
    while selected_weapon.reload_time_ > 0:
        if blink:
            text = font.render("Reloading", True, text_color)
            screen.blit(text, center)
            blink = False
        else:
            blink = True
        remaining_ammo += ammo_increment
        selected_weapon.reload_time_ = round(selected_weapon.reload_time_ - 0.1, 1)
        pygame.mixer.Sound.play(reloading_sound)
        time.sleep(0.1)
    selected_weapon.reload_time_ = reload_time
    pygame.mixer.music.stop()
    reloading = False


player = Player()


# =================== Enemies ====================
class Snake:
    alive = True
    x_pos = None
    y_pos = None
    health_bar = None
    image = snake
    attack_speed = 1
    health = 100
    damage_caused = 1

    def spawn(self, x, y):
        screen.blit(self.image, (x, y))
        self.health_bar.draw(screen)

    def die(self):
        screen.blit(snake_shot, (self.x_pos, self.y_pos))
        pygame.mixer.Sound.play(killed_sound)
        pygame.mixer.music.stop()
        worms.remove(self)

    def hunt(self, hunter, prey):
        # stepx, stepy = 0, 0
        hunterx, huntery = hunter[0], hunter[1]
        preyx, prey_y = prey[0], prey[1]
        x_diff = hunterx - preyx
        y_diff = huntery - prey_y
        if x_diff < 0:
            self.x_pos += self.attack_speed
            self.health_bar.x += self.attack_speed
        else:
            self.x_pos -= self.attack_speed
            self.health_bar.x -= self.attack_speed
        if y_diff < 0:
            self.y_pos += self.attack_speed
            self.health_bar.y += self.attack_speed
        else:
            self.y_pos -= self.attack_speed
            self.health_bar.y -= self.attack_speed
        self.spawn(self.x_pos, self.y_pos)

    def catch(self):
        lower_bound_X = player.player_pos.x - 72
        upper_bound_X = player.player_pos.x + 72
        lower_bound_Y = player.player_pos.y - 72
        upper_bound_Y = player.player_pos.y + 72

        if lower_bound_X <= self.x_pos <= upper_bound_X and lower_bound_Y <= self.y_pos <= upper_bound_Y:
            player.health -= self.damage_caused
            player.update_hp()
            if player.health <= 0:
                return True
        elif lower_bound_X <= self.x_pos <= upper_bound_X and upper_bound_Y >= self.y_pos >= lower_bound_Y:
            player.health -= self.damage_caused
            player.update_hp()
            if player.health <= 0:
                return True
        elif lower_bound_X <= self.x_pos <= upper_bound_X and lower_bound_Y <= self.y_pos <= upper_bound_Y:
            player.health -= self.damage_caused
            player.update_hp()
            if player.health <= 0:
                return True

        elif upper_bound_X >= self.x_pos >= lower_bound_X and lower_bound_Y <= self.y_pos <= upper_bound_Y:
            player.health -= self.damage_caused
            player.update_hp()
            if player.health <= 0:
                return True
        else:
            return False


class Croc(Snake):
    health = 150
    damage_caused = 2
    attack_speed = 2
    image = croc


bullets = []


# Bullets
class Bullet:
    def __init__(self, damage, image, direction, x_pos, y_pos):
        self.damage = damage
        self.image = image
        self.direction = direction
        self.x_pos = x_pos
        self.y_pos = y_pos

    def kill(self):
        bullets.remove(self)
        # print("bullet killed")

    def hit(self):
        _hit = True
        # print("hit")
        global score
        for s in worms:
            b_lower_bound_X = s.x_pos
            b_upper_bound_X = s.x_pos + 72
            b_lower_bound_Y = s.y_pos
            b_upper_bound_Y = s.y_pos + 72
            if b_lower_bound_X <= self.x_pos <= b_upper_bound_X and b_lower_bound_Y <= self.y_pos <= b_upper_bound_Y:
                pygame.mixer.Sound.play(hit_sound)
                pygame.mixer.music.stop()
                s.health -= self.damage
                s.health_bar.hp = s.health
                s.health_bar.draw(screen)
                if s.health <= 0:
                    s.alive = False
                    score += 10 * multiplier
                self.kill()
                return True
            elif b_lower_bound_X <= self.x_pos <= b_upper_bound_X and b_upper_bound_Y >= self.y_pos >= b_lower_bound_Y:
                pygame.mixer.Sound.play(hit_sound)
                pygame.mixer.music.stop()
                s.health -= self.damage
                s.health_bar.hp = s.health
                s.health_bar.draw(screen)
                if s.health <= 0:
                    s.alive = False
                    score += 10 * multiplier
                self.kill()
                return True
            elif b_lower_bound_X <= self.x_pos <= b_upper_bound_X and b_lower_bound_Y <= self.y_pos <= \
                    b_upper_bound_Y:
                pygame.mixer.Sound.play(hit_sound)
                pygame.mixer.music.stop()
                s.health -= self.damage
                s.health_bar.hp = s.health
                s.health_bar.draw(screen)
                if s.health <= 0:
                    s.alive = False
                    score += 10 * multiplier
                self.kill()
                return True
            elif b_upper_bound_X >= self.x_pos >= b_lower_bound_X and b_lower_bound_Y <= self.y_pos <= \
                    b_upper_bound_Y:
                pygame.mixer.Sound.play(hit_sound)
                pygame.mixer.music.stop()
                s.health -= self.damage
                s.health_bar.hp = s.health
                s.health_bar.draw(screen)
                if s.health <= 0:
                    s.alive = False
                    score += 10 * multiplier
                self.kill()
                return True

    def show(self):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    def travel(self):
        if self.direction == "up":
            self.y_pos -= 20
            if self.y_pos < 0:
                self.kill()
            self.show()

        elif self.direction == "down":
            self.y_pos += 20
            if self.y_pos > 720:
                self.kill()
            self.show()

        elif self.direction == "right":
            self.x_pos += 20
            if self.x_pos > 1024:
                self.kill()
            self.show()
        else:
            self.x_pos -= 20
            if self.x_pos < 0:
                self.kill()
            self.show()

        self.hit()


def reset():
    global bullets, weaponselect, ammo_round, \
        menuscreen, reload_time, score, worms, \
        player, start_game, spawn_size, spawned_enemies, remaining_ammo, map_select_, delay

    delay = 4
    bullets.clear()
    menuscreen = True
    weaponselect = False
    map_select_ = False
    start_game = False
    ammo_round = selected_weapon.max_ammo
    remaining_ammo = 0
    reload_time = selected_weapon.reload_time_
    worms.clear()
    score = 0
    spawn_size = 0
    spawned_enemies = 0
    player.health = 100
    player.player_pos = pygame.Vector2((screen.get_width() / 2) + 5, screen.get_height() / 2)


menuscreen = False
weaponselect = False
map_select_ = False


def display_background(page, pos):
    screen.blit(page, pos)


menu_song_on = False


# Display Menu Screen

def show_menu():
    global start_game, menuscreen, weaponselect, menu_song_on

    if not menu_song_on:
        pygame.mixer.Sound.play(menu_sound)

    menu_width = menu.get_width()
    menu_height = menu.get_height()
    scaled = pygame.transform.scale(menu, (int(menu_width * 1.6), int(menu_height * 1.3)))
    screen.blit(scaled, (0, 0))
    _start_button = Button(400, 300, start_button)
    if _start_button.draw():
        menu_sound.stop()
        pygame.mixer.Sound.play(switch_sound)
        menuscreen = False
        weaponselect = True


login = True
login_called = False
address = ""
password = ""
weapon_values = []

"""User logs in by providing address registered with the game smart-contract as well as the password whose hash they 
registered with"""


def sign_in_window(_events):
    global login_called, login, menuscreen, weapons, address, password, weapon_values

    def clear_text(widget):
        widget.delete(0, END)
        widget.configure(text_color="white")

    def set_creds(_address, _password):
        global login, menuscreen, weapons, address, weapon_values
        _auth = asset_loader.auth(_address, _password)
        if _auth:
            login = False
            menuscreen = True
            address = _address
            page.destroy()
            for i in asset_loader.load_weapons(_address):
                if i == '0x86602Acf172312a56F773215E38CfE6886488565':
                    weapons[i] = weapon1
                elif i == '0x8Cf403eF46ABfee1c6755A6A5C54fed88277058C':
                    weapons[i] = Weapon(30, bullet2_up, bullet2_down, bullet2_right, bullet2_left, 35, 3,
                                        "GreenFireBall")
                elif i == '0xE7b6168784B0f2A708222641e23c27CBf7b583b0':
                    weapons[i] = Weapon(30, bullet3_up, bullet3_down, bullet3_right, bullet3_left, 35, 2,
                                        "GreenFireBall")
            weapon_values = list(weapons.values())
            assert len(weapon_values) > 0

    login_called = True
    page = tk.CTk()
    address_text = StringVar()
    address_text.set("Address")
    password_text = StringVar()
    password_text.set("Password")
    page.geometry("200x200")
    page.title("FroggieWarfare")
    frame = Frame(page)
    address_input = Entry(frame, textvariable=address_text, text_color="grey")
    password_input = Entry(frame, textvariable=password_text, text_color="grey")
    address_input.bind("<FocusIn>", lambda address_widget: clear_text(address_input))
    password_input.bind("<FocusIn>", lambda password_widget: clear_text(password_input))
    submit = _Button(frame, text="submit", command=lambda: set_creds(address_input.get(), password_input.get()))
    frame.pack(expand=True)
    address_input.pack()
    password_input.pack()
    submit.pack()
    page.mainloop()


weapon_index = 0

"""Weapon Selection Page: Users can select weapons which they have on the address they signed in with.
New weapons can be purchased via the game smart contract as soul bound NFTs"""


def weapon_selection():
    global start_game, remaining_ammo, selected_weapon, ammo_round, weaponselect, map_select_, weapon_index,\
        weapon_values
    screen.blit(weapon_selectBG, (0, 0))
    x = 400
    y = 250
    if weapon_index > len(weapon_values) - 1:
        weapon_index = len(weapon_values) - 1
    if weapon_index < 0:
        weapon_index = 0
    width_ = weapon_values[weapon_index].bullet_up_.get_width()
    height_ = weapon_values[weapon_index].bullet_up_.get_height()
    scaled_image = pygame.transform.scale(weapon_values[weapon_index].bullet_up_, (int(width_ * 6), int(height_ * 6)))
    weapon_button = Button(x, y, scaled_image)
    ws_font = pygame.font.Font('freesansbold.ttf', 20)
    w_name = ws_font.render(f"Name: {weapon_values[weapon_index].name.upper()}", True, text_color)
    total_weapons = ws_font.render(f"Weapons You Own: {len(weapon_values)}", True, text_color)
    screen.blit(total_weapons, (0, 0))
    w_damage_bar = HealthBar(300, 540, 50, 5, 100)
    w_damage_bar.hp = weapon_values[weapon_index].damage
    w_damage_bar.draw(screen)
    w_damage = ws_font.render(f"Damage: ", True, text_color)
    w_reload = ws_font.render(f"Reload Delay: {weapon_values[weapon_index].reload_time_}s", True, text_color)
    screen.blit(w_name, (200, 500))
    screen.blit(w_damage, (200, 530))
    screen.blit(w_reload, (200, 560))
    _keys = pygame.key.get_pressed()

    if _keys[pygame.K_RIGHT]:
        weapon_index += 1
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(switch_sound)
    if _keys[pygame.K_LEFT]:
        weapon_index -= 1
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(switch_sound)

    if weapon_button.draw():
        selected_weapon = weapon_values[weapon_index]
        ammo_round = selected_weapon.max_ammo
        remaining_ammo = selected_weapon.max_ammo
        weaponselect = False
        map_select_ = True
        pygame.mixer.Sound.play(switch_sound)


spawn_size = 1
delay = 4


map_index = 0


def map_select():
    global map_index, start_game, selected_map, map_select_
    screen.blit(background, (0, 0))
    if map_index > len(maps) - 1:
        map_index = 0
    if map_index < 0:
        map_index = 0

    width_ = maps[map_index].get_width()
    height_ = maps[map_index].get_height()
    scaled_image = pygame.transform.scale(maps[map_index], (int(width_ / 4), int(height_ / 6)))
    map_button = Button(350, 200, scaled_image)
    _keys = pygame.key.get_pressed()

    _font = pygame.font.Font('freesansbold.ttf', 20)
    _text = _font.render("Select Map <   >", True, text_color)
    screen.blit(_text, (center.x - 90, center.y + 20))
    if _keys[pygame.K_RIGHT]:
        map_index += 1
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(switch_sound)
    if _keys[pygame.K_LEFT]:
        map_index -= 1
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(switch_sound)

    if map_button.draw():
        # reset()
        selected_map = maps[map_index]
        map_select_ = False
        start_game = True
        pygame.mixer.Sound.play(switch_sound)


# spawn new enemies. Ensures there's at least 5 sec difference between worm spawns
def spawner():
    global worms, spawn_size, start_game, spawned_enemies, delay
    _croc = False
    _snake = True
    _spawn_size = 2

    def set_pos():
        # Ensure enemies can't spawn at player position

        _spawn_pos_x = 0
        _spawn_pos_y = 0
        current_player_pos = player.player_pos

        _spawn_pos_x = random.randint(0, 1024)
        _spawn_pos_y = random.randint(0, 720)
        if (_spawn_pos_x, _spawn_pos_y) == current_player_pos:
            set_pos()
        return _spawn_pos_x, _spawn_pos_y

    # keep spawning enemies at fixed interval (survival mode)
    enemies = ["snake", "croc"]
    _font = pygame.font.Font('freesansbold.ttf', 50)

    while True:
        if not start_game:
            pass
        else:
            if delay > 0:
                text = _font.render(str(delay), True, text_color)
                screen.blit(text, (center.x, center.y - 10))
                time.sleep(1)
                delay -= 1
            else:
                if spawn_size > 10:
                    _croc = True
                for i in range(_spawn_size):
                    if _croc:
                        choice = random.choice(enemies)
                        if choice == "snake":
                            spawn_pos_x, spawn_pos_y = set_pos()
                            new_worm = Snake()
                            new_worm.health_bar = HealthBar(spawn_pos_x + 10, spawn_pos_y - 10, 50, 3, new_worm.health)
                            new_worm.spawn(spawn_pos_x, spawn_pos_y)
                            new_worm.x_pos = spawn_pos_x
                            new_worm.y_pos = spawn_pos_y
                            worms.append(new_worm)
                            spawn_size += 1
                        else:
                            spawn_pos_x, spawn_pos_y = set_pos()
                            new_worm = Croc()
                            new_worm.health_bar = HealthBar(spawn_pos_x + 10, spawn_pos_y - 10, 50, 3, new_worm.health)
                            new_worm.spawn(spawn_pos_x, spawn_pos_y)
                            new_worm.x_pos = spawn_pos_x
                            new_worm.y_pos = spawn_pos_y
                            worms.append(new_worm)
                            spawn_size += 1
                    else:
                        spawn_pos_x, spawn_pos_y = set_pos()
                        new_worm = Snake()
                        new_worm.health_bar = HealthBar(spawn_pos_x + 10, spawn_pos_y - 10, 50, 3, new_worm.health)
                        new_worm.spawn(spawn_pos_x, spawn_pos_y)
                        new_worm.x_pos = spawn_pos_x
                        new_worm.y_pos = spawn_pos_y
                        worms.append(new_worm)
                        spawn_size += 1
                time.sleep(5)


timer = Thread(target=spawner, daemon=True)
timer.start()
selected_map = random.choice(maps)

# Main Game Loop
while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if not start_game:
        if login:
            if login_called:
                pass
            else:
                sign_in_window(events)
        if menuscreen:
            show_menu()
        elif weaponselect:
            weapon_selection()
        elif map_select_:
            map_select()

    else:
        screen.blit(selected_map, (0, 0))
        show_score()
        player.keep_on_screen()
        image_to_blit = frog_view

        if frog_view == frog_tongue_down:
            image_to_blit = frog_down
        elif frog_view == frog_tongue_up:
            image_to_blit = frog_up
        elif frog_view == frog_tongue_left:
            image_to_blit = frog_left
        elif frog_view == frog_tongue_right:
            image_to_blit = frog_right
        else:
            image_to_blit = frog_view

        player.update_hp()

        # ======== Control actions =================
        keys = pygame.key.get_pressed()

        # Movements
        if keys[pygame.K_w]:
            player.move_up()
            image_to_blit = frog_up

        if keys[pygame.K_s]:
            player.move_down()
            image_to_blit = frog_down

        if keys[pygame.K_a]:
            player.move_left()
            image_to_blit = frog_left

        if keys[pygame.K_d]:
            player.move_right()
            image_to_blit = frog_right

        # Shooting
        if keys[pygame.K_SPACE] and frog_view == frog_up:
            image_to_blit = frog_tongue_up
            if reloading:
                pass
            else:
                player.shoot_up()
                remaining_ammo -= 1
                pygame.mixer.Sound.play(shoot_sound)
                pygame.mixer.music.stop()

        if keys[pygame.K_SPACE] and frog_view == frog_down:
            image_to_blit = frog_tongue_down
            if reloading:
                pass
            else:
                player.shoot_down()
                remaining_ammo -= 1
                pygame.mixer.Sound.play(shoot_sound)
                pygame.mixer.music.stop()

        if keys[pygame.K_SPACE] and frog_view == frog_right:
            image_to_blit = frog_tongue_right
            if reloading:
                pass
            else:
                player.shoot_right()
                remaining_ammo -= 1
                pygame.mixer.Sound.play(shoot_sound)
                pygame.mixer.music.stop()

        if keys[pygame.K_SPACE] and frog_view == frog_left:
            image_to_blit = frog_tongue_left
            if reloading:
                pass
            else:
                player.shoot_left()
                remaining_ammo -= 1
                pygame.mixer.Sound.play(shoot_sound)
                pygame.mixer.music.stop()

        show_ammo(selected_weapon.bullet_up_)

        for bullet in bullets:
            bullet.travel()

        for w in worms:
            if not w.alive:
                w.die()
            else:
                w.hunt([w.x_pos, w.y_pos], player.player_pos)
                if w.catch():
                    player.die()
                    reset()
        # keep worms that are alive on screen
        for w in worms:
            w.spawn(w.x_pos, w.y_pos)
        screen.blit(image_to_blit, player.player_pos)
        frog_view = image_to_blit

        if remaining_ammo == 0:
            reloading = True
            reload_thread = Thread(target=reload, daemon=True)
            reload_thread.start()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(30) / 1000
    pygame.display.flip()
pygame.quit()
