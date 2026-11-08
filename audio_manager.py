"""Procedural background music and shared sound-effect volume control."""

from array import array
import math
import sys

import pygame


_music_sound = None
_music_channel = None
_sound_volume = 0.7
_music_volume = 0.25


def _make_music(sample_rate, channels):
    notes = (
        261.63, 329.63, 392.00, 329.63,
        293.66, 349.23, 440.00, 349.23,
        261.63, 329.63, 392.00, 523.25,
        440.00, 392.00, 349.23, 293.66,
    )
    note_samples = sample_rate // 2
    samples = array("h")
    for note in notes:
        for index in range(note_samples):
            phase = index / sample_rate
            envelope = min(1.0, index / (sample_rate * 0.025),
                           (note_samples - index) / (sample_rate * 0.06))
            tone = math.sin(2 * math.pi * note * phase)
            tone += 0.22 * math.sin(2 * math.pi * note * 2 * phase)
            value = int(6000 * max(0.0, envelope) * tone)
            samples.extend([value] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())


def start_music(settings):
    global _music_sound, _music_channel
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            return
        sample_rate, _, channels = mixer_info
        _music_sound = _make_music(sample_rate, channels)
        _music_channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        _music_channel.play(_music_sound, loops=-1)
        apply_settings(settings)
    except pygame.error as exc:
        print(f"[audio] Background music is unavailable: {exc}", file=sys.stderr)


def apply_settings(settings):
    global _sound_volume, _music_volume
    _sound_volume = max(0.0, min(1.0, float(settings.get("sound_volume", 0.7))))
    _music_volume = max(0.0, min(1.0, float(settings.get("music_volume", 0.25))))
    if _music_channel is not None:
        _music_channel.set_volume(_music_volume)


def play_effect(sound):
    if sound is not None:
        sound.set_volume(_sound_volume)
        sound.play()
