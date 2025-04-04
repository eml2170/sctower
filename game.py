import pygame
import sys
import math
import random
import os
from game_balance import *  # Import all balance parameters

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 880
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
PURPLE = (128, 0, 128)


# Game variables
FPS = 60
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 24)

# Board position offset
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 50

# Asset paths
ASSET_DIR = "assets"
IMG_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

# Create directories if they don't exist
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(SOUND_DIR, exist_ok=True)

# Load images
def load_image(name, scale=1.0):
    try:
        image = pygame.image.load(os.path.join(IMG_DIR, name))
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except pygame.error:
        # If image is not found, create a placeholder surface
        placeholder = pygame.Surface((40, 40))
        placeholder.fill(WHITE)
        pygame.draw.rect(placeholder, BLACK, (0, 0, 40, 40), 2)
        return placeholder

# Create placeholder images for use until real assets are added
def create_placeholder_images():
    # Create Marine placeholder
    marine_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(marine_img, BLUE, (20, 20), 18)
    pygame.draw.circle(marine_img, GRAY, (20, 20), 18, 2)
    pygame.draw.rect(marine_img, GRAY, (10, 5, 20, 15))
    pygame.image.save(marine_img, os.path.join(IMG_DIR, "marine.png"))
    
    # Create Firebat placeholder
    firebat_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(firebat_img, RED, (20, 20), 18)
    pygame.draw.circle(firebat_img, BLACK, (20, 20), 18, 2)
    pygame.draw.polygon(firebat_img, BLACK, [(10, 10), (30, 10), (20, 25)])
    pygame.image.save(firebat_img, os.path.join(IMG_DIR, "firebat.png"))
    
    # Create Tank placeholder
    tank_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(tank_img, GRAY, (20, 20), 18)
    pygame.draw.circle(tank_img, BLACK, (20, 20), 18, 2)
    pygame.draw.rect(tank_img, BLACK, (10, 15, 20, 10))
    pygame.draw.rect(tank_img, BLACK, (15, 10, 10, 20))
    pygame.image.save(tank_img, os.path.join(IMG_DIR, "tank.png"))
    
    # Create Zergling placeholder
    zergling_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(zergling_img, (150, 0, 0), (15, 15), 13)
    pygame.draw.circle(zergling_img, BLACK, (15, 15), 13, 2)
    pygame.draw.line(zergling_img, BLACK, (5, 5), (10, 10), 2)
    pygame.draw.line(zergling_img, BLACK, (25, 5), (20, 10), 2)
    pygame.image.save(zergling_img, os.path.join(IMG_DIR, "zergling.png"))
    
    # Create Hydralisk placeholder
    hydralisk_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(hydralisk_img, (0, 150, 0), (15, 15), 13)
    pygame.draw.circle(hydralisk_img, BLACK, (15, 15), 13, 2)
    pygame.draw.polygon(hydralisk_img, BLACK, [(5, 5), (25, 5), (15, 25)])
    pygame.image.save(hydralisk_img, os.path.join(IMG_DIR, "hydralisk.png"))
    
    # Create Ultralisk placeholder
    ultralisk_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(ultralisk_img, (150, 0, 150), (15, 15), 13)
    pygame.draw.circle(ultralisk_img, BLACK, (15, 15), 13, 2)
    pygame.draw.polygon(ultralisk_img, BLACK, [(5, 10), (25, 10), (15, 3)])
    pygame.draw.polygon(ultralisk_img, BLACK, [(5, 20), (25, 20), (15, 27)])
    pygame.image.save(ultralisk_img, os.path.join(IMG_DIR, "ultralisk.png"))

# Load sound effects
def load_sound(name):
    try:
        sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, name))
        return sound
    except pygame.error:
        # Return a dummy sound if file not found
        return pygame.mixer.Sound(buffer=bytes([0]))

# Create placeholder WAV files for sounds
def create_placeholder_sounds():
    # We can't easily create sound files in code, so let's skip this for now
    # In a real implementation, you would distribute sound files with your game
    pass

# Generate placeholder assets if they don't exist yet
create_placeholder_images()
create_placeholder_sounds()

# Load images
marine_img = load_image("marine.png")
firebat_img = load_image("firebat.png")
tank_img = load_image("tank.png")
zergling_img = load_image("zergling.png")
hydralisk_img = load_image("hydralisk.png")
ultralisk_img = load_image("ultralisk.png")

