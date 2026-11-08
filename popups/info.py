import pygame

from cardscan import registry
from popups import base


WIDTH = HEIGHT = 0
_close_popup = None
panel_rect = None
close_btn_rect = None
_tabs = {}
_previous_rect = None
_next_rect = None
_section = "guide"
_page = 0

_GUIDE = (
    "Choose Play, then select a chapter from the farm map.",
    "Read the story and tap to continue. On choice scenes, select an answer.",
    "For action challenges, follow the card prompt and choose the matching action.",
    "Care meters appear when a chapter first needs that kind of plant care.",
    "Finish a chapter to save your progress, then choose whether to record your score.",
    "Open the Card Scan Tester from the main menu to preview a camera and test cards.",
)


def init(width, height, close_popup_callback):
    global WIDTH, HEIGHT, _close_popup, panel_rect, close_btn_rect
    global _tabs, _previous_rect, _next_rect
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    panel_rect = base.make_panel_rect(WIDTH, HEIGHT, w_pct=0.86, h_pct=0.84)
    close_btn_rect = base.make_close_rect(panel_rect, WIDTH, HEIGHT)
    tab_gap = max(8, int(panel_rect.width * 0.012))
    tab_width = (panel_rect.width - tab_gap * 2) // 3
    tab_height = max(38, int(HEIGHT * 0.065))
    tab_y = panel_rect.top + int(HEIGHT * 0.105)
    _tabs = {
        key: pygame.Rect(
            panel_rect.left + index * (tab_width + tab_gap),
            tab_y,
            tab_width,
            tab_height,
        )
        for index, key in enumerate(("guide", "cards", "crops"))
    }
    button_size = max(42, int(HEIGHT * 0.065))
    page_gap = max(10, int(HEIGHT * 0.025))
    page_label_width = max(64, int(WIDTH * 0.075))
    bottom = panel_rect.bottom - int(HEIGHT * 0.035)
    button_y = bottom - button_size
    _previous_rect = pygame.Rect(
        panel_rect.centerx - page_label_width // 2 - page_gap - button_size,
        button_y,
        button_size,
        button_size,
    )
    _next_rect = pygame.Rect(
        panel_rect.centerx + page_label_width // 2 + page_gap,
        button_y,
        button_size,
        button_size,
    )


def _items(section):
    if section == "guide":
        return list(_GUIDE)
    if section == "cards":
        return [card for card in registry.CARDS if not card.details.get("days")]
    return [card for card in registry.CARDS if card.details.get("days")]


def _page_size():
    return 2 if HEIGHT < 600 else 4


def handle_tap(px, py):
    global _section, _page
    if close_btn_rect.collidepoint(px, py):
        _close_popup()
        return
    if not panel_rect.collidepoint(px, py):
        _close_popup()
        return
    for section, rect in _tabs.items():
        if rect.collidepoint(px, py):
            _section = section
            _page = 0
            return
    if _previous_rect.collidepoint(px, py):
        _page = max(0, _page - 1)
    elif _next_rect.collidepoint(px, py):
        size = _page_size()
        page_count = max(1, (len(_items(_section)) + size - 1) // size)
        _page = min(page_count - 1, _page + 1)


def _wrap_lines(font, text, max_width):
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(surf, font, text, color, x, y, max_width, line_gap):
    for line in _wrap_lines(font, text, max_width):
        surf.blit(font.render(line, True, color), (x, y))
        y += line_gap
    return y


def _item_text(section, item):
    if section == "guide":
        return item
    details = item.details
    if section == "cards":
        effect = details.get("effect", "Use when the story asks for this kind of action.")
        when = details.get("when_to_use", "")
        return f"{item.display}: {effect} {when}".strip()
    crop_name = details.get("english", item.name)
    local_name = details.get("filipino", "")
    tip = details.get("tip", "")
    care = (
        f"Water {details.get('water', '?')}, fertilizer {details.get('fertilizer', '?')}, "
        f"weeds {details.get('weeds', '?')}, pests {details.get('pests', '?')}."
    )
    return (
        f"{crop_name} ({local_name}) — about {details.get('days', '?')} days; "
        f"season: {details.get('season', 'varies')}. {care} {tip}"
    )


def _draw_tab(surf, rect, label, active):
    fill = (79, 119, 62) if active else (65, 64, 51)
    pygame.draw.rect(surf, fill, rect, border_radius=10)
    pygame.draw.rect(surf, (226, 205, 157), rect, width=2, border_radius=10)
    font = pygame.font.SysFont(None, max(17, int(HEIGHT * 0.029)))
    text = font.render(label, True, (255, 246, 220))
    surf.blit(text, text.get_rect(center=rect.center))


def _draw_content(surf):
    items = _items(_section)
    page_size = _page_size()
    page_count = max(1, (len(items) + page_size - 1) // page_size)
    page = min(_page, page_count - 1)
    first = page * page_size
    font_size = max(17, int(HEIGHT * (0.03 if _section == "guide" else 0.026)))
    body_font = pygame.font.SysFont(None, font_size)
    line_gap = max(21, int(HEIGHT * 0.034))
    x = panel_rect.left + int(panel_rect.width * 0.075)
    y = _tabs["guide"].bottom + int(HEIGHT * 0.055)
    max_width = int(panel_rect.width * 0.85)
    item_gap = max(18, int(HEIGHT * 0.025))
    visible = items[first:first + page_size]
    for index, item in enumerate(visible, first + 1):
        text = f"{index}. {item}" if _section == "guide" else _item_text(_section, item)
        y = _draw_wrapped(surf, body_font, text, (237, 231, 211), x, y,
                          max_width, line_gap)
        y += item_gap

    nav_font = pygame.font.SysFont(None, max(18, int(HEIGHT * 0.03)))
    pygame.draw.rect(surf, (79, 119, 62), _previous_rect, border_radius=8)
    pygame.draw.rect(surf, (79, 119, 62), _next_rect, border_radius=8)
    previous_label = nav_font.render("<", True, (255, 246, 220))
    surf.blit(previous_label, previous_label.get_rect(center=_previous_rect.center))
    next_label = nav_font.render(">", True, (255, 246, 220))
    surf.blit(next_label, next_label.get_rect(center=_next_rect.center))
    page_text = nav_font.render(f"{page + 1} / {page_count}", True, (235, 225, 200))
    surf.blit(page_text, page_text.get_rect(center=(panel_rect.centerx, _previous_rect.centery)))


def draw(surf):
    base.draw_overlay(surf, WIDTH, HEIGHT)
    base.draw_panel_frame(surf, panel_rect, "Farm Guide",
                          title_font_size=max(30, int(HEIGHT * 0.05)))
    for section, label in (("guide", "How to play"), ("cards", "Action cards"),
                           ("crops", "Crops")):
        _draw_tab(surf, _tabs[section], label, _section == section)
    _draw_content(surf)
    base.draw_close_button(surf, close_btn_rect)
