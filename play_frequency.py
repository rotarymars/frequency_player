#!/usr/bin/env python3
"""
Simple script to play specific frequency sounds.
Usage:
  Single frequency: python play_frequency.py [frequency_hz] [duration_seconds]
  Multiple frequencies: python play_frequency.py freq1,freq2,freq3 [duration_seconds]

Examples:
  python play_frequency.py 440          # Play A4 note
  python play_frequency.py 440,554,659  # Play A major chord
"""

import numpy as np
import sounddevice as sd
import sys


def play_frequency(frequency=440, duration=2.0, sample_rate=44100, amplitude=0.3):
    """
    Play a pure tone at the specified frequency.

    Args:
        frequency: Frequency in Hz (default: 440 Hz, which is A4 note)
        duration: Duration in seconds (default: 2.0)
        sample_rate: Sample rate in Hz (default: 44100)
        amplitude: Volume level between 0.0 and 1.0 (default: 0.3)
    """
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Generate sine wave
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    wave *= 10

    # Play the sound
    print(f"Playing {frequency} Hz for {duration} seconds...")
    sd.play(wave, sample_rate)
    sd.wait()  # Wait until sound finishes playing
    print("Done!")


def play_multiple_frequencies(frequencies, duration=2.0, sample_rate=44100, amplitude=0.3):
    """
    Play multiple frequencies simultaneously by mixing sine waves.

    Args:
        frequencies: List of frequencies in Hz
        duration: Duration in seconds (default: 2.0)
        sample_rate: Sample rate in Hz (default: 44100)
        amplitude: Volume level between 0.0 and 1.0 (default: 0.3)
    """
    if not frequencies:
        print("Error: No frequencies provided")
        return

    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Mix all frequencies together
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += np.sin(2 * np.pi * freq * t)

    # Normalize to prevent clipping (divide by number of frequencies)
    wave = wave / len(frequencies)

    # Apply amplitude
    wave = amplitude * wave

    # Play the sound
    freq_str = ", ".join([f"{f} Hz" for f in frequencies])
    print(f"Playing {len(frequencies)} frequencies simultaneously: {freq_str}")
    print(f"Duration: {duration} seconds")
    sd.play(wave, sample_rate)
    sd.wait()  # Wait until sound finishes playing
    print("Done!")


if __name__ == "__main__":
    # Default values
    frequencies = [440]  # A4 note
    dur = 2.0   # 2 seconds

    # Parse command line arguments
    if len(sys.argv) > 1:
        freq_input = sys.argv[1]

        # Check if input contains comma (multiple frequencies)
        if ',' in freq_input:
            try:
                frequencies = [float(f.strip()) for f in freq_input.split(',')]
            except ValueError:
                print(f"Invalid frequency list: {freq_input}")
                print("Format: freq1,freq2,freq3 (e.g., 440,554,659)")
                sys.exit(1)
        else:
            # Single frequency
            try:
                frequencies = [float(freq_input)]
            except ValueError:
                print(f"Invalid frequency: {freq_input}")
                sys.exit(1)

    if len(sys.argv) > 2:
        try:
            dur = float(sys.argv[2])
        except ValueError:
            print(f"Invalid duration: {sys.argv[2]}")
            sys.exit(1)

    # Play the frequency or frequencies
    if len(frequencies) == 1:
        play_frequency(frequency=frequencies[0], duration=dur)
    else:
        play_multiple_frequencies(frequencies=frequencies, duration=dur)