# Load sounds (commented out until real sound files are available)
# We define these here but the actual sound loading will happen when the files exist
# build_sound = load_sound("build.wav")
upgrade_sound = load_sound("upgrade.wav")
sell_sound = load_sound("sell.wav")
marine_attack_sound = load_sound("marine_attack.wav")
firebat_attack_sound = load_sound("firebat_attack.wav")
tank_attack_sound = load_sound("tank_attack.wav")
zergling_death_sound = load_sound("zergling_death.wav")
hydralisk_death_sound = load_sound("hydralisk_death.wav")
ultralisk_death_sound = load_sound("ultralisk_death.wav")
wave_start_sound = load_sound("wave_start.wav")
game_over_sound = load_sound("game_over.wav")

# Player stats
minerals = STARTING_MINERALS
gas = STARTING_GAS
lives = STARTING_LIVES
score = 0
wave = 1

# Game phases
PHASE_BUILD = 0
PHASE_WAVE = 1
current_phase = PHASE_BUILD
phase_timer = 30 * FPS  # 30 seconds for build phase
remaining_zerg = 0

class Projectile:
    def __init__(self, start_x, start_y, end_x, end_y, tower_type, damage, aoe_radius=0):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.tower_type = tower_type
        self.damage = damage
        self.aoe_radius = aoe_radius
        
        # Increase lifetime for better visuals
        if tower_type == "marine":
            self.lifetime = 20  # Shorter for bullets
        elif tower_type == "firebat":
            self.lifetime = 25  # Medium for flames
        else:  # Tank
            self.lifetime = 45  # Longer for tank shells/explosions
            
        self.current_frame = 0
        self.speed = 10  # Slower speed for better visuals
        
        # Calculate direction vector
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed
        
        # Calculate angle for cone direction
        self.angle = math.atan2(dy, dx)
        
        # Current position
        self.x = start_x
        self.y = start_y
        
        # For AoE effects
        self.exploded = False
        self.explosion_radius = 0
        self.max_explosion_radius = aoe_radius
        self.explosion_duration = 0  # Track how long explosion has been active
        
        # For flame effects
        self.flame_width = 0.3  # Starting width in radians
        self.cone_length = 15  # Length of the flame cone
        
    def update(self):
        if not self.exploded:
            # Move projectile
            self.x += self.dx
            self.y += self.dy
            
            # Check if reached target
            distance_to_target = math.sqrt((self.end_x - self.x)**2 + (self.end_y - self.y)**2)
            if distance_to_target < self.speed:
                self.exploded = True
                self.explosion_duration = 0
                
            # For firebat: make flame wider as it travels
            if self.tower_type == "firebat" and self.flame_width < 0.8:
                self.flame_width += 0.05
                self.cone_length += 2  # Make the cone longer as it travels
        else:
            # Track explosion duration
            self.explosion_duration += 1
            
            # Expand explosion (faster for more impact)
            if self.tower_type == "tank":
                self.explosion_radius = min(self.max_explosion_radius, 
                                         self.explosion_radius + self.max_explosion_radius / 5)
            elif self.tower_type == "firebat":
                # For firebat, we don't need to grow the explosion radius much
                # since we'll draw the explosion as an extension of the cone
                self.explosion_radius = min(self.max_explosion_radius,
                                         self.explosion_radius + self.max_explosion_radius / 3)
        
        self.current_frame += 1
        
        # Keep explosion alive for at least 20 frames
        if self.exploded and self.explosion_duration < 20:
            return True
            
        return self.current_frame < self.lifetime
    
    def draw(self, surface):
        if not self.exploded:
            if self.tower_type == "marine":
                # Draw bullet with tracer effect
                pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), 3)
                # Add bullet trail
                trail_length = 15
                trail_end_x = self.x - self.dx * trail_length / self.speed
                trail_end_y = self.y - self.dy * trail_length / self.speed
                pygame.draw.line(surface, (255, 255, 100), (self.x, self.y), 
                                (trail_end_x, trail_end_y), 2)
            elif self.tower_type == "firebat":
                # Draw flame cone with random flicker
                flame_length = self.cone_length + random.randint(-5, 5)  # Random flicker
                cone_width = self.flame_width
                
                # Create base cone shape
                points = [
                    (self.x, self.y),
                    (self.x + math.cos(self.angle + cone_width) * flame_length * 0.8, 
                     self.y + math.sin(self.angle + cone_width) * flame_length * 0.8),
                    (self.x + math.cos(self.angle) * flame_length * 1.2, 
                     self.y + math.sin(self.angle) * flame_length * 1.2),
                    (self.x + math.cos(self.angle - cone_width) * flame_length * 0.8, 
                     self.y + math.sin(self.angle - cone_width) * flame_length * 0.8)
                ]
                
                # Draw multiple flame layers with different colors
                # Base layer (darker orange)
                pygame.draw.polygon(surface, (230, 100, 20), points)
                
                # Inner cone (brighter yellow-orange)
                inner_width = cone_width * 0.6
                inner_points = [
                    (self.x, self.y),
                    (self.x + math.cos(self.angle + inner_width) * flame_length * 0.6, 
                     self.y + math.sin(self.angle + inner_width) * flame_length * 0.6),
                    (self.x + math.cos(self.angle) * flame_length * 0.9, 
                     self.y + math.sin(self.angle) * flame_length * 0.9),
                    (self.x + math.cos(self.angle - inner_width) * flame_length * 0.6, 
                     self.y + math.sin(self.angle - inner_width) * flame_length * 0.6)
                ]
                pygame.draw.polygon(surface, (255, 180, 50), inner_points)
                
                # Core (white-yellow)
                core_width = cone_width * 0.3
                core_points = [
                    (self.x, self.y),
                    (self.x + math.cos(self.angle + core_width) * flame_length * 0.4, 
                     self.y + math.sin(self.angle + core_width) * flame_length * 0.4),
                    (self.x + math.cos(self.angle) * flame_length * 0.6, 
                     self.y + math.sin(self.angle) * flame_length * 0.6),
                    (self.x + math.cos(self.angle - core_width) * flame_length * 0.4, 
                     self.y + math.sin(self.angle - core_width) * flame_length * 0.4)
                ]
                pygame.draw.polygon(surface, (255, 230, 150), core_points)
                
                # Add some random flickers/sparks
                for _ in range(3):
                    spark_angle = self.angle + random.uniform(-cone_width, cone_width)
                    spark_dist = random.uniform(0.5, 0.9) * flame_length
                    spark_x = self.x + math.cos(spark_angle) * spark_dist
                    spark_y = self.y + math.sin(spark_angle) * spark_dist
                    spark_size = random.uniform(1.5, 3.0)
                    pygame.draw.circle(surface, (255, 255, 200), (int(spark_x), int(spark_y)), int(spark_size))
                
            elif self.tower_type == "tank":
                # Draw tank shell with smoke trail
                pygame.draw.circle(surface, GRAY, (int(self.x), int(self.y)), 5)
                
                # Draw smoke trail (more visible)
                for i in range(7):
                    trail_x = self.x - self.dx * (i * 3) / self.speed
                    trail_y = self.y - self.dy * (i * 3) / self.speed
                    size = 5 - i * 0.6
                    smoke_color = (120 - i * 10, 120 - i * 10, 120 - i * 10)
                    pygame.draw.circle(surface, smoke_color, (int(trail_x), int(trail_y)), int(size))
        else:
            # Draw explosion effects
            if self.tower_type == "tank":
                # Multi-layered explosion with shockwave
                colors = [
                    (255, 200, 50),  # Bright yellow core
                    (255, 140, 0),   # Orange middle
                    (200, 0, 0),     # Red outer
                    (100, 100, 100)  # Gray smoke ring
                ]
                
                # Scale down the explosion in the last frames
                scale_factor = 1.0
                if self.explosion_duration > 15:
                    scale_factor = max(0.5, 1.0 - (self.explosion_duration - 15) / 10)
                
                for i, color in enumerate(colors):
                    radius = self.explosion_radius * (0.8 - i * 0.2) * scale_factor
                    if radius > 0:
                        pygame.draw.circle(surface, color, (int(self.end_x), int(self.end_y)), 
                                        int(radius))
                
                # Draw shockwave ring
                if self.explosion_radius > 10:
                    pygame.draw.circle(surface, WHITE, (int(self.end_x), int(self.end_y)), 
                                     int(self.explosion_radius * scale_factor), 2)
            
            elif self.tower_type == "firebat" and self.explosion_radius > 0:
                # Continue the cone explosion but fade it out
                flame_length = self.cone_length + self.explosion_radius * 0.5
                cone_width = self.flame_width * (1 + self.explosion_duration * 0.02)
                fade_factor = max(0, 1.0 - self.explosion_duration / 20)
                
                # Base cone with larger width at the end
                points = [
                    (self.x, self.y),
                    (self.x + math.cos(self.angle + cone_width) * flame_length * 0.9, 
                     self.y + math.sin(self.angle + cone_width) * flame_length * 0.9),
                    (self.x + math.cos(self.angle) * flame_length * 1.3, 
                     self.y + math.sin(self.angle) * flame_length * 1.3),
                    (self.x + math.cos(self.angle - cone_width) * flame_length * 0.9, 
                     self.y + math.sin(self.angle - cone_width) * flame_length * 0.9)
                ]
                
                # Adjust colors to fade out
                base_color = (int(230 * fade_factor), int(100 * fade_factor), int(20 * fade_factor))
                inner_color = (int(255 * fade_factor), int(180 * fade_factor), int(50 * fade_factor))
                core_color = (int(255 * fade_factor), int(230 * fade_factor), int(150 * fade_factor))
                
                pygame.draw.polygon(surface, base_color, points)
                
                # Smaller inner cone
                inner_width = cone_width * 0.7
                inner_points = [
                    (self.x, self.y),
                    (self.x + math.cos(self.angle + inner_width) * flame_length * 0.7, 
                     self.y + math.sin(self.angle + inner_width) * flame_length * 0.7),
                    (self.x + math.cos(self.angle) * flame_length * 1.0, 
                     self.y + math.sin(self.angle) * flame_length * 1.0),
                    (self.x + math.cos(self.angle - inner_width) * flame_length * 0.7, 
                     self.y + math.sin(self.angle - inner_width) * flame_length * 0.7)
                ]
                pygame.draw.polygon(surface, inner_color, inner_points)
                
                # Add some random flickers/sparks at the end of the cone
                for _ in range(5):
                    # Place sparks mostly near the end of the cone
                    end_angle = self.angle + random.uniform(-cone_width * 0.8, cone_width * 0.8)
                    end_dist = flame_length * random.uniform(0.8, 1.1)
                    spark_x = self.x + math.cos(end_angle) * end_dist
                    spark_y = self.y + math.sin(end_angle) * end_dist
                    spark_size = random.uniform(1.5, 4.0) * fade_factor
                    spark_color = (int(255 * fade_factor), int(255 * fade_factor), int(200 * fade_factor))
                    pygame.draw.circle(surface, spark_color, (int(spark_x), int(spark_y)), int(spark_size))

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        self.cooldown = 0
        
        if tower_type == "marine":
            self.damage = MARINE_STATS["damage"]
            self.range = MARINE_STATS["range"]
            self.fire_rate = MARINE_STATS["fire_rate"]
            self.cost = MARINE_STATS["cost"]
            self.color = BLUE
            self.image = marine_img
            self.attack_sound = marine_attack_sound
            self.aoe_radius = 0  # No AoE for marines
        elif tower_type == "firebat":
            self.damage = FIREBAT_STATS["damage"]
            self.range = FIREBAT_STATS["range"]
            self.fire_rate = FIREBAT_STATS["fire_rate"]
            self.cost = FIREBAT_STATS["cost"]
            self.color = RED
            self.image = firebat_img
            self.attack_sound = firebat_attack_sound
            self.aoe_radius = 10  # Small AoE for firebats
        elif tower_type == "tank":
            self.damage = TANK_STATS["damage"]
            self.range = TANK_STATS["range"]
            self.fire_rate = TANK_STATS["fire_rate"]
            self.cost = TANK_STATS["cost"]
            self.color = GRAY
            self.image = tank_img
            self.attack_sound = tank_attack_sound
            self.aoe_radius = 30  # Large AoE for tanks
        
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
            
            # Create projectile
            projectile = Projectile(self.x, self.y, target.x, target.y, 
                                 self.tower_type, self.damage, self.aoe_radius)
            
            # Apply damage to primary target
            target.hp -= self.damage
            
            # Apply AoE damage if applicable
            if self.aoe_radius > 0:
                if self.tower_type == "firebat":
                    # Firebat: Only damage enemies in a cone shape in the direction of the target
                    # Calculate angle to target
                    angle_to_target = math.atan2(target.y - self.y, target.x - self.x)
                    cone_width = 0.8  # Cone width in radians (about 45 degrees)
                    
                    for enemy in enemies:
                        if enemy != target:  # Don't damage primary target twice
                            # Calculate angle to this enemy
                            angle_to_enemy = math.atan2(enemy.y - self.y, enemy.x - self.x)
                            
                            # Find the angular difference
                            angle_diff = abs((angle_to_enemy - angle_to_target + math.pi) % (2 * math.pi) - math.pi)
                            
                            # Check if enemy is within the cone and within range
                            distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                            if angle_diff <= cone_width and distance <= self.aoe_radius:
                                # Reduce damage based on distance and angle
                                angle_factor = 1.0 - (angle_diff / cone_width)
                                distance_factor = 1.0 - (distance / self.aoe_radius)
                                aoe_damage = self.damage * angle_factor * distance_factor
                                enemy.hp -= aoe_damage
                else:
                    # Tank: Circular AoE
                    for enemy in enemies:
                        if enemy != target:  # Don't damage primary target twice
                            distance = math.sqrt((target.x - enemy.x)**2 + (target.y - enemy.y)**2)
                            if distance <= self.aoe_radius:
                                # Reduce damage based on distance
                                aoe_damage = self.damage * (1 - distance / self.aoe_radius)
                                enemy.hp -= aoe_damage
            
            # Play attack sound
            self.attack_sound.play()
            
            # Reset cooldown
            self.cooldown = self.fire_rate
            
            return projectile
        return None
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def draw(self, surface):
        # Draw tower image
        img_rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, img_rect)
        
        # Draw range circle (only when selected)
        if self == selected_tower:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.range, 1)
        
        # Draw tower level
        # level_text = game_font.render(str(self.level), True, WHITE)
        # level_rect = level_text.get_rect(center=(self.x, self.y + 25))
        # surface.blit(level_text, level_rect)

