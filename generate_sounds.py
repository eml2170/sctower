import wave
import struct
import math
import os
import random

# Create the sounds directory if it doesn't exist
sounds_dir = "assets/sounds"
os.makedirs(sounds_dir, exist_ok=True)

def generate_tone(filename, frequency=440, duration=0.5, volume=0.5, sample_rate=44100):
    """Generate a simple sine wave tone"""
    filepath = os.path.join(sounds_dir, filename)
    
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes (16 bits) per sample
        wav.setframerate(sample_rate)
        
        # Generate frames
        for i in range(num_frames):
            t = float(i) / sample_rate
            value = int(volume * 32767.0 * math.sin(2 * math.pi * frequency * t))
            data = struct.pack('<h', value)
            wav.writeframes(data)
    
    print(f"Generated {filepath}")

def generate_noise(filename, duration=0.3, volume=0.5, sample_rate=44100):
    """Generate white noise"""
    filepath = os.path.join(sounds_dir, filename)
    
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes (16 bits) per sample
        wav.setframerate(sample_rate)
        
        # Generate frames
        for i in range(num_frames):
            value = int(volume * 32767.0 * (random.random() * 2 - 1))
            data = struct.pack('<h', value)
            wav.writeframes(data)
    
    print(f"Generated {filepath}")

def generate_attack_sound(filename, base_freq=880, duration=0.1, volume=0.4):
    """Generate a quick attack sound"""
    filepath = os.path.join(sounds_dir, filename)
    sample_rate = 44100
    num_frames = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes per sample
        wav.setframerate(sample_rate)
        
        for i in range(num_frames):
            t = float(i) / sample_rate
            # Frequency drop over time
            freq = base_freq * (1.0 - t/duration * 0.5)
            # Volume decay
            vol = volume * (1.0 - t/duration)
            value = int(vol * 32767.0 * math.sin(2 * math.pi * freq * t))
            data = struct.pack('<h', value)
            wav.writeframes(data)
    
    print(f"Generated {filepath}")

def generate_explosion(filename, duration=0.4, volume=0.7):
    """Generate an explosion-like sound"""
    filepath = os.path.join(sounds_dir, filename)
    sample_rate = 44100
    num_frames = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes per sample
        wav.setframerate(sample_rate)
        
        for i in range(num_frames):
            t = float(i) / sample_rate
            # Volume decay
            vol = volume * (1.0 - t/duration)
            # Random noise with some low-frequency components
            noise = random.random() * 2 - 1
            low_freq = math.sin(2 * math.pi * 60 * t) * 0.5
            value = int(vol * 32767.0 * (noise * 0.7 + low_freq * 0.3))
            data = struct.pack('<h', value)
            wav.writeframes(data)
    
    print(f"Generated {filepath}")

# Generate game sounds
generate_tone("build.wav", frequency=440, duration=0.3, volume=0.4)
generate_tone("upgrade.wav", frequency=660, duration=0.4, volume=0.4)
generate_tone("sell.wav", frequency=330, duration=0.3, volume=0.3)

# Unit attack sounds
generate_attack_sound("marine_attack.wav", base_freq=880, duration=0.1, volume=0.3)
generate_attack_sound("firebat_attack.wav", base_freq=440, duration=0.3, volume=0.5)
generate_attack_sound("tank_attack.wav", base_freq=220, duration=0.4, volume=0.7)

# Death sounds
generate_explosion("zergling_death.wav", duration=0.2, volume=0.4)
generate_explosion("hydralisk_death.wav", duration=0.3, volume=0.5)
generate_explosion("ultralisk_death.wav", duration=0.4, volume=0.6)

# Game state sounds
generate_tone("wave_start.wav", frequency=550, duration=0.5, volume=0.5)
generate_tone("game_over.wav", frequency=220, duration=1.0, volume=0.7)

print("All sound effects generated successfully!") 