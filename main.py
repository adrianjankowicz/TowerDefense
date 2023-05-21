# Importowanie wymaganych bibliotek
import pygame  # Podstawowa biblioteka do tworzenia gier w Pythonie
import sys  # Moduł sys używany do manipulacji różnymi częściami środowiska Pythona
import random  # Generowanie liczb losowych
import math  # Operacje matematyczne

# Inicjalizacja biblioteki Pygame
pygame.init()

# Inicjalizacja mixer'a
pygame.mixer.init()

# Wczytanie pliku muzycznego
pygame.mixer.music.load('assets/music/music.mp3')
lottery_sound = pygame.mixer.Sound('assets/music/opening.mp3')

# Ustawienie głośności
music_volume = 0.05
lottery_volume = 0.5
pygame.mixer.music.set_volume(music_volume) 
lottery_sound.set_volume(lottery_volume)
# Odtwarzanie muzyki
pygame.mixer.music.play(-1) # -1 oznacza pętlę nieskończoną

# Ustawienia ekranu
width, height = 800, 600  # Rozmiar ekranu gry
screen = pygame.display.set_mode((width, height))  # Utworzenie ekranu o określonym rozmiarze
font = pygame.font.Font(None, 36)  # Ustalenie czcionki dla tekstów w grze
pygame.display.set_caption("Tower defense")  # Ustawienie tytułu okna gry

# Definiowanie kolorów
WHITE = (255, 255, 255)  # Biały
RED = (255, 0, 0)  # Czerwony
GREEN = (0, 255, 0)  # Zielony
PURPLE = (187, 123, 247)  # Fioletowy
BLUE = (27, 70, 245)  # Niebieski
YELLOW = (255,255,0) # Żółty

# Definiowanie klasy Zamku
class Castle(pygame.sprite.Sprite):
    """
    \brief Klasa reprezentująca zamek w grze.
    
    Klasa zawiera informacje na temat położenia, grafiki oraz punktów zdrowia zamku.
    """
    def __init__(self, x, y, image):
        """
        \brief Konstruktor klasy Castle.
        
        \param[in] x Współrzędna x zamku.
        \param[in] y Współrzędna y zamku.
        """
        super().__init__()
        self.image = image
        self.hp = 5
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.collision_padding_bottom= 25
        self.collision_padding_top = 55
        self.collision_rect = self.rect.copy()
        self.collision_rect.height = int(self.collision_rect.height * 2 / 4)
        self.collision_rect.top += self.collision_padding_top
        self.collision_rect.bottom += self.collision_padding_bottom
        self.last_shot_time = 0

class Enemy(pygame.sprite.Sprite):
    """
    \brief Klasa reprezentująca wroga w grze.
    
    Klasa zawiera informacje na temat położenia, grafiki, prędkości, zdrowia, stanu i typu wroga.
    """
    def __init__(self, enemy_type = 0, hp = 1, speed_multiplier=1.0, hp_multiplier=1.0):
        """
        \brief Konstruktor klasy Enemy.
        
        \param[in] enemy_type Typ wroga.
        \param[in] hp Początkowe zdrowie wroga.
        \param[in] speed_multiplier Mnożnik prędkości wroga.
        \param[in] hp_multiplier Mnożnik zdrowia wroga.
        """
        super().__init__()
        self.image = enemies0_walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randint(height // 2, height - self.rect.height)
        self.last_hit_time = 0
        self.speed = 1 * speed_multiplier
        self.hp = hp * hp_multiplier
        self.max_hp = hp * hp_multiplier
        self.state = 'walk'  # Możliwe stany to: 'walk', 'attack', 'death'
        self.animation_index = 0
        self.enemy_type = enemy_type
        self.last_update_time = pygame.time.get_ticks()

        if enemy_type == 3:
                self.rect.y = height / 2  + 80  # środek ekranu
        else:
                self.rect.y = random.randint(height // 2, height - self.rect.height)

    def update(self):
        """
        \brief Metoda aktualizacji stanu wroga.
        
        Metoda ta jest wywoływana w każdej klatce gry. 
        Odpowiada za aktualizację pozycji, stanu i animacji wroga.
        """
        global enemies_to_defeat, currency
        current_time = pygame.time.get_ticks()
        if self.state != 'death':
            if self.rect.colliderect(castle.collision_rect):
                if current_time - self.last_hit_time > 500:
                    castle.hp -= 1
                    self.last_hit_time = current_time
                    self.state = 'attack'
            elif self.rect.x + self.rect.width >= width:
                castle.hp -= 1
                self.kill() 
                enemies_to_defeat -= 1
            else:
                self.rect.x += self.speed
        
        if self.enemy_type == 0:
            if self.state == 'walk':
                self.image = enemies0_walk_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies0_walk_images):
                    self.animation_index = 0
            elif self.state == 'attack':
                self.image = enemies0_attack_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies0_attack_images):
                    self.animation_index = 0
            elif self.state == 'death':
                if self.animation_index < len(enemies0_death_images):
                    self.image = enemies0_death_images[self.animation_index]
                    self.animation_index += 1
                else:
                    self.kill()
                    currency += 2
                    enemies_to_defeat -= 1

        if self.enemy_type == 1:
            if self.state == 'walk':
                self.image = enemies1_walk_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies1_walk_images):
                    self.animation_index = 0
            elif self.state == 'attack':
                self.image = enemies1_attack_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies1_attack_images):
                    self.animation_index = 0
            elif self.state == 'death':
                if self.animation_index < len(enemies1_death_images):
                    self.image = enemies1_death_images[self.animation_index]
                    self.animation_index += 1
                else:
                    self.kill()
                    currency += 3
                    enemies_to_defeat -= 1

        if self.enemy_type == 2:
            if self.state == 'walk':
                self.image = enemies2_walk_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies2_walk_images):
                    self.animation_index = 0
            elif self.state == 'attack':
                self.image = enemies2_attack_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies2_attack_images):
                    self.animation_index = 0
            elif self.state == 'death':
                if self.animation_index < len(enemies2_death_images):
                    self.image = enemies2_death_images[self.animation_index]
                    self.animation_index += 1
                else:
                    self.kill()
                    currency += 4
                    enemies_to_defeat -= 1

        if self.enemy_type == 3:
            if self.state == 'walk':
                self.image = enemies3_walk_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies3_walk_images):
                    self.animation_index = 0
            elif self.state == 'attack':
                self.image = enemies3_attack_images[self.animation_index]
                self.animation_index += 1
                if self.animation_index >= len(enemies3_attack_images):
                    self.animation_index = 0
            elif self.state == 'death':
                if self.animation_index < len(enemies3_death_images):
                    self.image = enemies3_death_images[self.animation_index]
                    self.animation_index += 1
                else:
                    self.kill()
                    currency += 30
                    enemies_to_defeat -= 1
        
    def take_damage(self, damage):
        """
        \brief Metoda odpowiedzialna za zadawanie obrażeń wrogowi.
        
        \param[in] damage Ilość obrażeń do zadania.
        """
        self.hp -= damage
        if self.hp <= 0:
            self.state = 'death'