class Enemy:
    def __init__(self, path, enemy_type):
        self.path = path
        self.path_index = 0
        # Apply offset when initializing enemy position
        self.x, self.y = path[0][0] + BOARD_OFFSET_X, path[0][1] + BOARD_OFFSET_Y
        self.enemy_type = enemy_type
        self.progress = 0
        self.dead = False
        
        if enemy_type == "zergling":
            self.hp = ZERGLING_STATS["hp"]
            self.max_hp = ZERGLING_STATS["hp"]
            self.speed = ZERGLING_STATS["speed"]
            self.reward = ZERGLING_STATS["reward"]
            self.damage = ZERGLING_STATS["damage"]
            self.color = (150, 0, 0)
            self.image = zergling_img
            self.death_sound = zergling_death_sound
        elif enemy_type == "hydralisk":
            self.hp = HYDRALISK_STATS["hp"]
            self.max_hp = HYDRALISK_STATS["hp"]
            self.speed = HYDRALISK_STATS["speed"]
            self.reward = HYDRALISK_STATS["reward"]
            self.damage = HYDRALISK_STATS["damage"]
            self.color = (0, 150, 0)
            self.image = hydralisk_img
            self.death_sound = hydralisk_death_sound
        elif enemy_type == "ultralisk":
            self.hp = ULTRALISK_STATS["hp"]
            self.max_hp = ULTRALISK_STATS["hp"]
            self.speed = ULTRALISK_STATS["speed"]
            self.reward = ULTRALISK_STATS["reward"]
            self.damage = ULTRALISK_STATS["damage"]
            self.color = (150, 0, 150)
            self.image = ultralisk_img
            self.death_sound = ultralisk_death_sound
    
    def update(self):
        if self.path_index < len(self.path) - 1:
            # Calculate direction to next point (with offset)
            target_x = self.path[self.path_index + 1][0] + BOARD_OFFSET_X
            target_y = self.path[self.path_index + 1][1] + BOARD_OFFSET_Y
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
            # Play death sound
            self.death_sound.play()
            return False
        
        return False
    
    def draw(self, surface):
        # Draw enemy image
        img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, img_rect)
        
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
    (0, 75),  #
    (275, 75),      #
    (275, 225),     #
    (425, 225),              #
    (425, 325),              #
    (600, 325)                     #
]

