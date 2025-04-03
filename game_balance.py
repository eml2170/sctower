# Starting resources
STARTING_MINERALS = 150
STARTING_GAS = 25
STARTING_LIVES = 15

# Tower stats
MARINE_STATS = {
    "damage": 5,
    "range": 120,
    "fire_rate": 30,  # dps=0.16
    "cost": (50, 0),  # (minerals, gas)
}

FIREBAT_STATS = {
    "damage": 16,
    "range": 40,
    "fire_rate": 50,  # dps=0.32
    "cost": (75, 25),
}

TANK_STATS = {
    "damage": 40,
    "range": 180,
    "fire_rate": 90,  #dps=0.44
    "cost": (150, 75),
}

# Enemy stats
ZERGLING_STATS = {
    "hp": 20,
    "speed": 2,
    "reward": (6, 0),  # (minerals, gas)
    "damage": 2,
}

HYDRALISK_STATS = {
    "hp": 80,
    "speed": 1,
    "reward": (12, 4),
    "damage": 2,
}

ULTRALISK_STATS = {
    "hp": 300,
    "speed": 0.5,
    "reward": (25, 12),
    "damage": 5,
}

# Wave settings
WAVE_SPAWN_DELAY = 60  # Base delay between spawns
WAVE_SPAWN_DELAY_REDUCTION = 5  # How much to reduce delay per wave
MIN_WAVE_SPAWN_DELAY = 10  # Minimum delay between spawns

# Build phase settings
INITIAL_BUILD_TIME = 30  # Seconds
MIN_BUILD_TIME = 15  # Minimum seconds for build phase
BUILD_TIME_REDUCTION = 1  # How many seconds to reduce per wave

# Wave completion rewards
BASE_MINERAL_REWARD = 80
MINERAL_REWARD_PER_WAVE = 15
BASE_GAS_REWARD = 20
GAS_REWARD_PER_WAVE = 4

# Tower upgrade multipliers
DAMAGE_UPGRADE_MULTIPLIER = 1.5
RANGE_UPGRADE_MULTIPLIER = 1.2
FIRE_RATE_UPGRADE_MULTIPLIER = 0.8  # Reduction in fire rate (faster firing)
MIN_FIRE_RATE = 10
TOWER_SELL_MULTIPLIER = 0.7

# Enemy spawn probabilities for different waves
WAVE_1_2_PROBS = {
    "zergling": 1.0,
    "hydralisk": 0.0,
    "ultralisk": 0.0
}

WAVE_3_4_PROBS = {
    "zergling": 0.7,
    "hydralisk": 0.3,
    "ultralisk": 0.0
}

WAVE_5_PLUS_PROBS = {
    "zergling": 0.6,
    "hydralisk": 0.3,
    "ultralisk": 0.1
}

# Wave size calculations
BASE_ZERGLING_COUNT = 6
ZERGLING_PER_WAVE = 4
HYDRALISK_WAVE_START = 2  # Wave when hydralisks start appearing
HYDRALISK_PER_WAVE = 2
ULTRALISK_WAVE_START = 4  # Wave when ultralisks start appearing 