# Definiowanie klasy Pocisku
class Bullet(pygame.sprite.Sprite):
    """
    \brief Klasa reprezentująca pocisk w grze.
    
    Klasa zawiera informacje na temat położenia, grafiki, prędkości i obrażeń pocisku.
    """
    damage = 1  # Obrażenia zadawane przez pocisk
    speed = 12  # Prędkość pocisku

    def __init__(self, pos, target_pos):
        """
        \brief Konstruktor klasy Bullet.
        
        \param[in] pos Aktualna pozycja pocisku.
        \param[in] target_pos Pozycja celu pocisku.
        """
        super().__init__()  
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed
    
    def update(self):
        """
        \brief Metoda aktualizacji stanu pocisku.
        
        Metoda ta jest wywoływana w każdej klatce gry. 
        Odpowiada za aktualizację pozycji pocisku.
        """
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x > width:
            self.kill()

# Definiowanie klasy Przycisku
class Button:
    """
    \brief Klasa reprezentująca przycisk w interfejsie użytkownika gry.
    
    Klasa zawiera informacje na temat położenia, wymiarów, tekstu, koloru tła i tekstu przycisku.
    """
    def __init__(self, x, y, width, height, text, color, text_color):
        """
        \brief Konstruktor klasy Button.
        
        \param[in] x Współrzędna x przycisku.
        \param[in] y Współrzędna y przycisku.
        \param[in] width Szerokość przycisku.
        \param[in] height Wysokość przycisku.
        \param[in] text Tekst na przycisku.
        \param[in] color Kolor tła przycisku.
        \param[in] text_color Kolor tekstu przycisku.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
    
    def draw(self, screen, font):
        """
        \brief Metoda rysująca przycisk na ekranie.
        
        \param[in] screen Ekran na którym przycisk ma być narysowany.
        \param[in] font Czcionka tekstu przycisku.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        """
        \brief Metoda sprawdzająca czy przycisk został kliknięty.
        
        \param[in] pos Pozycja kliknięcia.
        \return Zwraca wartość True, jeśli przycisk został kliknięty, w przeciwnym razie False.
        """
        return self.rect.collidepoint(pos)
    
class Tower(pygame.sprite.Sprite):
    """
    \brief Klasa reprezentująca wieżę w grze.
    
    Klasa zawiera informacje na temat położenia, grafiki, zasięgu, opóźnienia ataku i czasu ostatniego ataku wieży.
    """
    attack_delay = 2000

    def __init__(self, x, y):
        """
        \brief Konstruktor klasy Tower.
        
        \param[in] x Współrzędna x wieży.
        \param[in] y Współrzędna y wieży.
        """
        super().__init__()
        self.image = load_and_scale_image('assets/img/other/tower.png', 40, 60)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.distance = 200
        self.range = 500
        self.last_attack_time = 0

# Definiowanie klasy Błyskawicy
class Lightning(pygame.sprite.Sprite):
    """
    \brief Klasa reprezentująca błyskawicę w grze.
    
    Klasa zawiera informacje na temat klatek animacji błyskawicy i aktualnej klatki.
    """
    def __init__(self):
        super().__init__()
        self.frames = lightning_frames
        self.current_frame = 0
        
    def update(self):
        """
        \brief Metoda aktualizacji stanu błyskawicy.
        
        Metoda ta jest wywoływana w każdej klatce gry. 
        Odpowiada za aktualizację klatki błyskawicy.
        """
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            return False
        return True

    def draw(self, screen):
        """
        \brief Metoda rysująca błyskawicę na ekranie.
        
        \param[in] screen Ekran na którym błyskawica ma być narysowana.
        """
        screen.blit(self.frames[self.current_frame], (0, 0))

# Definiowanie klasy Upgrade
class Upgrade:
    """
    \brief Klasa reprezentująca ulepszenie w grze.
    
    Klasa zawiera informacje na temat nazwy, kosztu i klucza ulepszenia.
    """
    def __init__(self, name, cost, key):
        """
        \brief Konstruktor klasy Upgrade.
        
        \param[in] name Nazwa ulepszenia.
        \param[in] cost Koszt ulepszenia.
        \param[in] key Klucz ulepszenia.
        """
        self.name = name
        self.cost = cost
        self.key = key

def draw_enemies_to_defeat():
    """
    \brief Rysuje ilość wrogów, którzy pozostali do pokonania.
    
    Wyświetla tekst informujący o pozostałej ilości wrogów na ekranie.
    """
    enemies_text = f'Pozostało {enemies_to_defeat} wrogów'
    render_text(enemies_text, (19, 113, 45), (width - 220, 10), font_size=30)


def draw_hp_bar(surface, enemy, color=(255, 0, 0)):
    """
    \brief Rysuje pasek zdrowia przeciwnika.
    
    \param[in] surface Powierzchnia na której pasek zdrowia ma być narysowany.
    \param[in] enemy Przeciwnik, którego pasek zdrowia ma być narysowany.
    \param[in] color Kolor paska zdrowia.
    """
    hp_percentage = enemy.hp / enemy.max_hp
    bar_width = 30
    bar_height = 5
    bar_x = enemy.rect.x + (enemy.rect.width - bar_width) // 2
    bar_y = enemy.rect.y - bar_height - 5
    pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)
    pygame.draw.rect(surface, color, (bar_x, bar_y, int(hp_percentage * bar_width), bar_height))

def load_and_scale_image(filename, new_width, new_height):
    """
    \brief Ładuje i skaluje obraz.
    
    \param[in] filename Nazwa pliku z obrazem.
    \param[in] new_width Nowa szerokość obrazu.
    \param[in] new_height Nowa wysokość obrazu.
    \return Skalowany obraz.
    """
    image = pygame.image.load(filename).convert_alpha()
    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    return scaled_image

def render_text(text, color, pos, font_size = 36, centered=False):
    """
    \brief Renderuje tekst do wyświetlenia na ekranie.
    
    \param[in] text Tekst do wyrenderowania.
    \param[in] color Kolor tekstu.
    \param[in] pos Pozycja tekstu na ekranie.
    \param[in] font_size Rozmiar czcionki.
    \param[in] centered Czy tekst powinien być wyśrodkowany.
    """
    custom_font = pygame.font.Font(None, font_size)
    text_surface = custom_font.render(text, True, color)
    if centered:
        pos_x = pos[0] - text_surface.get_width() // 2
        pos_y = pos[1]
        screen.blit(text_surface, (pos_x, pos_y))
    else:
        screen.blit(text_surface, pos)

