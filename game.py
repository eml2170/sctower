import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StarCraft Tower Defense: Terran vs Zerg")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Game variables
FPS = 60
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 24)

# Player stats
minerals = 200
gas = 50
lives = 20
score = 0
wave = 1

# Game phases
PHASE_BUILD = 0
PHASE_WAVE = 1
current_phase = PHASE_BUILD
phase_timer = 30 * FPS  # 30 seconds for build phase
remaining_zerg = 0

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        self.cooldown = 0
        
        if tower_type == "marine":
            self.damage = 5
            self.range = 150
            self.fire_rate = 30
            self.cost = (50, 0)  # (minerals, gas)
            self.color = BLUE
        elif tower_type == "firebat":
            self.damage = 12
            self.range = 100
            self.fire_rate = 45
            self.cost = (75, 25)
            self.color = RED
        elif tower_type == "tank":
            self.damage = 30
            self.range = 200
            self.fire_rate = 90
            self.cost = (150, 75)
            self.color = GRAY
        
        self.targets = []
    
    def find_targets(self, enemies):
        self.targets = []
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if distance <= self.range:
                self.targets.append((enemy, distance))
        self.targets.sort(key=lambda x: x[1])  # Sort by distance
    
    def attack(self, enemies):
        if self.cooldown <= 0 and self.targets:
            target = self.targets[0][0]
            target.hp -= self.damage
            
            # Reset cooldown
            self.cooldown = self.fire_rate
            
            # Return attack information
            return (self.x, self.y, target.x, target.y)
        return None
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 20)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), 20, 2)
        
        # Draw range circle (only when selected)
        if self == selected_tower:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.range, 1)
        
        # Draw tower level
        level_text = game_font.render(str(self.level), True, BLACK)
        surface.blit(level_text, (self.x - 5, self.y - 10))