# Create a function to draw the hatchery
def draw_hatchery(surface):
    # Hatchery position (at the start of the path)
    hatchery_x = path[0][0] + BOARD_OFFSET_X - 10  # Slightly before path start
    hatchery_y = path[0][1] + BOARD_OFFSET_Y
    
    # Base structure (circular mound)
    hatchery_radius = 30
    pygame.draw.circle(surface, (139, 69, 19), (hatchery_x, hatchery_y), hatchery_radius)  # Brown base
    
    # Creep (purple ground texture around the hatchery)
    creep_radius = hatchery_radius + 10
    pygame.draw.circle(surface, (128, 0, 128, 150), (hatchery_x, hatchery_y), creep_radius)
    
    # Main structure (dome)
    pygame.draw.circle(surface, (160, 32, 240), (hatchery_x, hatchery_y - 10), hatchery_radius - 10)  # Purple dome
    
    # Entrance (where zerg come out)
    entrance_width = 20
    entrance_height = 15
    pygame.draw.ellipse(surface, (0, 0, 0), 
                        (hatchery_x - entrance_width//2, 
                         hatchery_y - entrance_height//2 + 15, 
                         entrance_width, entrance_height))
    
    # Add some texture/details
    for i in range(3):
        angle = math.pi/4 + i * 2*math.pi/3
        spike_x = hatchery_x + int(math.cos(angle) * (hatchery_radius - 15))
        spike_y = hatchery_y + int(math.sin(angle) * (hatchery_radius - 15)) - 15
        spike_size = 7
        pygame.draw.circle(surface, (220, 20, 60), (spike_x, spike_y), spike_size)  # Red spikes