def render_gradient_text(text, color1, color2, pos, font_size = 36, centered=False):
    """
    \brief Renderuje tekst do wyświetlenia na ekranie z efektem gradientu.
    
    \param[in] text Tekst do wyrenderowania.
    \param[in] color1 Kolor tekstu na początku gradientu.
    \param[in] color2 Kolor tekstu na końcu gradientu.
    \param[in] pos Pozycja tekstu na ekranie.
    \param[in] font_size Rozmiar czcionki.
    \param[in] centered Czy tekst powinien być wyśrodkowany.
    """
    custom_font = pygame.font.Font(None, font_size)
    text_surface = custom_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()

    gradient_surface = pygame.Surface((text_rect.width, text_rect.height))
    for y in range(text_rect.height):
        alpha = y / text_rect.height
        color = (
            int(color1[0] * (1-alpha) + color2[0] * alpha),
            int(color1[1] * (1-alpha) + color2[1] * alpha),
            int(color1[2] * (1-alpha) + color2[2] * alpha)
        )
        pygame.draw.line(gradient_surface, color, (0, y), (text_rect.width, y))

    text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_MULT)

    if centered:
        pos_x = pos[0] - text_surface.get_width() // 2
        pos_y = pos[1]
        screen.blit(text_surface, (pos_x, pos_y))
    else:
        screen.blit(text_surface, pos)
        
def draw_upgrade_rects():
    """
    \brief Rysuje prostokąty reprezentujące dostępne ulepszenia.

    Prostokąty są rysowane w linii poziomej na górze ekranu, a ich liczba odpowiada liczbie dostępnych ulepszeń.
    """
    x = width // 2 - (len(upgrades) * 50 + (len(upgrades) - 1) * 10) // 2
    for upgrade in upgrades:
        pygame.draw.rect(screen, WHITE, (x, 10, 50, 50), 2)
        x += 60

def draw_upgrade_numbers():
    """
    \brief Rysuje numery ulepszeń.
    
    Numery są rysowane na ekranie, bezpośrednio pod odpowiadającymi im prostokątami ulepszeń.
    """
    x = width // 2 - (len(upgrades) * 50 + (len(upgrades) - 1) * 10) // 2 + 25
    for i, _ in enumerate(upgrades):
        render_text(str(i + 1), WHITE, (x, 65))
        x += 60

def save_high_score():
    """
    \brief Zapisuje najwyższy wynik (jeśli obecny poziom jest wyższy).
    
    Jeżeli obecny poziom jest wyższy niż zapisany najwyższy wynik, to obecny poziom zostaje zapisany jako nowy najwyższy wynik.
    """
    if current_level > high_score:
        with open('high_score.txt', "w") as file:
            file.write(str(current_level))

def load_high_score():
    """
    \brief Wczytuje najwyższy wynik z pliku.
    
    \return Najwyższy wynik zapisany w pliku. Jeśli plik nie istnieje, zwraca 0.
    """
    try:
        with open("high_score.txt", "r") as f:
            high_score = int(f.read())
            return high_score
    except FileNotFoundError:
        high_score = 0
        return high_score
    
def buy_hp():
    """
    \brief Kupuje dodatkowe punkty zdrowia dla zamku.
    
    \return True, jeżeli udało się kupić ulepszenie. False, jeżeli nie było wystarczająco waluty.
    """
    global currency
    if currency >= upgrades[0].cost:
            currency -= upgrades[0].cost
            castle.hp += 5
            return True
    else:return False

