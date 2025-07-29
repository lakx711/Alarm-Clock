import pygame
import numpy as np
import os
import tempfile

def generate_default_alarm_sound():
    """
    Generate a simple beeping alarm sound using pygame.
    Returns the path to the generated sound file.
    """
    try:
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        
        # Generate a simple beeping sound
        sample_rate = 44100
        duration = 0.5  # 0.5 seconds per beep
        frequency = 800  # 800 Hz tone
        
        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Convert to 16-bit integer
        tone = (tone * 32767).astype(np.int16)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        # Save as WAV file using scipy
        try:
            import scipy.io.wavfile as wavfile
            wavfile.write(temp_path, sample_rate, tone)
        except ImportError:
            # Fallback: create a simple beep using pygame
            import wave
            import struct
            
            with wave.open(temp_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(tone.tobytes())
        
        return temp_path
        
    except Exception as e:
        print(f"Error generating default sound: {e}")
        return None

def cleanup_temp_sound(sound_path):
    """
    Clean up temporary sound file.
    """
    try:
        if sound_path and os.path.exists(sound_path):
            os.unlink(sound_path)
    except Exception as e:
        print(f"Error cleaning up sound file: {e}")

if __name__ == "__main__":
    # Test sound generation
    sound_path = generate_default_alarm_sound()
    if sound_path:
        print(f"Generated sound file: {sound_path}")
        
        # Play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        pygame.time.wait(2000)
        
        # Clean up
        cleanup_temp_sound(sound_path)
        print("Sound test completed.")
    else:
        print("Failed to generate sound.") 