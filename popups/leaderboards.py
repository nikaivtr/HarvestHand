import pygame

import data.chapters as chapters_data
from popups import base
import player_data


WIDTH = HEIGHT = 0
_close_popup = None
panel_rect = None
close_btn_rect = None
_chapter_tab = None
_minigame_tab = None
_previous_rect = None
_next_rect = None
_tab = "chapters"
_page = 0
_PAGE_SIZE = 5


def init(width, height, close_popup_callback):
    global WIDTH, HEIGHT, _close_popup, panel_rect, close_btn_rect
    global _chapter_tab, _minigame_tab, _previous_rect, _next_rect
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    panel_rect = base.make_panel_rect(WIDTH, HEIGHT, w_pct=0.86, h_pct=0.84)
    close_btn_rect = base.make_close_rect(panel_rect, WIDTH, HEIGHT)
    tab_width = int(panel_rect.width * 0.34)
    tab_height = max(38, int(HEIGHT * 0.065))
    tab_y = panel_rect.top + int(HEIGHT * 0.105)
    _chapter_tab = pygame.Rect(0, tab_y, tab_width, tab_height)
    _chapter_tab.centerx = panel_rect.centerx - tab_width // 2
    _minigame_tab = pygame.Rect(0, tab_y, tab_width, tab_height)
    _minigame_tab.centerx = panel_rect.centerx + tab_width // 2
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