def buy_turret():
    """
    \brief Kupuje i umieszcza nową wieżyczkę.
    
    Nowa wieżyczka jest umieszczana na miejscu kursora myszy, pod warunkiem, że jest ona w odpowiednim obszarze i jest wystarczająco blisko zamku.
    
    \return True, jeżeli udało się kupić i umieścić wieżyczkę. False, jeżeli nie było wystarczająco waluty oraz None, jeśli wieżyczka nie mogła być umieszczona na danej pozycji.
    """
    global currency
    if currency >= upgrades[1].cost:
            mouse_pos = pygame.mouse.get_pos()
            new_tower = Tower(mouse_pos[0] - tower_icon.get_width() // 2, mouse_pos[1] - tower_icon.get_height() // 2)
            # Sprawdzenie, czy wieżyczka jest postawiona w dozwolonym obszarze
            if pygame.sprite.collide_rect(new_tower, castle):
                return None
            dx = castle.collision_rect.x - new_tower.rect.x
            dy = castle.collision_rect.y - new_tower.rect.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= new_tower.distance:
                towers.add(new_tower)
                currency -= upgrades[1].cost
                return True
    else: return False

def buy_damage():
    """
    \brief Kupuje ulepszenie do obrażeń pocisków.
    
    \return True, jeżeli udało się kupić ulepszenie. False, jeżeli nie było wystarczająco waluty.
    """
    global currency   
    if currency >= upgrades[2].cost:
        currency -= upgrades[2].cost
        Bullet.damage += 0.75
        return True
    else: return False

def buy_bullet_speed():
    """
    \brief Kupuje ulepszenie do prędkości pocisków.
    
    \return True, jeżeli udało się kupić ulepszenie. False, jeżeli nie było wystarczająco waluty.
    """
    global currency, shoot_delay
    if currency >= upgrades[3].cost:
        currency -= upgrades[3].cost
        Bullet.speed += 0.8
        shoot_delay -= 50
        Tower.attack_delay -= 200
        if Tower.attack_delay <= 500: Tower.attack_delay = 500
        if shoot_delay <= 10: shoot_delay = 10
        if Bullet.speed >= 50: Bullet.speed = 50
        return True
    else: return False

def buy_lightning():
    """
    \brief Kupuje atak błyskawicą.
    
    Atak błyskawicą zadaje obrażenia wszystkim przeciwnikom na ekranie.
    
    \return True, jeżeli udało się kupić atak. False, jeżeli nie było wystarczająco waluty.
    """
    global enemies, currency, lightnings, current_level
    if currency >= upgrades[4].cost:
            currency -= upgrades[4].cost
            for enemy in enemies:
                enemy.take_damage(current_level/2 * 1.5 + 1)
            lightnings.add(Lightning())
            return True
    else: return False

def find_nearest_enemy(tower, enemies):
    """
    \brief Znajduje najbliższego przeciwnika w zasięgu wieży.
    
    \param tower Obiekt wieży, dla której szukamy przeciwnika.
    \param enemies Lista przeciwników do przeszukania.
    
    \return Najbliższy przeciwnik w zasięgu wieży lub None, jeśli żaden przeciwnik nie jest w zasięgu.
    """
    nearest_enemy = None
    nearest_distance = 100000
    for enemy in enemies:
        dx = enemy.rect.x - tower.rect.x
        dy = enemy.rect.y - tower.rect.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < tower.range and distance < nearest_distance:
            nearest_enemy = enemy
            nearest_distance = distance
    return nearest_enemy


def main_menu():
    """
    \brief Wyświetla główne menu gry.
    
    W głównym menu użytkownik może rozpocząć nową grę lub zakończyć grę.
    """
    global is_muted
    start_button = Button(width // 2 - 100, height // 2, 200, 50, "Nowa gra", GREEN, WHITE)
    help_button = Button(width // 2 - 100, height // 2 + 80, 200, 50, "Pomoc", BLUE, WHITE)
    quit_button = Button(width // 2 - 100, height // 2 + 160, 200, 50, "Wyjście", RED, WHITE)

    pygame.mouse.set_visible(True)
    running = True
    while running:
        screen.blit(tlo, tlo_rect)

        title = "Tower defense"
        title_font = pygame.font.Font(None, 150)
        title_surface = title_font.render(title, True, PURPLE)
        title_width = title_surface.get_width()
        title_x = (width - title_width) // 2
        screen.blit(title_surface, (title_x, height // 2 - 180))

        start_button.draw(screen, font)
        quit_button.draw(screen, font)
        help_button.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    running = False
                elif quit_button.is_clicked(mouse_pos):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif help_button.is_clicked(mouse_pos):
                    help_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if not is_muted:
                        pygame.mixer.music.set_volume(0)
                        is_muted = True
                    else:
                        pygame.mixer.music.set_volume(music_volume)
                        is_muted = False
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()


def game_over():
    """
    \brief Wyświetla ekran końca gry.
    
    Na ekranie końca gry użytkownik może zacząć grę od nowa lub zakończyć grę.
    
    \return True, jeżeli użytkownik wybrał opcję restartu gry. False, jeżeli użytkownik zdecydował się zakończyć grę.
    """
    restart_button = Button(width // 2 - 250, height // 2, 200, 50, "Zacznij od nowa", GREEN, WHITE)
    quit_button = Button(width // 2 + 50, height // 2, 200, 50, "Wyjście", RED, WHITE)
    pygame.mouse.set_visible(True)
    while True:
        screen.blit(tlo, tlo_rect)
        darken_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        darken_surface.fill((0, 0, 0, 128))
        screen.blit(darken_surface, (0, 0))

        game_over_text = "Koniec gry"
        game_over_font = pygame.font.Font(None, 100)
        game_over_surface = game_over_font.render(game_over_text, True, RED)
        game_over_width = game_over_surface.get_width()
        game_over_x = (width - game_over_width) // 2
        screen.blit(game_over_surface, (game_over_x, height // 2 - 130))

        render_text(f"Poziom: {current_level}", RED, (width // 2, height // 2 - 30), centered=True)

        quit_button.draw(screen, font)
        restart_button.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.is_clicked(mouse_pos):
                    return False
                elif restart_button.is_clicked(mouse_pos):
                    return True


def start_new_level():
    """
    \brief Rozpoczyna nowy poziom gry.
    
    Zwiększa liczbę aktualnych poziomów, ustawia flagę aktywnego poziomu na True oraz resetuje niektóre zmienne związane z poziomem.
    """
    global current_level, enemies_per_level, level_active, level_start_time, enemies_to_spawn, bosses_spawned, enemies_to_defeat
    current_level += 1
    level_active = True
    level_start_time = pygame.time.get_ticks()
    enemies_to_spawn = current_level * 5 // 2 
    enemies_to_defeat = enemies_to_spawn
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, random.randint(500, 1000))  # Czas opóźnienia w milisekundach pomiędzy pojawianiem się przeciwników
    bosses_spawned = 0


def spawn_enemies():
    """
    \brief Tworzy i umieszcza nowych przeciwników na planszy.
    
    Funkcja ta jest wywoływana przez zdarzenie ENEMY_SPAWN_EVENT. Losowo tworzy różne typy przeciwników, a następnie dodaje je do grupy przeciwników.
    """
    global enemies_to_spawn, bosses_spawned
    if enemies_to_spawn > 0:
        speed_multiplier = 1 + (current_level - 1) * 0.05
        hp_multiplier = 1 + (current_level/2) * 0.1
        boss_speed_multiplier = 1
        boss_hp_multiplier = 1 + (current_level - 1) * 0.5
        if current_level % 5 == 0 and bosses_spawned < 1 and current_level == 5:
            boss = Enemy(3, 5, boss_speed_multiplier, 2)
            enemies.add(boss)
            bosses_spawned += 1
            enemies_to_spawn -= 1
        elif current_level % 5 == 0 and bosses_spawned < 1 and current_level > 5:
            boss = Enemy(3, 5, boss_speed_multiplier, boss_hp_multiplier)
            enemies.add(boss)
            bosses_spawned += 1
            enemies_to_spawn -= 1
        else:
            enemy_type = random.choice(["normal", "resistant", 'tank']) 
            if current_level <= 5:
                enemy = Enemy(0, 1, speed_multiplier, 1)
            elif current_level > 5 and current_level <= 10:
                if enemy_type == "normal":
                    enemy = Enemy(0, 1, speed_multiplier, hp_multiplier)
                elif enemy_type == "resistant":
                    enemy = Enemy(1, 2, speed_multiplier, hp_multiplier)
                elif enemy_type == "tank":
                    enemy = Enemy(0, 1, speed_multiplier, hp_multiplier)
            else:
                if enemy_type == "normal":
                    enemy = Enemy(0, 1, speed_multiplier, hp_multiplier)
                elif enemy_type == "resistant":
                    enemy = Enemy(1, 2, speed_multiplier, hp_multiplier)
                elif enemy_type == "tank":
                    enemy = Enemy(2, 3, speed_multiplier, hp_multiplier)

            enemies.add(enemy)
            enemies_to_spawn -= 1
    else:
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, 0) 

def draw_level_info(screen, level):
    """
    \brief Wyświetla informacje o aktualnym poziomie na ekranie.
    
    \param screen Obiekt ekranu, na którym informacje mają być wyświetlane.
    \param level Aktualny poziom gry.
    """
    level_text = f"Poziom {level}"
    level_font = pygame.font.Font(None, 36)
    level_color = (201, 75, 143)
    level_surface = level_font.render(level_text, True, level_color)
    level_rect = level_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 130))
    screen.blit(level_surface, level_rect)

def draw_pause_info(screen):
    """
    \brief Wyświetla informacje o pauzie na ekranie.
    
    \param screen Obiekt ekranu, na którym informacje mają być wyświetlane.
    """
    darken_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    darken_surface.fill((0, 0, 0, 128))
    screen.blit(darken_surface, (0, 0))

    pause_text = "Pauza"
    pause_font = pygame.font.Font(None, 55)
    pause_color = WHITE
    pause_surface = pause_font.render(pause_text, True, pause_color)
    pause_rect = pause_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 180))
    screen.blit(pause_surface, pause_rect)

    resume_text = "Wciśnij klawisz p, aby wznowić grę"
    resume_surface = pause_font.render(resume_text, True, pause_color)
    resume_rect = resume_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 140))
    screen.blit(resume_surface, resume_rect)

    pygame.mouse.set_visible(True)


def draw_help(screen):
    """
    \brief Wyświetla okno pomocy z opisem sterowania w grze.
    
    \param screen Obiekt ekranu pygame, na którym zostanie wyświetlone okno pomocy.
    """
    darken_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    darken_surface.fill((0, 0, 0, 128))
    screen.blit(darken_surface, (0, 0))

    help_text = "Sterowanie"
    help_font = pygame.font.Font(None, 55)
    help_color = WHITE
    help_surface = help_font.render(help_text, True, help_color)
    help_rect = help_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 180))
    screen.blit(help_surface, (help_rect))

    font = pygame.font.Font(None, 24)
    max_text_width = 0
    total_text_height = 0
    line_spacing = 30

    help_keys = ['LPM (Lewy przycisk myszy) - strzał', '1 - zakup punktów zdrowia', 
                 '2 - zakup automatycznej wieżyczki', '3 - zwiększenie obrażeń od strzału', '4 - zwiększenie szybkości pocisków', 
                 '5 - zakup błyskawicy', 'M - wyciszenie/odciszenie muzyki', 'SPACJA - losowanie', 
                 'P - pauzowanie/odpauzowanie gry', 'ESC - wyjście z gry']

    for key_description in help_keys:
        text_surface = font.render(key_description, True, (255, 255, 255))
        max_text_width = max(max_text_width, text_surface.get_width())
        total_text_height += line_spacing

    # Oblicz współrzędne x i y startowe, aby wyśrodkować tekst
    x = (width - max_text_width) // 2
    y = (height - total_text_height) // 2 + 20

    for key_description in help_keys:
        text_surface = font.render(key_description, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        y += line_spacing

    pygame.mouse.set_visible(True)


def help_menu():
    """
    \brief Wyświetla menu pomocy z przyciskiem "Wstecz".
    
    Menu pomocy zawiera przycisk "Wstecz", który po naciśnięciu przenosi użytkownika z powrotem do głównego menu.
    """
    back_button = Button(width // 2 - 100, height // 2 + 200, 200, 50, "Wstecz", RED, WHITE)
    running = True

    while running:
        screen.blit(tlo, tlo_rect)

        draw_help(screen)

        back_button.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    running = False

def add_purchased_message(message, overwrite=True):
    """
    \brief Dodaje wiadomość o zakupie do listy wyświetlanych wiadomości.
    
    \param message Tekst wiadomości do wyświetlenia.
    \param overwrite Jeśli True, wiadomość o tym samym zakupie zostanie nadpisana. Jeśli False, zostanie dodana nowa wiadomość.
    """
    if overwrite:
        for msg in purchased_messages:
            if msg["text"] == message:
                msg["time"] = pygame.time.get_ticks() + 1000
                return
    purchased_messages.append({"text": message, "time": pygame.time.get_ticks() + 1000})

def generate_lottery_drop(result):
    """
    \brief Funkcja odpowiada za generowanie wyników losowania w grze.

    \param result: Nazwa obrazka, który został wybrany podczas animacji losowania.
    \return: Komunikat do wyświetlenia graczowi, opisujący wynik losowania.
    """
    global shoot_delay, currency, current_level, enemies_to_defeat, enemies_to_spawn
    if result == 'item0':
            dmg = []
            for _ in range(2):
                dmg.append(10)
            for _ in range(10):
                dmg.append(5)
            for _ in range(10):
                dmg.append(1)
            for _ in range(1):
                dmg.append(-3)
            for _ in range(3):
                dmg.append(-2)
            for _ in range(5):
                dmg.append(-1)     

            drop = random.choice(dmg)
            Bullet.damage += drop
            if  Bullet.damage <=1: Bullet.damage = 1
            if drop < 0:
                return f'Obrażenia zostały zmniejszone o {-drop}'
            elif drop > 0:
                return f'Obrażenia zostały zwiększone o {drop}'
    if result == 'item1':
            speed = []
            for _ in range(2):
                speed.append(10)
            for _ in range(10):
                speed.append(5)
            for _ in range(10):
                speed.append(2)
            for _ in range(1):
                speed.append(-2)
            for _ in range(3):
                speed.append(-1)
            for _ in range(5):
                speed.append(-0.5)

            drop = random.choice(speed)
            Bullet.speed += drop
            if drop > 0: 
                shoot_delay -= 100
                Tower.attack_delay -= 200
            else:
                shoot_delay += 100
                Tower.attack_delay += 200
            
            if Bullet.speed >= 50: Bullet.speed = 50
            if Bullet.speed <= 12: Bullet.speed = 12 
            if Tower.attack_delay <= 500: Tower.attack_delay = 500
            if Tower.attack_delay >= 2000: Tower.attack_delay = 2000
            if shoot_delay <= 10: shoot_delay = 10
            if shoot_delay >= 500: shoot_delay = 500

            if drop < 0:
                return f'Szybkość strzału została zmniejszona o {-drop}'
            elif drop > 0:
                return f'Szybkość strzału została zwiększona o {drop}'
    
    if result == 'item2':
            hp = []
            for _ in range(5):
                hp.append(50)
            for _ in range(10):
                hp.append(10)
            for _ in range(10):
                hp.append(5)
            # for _ in range(1):
            #     hp.append(-20)
            # for _ in range(3):
            #     hp.append(-5)
            # for _ in range(5):
            #     hp.append(-1)     
            
            drop = random.choice(hp)
            castle.hp += drop
            if castle.hp <=1: castle.hp = 1
            if drop < 0:
                return f'Życie zostało zmniejszone o {-drop}'
            elif drop > 0:
                return f'Życie zostało zwiększone o {drop}'
    if result == 'item3':
            gold = []
            for _ in range(1):
                gold.append(100)
            for _ in range(10):
                gold.append(50)
            for _ in range(10):
                gold.append(20)
            for _ in range(2):
                gold.append(-50)
            for _ in range(5):
                gold.append(-20)
            for _ in range(10):
                gold.append(-10)  
                
            drop = random.choice(gold)
            currency += drop
            if currency <= 0: currency = 0
            if drop < 0:
                return f'Złoto zostało zmniejszone o {-drop}'
            elif drop > 0:
                return f'Złoto zostało zwiększone o {drop}'
    if result == 'item4':  
            castle.hp = 1
            return 'Twoje hp spada do 1'
    if result == 'item5':
            currency = 0
            return 'Reset złota do 0'
    if result == 'item6':
            Bullet.speed = 12
            Bullet.damage = 1
            Tower.attack_delay = 2000
            shoot_delay = 500
            towers.empty()
            return 'Reset wszystkich ulepszeń'
    if result == 'item7':
            current_level = 0
            enemies_to_defeat = 0
            enemies_to_spawn = 0
            enemies.empty()
            return "Reset wszystkich poziomów"

    
def start_animation():
    """
    \brief Funkcja inicjalizująca animację losowania. Losuje sekwencję obrazków i zapisuje czas rozpoczęcia animacji.
    """
    global animation_start_time, animation_sequence

    # Wygeneruj losową sekwencję obrazków
    animation_sequence = random.choices(list(item_images.keys()), k=animation_length)

    # Zapisz czas rozpoczęcia animacji
    animation_start_time = pygame.time.get_ticks()

    # Odtwarzaj muzyke podczas openingu
    lottery_sound.play()  # Dodaj tę linię, aby odtworzyć dźwięk
    


def ease_out_quad(x):
    """
    \brief Funkcja, która implementuje funkcję łagodzenia (easing) typu ease out quad.

    \param x: Wartość wejściowa do funkcji łagodzenia, zwykle czas w zakresie 0-1.
    \return: Wartość wyjściowa funkcji łagodzenia.
    """
    return 1 - (1 - x) * (1 - x)

def draw_animation(screen):
    """
    \brief Funkcja odpowiada za rysowanie animacji losowania na ekranie.

    \param screen: Powierzchnia do rysowania, na której będzie wyświetlana animacja.
    \return: Nazwę obrazka, który został wybrany podczas animacji losowania, jeśli animacja się zakończyła. W przeciwnym razie zwraca None.
    """
    global animation_start_time, animation_sequence

    elapsed_time = pygame.time.get_ticks() - animation_start_time
    t = min(1, elapsed_time / animation_time)  # Normalizacja czasu do zakresu 0-1
    eased_t = ease_out_quad(t)  # zwalnia animację pod koniec

    offset = eased_t * (len(animation_sequence) * item_width)

    start_x = (width - item_width) // 2 
    
    for i in range(len(animation_sequence) * 5):  
        image_name = animation_sequence[i % len(animation_sequence)]
        image_x = start_x - 100 + i * item_width - offset
        distance = abs(width // 2 - image_x)

        alpha = min(255, max(0, 255 - (distance / item_width) * 255))
        image = item_images[image_name].copy()
        image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        if start_x - 300 - item_width <= image_x <= start_x + 300 + len(animation_sequence) * item_width + item_width: 
            screen.blit(image, (image_x, 100))

    pygame.draw.line(screen, (255, 0, 0), (width // 2, 100), (width // 2, 150), 5)

    if elapsed_time >= animation_time:
        # Znajdź indeks obrazka, który jest na linii (w środku ekranu)
        chosen_item_index = int(((width // 2 - start_x + 100) + offset) // item_width) % len(animation_sequence)
        chosen_item_name = animation_sequence[chosen_item_index]
        return chosen_item_name

    return None



# Lista dostępnych ulepszeń do zakupu.
upgrades = [
    Upgrade("Zwiększenie HP zamku", 30, pygame.K_1),
    Upgrade("Automatyczna Wieżyczka", 80, pygame.K_2),
    Upgrade("Zwiększenie obrażeń", 30, pygame.K_3),
    Upgrade("Szybkość lotu pocisków", 30, pygame.K_4),
    Upgrade("Błyskawica", 100, pygame.K_5)
]

currency = 0  # Aktualna waluta gracza.

spawn_timer = 0  # Timer do generowania przeciwników.

current_level = 0  # Aktualny poziom gry.

enemies_per_level = 10  # Liczba przeciwników generowanych na poziom.

level_active = False  # Flaga wskazująca, czy poziom jest aktywny.

level_start_time = 0  # Czas rozpoczęcia aktualnego poziomu.

bosses_spawned = 0  # Liczba bossów wygenerowanych na aktualnym poziomie.

enemies_to_defeat = 0  # Liczba przeciwników do pokonania, aby zakończyć poziom.

shoot_delay = 500  # Opóźnienie strzału dla zamku.

purchased_messages = []  # Lista wiadomości o zakupach do wyświetlenia.

ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1  # Zdarzenie generujące przeciwników.

is_muted = False  # Zmienna do przechowywania stanu wyciszenia muzyki

game_paused = False  # Nowa zmienna do śledzenia, czy gra jest wstrzymana

help_displayed = False # Zmienna przechowująca stan okna pomocy

slots_cost = 20 # Koszt zakupu losowania

FPS = 60  # Liczba klatek na sekundę, na których działa gra.

# Ustawienia animacji
animation_length = 10  # Ile obrazków ma być wyświetlanych na raz
animation_time = 3000  # Czas trwania animacji w milisekundach

# Inicjalizacja animacji
animation_start_time = None # Przechowywanie informacji odnośnie startu losowania
animation_sequence = [] # Sekwencja obrazków do losowania

castle_image = load_and_scale_image('assets/img/other/zamek.png', 200, 230)
bullet_image = load_and_scale_image('assets/img/other/bullet.png', 10, 10)  # Obraz pocisku skalowany do 10x10 pikseli.
tlo = load_and_scale_image("assets/img/other/tlo.png", width, height)  # Obraz tła skalowany do rozmiaru ekranu.
hp_upgrade_image = load_and_scale_image('assets/img/other/hp.png', 52, 44)  # Obraz ikony ulepszenia HP skalowany do 50x50 pikseli.
bullet_icon = load_and_scale_image('assets/img/other/dmg_icon.png', 50, 50)  # Obraz ikony pocisku skalowany do 50x50 pikseli.
tlo_rect = tlo.get_rect()  # Prostokątne granice obrazu tła.
tower_icon = load_and_scale_image('assets/img/other/tower.png', 32, 51)  # Obraz ikony wieżyczki skalowany do 32x51 pikseli.
lightning_icon = load_and_scale_image('assets/img/other/lightning.png', 50, 58)  # Obraz ikony błyskawicy skalowany do 50x58 pikseli.
bullet_speed_icon = load_and_scale_image('assets/img/other/bullet_speed_icon.png', 47, 58)  # Obraz ikony prędkości pocisku skalowany do 47x58 pikseli.

crosshair_image = load_and_scale_image('assets/img/other/celownik.png', 20, 20)  # Obraz celownika skalowany do 20x20 pikseli.
crosshair_rect = crosshair_image.get_rect()  # Prostokątne granice obrazu celownika.

item_images = {f"item{i}": load_and_scale_image(f'assets/img/slots/icons/{i}.png', 50, 50) for i in range(8)}

item_width = next(iter(item_images.values())).get_width() # Szerokość obrazków animacji

lightning_frames = [pygame.image.load(f'assets/img/lightning_frames/{i}.png') for i in range(12)]  # Klatki animacji błyskawicy.

# Klatki animacji dla różnych typów przeciwników.
# Klatki są skalowane do odpowiednich rozmiarów i wczytywane do list.
# Większość przeciwników ma klatki o rozmiarze 50x50 pikseli, ale niektóre są większe.
enemies0_walk_images = [load_and_scale_image(f'assets/img/enemies/enemies0/walk/{i}.png', 50, 50) for i in range(19)]
enemies0_attack_images = [load_and_scale_image(f'assets/img/enemies/enemies0/attack/{i}.png', 50, 50) for i in range(19)]
enemies0_death_images = [load_and_scale_image(f'assets/img/enemies/enemies0/death/{i}.png', 50, 50) for i in range(19)]

enemies1_walk_images = [load_and_scale_image(f'assets/img/enemies/enemies1/walk/{i}.png', 50, 50) for i in range(19)]
enemies1_attack_images = [load_and_scale_image(f'assets/img/enemies/enemies1/attack/{i}.png', 50, 50) for i in range(19)]
enemies1_death_images = [load_and_scale_image(f'assets/img/enemies/enemies1/death/{i}.png', 50, 50) for i in range(19)]

enemies2_walk_images = [load_and_scale_image(f'assets/img/enemies/enemies2/walk/{i}.png', 50, 50) for i in range(19)]
enemies2_attack_images = [load_and_scale_image(f'assets/img/enemies/enemies2/attack/{i}.png', 50, 50) for i in range(19)]
enemies2_death_images = [load_and_scale_image(f'assets/img/enemies/enemies2/death/{i}.png', 50, 50) for i in range(19)]

enemies3_walk_images = [load_and_scale_image(f'assets/img/enemies/enemies3/walk/{i}.png', 70, 70) for i in range(19)]
enemies3_attack_images = [load_and_scale_image(f'assets/img/enemies/enemies3/attack/{i}.png', 70, 70) for i in range(19)]
enemies3_death_images = [load_and_scale_image(f'assets/img/enemies/enemies3/death/{i}.png', 70, 70) for i in range(19)]

castle = Castle(width + 50, int(height * 2/3), castle_image)  # Inicjalizacja zamku na określonej pozycji.

# Inicjalizacja grup sprite'ów dla różnych typów obiektów w grze.
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
towers = pygame.sprite.Group()
lightnings = pygame.sprite.Group()

clock = pygame.time.Clock()  # Zegar do kontrolowania tempa gry.

high_score = load_high_score()  # Wczytanie najwyższego wyniku z pliku.

main_menu()  # Wywołanie głównego menu gry.

while True:  # Główna pętla gry.
    screen.blit(tlo, tlo_rect)  # Wyświetlanie tła gry.
    enemies.draw(screen)  # Rysowanie przeciwników na ekranie.
    screen.blit(castle.image, castle.rect)  # Wyświetlanie zamku.
    bullets.draw(screen)  # Rysowanie pocisków na ekranie.
    towers.draw(screen)  # Rysowanie wież na ekranie.

    # Wyświetlanie różnych informacji na ekranie, takich jak HP, złoto, aktualny poziom i najwyższy wynik.
    render_text(f"HP: {castle.hp}", RED, (10, 10))
    render_text(f"Złoto: {currency}", YELLOW, (10, 40))
    render_text(f"Aktualny poziom: {current_level}", PURPLE, (10, 70))
    render_text(f"Najlepszy poziom: {high_score}", PURPLE, (10, 100))

    draw_upgrade_rects()  # Rysowanie prostokątów ulepszeń.
    draw_upgrade_numbers()  # Rysowanie numerów ulepszeń.
    draw_enemies_to_defeat()  # Rysowanie liczby pokonanych przeciwników.

    # Wyświetlanie obrazów ulepszeń i ich kosztów.
    screen.blit(hp_upgrade_image, (width // 2 - 147, 12))
    render_text(str(upgrades[0].cost), RED, (width // 2 - 105, 6), font_size=20)
    screen.blit(tower_icon, (width // 2 - 75, 10))
    render_text(str(upgrades[1].cost), RED, (width // 2 - 45, 6), font_size=20)
    screen.blit(bullet_icon, (width // 2 - 25, 10))
    render_text(str(upgrades[2].cost), RED, (width // 2 + 18, 6), font_size=20)
    screen.blit(bullet_speed_icon, (width // 2 + 35, 5))
    render_text(str(upgrades[3].cost), RED, (width // 2 + 75, 6), font_size=20)
    screen.blit(lightning_icon, (width // 2 + 95, 5))
    render_text(str(upgrades[4].cost), RED, (width // 2 + 130, 6), font_size=20)

    render_gradient_text('Spacja - losowanie', (8, 115, 127), (0,212,255), (width // 2, 82), font_size=25, centered=True)
    render_text('20', RED, (width // 2 + 75, 80), font_size=15)

    pygame.mouse.set_visible(False)  # Ukrywanie kursora myszy.
    mouse_pos = pygame.mouse.get_pos()  # Pobieranie pozycji myszy.
    crosshair_rect.center = mouse_pos  # Centrowanie celownika na pozycji myszy.
    screen.blit(crosshair_image, crosshair_rect)  # Wyświetlanie celownika na ekranie.

    for event in pygame.event.get():  # Obsługa zdarzeń.
        if event.type == pygame.QUIT:  # Zakończenie gry, gdy gracz zamknie okno.
            pygame.quit()
            sys.exit()

        # Strzelanie pociskiem, gdy gracz kliknie myszą.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - castle.last_shot_time > shoot_delay: 
                    bullet = Bullet(castle.rect.center, event.pos)
                    bullets.add(bullet)
                    castle.last_shot_time = current_time
        
        # Obsługa kupowania ulepszeń, gdy gracz naciśnie odpowiedni klawisz.
        if event.type == pygame.KEYDOWN:
            if event.key == upgrades[0].key:
                result = buy_hp()
                if result is True:
                    add_purchased_message(f"Zakupiono: {upgrades[0].name}")
                elif result is False:
                        purchased_messages.append({"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000})
            if event.key == upgrades[1].key:
                    result = buy_turret()
                    if result is True:
                        add_purchased_message(f"Zakupiono: {upgrades[1].name}")
                    elif result is None:
                        purchased_messages.append({"text": "Wieża zbyt oddalona od zamku", "time": pygame.time.get_ticks() + 1000})
                    elif result is False:
                        purchased_messages.append({"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000})
            if event.key == upgrades[2].key:
                    result = buy_damage()
                    if result is True:
                        add_purchased_message(f"Zakupiono: {upgrades[2].name}")
                    elif result is False:
                            purchased_messages.append(
                                {"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000}
                            )
            if event.key == upgrades[3].key:
                result = buy_bullet_speed()
                if result is True:
                    add_purchased_message(f"Zakupiono: {upgrades[3].name}")
                elif result is False:
                        purchased_messages.append(
                            {"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000}
                        )
            if event.key == upgrades[4].key:
                result = buy_lightning()
                if result is True:
                    add_purchased_message(f"Zakupiono: {upgrades[4].name}")
                elif result is False:
                        purchased_messages.append(
                            {"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000})

            # Dodawanie dużo złota w celach deweloperskich.
            if event.key == pygame.K_l:
                    currency+=99999

            # Wycisz muzykę, jeśli nie jest wyciszona; w przeciwnym razie przywróć głośność
            if event.key == pygame.K_m:
                if not is_muted:
                    pygame.mixer.music.set_volume(0)
                    is_muted = True
                else:
                    pygame.mixer.music.set_volume(music_volume)
                    is_muted = False
            
            # Zakończenie gry, gdy gracz wcisnie klawisz ESC.
            if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Gra jest pauzowana po wciśnięciu klawisza 'p'
            if event.key == pygame.K_p:
                game_paused = not game_paused  # Zmień stan gry na przeciwny
            
            if event.key == pygame.K_h:
                help_displayed = not help_displayed
                
            # Rozpoczęcie animacji losowania po wciśnięciu klawisza SPACE
            if event.key == pygame.K_SPACE and animation_start_time is None:
                if currency >= slots_cost:
                    currency -= slots_cost
                    start_animation()
                else:
                    purchased_messages.append(
                                {"text": "Nie masz wystarczająco złota", "time": pygame.time.get_ticks() + 1000})

        # Spawnowanie przeciwników, gdy wystąpi zdarzenie SPAWN_ENEMY.
        if event.type == ENEMY_SPAWN_EVENT:
            if len(enemies) < current_level * enemies_per_level:
                spawn_enemies()
            else:
                pygame.time.set_timer(ENEMY_SPAWN_EVENT, 0)

    # Menu pauzy 
    if game_paused:
        draw_pause_info(screen)
        pygame.display.flip()
        while game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_paused = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_paused = False  
                    if event.key == pygame.K_m:
                        if not is_muted:
                            pygame.mixer.music.set_volume(0)
                            is_muted = True
                        else:
                            pygame.mixer.music.set_volume(music_volume)
                            is_muted = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    else:
        pass
    
    # Menu pomocy
    if help_displayed:
        draw_help(screen)
        pygame.display.flip()
        while help_displayed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    help_displayed = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if not is_muted:
                            pygame.mixer.music.set_volume(0)
                            is_muted = True
                        else:
                            pygame.mixer.music.set_volume(music_volume)
                            is_muted = False
                    if event.key == pygame.K_h:
                        help_displayed = not help_displayed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    else:
        pass
    
    # Wczytywanie logiki odnośnie losowania oraz wyświetlanie jej na ekranie.
    if animation_start_time is not None:
        result = draw_animation(screen)
        if result is not None:
            text = generate_lottery_drop(result)
            purchased_messages.append({"text": f"{text}", "time": pygame.time.get_ticks() + 2000})
            animation_start_time = None


            

    # Atakowanie najbliższego przeciwnika przez każdą wieżę.
    for tower in towers:
        nearest_enemy = find_nearest_enemy(tower, enemies)
        if nearest_enemy is not None:
            current_time = pygame.time.get_ticks()
            if current_time - tower.last_attack_time > tower.attack_delay:
                bullet = Bullet(tower.rect.center, nearest_enemy.rect.center)
                bullets.add(bullet)
                tower.last_attack_time = current_time

    # Sprawdzanie kolizji pocisków z przeciwnikami i zadawanie im obrażeń.
    for bullet in bullets:
        hit_enemies = [enemy for enemy in enemies if pygame.sprite.collide_rect(bullet, enemy)]
        for enemy in hit_enemies:
            if hit_enemies:
                enemy.take_damage(bullet.damage)
            bullet.kill()

    # Koniec gry, gdy HP zamku spadnie do 0.
    if castle.hp <= 0:
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, castle):
                enemy.kill()
        if game_over():
            castle.hp = 5
            currency = 0
            current_level = 0
            enemies.empty()
            bullets.empty()
            towers.empty()
            high_score = load_high_score()
            enemies_to_defeat = 0
            Bullet.speed = 12
            Bullet.damage = 1
            Tower.attack_delay = 2000
            shoot_delay = 500
        else:
            break

    # Rozpoczynanie nowego poziomu, gdy wszystkich przeciwników pokonano.
    if not level_active:
        if enemies_to_defeat <= 0:
            start_new_level()
    else:
        if pygame.time.get_ticks() - level_start_time > 3000:  # Czas wyświetlania informacji o poziomie (3 sekundy)
            level_active = False

    # Wyświetlanie informacji o poziomie, jeśli jest aktywny.
    if level_active:
        draw_level_info(screen, current_level)
    
    # Wyświetlanie wiadomości po zakupie ulepszeń i usuwanie starych wiadomości.
    for message in purchased_messages:
        if message["time"] > pygame.time.get_ticks():
            render_text(
                message["text"], RED, (width // 2, height // 4-30), font_size=24, centered=True
            )
        else:
            purchased_messages.remove(message)

    # Aktualizowanie i rysowanie błyskawic, usuwanie starych błyskawic.
    for lightning in lightnings.sprites():
        if not lightning.update():
            lightnings.remove(lightning)
        else:
            lightning.draw(screen)

    bullets.update()  # Aktualizowanie pocisków.
    enemies.update()  # Aktualizowanie przeciwników.

    for enemy in enemies:
        if enemy.hp < enemy.max_hp:  # Rysowanie paska HP dla przeciwników z uszkodzonym zdrowiem.
            draw_hp_bar(screen, enemy)

    save_high_score()  # Zapisywanie najwyższego wyniku.

    pygame.display.flip()  # Aktualizowanie wyświetlanego obrazu.
    clock.tick(FPS)  # Ograniczanie liczby klatek na sekundę do wartości FPS.
