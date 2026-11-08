import pygame

import audio_manager
from cardscan.camera import CameraError, open_camera
from popups import base
import player_data


WIDTH = HEIGHT = 0
_close_popup = None
_display_change = None
panel_rect = None
close_btn_rect = None
_slider_rects = {}
_display_rect = None
_camera_minus_rect = None
_camera_plus_rect = None
_camera_preview_rect = None
_camera_retry_rect = None
_camera = None
_camera_error = ""
_drag_control = None
_status = ""
_settings_values = {}


def init(width, height, close_popup_callback):
    global WIDTH, HEIGHT, _close_popup, panel_rect, close_btn_rect
    global _slider_rects, _display_rect, _camera_minus_rect, _camera_plus_rect
    global _settings_values, _camera_preview_rect, _camera_retry_rect
    close()
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    _settings_values = player_data.get_settings()
    panel_rect = base.make_panel_rect(WIDTH, HEIGHT, w_pct=0.84, h_pct=0.82)
    close_btn_rect = base.make_close_rect(panel_rect, WIDTH, HEIGHT)
    track_x = panel_rect.left + int(panel_rect.width * 0.39)
    track_w = int(panel_rect.width * 0.37)
    track_h = max(18, int(HEIGHT * 0.03))
    _slider_rects = {
        "sound_volume": pygame.Rect(track_x, panel_rect.top + int(panel_rect.height * 0.18),
                                    track_w, track_h),
        "music_volume": pygame.Rect(track_x, panel_rect.top + int(panel_rect.height * 0.30),
                                    track_w, track_h),
    }
    button_h = max(42, int(HEIGHT * 0.07))
    button_w = int(panel_rect.width * 0.40)
    _display_rect = pygame.Rect(0, 0, button_w, button_h)
    _display_rect.center = (panel_rect.centerx,
                            panel_rect.top + int(panel_rect.height * 0.43))
    camera_y = panel_rect.top + int(panel_rect.height * 0.54)
    small_w = max(44, int(HEIGHT * 0.065))
    _camera_minus_rect = pygame.Rect(
        panel_rect.centerx - int(panel_rect.width * 0.24) - small_w // 2,
        camera_y,
        small_w,
        button_h,
    )
    _camera_plus_rect = pygame.Rect(
        panel_rect.centerx + int(panel_rect.width * 0.24) - small_w // 2,
        camera_y,
        small_w,
        button_h,
    )
    preview_width = int(panel_rect.width * 0.48)
    preview_height = int(panel_rect.height * 0.24)
    _camera_preview_rect = pygame.Rect(
        panel_rect.centerx - preview_width // 2,
        panel_rect.top + int(panel_rect.height * 0.72),
        preview_width,
        preview_height,
    )
    retry_w = min(int(_camera_preview_rect.width * 0.6), max(112, int(WIDTH * 0.15)))
    retry_h = max(34, int(HEIGHT * 0.055))
    _camera_retry_rect = pygame.Rect(0, 0, retry_w, retry_h)
    _camera_retry_rect.center = (
        _camera_preview_rect.centerx,
        _camera_preview_rect.centery,
    )


def open():
    """Open the selected camera for the live Settings preview."""
    global _camera, _camera_error
    close()
    try:
        _camera = open_camera(
            kind="opencv",
            device=_settings_values["camera_device"],
        )
        _camera_error = ""
    except CameraError as exc:
        _camera = None
        _camera_error = str(exc)


def close():
    global _camera
    if _camera is not None:
        _camera.release()
        _camera = None


def _select_camera(step):
    device = max(0, min(9, _settings_values["camera_device"] + step))
    if device == _settings_values["camera_device"]:
        return
    _save_settings(camera_device=device)
    open()


def set_display_callback(callback):
    global _display_change
    _display_change = callback


def _save_settings(**changes):
    global _status, _settings_values
    _settings_values.update(changes)
    saved = player_data.update_settings(**changes)
    audio_manager.apply_settings(player_data.get_settings())
    _status = "Settings saved." if saved else player_data.last_error()


def _set_slider_value(name, px):
    global _status
    rect = _slider_rects[name]
    ratio = max(0.0, min(1.0, (px - rect.left) / rect.width))
    _settings_values[name] = round(ratio, 2)
    audio_manager.apply_settings(_settings_values)
    _status = "Release to save volume."


def handle_tap(px, py):
    global _drag_control
    if close_btn_rect.collidepoint(px, py):
        _close_popup()
        return
    if _camera_retry_rect.collidepoint(px, py) and _camera is None:
        open()
        return
    if not panel_rect.collidepoint(px, py):
        _close_popup()
        return

    for name, rect in _slider_rects.items():
        hit = rect.inflate(0, max(24, int(HEIGHT * 0.04)))
        if hit.collidepoint(px, py):
            _drag_control = name
            _set_slider_value(name, px)
            return

    if _display_rect.collidepoint(px, py):
        fullscreen = not player_data.get_settings()["fullscreen"]
        _save_settings(fullscreen=fullscreen)
        if _display_change is not None:
            _display_change(fullscreen)
        return
    if _camera_minus_rect.collidepoint(px, py):
        _select_camera(-1)
    elif _camera_plus_rect.collidepoint(px, py):
        _select_camera(1)


def handle_drag(px, py):
    if _drag_control is not None:
        _set_slider_value(_drag_control, px)


