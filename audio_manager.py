"""Procedural background music and shared sound-effect volume control."""

from array import array
import math
import sys

import pygame


_music_sound = None
_music_channel = None
_music_sounds = {}
_music_context = None
_desired_context = "menu"
_sound_volume = 0.7
_music_volume = 0.25


_TRACKS = {
    "menu": (
        (261.63, 329.63, 392.00, 329.63, 293.66, 349.23, 440.00, 349.23,
         261.63, 329.63, 392.00, 523.25, 440.00, 392.00, 349.23, 293.66),
        0.44,
    ),
    "chapter": (
        (293.66, 349.23, 392.00, 349.23, 261.63, 293.66, 349.23, 440.00,
         392.00, 349.23, 293.66, 261.63, 220.00, 261.63, 293.66, 349.23),
        0.58,
    ),
    "minigame": (
        (392.00, 493.88, 587.33, 493.88, 440.00, 523.25, 659.25, 523.25,
         392.00, 493.88, 587.33, 783.99, 659.25, 587.33, 523.25, 493.88),
        0.30,
    ),
}


def _make_music(sample_rate, channels, notes, beat_seconds):
    note_samples = max(1, int(sample_rate * beat_seconds))
    samples = array("h")
    for note_index, note in enumerate(notes):
        for index in range(note_samples):
            phase = index / sample_rate
            attack = min(1.0, index / (sample_rate * 0.035))
            release = min(
                1.0,
                (note_samples - index) / (sample_rate * 0.08),
            )
            envelope = max(0.0, min(attack, release))
            melody = math.sin(2 * math.pi * note * phase)
            overtone = math.sin(2 * math.pi * note * 2 * phase)
            bass = math.sin(2 * math.pi * notes[(note_index // 4) % len(notes)] * 0.5 * phase)
            tone = 0.68 * melody + 0.18 * overtone + 0.14 * bass
            value = int(5200 * envelope * tone)
            samples.extend([value] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())


def start_music(settings, context=None):
    global _music_sound, _music_channel, _music_sounds, _music_context
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            return
        sample_rate, _, channels = mixer_info
        context = context or _desired_context
        _music_sounds = {
            name: _make_music(sample_rate, channels, notes, beat_seconds)
            for name, (notes, beat_seconds) in _TRACKS.items()
        }
        _music_channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        _music_context = None
        apply_settings(settings)
        set_context(context)
    except pygame.error as exc:
        print(f"[audio] Background music is unavailable: {exc}", file=sys.stderr)


def apply_settings(settings):
    global _sound_volume, _music_volume
    _sound_volume = max(0.0, min(1.0, float(settings.get("sound_volume", 0.7))))
    _music_volume = max(0.0, min(1.0, float(settings.get("music_volume", 0.25))))
    if _music_channel is not None:
        _music_channel.set_volume(_music_volume)


def set_context(context):
    global _music_sound, _music_context, _desired_context
    if context not in _TRACKS:
        raise ValueError(f"Unknown music context: {context!r}")
    _desired_context = context
    if _music_channel is None or _music_context == context:
        return
    _music_sound = _music_sounds[context]
    _music_channel.play(_music_sound, loops=-1, fade_ms=350)
    _music_context = context


def play_effect(sound):
    if sound is not None:
        sound.set_volume(_sound_volume)
        sound.play()