class Enemy:
    def __init__(self, path, enemy_type):
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.enemy_type = enemy_type
        self.progress = 0
        self.dead = False
        
        if enemy_type == "zergling":
            self.hp = 30
            self.max_hp = 30
            self.speed = 2
            self.reward = (8, 0)  # (minerals, gas)
            self.damage = 1
            self.color = (150, 0, 0)
        elif enemy_type == "hydralisk":
            self.hp = 80
            self.max_hp = 80
            self.speed = 1.5
            self.reward = (15, 5)
            self.damage = 2
            self.color = (0, 150, 0)
        elif enemy_type == "ultralisk":
            self.hp = 300
            self.max_hp = 300
            self.speed = 0.8
            self.reward = (30, 15)
            self.damage = 5
            self.color = (150, 0, 150)
    
    def update(self):
        if self.path_index < len(self.path) - 1:
            # Calculate direction to next point
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < self.speed:
                self.path_index += 1
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        
        # Check if enemy reached the end
        if self.path_index == len(self.path) - 1:
            return True
        
        # Check if enemy died
        if self.hp <= 0:
            self.dead = True
            return False
        
        return False
    
    def draw(self, surface):
        # Draw enemy
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 15)
        
        # Draw health bar
        bar_width = 30
        bar_height = 5
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(surface, RED, (self.x - bar_width//2, self.y - 25, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.x - bar_width//2, self.y - 25, bar_width * health_percentage, bar_height))

# Define map and path
game_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

TILE_SIZE = 50

# Define enemy path
path = [
    (0, 75),
    (300, 75),
    (300, 175),
    (450, 175),
    (450, 325),
    (600, 325)
]

# Game state variables
towers = []
enemies = []
projectiles = []
selected_tower = None
spawn_cooldown = 0
game_over = False
selected_tower_type = "marine"

def calculate_wave_size():
    # Calculate number of zerg units for this wave
    base_amount = 5
    zergling_count = max(5, wave * 3)
    hydralisk_count = max(0, (wave - 2) * 2)
    ultralisk_count = max(0, wave - 4)
    
    return zergling_count + hydralisk_count + ultralisk_count

def spawn_enemy():
    global remaining_zerg
    
    if remaining_zerg <= 0:
        return False
    
    # Determine enemy type based on wave and what's left
    if wave < 3:
        enemy_type = "zergling"
    elif wave < 5:
        if random.random() < 0.7:  # 70% chance for zergling, 30% for hydralisk
            enemy_type = "zergling"
        else:
            enemy_type = "hydralisk"
    else:
        r = random.random()
        if r < 0.6:  # 60% zergling
            enemy_type = "zergling"
        elif r < 0.9:  # 30% hydralisk
            enemy_type = "hydralisk"
        else:  # 10% ultralisk
            enemy_type = "ultralisk"
    
    enemies.append(Enemy(path, enemy_type))
    remaining_zerg -= 1
    return True

def start_wave_phase():
    global current_phase, phase_timer, remaining_zerg
    
    current_phase = PHASE_WAVE
    remaining_zerg = calculate_wave_size()
    phase_timer = max(5, 30 - wave) * FPS  # Time between spawns decreases with wave

def start_build_phase():
    global current_phase, phase_timer, minerals, gas, wave
    
    current_phase = PHASE_BUILD
    phase_timer = 30 * FPS  # 30 seconds for build phase
    
    # Give resources for completing wave
    minerals += 100 + wave * 20
    gas += 25 + wave * 5
    
    # Increment wave counter
    wave += 1

def draw_map():
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if game_map[y][x] == 1:  # Path
                pygame.draw.rect(screen, BROWN, rect)
            else:  # Buildable
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

def draw_path():
    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLACK, path[i], path[i+1], 3)

def draw_ui():
    # Draw resources
    mineral_text = game_font.render(f"Minerals: {minerals}", True, BLUE)
    gas_text = game_font.render(f"Gas: {gas}", True, GREEN)
    lives_text = game_font.render(f"Lives: {lives}", True, RED)
    wave_text = game_font.render(f"Wave: {wave}", True, WHITE)
    score_text = game_font.render(f"Score: {score}", True, WHITE)
    
    screen.blit(mineral_text, (10, 10))
    screen.blit(gas_text, (10, 40))
    screen.blit(lives_text, (10, 70))
    screen.blit(wave_text, (SCREEN_WIDTH - 100, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 100, 40))
    
    # Draw phase information
    if current_phase == PHASE_BUILD:
        phase_text = game_font.render("BUILD PHASE", True, YELLOW)
        timer_text = game_font.render(f"Next wave in: {phase_timer // FPS}s", True, YELLOW)
    else:
        phase_text = game_font.render("WAVE PHASE", True, RED)
        timer_text = game_font.render(f"Remaining Zerg: {remaining_zerg + len(enemies)}", True, RED)
    
    screen.blit(phase_text, (SCREEN_WIDTH//2 - 70, 10))
    screen.blit(timer_text, (SCREEN_WIDTH//2 - 100, 40))
    
    # Draw tower buttons with costs
    small_font = pygame.font.SysFont("Arial", 16)
    
    # Marine button
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 130, 60, 80))
    marine_text = small_font.render("Marine", True, WHITE)
    marine_cost = small_font.render("50 M", True, WHITE)
    marine_cost2 = small_font.render("0 G", True, WHITE)
    screen.blit(marine_text, (SCREEN_WIDTH - 205, SCREEN_HEIGHT - 125))
    screen.blit(marine_cost, (SCREEN_WIDTH - 195, SCREEN_HEIGHT - 95))
    screen.blit(marine_cost2, (SCREEN_WIDTH - 195, SCREEN_HEIGHT - 75))
    
    # Firebat button
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 130, 60, 80))
    firebat_text = small_font.render("Firebat", True, WHITE)
    firebat_cost = small_font.render("75 M", True, WHITE)
    firebat_cost2 = small_font.render("25 G", True, WHITE)
    screen.blit(firebat_text, (SCREEN_WIDTH - 135, SCREEN_HEIGHT - 125))
    screen.blit(firebat_cost, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 95))
    screen.blit(firebat_cost2, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 75))
    
    # Tank button
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 130, 60, 80))
    tank_text = small_font.render("Tank", True, WHITE)
    tank_cost = small_font.render("150 M", True, WHITE)
    tank_cost2 = small_font.render("75 G", True, WHITE)
    screen.blit(tank_text, (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 125))
    screen.blit(tank_cost, (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 95))
    screen.blit(tank_cost2, (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 75))
    
    # Draw selected tower type
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 190, 30))
    selected_text = game_font.render(f"Selected: {selected_tower_type.capitalize()}", True, BLACK)
    screen.blit(selected_text, (SCREEN_WIDTH - 195, SCREEN_HEIGHT - 35))
    
    # If tower is selected, show upgrade option with better layout
    if selected_tower:
        # Create separate texts for better layout
        upgrade_label = small_font.render("Upgrade:", True, BLACK)
        upgrade_cost = small_font.render(f"{selected_tower.cost[0] * selected_tower.level} M / {selected_tower.cost[1] * selected_tower.level} G", True, BLACK)
        sell_text = small_font.render(f"Sell: {int(selected_tower.cost[0] * 0.7 * selected_tower.level)} M", True, BLACK)
        
        # Draw upgrade button - made wider
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 180, 110, 30))
        # Draw sell button
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 180, 70, 30))
        
        # Place texts
        screen.blit(upgrade_label, (SCREEN_WIDTH - 195, SCREEN_HEIGHT - 178))
        screen.blit(upgrade_cost, (SCREEN_WIDTH - 195, SCREEN_HEIGHT - 162))
        screen.blit(sell_text, (SCREEN_WIDTH - 78, SCREEN_HEIGHT - 170))
    
    # Draw start wave button during build phase
    if current_phase == PHASE_BUILD:
        pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT - 50, 160, 40))
        start_text = game_font.render("START WAVE", True, BLACK)
        screen.blit(start_text, (SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 40))

