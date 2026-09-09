"""Shared helpers for loading/scaling images. Used by every scene and popup."""

import pygame

import config


def load_img(path, size=None):
    """Load an image (with alpha) from config.IMG_DIR; smoothscale to (w, h) if size given."""
    img = pygame.image.load(config.IMG_DIR + path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img


def load_bg(path, size):
    """Load an opaque background image from config.IMG_DIR and scale it to (w, h)."""
    img = pygame.image.load(config.IMG_DIR + path).convert()
    return pygame.transform.smoothscale(img, size)


def btn_size(target_w):
    """Given a desired pixel width, return (w, h) preserving the button canvas's aspect ratio."""
    return (int(target_w), int(target_w / config.BTN_ASPECT))