# Create a function to draw the command center
def draw_command_center(surface):
    # Command Center position (at the end of the path)
    cc_x = path[-1][0] + BOARD_OFFSET_X + 20  # Slightly after path end
    cc_y = path[-1][1] + BOARD_OFFSET_Y
    
    # Base structure (rectangular building)
    cc_width = 80
    cc_height = 60
    pygame.draw.rect(surface, (100, 100, 100), 
                    (cc_x - cc_width//2, cc_y - cc_height//2, 
                     cc_width, cc_height))
    
    # Main building (slightly smaller)
    pygame.draw.rect(surface, (180, 180, 180), 
                    (cc_x - cc_width//2 + 5, cc_y - cc_height//2 - 10, 
                     cc_width - 10, cc_height - 10))
    
    # Entrance (where SCVs would come out)
    entrance_width = 20
    entrance_height = 15
    pygame.draw.rect(surface, (50, 50, 50), 
                    (cc_x - entrance_width//2, 
                     cc_y + cc_height//2 - entrance_height - 5, 
                     entrance_width, entrance_height))
    
    # Add Terran logo/symbol
    logo_size = 15
    pygame.draw.circle(surface, (0, 0, 150), (cc_x, cc_y - 15), logo_size)
    pygame.draw.circle(surface, (180, 180, 180), (cc_x, cc_y - 15), logo_size - 3)
    pygame.draw.line(surface, (0, 0, 150), 
                    (cc_x - logo_size + 3, cc_y - 15), 
                    (cc_x + logo_size - 3, cc_y - 15), 3)
    
    # Add some windows/lights
    for i in range(4):
        window_x = cc_x - cc_width//3 + i * (cc_width//4)
        window_y = cc_y - cc_height//4
        window_size = 5
        pygame.draw.rect(surface, (255, 255, 150), 
                       (window_x - window_size//2, window_y - window_size//2, 
                        window_size, window_size))

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
    zergling_count = max(BASE_ZERGLING_COUNT, wave * ZERGLING_PER_WAVE)
    hydralisk_count = max(0, (wave - HYDRALISK_WAVE_START) * HYDRALISK_PER_WAVE)
    ultralisk_count = max(0, wave - ULTRALISK_WAVE_START)
    
    return zergling_count + hydralisk_count + ultralisk_count

