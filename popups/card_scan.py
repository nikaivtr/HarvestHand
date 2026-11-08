"""Card scanner test panel."""
import os
import pygame
import player_data
from cardscan import CardScanner, all_cards, CameraError, get as get_card

WIDTH = 0
HEIGHT = 0
_close_popup = None

_panel = None
_close_rect = None
_scanner = None
_cam_opened = False
_cards = []
_selected_idx = 0
_result_msg = "Select a card, then hold it up."
_card_rects = []
_card_indices = []
_card_page = 0
_card_page_size = 8
_page_prev_rect = None
_page_next_rect = None
_retry_rect = None
_detail_rect = None
_preview_rect = None
_result_msg_until = 0
_result_msg_color = (210, 130, 80)
_select_model_page = True

def _make_font(size, bold=False):
    try:
        return pygame.font.Font(os.path.join("fonts", "RumRaisin-Regular.ttf"), size)
    except (pygame.error, OSError):
        return pygame.font.SysFont("Arial", size, bold=bold)


def init(width, height, close_popup_callback):
    global WIDTH, HEIGHT, _close_popup, _panel, _close_rect, _close_img, _scanner, _cards, _cam_opened, _selected_idx
    global _card_page, _card_page_size, _result_msg, _result_msg_until
    global _result_msg_color, _select_model_page
    if _scanner is not None:
        _scanner.cancel()
    WIDTH, HEIGHT = width, height
    _close_popup = close_popup_callback
    panel_w = int(WIDTH * 0.9)
    panel_h = int(HEIGHT * 0.9)
    _panel = pygame.Rect(0, 0, panel_w, panel_h)
    _panel.center = (WIDTH // 2, HEIGHT // 2)
    _close_rect = pygame.Rect(_panel.right - 44, _panel.top + 10, 36, 36)
    import utils
    _close_img = utils.load_img("buttons/btn_close.png", utils.btn_size(int(WIDTH * 0.06)))
    _close_rect = _close_img.get_rect(topright=(_panel.right - 10, _panel.top + 10))
    _cards = all_cards()
    _scanner = CardScanner(confirm_frames=12)
    trained_cards = set(_scanner.model.get("cards", {})) if _scanner.model else set()
    _selected_idx = next(
        (index for index, card in enumerate(_cards) if card.slug in trained_cards),
        0,
    )
    _card_page = 0
    _card_page_size = 8
    _select_model_page = True
    _cam_opened = False
    _result_msg = "Camera will start when the tester opens."
    _result_msg_until = 0
    _result_msg_color = (210, 190, 145)


def open():
    """Open the camera when the tester becomes visible."""
    global _cam_opened, _result_msg, _result_msg_until, _result_msg_color
    if _scanner is None:
        return
    if not _cam_opened:
        try:
            _scanner.open_camera(
                kind="opencv",
                device=player_data.get_settings()["camera_device"],
            )
            _cam_opened = True
        except CameraError as exc:
            _result_msg = f"Camera unavailable: {exc}"
            _result_msg_until = pygame.time.get_ticks() + 5000
            _result_msg_color = (255, 170, 140)
            return
    if _cards:
        _scanner.start(_cards[_selected_idx].display)
    if not _scanner.can_recognize:
        _result_msg = "Train at least two card types before testing recognition."
        _result_msg_color = (255, 190, 130)
    else:
        _result_msg = "Camera ready. Hold the selected card in view."
        _result_msg_color = (210, 190, 145)
    _result_msg_until = 0


def retry_camera():
    close()
    open()


def close():
    """Release the live camera when leaving the tester."""
    global _cam_opened
    if _scanner is not None:
        _scanner.cancel()
    _cam_opened = False


def handle_tap(px, py):
    global _selected_idx, _card_page, _result_msg, _result_msg_until
    global _select_model_page
    if _close_rect and _close_rect.collidepoint(px, py):
        _close_popup()
        return
    if _panel and not _panel.collidepoint(px, py):
        _close_popup()
        return
    if _retry_rect and _retry_rect.collidepoint(px, py):
        retry_camera()
        return
    if _page_prev_rect and _page_prev_rect.collidepoint(px, py):
        _card_page = max(0, _card_page - 1)
        _select_model_page = False
        _select_visible_page()
        return
    if _page_next_rect and _page_next_rect.collidepoint(px, py):
        max_page = max(0, (len(_cards) - 1) // _card_page_size)
        _card_page = min(max_page, _card_page + 1)
        _select_model_page = False
        _select_visible_page()
        return
    for index, r in zip(_card_indices, _card_rects):
        if r.collidepoint(px, py):
            _selected_idx = index
            _select_model_page = False
            if _scanner:
                _scanner.start(_cards[index].display)
            _result_msg = f"Show {_cards[index].display} to the camera."
            _result_msg_until = 0
            return


def _select_visible_page():
    global _selected_idx, _result_msg, _result_msg_until
    first = _card_page * _card_page_size
    if first < len(_cards):
        _selected_idx = first
        if _scanner:
            _scanner.start(_cards[first].display)
        _result_msg = f"Show {_cards[first].display} to the camera."
        _result_msg_until = 0


def _frame_to_surface(frame):
    if frame is None or _preview_rect is None:
        return None
    if isinstance(frame, pygame.Surface):
        scale = min(
            _preview_rect.width / frame.get_width(),
            _preview_rect.height / frame.get_height(),
        )
        size = (
            max(1, int(frame.get_width() * scale)),
            max(1, int(frame.get_height() * scale)),
        )
        return pygame.transform.smoothscale(frame, size)
    return None


def _draw_retry_button(surf, body_font):
    global _retry_rect
    retry_w = min(int(_preview_rect.width * 0.58), max(118, int(WIDTH * 0.15)))
    retry_h = max(34, int(HEIGHT * 0.06))
    _retry_rect = pygame.Rect(0, 0, retry_w, retry_h)
    _retry_rect.center = (_preview_rect.centerx, _preview_rect.bottom - retry_h // 2 - 12)
    pygame.draw.rect(surf, (55, 107, 70), _retry_rect, border_radius=8)
    pygame.draw.rect(surf, (210, 220, 205), _retry_rect, width=2, border_radius=8)
    retry_label = _fit_text_surface(
        "Retry camera", body_font, _retry_rect.width - 12, (245, 245, 230)
    )
    surf.blit(retry_label, retry_label.get_rect(center=_retry_rect.center))


def draw(surf):
    global _result_msg, _preview_rect, _card_rects, _card_indices
    global _page_prev_rect, _page_next_rect, _retry_rect, _detail_rect, _card_page
    global _result_msg_until, _result_msg_color
    global _select_model_page
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surf.blit(overlay, (0, 0))
    pygame.draw.rect(surf, (26, 32, 40), _panel, border_radius=16)
    pygame.draw.rect(surf, (90, 110, 100), _panel, width=2, border_radius=16)

    title_font = _make_font(max(22, int(HEIGHT * 0.045)), bold=True)
    body_font = _make_font(max(13, int(HEIGHT * 0.022)))
    t = title_font.render("Card Scan Tester", True, (240, 235, 225))
    surf.blit(t, t.get_rect(midtop=(_panel.centerx, _panel.top + 16)))

    # camera preview (center-left)
    pw = int(_panel.width * 0.55)
    ph = int(_panel.height * 0.55)
    _preview_rect = pygame.Rect(0, 0, pw, ph)
    _preview_rect.center = (_panel.left + int(_panel.width * 0.32), _panel.centery + 20)
    pygame.draw.rect(surf, (0, 0, 0), _preview_rect, border_radius=10)
    pygame.draw.rect(surf, (90, 110, 100), _preview_rect, width=2, border_radius=10)

    if _scanner and _cam_opened:
        try:
            res = _scanner.update(1.0 / 60.0)
        except CameraError as exc:
            _result_msg = f"Camera unavailable: {exc}"
            _result_msg_until = pygame.time.get_ticks() + 5000
            _result_msg_color = (255, 170, 140)
            close()
            res = None
        if res is not None:
            if pygame.time.get_ticks() >= _result_msg_until:
                detected = get_card(res.card)
                expected = get_card(res.expected)
                if res.status == res.MATCH:
                    _result_msg = f"Matched: {detected.display if detected else res.card}"
                    _result_msg_color = (110, 220, 130)
                elif res.status == res.WRONG:
                    _result_msg = (
                        f"Detected {detected.display if detected else res.card}. "
                        f"Show {expected.display if expected else res.expected}."
                    )
                    _result_msg_color = (255, 180, 120)
                else:
                    _result_msg = str(res)
                    _result_msg_color = (210, 190, 145)
                _result_msg_until = pygame.time.get_ticks() + 3000
        frame = _scanner.frame if _cam_opened else None
        s = _frame_to_surface(frame)
        if s:
            surf.blit(s, s.get_rect(center=_preview_rect.center))
        else:
            nf = body_font.render("No camera frame. Check connection.", True, (220, 170, 120))
            surf.blit(nf, nf.get_rect(center=_preview_rect.center))
            _draw_retry_button(surf, body_font)
        resolution = (
            f"{_scanner.frame.get_width()}x{_scanner.frame.get_height()}"
            if _scanner.frame is not None else "Camera ready"
        )
        _draw_fit_text(
            surf,
            f"{resolution} | Keep card steady; move face out of frame to focus.",
            body_font,
            pygame.Rect(
                _preview_rect.left,
                _preview_rect.bottom + 6,
                _preview_rect.width,
                body_font.get_linesize() + 2,
            ),
            (205, 210, 195),
            center=True,
        )
        if s is not None:
            _retry_rect = None
    else:
        camera_text = "Camera unavailable" if _result_msg.startswith("Camera unavailable:") else "Camera preview"
        _draw_fit_text(
            surf,
            camera_text,
            body_font,
            _preview_rect.inflate(-16, -16),
            (220, 170, 120),
            center=True,
        )
        _draw_retry_button(surf, body_font)

    # Card list (right), paged so all registered cards remain selectable.
    _card_rects = []
    _card_indices = []
    column_width = int(_panel.width * 0.34)
    lx = _panel.right - column_width - int(_panel.width * 0.025)
    list_width = column_width
    ly = _panel.top + int(_panel.height * 0.18)
    detail_height = max(
        int(_panel.height * 0.30),
        int(body_font.get_linesize() * 7 + 16),
    )
    detail_bottom = _panel.bottom - max(12, int(HEIGHT * 0.018))
    detail_top = detail_bottom - min(detail_height, int(_panel.height * 0.36))
    _detail_rect = pygame.Rect(
        lx,
        detail_top,
        list_width,
        detail_bottom - detail_top,
    )
    nav_h = max(24, int(HEIGHT * 0.042))
    nav_y = detail_top - nav_h - max(6, int(HEIGHT * 0.012))
    list_bottom = nav_y - max(6, int(HEIGHT * 0.012))
    row_step = max(30, min(44, int(HEIGHT * 0.052)))
    _card_page_size = max(1, (list_bottom - ly) // row_step)
    max_page = max(0, (len(_cards) - 1) // _card_page_size)
    if _select_model_page:
        _card_page = _selected_idx // _card_page_size
        _select_model_page = False
    _card_page = min(_card_page, max_page)
    page_start = _card_page * _card_page_size
    page_end = min(len(_cards), page_start + _card_page_size)
    for index in range(page_start, page_end):
        c = _cards[index]
        r = pygame.Rect(
            lx,
            ly + (index - page_start) * row_step,
            list_width,
            max(24, row_step - 5),
        )
        _card_rects.append(r)
        _card_indices.append(index)
        color = (60, 90, 70) if index == _selected_idx else (40, 50, 60)
        pygame.draw.rect(surf, color, r, border_radius=8)
        pygame.draw.rect(surf, (90, 110, 100), r, width=1, border_radius=8)
        lbl = _fit_text_surface(c.display, body_font, r.width - 16, (240, 235, 225))
        surf.blit(lbl, lbl.get_rect(midleft=(r.left + 8, r.centery)))

    nav_w = min(int(list_width * 0.22), max(32, int(HEIGHT * 0.07)))
    _page_prev_rect = pygame.Rect(lx, nav_y, nav_w, nav_h)
    _page_next_rect = pygame.Rect(lx + list_width - nav_w, nav_y, nav_w, nav_h)
    page_count = max(1, max_page + 1)
    for rect, label, enabled in (
        (_page_prev_rect, "<", _card_page > 0),
        (_page_next_rect, ">", _card_page < max_page),
    ):
        pygame.draw.rect(surf, (55, 75, 65) if enabled else (40, 48, 46), rect, border_radius=6)
        pygame.draw.rect(surf, (90, 110, 100), rect, width=1, border_radius=6)
        nav_label = body_font.render(label, True, (240, 235, 225))
        surf.blit(nav_label, nav_label.get_rect(center=rect.center))
    page_label = body_font.render(f"{_card_page + 1} / {page_count}", True, (200, 205, 200))
    surf.blit(page_label, page_label.get_rect(center=(_detail_rect.centerx, nav_y + nav_h // 2)))

    _draw_card_details(surf)

    # result message
    result_rect = pygame.Rect(
        _panel.left + int(_panel.width * 0.025),
        _panel.bottom - body_font.get_linesize() - 12,
        int(_panel.width * 0.58),
        body_font.get_linesize(),
    )
    _draw_fit_text(surf, _result_msg, body_font, result_rect, _result_msg_color)

    # close button
    surf.blit(_close_img, _close_rect)


def _draw_card_details(surf):
    card = _cards[_selected_idx] if _cards else None
    if card is None or _detail_rect is None:
        return
    pygame.draw.rect(surf, (34, 42, 44), _detail_rect, border_radius=8)
    pygame.draw.rect(surf, (90, 110, 100), _detail_rect, width=1, border_radius=8)
    lines = []
    details = card.details
    if "days" in details:
        lines.append(
            f"{details['english']} | {details['days']} days | "
            f"{details['season']} season | {details['growth']} growth"
        )
        lines.append(
            f"Water {details['water']}  Fertilizer {details['fertilizer']}  "
            f"Weeds {details['weeds']}  Pests {details['pests']}"
        )
        lines.append(f"Tip: {details['tip']}")
        lines.append(f"Fact: {details['fact']}")
        lines.append(f"Dish: {details['dish']}")
    else:
        if details.get("effect"):
            lines.append(f"Effect: {details['effect']}")
        if details.get("when_to_use"):
            lines.append(f"Use: {details['when_to_use']}")

    small_font = _make_font(max(12, int(HEIGHT * 0.018)))
    y = _detail_rect.top + 6
    max_width = _detail_rect.width - 12
    for line in lines:
        words = line.split()
        wrapped = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if small_font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    wrapped.append(current)
                current = word
                while current and small_font.size(current)[0] > max_width:
                    wrapped.append(current[:1])
                    current = current[1:]
        if current:
            wrapped.append(current)
        for part in wrapped:
            if y + small_font.get_linesize() > _detail_rect.bottom - 4:
                return
            surf.blit(small_font.render(part, True, (220, 225, 215)), (_detail_rect.left + 6, y))
            y += small_font.get_linesize()


def _fit_text_surface(text, font, max_width, color):
    rendered = font.render(text, True, color)
    if rendered.get_width() <= max_width:
        return rendered
    target_width = max(1, max_width)
    target_height = max(1, int(rendered.get_height() * target_width / rendered.get_width()))
    return pygame.transform.smoothscale(rendered, (target_width, target_height))


def _draw_fit_text(surf, text, font, rect, color, center=False):
    rendered = _fit_text_surface(text, font, rect.width, color)
    if center:
        target = rendered.get_rect(center=rect.center)
    else:
        target = rendered.get_rect(midleft=(rect.left, rect.centery))
    surf.blit(rendered, target)