def can_place_tower(x, y):
    # Check if position is on a path tile
    map_x = x // TILE_SIZE
    map_y = y // TILE_SIZE
    
    if map_x < 0 or map_x >= len(game_map[0]) or map_y < 0 or map_y >= len(game_map):
        return False
    
    if game_map[map_y][map_x] == 1:  # Path tile
        return False
    
    # Check if position is already occupied by another tower
    for tower in towers:
        if math.sqrt((tower.x - x)**2 + (tower.y - y)**2) < 30:
            return False
    
    return True

# Main game loop
running = True
paused = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_1:
                selected_tower_type = "marine"
            elif event.key == pygame.K_2:
                selected_tower_type = "firebat"
            elif event.key == pygame.K_3:
                selected_tower_type = "tank"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if clicked on start wave button
                if current_phase == PHASE_BUILD and SCREEN_WIDTH//2 - 80 <= mouse_x <= SCREEN_WIDTH//2 + 80 and SCREEN_HEIGHT - 50 <= mouse_y <= SCREEN_HEIGHT - 10:
                    start_wave_phase()
                # Check if clicked on tower buttons
                elif SCREEN_WIDTH - 210 <= mouse_x <= SCREEN_WIDTH - 150 and SCREEN_HEIGHT - 130 <= mouse_y <= SCREEN_HEIGHT - 50:
                    selected_tower_type = "marine"
                elif SCREEN_WIDTH - 140 <= mouse_x <= SCREEN_WIDTH - 80 and SCREEN_HEIGHT - 130 <= mouse_y <= SCREEN_HEIGHT - 50:
                    selected_tower_type = "firebat"
                elif SCREEN_WIDTH - 70 <= mouse_x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 130 <= mouse_y <= SCREEN_HEIGHT - 50:
                    selected_tower_type = "tank"
                # Check if clicked on upgrade/sell buttons - updated coordinates
                elif selected_tower and SCREEN_WIDTH - 200 <= mouse_x <= SCREEN_WIDTH - 90 and SCREEN_HEIGHT - 180 <= mouse_y <= SCREEN_HEIGHT - 150:
                    # Upgrade tower
                    mineral_cost = selected_tower.cost[0] * selected_tower.level
                    gas_cost = selected_tower.cost[1] * selected_tower.level
                    
                    if minerals >= mineral_cost and gas >= gas_cost:
                        minerals -= mineral_cost
                        gas -= gas_cost
                        selected_tower.level += 1
                        selected_tower.damage = int(selected_tower.damage * 1.5)
                        selected_tower.range = int(selected_tower.range * 1.2)
                        selected_tower.fire_rate = max(10, int(selected_tower.fire_rate * 0.8))
                elif selected_tower and SCREEN_WIDTH - 80 <= mouse_x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 180 <= mouse_y <= SCREEN_HEIGHT - 150:
                    # Sell tower
                    minerals += int(selected_tower.cost[0] * 0.7 * selected_tower.level)
                    towers.remove(selected_tower)
                    selected_tower = None
                else:
                    # Check if a tower is clicked
                    selected_tower = None
                    for tower in towers:
                        if math.sqrt((tower.x - mouse_x)**2 + (tower.y - mouse_y)**2) < 20:
                            selected_tower = tower
                            break
                    
                    # If no tower is clicked, try to place a new tower (only in build phase)
                    if selected_tower is None and current_phase == PHASE_BUILD and can_place_tower(mouse_x, mouse_y):
                        new_tower = Tower(mouse_x, mouse_y, selected_tower_type)
                        mineral_cost, gas_cost = new_tower.cost
                        
                        if minerals >= mineral_cost and gas >= gas_cost:
                            minerals -= mineral_cost
                            gas -= gas_cost
                            towers.append(new_tower)
    
    if game_over:
        # Display game over screen
        screen.fill(BLACK)
        game_over_text = game_font.render("GAME OVER", True, RED)
        score_text = game_font.render(f"Final Score: {score}", True, WHITE)
        restart_text = game_font.render("Press ESC to quit", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()
        continue
    
    if not paused:
        # Update phase timer
        if phase_timer > 0:
            phase_timer -= 1
        
        # Phase logic
        if current_phase == PHASE_BUILD:
            # Automatically start wave when timer runs out
            if phase_timer <= 0:
                start_wave_phase()
        else:  # PHASE_WAVE
            # Spawn enemies
            if remaining_zerg > 0 and spawn_cooldown <= 0:
                spawn_enemy()
                spawn_cooldown = max(10, 60 - wave * 5)  # Spawn faster in later waves
            else:
                spawn_cooldown -= 1
            
            # Start a new build phase if all enemies are defeated
            if remaining_zerg <= 0 and len(enemies) == 0:
                start_build_phase()
        
            # Update towers
            for tower in towers:
                tower.update()
                tower.find_targets(enemies)
                attack_info = tower.attack(enemies)
                if attack_info:
                    projectiles.append(attack_info)
            
            # Update enemies
            for enemy in enemies[:]:
                if enemy.update():  # Enemy reached the end
                    lives -= enemy.damage
                    enemies.remove(enemy)
                    if lives <= 0:
                        game_over = True
                elif enemy.dead:  # Enemy died
                    minerals += enemy.reward[0]
                    gas += enemy.reward[1]
                    score += enemy.max_hp
                    enemies.remove(enemy)
        
        # Update projectiles (simplified as they just appear for one frame)
        projectiles = []
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw game map
    draw_map()
    draw_path()
    
    # Draw towers
    for tower in towers:
        tower.draw(screen)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw projectiles
    for start_x, start_y, end_x, end_y in projectiles:
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 2)
    
    # Draw UI
    draw_ui()
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