def spawn_enemy():
    global remaining_zerg
    
    if remaining_zerg <= 0:
        return False
    
    # Determine enemy type based on wave and what's left
    if wave < 3:
        probs = WAVE_1_2_PROBS
    elif wave < 5:
        probs = WAVE_3_4_PROBS
    else:
        probs = WAVE_5_PLUS_PROBS
    
    r = random.random()
    cumulative = 0
    for enemy_type, prob in probs.items():
        cumulative += prob
        if r <= cumulative:
            enemies.append(Enemy(path, enemy_type))
            remaining_zerg -= 1
            return True
    
    return False

def start_wave_phase():
    global current_phase, phase_timer, remaining_zerg
    
    current_phase = PHASE_WAVE
    remaining_zerg = calculate_wave_size()
    phase_timer = max(MIN_WAVE_SPAWN_DELAY, WAVE_SPAWN_DELAY - wave * WAVE_SPAWN_DELAY_REDUCTION) * FPS
    
    # Play wave start sound
    wave_start_sound.play()

def start_build_phase():
    global current_phase, phase_timer, minerals, gas, wave
    
    current_phase = PHASE_BUILD
    phase_timer = max(MIN_BUILD_TIME, INITIAL_BUILD_TIME - wave * BUILD_TIME_REDUCTION) * FPS
    
    # Give resources for completing wave
    minerals += BASE_MINERAL_REWARD + wave * MINERAL_REWARD_PER_WAVE
    gas += BASE_GAS_REWARD + wave * GAS_REWARD_PER_WAVE
    
    # Increment wave counter
    wave += 1