def handle_release(_px, _py):
    global _drag_control
    if _drag_control is not None:
        _save_settings(**{_drag_control: _settings_values[_drag_control]})
    _drag_control = None


def _font(size):
    return pygame.font.SysFont(None, max(17, size))


def _draw_slider(surf, label, name, value):
    track = _slider_rects[name]
    label_font = _font(max(19, int(HEIGHT * 0.035)))
    small_font = _font(max(16, int(HEIGHT * 0.027)))
    title = label_font.render(label, True, (242, 231, 205))
    surf.blit(title, (panel_rect.left + int(panel_rect.width * 0.08),
                      track.centery - title.get_height() // 2))
    pygame.draw.rect(surf, (56, 58, 49), track, border_radius=track.height // 2)
    fill = track.copy()
    fill.width = int(track.width * value)
    if fill.width:
        pygame.draw.rect(surf, (118, 167, 83), fill, border_radius=track.height // 2)
    knob_x = track.left + int(track.width * value)
    pygame.draw.circle(surf, (255, 239, 190), (knob_x, track.centery), track.height)
    pygame.draw.circle(surf, (97, 82, 55), (knob_x, track.centery), track.height, 2)
    value_label = small_font.render(f"{round(value * 100)}%", True, (225, 215, 187))
    surf.blit(value_label, value_label.get_rect(
        midright=(panel_rect.right - int(panel_rect.width * 0.07), track.centery)
    ))


def _draw_button(surf, rect, label):
    pygame.draw.rect(surf, (79, 119, 62), rect, border_radius=10)
    pygame.draw.rect(surf, (226, 205, 157), rect, width=2, border_radius=10)
    text = _font(max(18, int(HEIGHT * 0.031))).render(label, True, (255, 246, 220))
    surf.blit(text, text.get_rect(center=rect.center))


def _draw_camera_preview(surf):
    global _camera, _camera_error, _camera_retry_rect
    pygame.draw.rect(surf, (8, 12, 12), _camera_preview_rect, border_radius=8)
    pygame.draw.rect(surf, (116, 131, 105), _camera_preview_rect, width=2, border_radius=8)
    try:
        frame = _camera.read() if _camera is not None else None
    except CameraError as exc:
        _camera_error = str(exc)
        close()
        frame = None
    if frame is not None:
        scale = min(
            (_camera_preview_rect.width - 8) / frame.get_width(),
            (_camera_preview_rect.height - 8) / frame.get_height(),
        )
        size = (
            max(1, int(frame.get_width() * scale)),
            max(1, int(frame.get_height() * scale)),
        )
        image = pygame.transform.smoothscale(frame, size)
        surf.blit(image, image.get_rect(center=_camera_preview_rect.center))
        label = "Live camera preview"
        color = (220, 236, 208)
    else:
        label = (
            f"Camera unavailable: {_camera_error}"
            if _camera_error
            else "No camera frame received"
        )
        color = (247, 185, 140)
    text = _font(max(15, int(HEIGHT * 0.023))).render(label, True, color)
    max_width = _camera_preview_rect.width - 20
    if text.get_width() > max_width:
        new_height = max(1, int(text.get_height() * max_width / text.get_width()))
        text = pygame.transform.smoothscale(text, (max_width, new_height))
    text_rect = text.get_rect(midbottom=(
        _camera_preview_rect.centerx,
        _camera_preview_rect.bottom - 8,
    ))
    backdrop = text_rect.inflate(12, 8)
    pygame.draw.rect(surf, (20, 28, 22), backdrop, border_radius=6)
    surf.blit(text, text_rect)
    if frame is None:
        pygame.draw.rect(surf, (55, 107, 70), _camera_retry_rect, border_radius=8)
        pygame.draw.rect(surf, (210, 220, 205), _camera_retry_rect, width=2, border_radius=8)
        retry = _font(max(15, int(HEIGHT * 0.022))).render(
            "Retry camera", True, (245, 245, 230)
        )
        surf.blit(retry, retry.get_rect(center=_camera_retry_rect.center))


def draw(surf):
    settings = _settings_values
    base.draw_overlay(surf, WIDTH, HEIGHT)
    base.draw_panel_frame(surf, panel_rect, "Settings",
                          title_font_size=max(30, int(HEIGHT * 0.05)))
    _draw_slider(surf, "Sound effects", "sound_volume", settings["sound_volume"])
    _draw_slider(surf, "Background music", "music_volume", settings["music_volume"])

    display_label = "Display: Fullscreen" if settings["fullscreen"] else "Display: Windowed"
    _draw_button(surf, _display_rect, display_label)

    _draw_button(surf, _camera_minus_rect, "-")
    _draw_button(surf, _camera_plus_rect, "+")
    camera_label = _font(max(18, int(HEIGHT * 0.031))).render(
        f"Camera {settings['camera_device']}", True, (242, 231, 205)
    )
    camera_label_rect = camera_label.get_rect(center=(
        panel_rect.centerx, _camera_minus_rect.centery
    ))
    surf.blit(camera_label, camera_label_rect)
    _draw_camera_preview(surf)
    if _status:
        status = _font(max(14, int(HEIGHT * 0.021))).render(_status, True, (238, 210, 150))
        status_rect = status.get_rect(midtop=(
            panel_rect.centerx,
            _camera_minus_rect.bottom + int(HEIGHT * 0.012),
        ))
        if status_rect.bottom < _camera_preview_rect.top:
            surf.blit(status, status_rect)
    base.draw_close_button(surf, close_btn_rect)