def handle_tap(px, py):
    global _tab, _page
    if close_btn_rect.collidepoint(px, py):
        _close_popup()
        return
    if not panel_rect.collidepoint(px, py):
        _close_popup()
        return
    if _chapter_tab.collidepoint(px, py):
        _tab = "chapters"
        _page = 0
    elif _minigame_tab.collidepoint(px, py):
        _tab = "minigames"
        _page = 0
    elif _previous_rect.collidepoint(px, py):
        _page = max(0, _page - 1)
    elif _next_rect.collidepoint(px, py):
        count = (
            len(player_data.chapter_rankings())
            if _tab == "chapters"
            else len(player_data.minigame_rankings())
        )
        page_count = max(1, (count + _PAGE_SIZE - 1) // _PAGE_SIZE)
        _page = min(page_count - 1, _page + 1)


def _chapter_title(chapter_id):
    try:
        chapter = chapters_data.load(chapter_id)
    except (ImportError, AttributeError, KeyError, ValueError):
        return chapter_id.replace("_", " ").title()
    chapter_number = chapters_data.CHAPTER_IDS.index(chapter_id) + 1
    return f"Chapter {chapter_number}: {chapter.get('crop', 'Farm')}"


def _draw_tab(surf, rect, label, active):
    fill = (79, 119, 62) if active else (65, 64, 51)
    pygame.draw.rect(surf, fill, rect, border_radius=10)
    pygame.draw.rect(surf, (226, 205, 157), rect, width=2, border_radius=10)
    font = pygame.font.SysFont(None, max(18, int(HEIGHT * 0.031)))
    text = font.render(label, True, (255, 246, 220))
    surf.blit(text, text.get_rect(center=rect.center))


def _draw_pagination(surf, count):
    pages = max(1, (count + _PAGE_SIZE - 1) // _PAGE_SIZE)
    page = min(_page, pages - 1)
    font = pygame.font.SysFont(None, max(18, int(HEIGHT * 0.03)))
    previous = font.render("<", True, (255, 246, 220))
    next_page = font.render(">", True, (255, 246, 220))
    pygame.draw.rect(surf, (79, 119, 62), _previous_rect, border_radius=8)
    pygame.draw.rect(surf, (79, 119, 62), _next_rect, border_radius=8)
    surf.blit(previous, previous.get_rect(center=_previous_rect.center))
    surf.blit(next_page, next_page.get_rect(center=_next_rect.center))
    label = font.render(f"{page + 1} / {pages}", True, (235, 225, 200))
    surf.blit(label, label.get_rect(center=(panel_rect.centerx, _previous_rect.centery)))
    return page


def _draw_empty(surf, message):
    font = pygame.font.SysFont(None, max(20, int(HEIGHT * 0.035)))
    text = font.render(message, True, (230, 230, 220))
    surf.blit(text, text.get_rect(center=(panel_rect.centerx, panel_rect.centery)))


def _draw_chapter_rankings(surf):
    records = player_data.chapter_rankings()
    completed = player_data.chapter_progress()
    summary_font = pygame.font.SysFont(None, max(18, int(HEIGHT * 0.028)))
    summary = summary_font.render(
        f"Chapters completed: {len(completed)} / {len(chapters_data.CHAPTER_IDS)}",
        True, (225, 215, 187),
    )
    surf.blit(summary, summary.get_rect(midtop=(panel_rect.centerx, _chapter_tab.bottom + 5)))
    formula_font = pygame.font.SysFont(None, max(14, int(HEIGHT * 0.021)))
    formula = formula_font.render(
        "Score: 1,000 completion + bonuses + mini-games - 50 per mistake",
        True, (205, 198, 178),
    )
    surf.blit(formula, formula.get_rect(midtop=(panel_rect.centerx,
                                                _chapter_tab.bottom + summary.get_height() + 8)))
    _draw_storage_warning(surf)
    if not records:
        _draw_empty(surf, "Finish a chapter to start your local rankings.")
        return

    page = _draw_pagination(surf, len(records))
    first = page * _PAGE_SIZE
    row_top = _chapter_tab.bottom + int(HEIGHT * 0.105)
    row_height = int(HEIGHT * 0.077)
    title_font = pygame.font.SysFont(None, max(18, int(HEIGHT * 0.029)))
    detail_font = pygame.font.SysFont(None, max(15, int(HEIGHT * 0.023)))
    for rank, record in enumerate(records[first:first + _PAGE_SIZE], first + 1):
        y = row_top + (rank - first - 1) * row_height
        player_name = str(record.get("player_name", "Player"))
        title = f"{rank}. {player_name} - {_chapter_title(record.get('chapter', ''))}"
        title_text = title_font.render(title, True, (255, 240, 200))
        surf.blit(title_text, (panel_rect.left + int(panel_rect.width * 0.07), y))
        score = int(record.get("score", 0))
        detail = (
            f"{score:,} pts   |   Bonus {int(record.get('time_bonus', 0)):,}"
            f"   |   Mistakes {int(record.get('mistakes', 0))}"
            f"   |   Mini-games {int(record.get('minigame_points', 0)):,}"
        )
        detail_text = detail_font.render(detail, True, (218, 218, 205))
        surf.blit(detail_text, (panel_rect.left + int(panel_rect.width * 0.10), y + title_text.get_height()))
        pygame.draw.line(surf, (100, 91, 70),
                         (panel_rect.left + 24, y + row_height - 3),
                         (panel_rect.right - 24, y + row_height - 3), 1)


def _draw_minigame_rankings(surf):
    records = player_data.minigame_rankings()
    _draw_storage_warning(surf)
    if not records:
        _draw_empty(surf, "Play a mini-game to record a local high score.")
        return
    page = _draw_pagination(surf, len(records))
    first = page * _PAGE_SIZE
    row_top = _chapter_tab.bottom + int(HEIGHT * 0.14)
    row_height = int(HEIGHT * 0.09)
    title_font = pygame.font.SysFont(None, max(20, int(HEIGHT * 0.034)))
    detail_font = pygame.font.SysFont(None, max(16, int(HEIGHT * 0.025)))
    for rank, record in enumerate(records[first:first + _PAGE_SIZE], first + 1):
        y = row_top + (rank - first - 1) * row_height
        game_name = str(record["game"]).replace("_", " ").title()
        player_name = str(record.get("player_name", "Player"))
        title = title_font.render(
            f"{rank}. {player_name} - {game_name}", True, (255, 240, 200)
        )
        surf.blit(title, (panel_rect.left + int(panel_rect.width * 0.08), y))
        detail = detail_font.render(
            f"Best score: {int(record.get('score', 0)):,}   |   "
            f"Time bonus: {int(record.get('time_bonus', 0)):,}   |   "
            f"Mistakes: {int(record.get('mistakes', 0))}",
            True, (218, 218, 205),
        )
        surf.blit(detail, (panel_rect.left + int(panel_rect.width * 0.12),
                           y + title.get_height()))


def _draw_storage_warning(surf):
    error = player_data.last_error()
    if not error:
        return
    font = pygame.font.SysFont(None, max(14, int(HEIGHT * 0.02)))
    text = font.render("Local save error: rankings may not persist.", True, (255, 170, 140))
    surf.blit(text, text.get_rect(midbottom=(panel_rect.centerx,
                                             panel_rect.bottom - int(HEIGHT * 0.10))))


def draw(surf):
    base.draw_overlay(surf, WIDTH, HEIGHT)
    base.draw_panel_frame(surf, panel_rect, "Local Rankings", title_font_size=max(30, int(HEIGHT * 0.05)))
    _draw_tab(surf, _chapter_tab, "Chapters", _tab == "chapters")
    _draw_tab(surf, _minigame_tab, "Mini-games", _tab == "minigames")
    if _tab == "chapters":
        _draw_chapter_rankings(surf)
    else:
        _draw_minigame_rankings(surf)
    base.draw_close_button(surf, close_btn_rect)