def draw_map():
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            rect = pygame.Rect(x * TILE_SIZE + BOARD_OFFSET_X, y * TILE_SIZE + BOARD_OFFSET_Y, TILE_SIZE, TILE_SIZE)
            if game_map[y][x] == 1:  # Path
                pygame.draw.rect(screen, BROWN, rect)
            else:  # Buildable
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
    
    # Draw the hatchery at the start of the path
    draw_hatchery(screen)
    
    # Draw the command center at the end of the path
    draw_command_center(screen)

def draw_path():
    for i in range(len(path) - 1):
        # Apply offset to path points when drawing
        start_point = (path[i][0] + BOARD_OFFSET_X, path[i][1] + BOARD_OFFSET_Y)
        end_point = (path[i+1][0] + BOARD_OFFSET_X, path[i+1][1] + BOARD_OFFSET_Y)
        pygame.draw.line(screen, PURPLE, start_point, end_point, 3)

def draw_ui():
    # Draw resources
    mineral_text = game_font.render(f"Minerals: {minerals}", True, BLUE)
    gas_text = game_font.render(f"Gas: {gas}", True, GREEN)
    lives_text = game_font.render(f"Lives: {lives}", True, RED)
    wave_text = game_font.render(f"Wave: {wave}", True, WHITE)
    score_text = game_font.render(f"Score: {score}", True, BLACK)
    
    # Draw resources above tower buttons
    screen.blit(mineral_text, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 190))
    screen.blit(gas_text, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 160))
    
    # Draw wave and score at top right
    screen.blit(wave_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 40))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 70))
    
    # Draw phase information
    if current_phase == PHASE_BUILD:
        phase_text = game_font.render("BUILD PHASE", True, BLACK)
        timer_text = game_font.render(f"Next wave in: {phase_timer // FPS}s", True, BLACK)
    else:
        phase_text = game_font.render("WAVE PHASE", True, RED)
        timer_text = game_font.render(f"Remaining Zerg: {remaining_zerg + len(enemies)}", True, RED)
    
    screen.blit(phase_text, (SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 100))
    screen.blit(timer_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT - 80))
    
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
    firebat_text = small_font.render("Firebat", True, BLACK)
    firebat_cost = small_font.render("75 M", True, BLACK)
    firebat_cost2 = small_font.render("25 G", True, BLACK)
    screen.blit(firebat_text, (SCREEN_WIDTH - 135, SCREEN_HEIGHT - 125))
    screen.blit(firebat_cost, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 95))
    screen.blit(firebat_cost2, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 75))
    
    # Tank button
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 130, 60, 80))
    tank_text = small_font.render("Tank", True, BLACK)
    tank_cost = small_font.render("150 M", True, BLACK)
    tank_cost2 = small_font.render("75 G", True, BLACK)
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
        sell_text = small_font.render(f"Sell: {int(selected_tower.cost[0] * TOWER_SELL_MULTIPLIER * selected_tower.level)} M", True, BLACK)
        
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
    # Adjust for offset when converting to grid coordinates
    adjusted_x = x - BOARD_OFFSET_X
    adjusted_y = y - BOARD_OFFSET_Y
    
    # Snap coordinates to grid intersections
    grid_x = round(adjusted_x / TILE_SIZE) * TILE_SIZE + BOARD_OFFSET_X
    grid_y = round(adjusted_y / TILE_SIZE) * TILE_SIZE + BOARD_OFFSET_Y
    
    # Convert to map coordinates
    map_x = (grid_x - BOARD_OFFSET_X) // TILE_SIZE
    map_y = (grid_y - BOARD_OFFSET_Y) // TILE_SIZE
    
    # Check boundaries
    if map_x < 0 or map_x >= len(game_map[0]) or map_y < 0 or map_y >= len(game_map):
        return False
    
    # Check if position is already occupied by another tower
    for tower in towers:
        if abs(tower.x - grid_x) < TILE_SIZE/2 and abs(tower.y - grid_y) < TILE_SIZE/2:
            return False
    
    return True, grid_x, grid_y  # Return the snapped coordinates if valid

def reset_game():
    global minerals, gas, lives, score, wave, current_phase, phase_timer
    global remaining_zerg, towers, enemies, projectiles, selected_tower
    global spawn_cooldown, game_over, selected_tower_type
    
    # Reset player stats
    minerals = STARTING_MINERALS
    gas = STARTING_GAS
    lives = STARTING_LIVES
    score = 0
    wave = 1
    
    # Reset game state
    current_phase = PHASE_BUILD
    phase_timer = INITIAL_BUILD_TIME * FPS
    remaining_zerg = 0
    towers = []
    enemies = []
    projectiles = []  # Make sure projectiles list is cleared
    selected_tower = None
    spawn_cooldown = 0
    game_over = False
    selected_tower_type = "marine"

# Add debug function outside the main loop
def draw_debug_info():
    debug_text = game_font.render(f"Projectiles: {len(projectiles)}", True, WHITE)
    screen.blit(debug_text, (10, 10))

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
            elif event.key == pygame.K_r:  # Allow restart at any time
                reset_game()
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
                        selected_tower.damage = int(selected_tower.damage * DAMAGE_UPGRADE_MULTIPLIER)
                        selected_tower.range = int(selected_tower.range * RANGE_UPGRADE_MULTIPLIER)
                        selected_tower.fire_rate = max(MIN_FIRE_RATE, int(selected_tower.fire_rate * FIRE_RATE_UPGRADE_MULTIPLIER))
                        # Play upgrade sound
                        upgrade_sound.play()
                elif selected_tower and SCREEN_WIDTH - 80 <= mouse_x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 180 <= mouse_y <= SCREEN_HEIGHT - 150:
                    # Sell tower
                    minerals += int(selected_tower.cost[0] * TOWER_SELL_MULTIPLIER * selected_tower.level)
                    towers.remove(selected_tower)
                    selected_tower = None
                    # Play sell sound
                    sell_sound.play()
                else:
                    # Check if a tower is clicked
                    selected_tower = None
                    for tower in towers:
                        if math.sqrt((tower.x - mouse_x)**2 + (tower.y - mouse_y)**2) < 20:
                            selected_tower = tower
                            break
                    
                    # If no tower is clicked, try to place a new tower (only in build phase)
                    if selected_tower is None and current_phase == PHASE_BUILD:
                        placement = can_place_tower(mouse_x, mouse_y)
                        if placement:  # placement will be (True, grid_x, grid_y) if valid
                            _, grid_x, grid_y = placement
                            new_tower = Tower(grid_x, grid_y, selected_tower_type)
                            mineral_cost, gas_cost = new_tower.cost
                            
                            if minerals >= mineral_cost and gas >= gas_cost:
                                minerals -= mineral_cost
                                gas -= gas_cost
                                towers.append(new_tower)
                                # Play build sound
                                # build_sound.play()
    
    if game_over:
        # Display game over screen
        screen.fill(BLACK)
        game_over_text = game_font.render("GAME OVER", True, RED)
        score_text = game_font.render(f"Final Score: {score}", True, WHITE)
        restart_text = game_font.render("Press R to restart, ESC to quit", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50))
        
        # Play game over sound once
        if lives == 0:
            game_over_sound.play()
            lives = -1  # Set to -1 to prevent repeated sound playing
        
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
                new_projectile = tower.attack(enemies)
                if new_projectile:
                    projectiles.append(new_projectile)
            
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
        
        # Update projectiles
        for projectile in projectiles[:]:
            if not projectile.update():
                projectiles.remove(projectile)
    
    # Drawing
    screen.fill(WHITE)
    
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
    for projectile in projectiles:
        projectile.draw(screen)
    
    # Draw UI
    draw_ui()
    
    # Draw debug info
    # draw_debug_info()
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
