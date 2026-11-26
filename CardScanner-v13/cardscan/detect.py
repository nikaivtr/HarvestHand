# ============================================================
#  Card boundary detection
#
#  Finds the four corners of a physical (5:7 portrait) card in a
#  camera frame. OpenCV + NumPy only.
#
#  Why this replaces the old contour-and-approxPolyDP step
#  -------------------------------------------------------
#  * approxPolyDP at 4-6 % of the perimeter turns almost ANY blob
#    into "4 points", so tables, floors and hands were accepted as
#    cards, and real cards got their corners cut off.
#  * A large-area shortcut skipped the edge check entirely.
#  * Fixed brightness thresholds (140 / 180) break whenever the room
#    light or the webcam's auto-exposure changes.
#
#  How this works
#  --------------
#  1. Look at the frame several independent ways (edges, distance
#     from the background colour, light / dark regions).
#  2. Every contour becomes a quadrilateral: convex hull -> 4 coarse
#     corners -> each side is re-fitted with a robust line fit and the
#     corners are re-computed as line intersections. Rounded card
#     corners therefore stop pulling the corners inwards.
#  3. Every quadrilateral is SCORED on things a real card has: a 5:7
#     shape, right-angled corners, a boundary that follows real image
#     edges, and a clear colour change between just-inside and
#     just-outside the boundary.
#  4. Duplicates are merged, an outer card outline is preferred over
#     the printed frame inside it, and a ranked list is returned so
#     the caller can verify the best few (the scanner re-ranks them
#     with the recognition model).
#
#  Corner order returned: top-left, top-right, bottom-right,
#  bottom-left of a PORTRAIT card (long side vertical), in the
#  coordinates of the image that was passed in.
# ============================================================

import math

import cv2
import numpy as np

# 5:7 portrait card (poker proportions: 63 x 88 mm)
CARD_ASPECT = 5.0 / 7.0

# Detection works on a downscaled copy; corners are scaled back up.
DETECT_MAX_DIM = 640

MIN_AREA_RATIO = 0.03        # card smaller than this is unreadable anyway
MAX_AREA_RATIO = 0.82
MIN_ASPECT = 0.50            # short side / long side, apparent (perspective)
MAX_ASPECT = 0.92
MAX_ANGLE_DEV = 32.0         # degrees away from a right angle
MIN_OPPOSITE_RATIO = 0.60    # shorter / longer of two opposite sides
MIN_SCORE = 0.42             # below this nothing is reported
MAX_CORNER_OUTSIDE = 0.04    # of frame size: card cut off by the frame


class Detection:
    """One candidate card boundary."""

    __slots__ = (
        "corners", "score", "area_ratio", "aspect", "contrast", "support",
        "fit", "angle_dev", "clipped", "source", "rank", "feat",
    )

    def __init__(self, corners, score, area_ratio, aspect, contrast, support,
                 fit, angle_dev, clipped, source):
        self.corners = corners          # (4, 2) float32, TL TR BR BL
        self.score = float(score)
        self.area_ratio = float(area_ratio)
        self.aspect = float(aspect)
        self.contrast = float(contrast)
        self.support = float(support)
        self.fit = float(fit)
        self.angle_dev = float(angle_dev)
        self.clipped = bool(clipped)
        self.source = source
        self.rank = float(score)
        self.feat = {}

    def as_dict(self):
        return {
            "points": [[float(x), float(y)] for x, y in self.corners],
            "score": round(self.score, 3),
            "area_ratio": round(self.area_ratio, 3),
            "aspect": round(self.aspect, 3),
            "contrast": round(self.contrast, 3),
            "edge_support": round(self.support, 3),
            "fit": round(self.fit, 3),
            "angle_dev": round(self.angle_dev, 1),
            "clipped": self.clipped,
            "source": self.source,
        }

    def __repr__(self):
        return ("<Detection score=%.2f area=%.2f aspect=%.2f via %s>"
                % (self.score, self.area_ratio, self.aspect, self.source))


# ------------------------------------------------------------------
#  geometry helpers
# ------------------------------------------------------------------

def _order_clockwise(pts):
    pts = np.asarray(pts, np.float32).reshape(4, 2)
    c = pts.mean(axis=0)
    ang = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
    return pts[np.argsort(ang)]          # image coords: increasing = clockwise


def _canonical(pts):
    """TL, TR, BR, BL of a portrait card, card top pointing up-ish."""
    q = _order_clockwise(pts)
    e = [np.linalg.norm(q[(i + 1) % 4] - q[i]) for i in range(4)]
    if (e[0] + e[2]) > (e[1] + e[3]):    # edge 0 is the LONG one -> shift
        q = np.roll(q, -1, axis=0)
    up = (q[0] + q[1]) / 2.0 - (q[3] + q[2]) / 2.0
    if up[1] > 0:                        # top of card points down: flip 180
        q = np.roll(q, -2, axis=0)
    return q.astype(np.float32)


def _side_lengths(q):
    return [float(np.linalg.norm(q[(i + 1) % 4] - q[i])) for i in range(4)]


def _angles(q):
    out = []
    for i in range(4):
        a = q[(i - 1) % 4] - q[i]
        b = q[(i + 1) % 4] - q[i]
        den = max(float(np.linalg.norm(a) * np.linalg.norm(b)), 1e-6)
        out.append(math.degrees(math.acos(
            max(-1.0, min(1.0, float(np.dot(a, b)) / den)))))
    return out


def _is_convex(q):
    return bool(cv2.isContourConvex(np.asarray(q, np.float32).reshape(4, 1, 2)))


def _quad_iou(a, b):
    ha = cv2.convexHull(np.asarray(a, np.float32).reshape(-1, 2))
    hb = cv2.convexHull(np.asarray(b, np.float32).reshape(-1, 2))
    inter, _ = cv2.intersectConvexConvex(ha, hb)
    union = cv2.contourArea(ha) + cv2.contourArea(hb) - inter
    return float(inter / union) if union > 0 else 0.0


def _containment(inner, outer):
    """Fraction of `inner`'s area that lies inside `outer`."""
    hi = cv2.convexHull(np.asarray(inner, np.float32).reshape(-1, 2))
    ho = cv2.convexHull(np.asarray(outer, np.float32).reshape(-1, 2))
    inter, _ = cv2.intersectConvexConvex(hi, ho)
    area = cv2.contourArea(hi)
    return float(inter / area) if area > 0 else 0.0


_UNIT_SQUARE = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], np.float32)


def _rectified_aspect(q, w, h, focal=0.80):
    """Width/height of the card AFTER undoing perspective.

    A card tilted away from the camera looks squashed, so the apparent
    ratio says little. Treat the quad as the image of a rectangle seen by
    a pinhole camera (principal point at the image centre). The
    homography H of the unit square gives the true ratio as
    |K^-1 h1| / |K^-1 h2|. The focal length is unknown, but for a
    rectangle the two directions must be orthogonal, which fixes it in
    closed form whenever there is visible perspective; otherwise a
    typical webcam value is used.
    Returns (aspect, orthogonality).
    """
    try:
        H = cv2.getPerspectiveTransform(_UNIT_SQUARE, q.astype(np.float32))
    except cv2.error:
        return None, 1.0
    cx, cy = w / 2.0, h / 2.0
    h1 = H[:, 0] / H[2, 2]
    h2 = H[:, 1] / H[2, 2]
    f = focal * float(w)
    denom = float(h1[2] * h2[2])
    if abs(denom) > 4e-8:                       # visible perspective
        num = -((h1[0] - cx * h1[2]) * (h2[0] - cx * h2[2])
                + (h1[1] - cy * h1[2]) * (h2[1] - cy * h2[2]))
        f2 = num / denom
        if f2 > 0:
            f = float(np.clip(math.sqrt(f2), 0.45 * w, 1.5 * w))
    kinv = np.array([[1.0 / f, 0.0, -cx / f],
                     [0.0, 1.0 / f, -cy / f],
                     [0.0, 0.0, 1.0]])
    a = kinv @ h1
    b = kinv @ h2
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na < 1e-9 or nb < 1e-9:
        return None, 1.0
    return na / nb, abs(float(a @ b)) / (na * nb)


def _fit_line(pts):
    vx, vy, x0, y0 = cv2.fitLine(
        np.asarray(pts, np.float32).reshape(-1, 1, 2),
        cv2.DIST_HUBER, 0, 0.01, 0.01).flatten()
    return np.array([x0, y0], np.float32), np.array([vx, vy], np.float32)


def _intersect(p1, d1, p2, d2):
    cross = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(cross) < 0.15:                # nearly parallel
        return None
    diff = p2 - p1
    t = (diff[0] * d2[1] - diff[1] * d2[0]) / cross
    return p1 + d1 * t


def _refine_quad(quad, pts):
    """Re-fit each side to the contour points near it (robust to rounded
    corners, fingers and the occasional merged blob) and intersect."""
    q = _order_clockwise(quad)
    diag = float(np.linalg.norm(q.max(axis=0) - q.min(axis=0)))
    if diag < 8:
        return quad
    pts = np.asarray(pts, np.float32).reshape(-1, 2)
    lines = []
    for i in range(4):
        a, b = q[i], q[(i + 1) % 4]
        d = b - a
        length = float(np.linalg.norm(d))
        if length < 4:
            return quad
        d = d / length
        n = np.array([-d[1], d[0]], np.float32)
        p0, d0 = a, d
        ok = False
        for tol_frac, lo, hi in ((0.05, 0.12, 0.88), (0.018, 0.08, 0.92)):
            rel = pts - p0
            t = (rel @ d0) / length
            # distance of each point from the CURRENT line estimate
            nn = np.array([-d0[1], d0[0]], np.float32)
            dist = np.abs(rel @ nn)
            sel = (t > lo) & (t < hi) & (dist < tol_frac * diag)
            if int(sel.sum()) < 6:
                break
            sp = pts[sel]
            tt = t[sel]
            if (tt.max() - tt.min()) < 0.25:
                break
            p0, d0 = _fit_line(sp)
            if (d0 @ d) < 0:
                d0 = -d0
            ok = True
        lines.append((p0, d0) if ok else (a, d))
    out = np.zeros((4, 2), np.float32)
    for i in range(4):
        pa, da = lines[(i - 1) % 4]
        pb, db = lines[i]
        x = _intersect(pa, da, pb, db)
        if x is None or float(np.linalg.norm(x - q[i])) > 0.14 * diag:
            out[i] = q[i]
        else:
            out[i] = x
    return out


def _quad_from_contour(cnt):
    """Contour -> list of refined quadrilateral hypotheses."""
    pts = cnt.reshape(-1, 2).astype(np.float32)
    if len(pts) < 8:
        return []
    hull = cv2.convexHull(pts.reshape(-1, 1, 2))
    if len(hull) < 4:
        return []
    peri = cv2.arcLength(hull, True)
    quad = None
    for eps in (0.008, 0.012, 0.018, 0.026, 0.036, 0.05, 0.07):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            quad = ap.reshape(4, 2).astype(np.float32)
            break
        if len(ap) < 4:
            break
    hyps = []
    if quad is not None:
        hyps.append(quad)
    rect = cv2.boxPoints(cv2.minAreaRect(hull)).astype(np.float32)
    hyps.append(rect)
    out = []
    for h in hyps:
        out.append(_refine_quad(h, pts))
    return out


# ------------------------------------------------------------------
#  line segments
# ------------------------------------------------------------------

_LSD = None


def _get_lsd():
    """LSD is validated statistically, so it ignores texture noise that
    floods Canny/Hough. It is missing from a few old OpenCV builds."""
    global _LSD
    if _LSD is None:
        try:
            _LSD = cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD)
        except (AttributeError, cv2.error):
            _LSD = False
    return _LSD


def _segments(Lraw, short):
    """Straight line segments (K,4) x0 y0 x1 y1 from the luminance."""
    Lb = cv2.GaussianBlur(Lraw, (0, 0), 1.1)
    lsd = _get_lsd()
    segs = None
    if lsd:
        try:
            segs = lsd.detect(Lb)[0]
        except cv2.error:
            segs = None
    if segs is None:
        e = cv2.Canny(cv2.GaussianBlur(Lraw, (0, 0), 1.6), 30, 90)
        segs = cv2.HoughLinesP(e, 1, math.pi / 180.0, threshold=24,
                               minLineLength=max(20, int(0.05 * short)),
                               maxLineGap=max(4, int(0.012 * short)))
    if segs is None:
        return np.zeros((0, 4), np.float32)
    segs = segs.reshape(-1, 4).astype(np.float32)
    ln = np.hypot(segs[:, 2] - segs[:, 0], segs[:, 3] - segs[:, 1])
    return segs[ln >= max(12.0, 0.03 * short)]


class _Line:
    __slots__ = ("p", "u", "n", "t0", "t1", "length", "theta", "mid")

    def __init__(self, p, u, t0, t1, length):
        self.p = p                       # point on the line
        self.u = u                       # unit direction
        self.n = np.array([-u[1], u[0]], np.float32)
        self.t0, self.t1 = t0, t1        # extent along u from p
        self.length = length             # covered length
        self.theta = math.atan2(u[1], u[0]) % math.pi
        self.mid = p + u * (t0 + t1) / 2.0


def _merge_segments(segs, short, max_lines=140):
    """Merge collinear segments into longer lines with a covered length."""
    K = len(segs)
    if K == 0:
        return []
    ln = np.hypot(segs[:, 2] - segs[:, 0], segs[:, 3] - segs[:, 1])
    order = np.argsort(-ln)[:700]
    th = np.arctan2(segs[:, 3] - segs[:, 1], segs[:, 2] - segs[:, 0]) % math.pi
    mx = (segs[:, 0] + segs[:, 2]) / 2.0
    my = (segs[:, 1] + segs[:, 3]) / 2.0
    th_c = np.zeros(K)
    rho_c = np.zeros(K)
    members = []
    rho_tol = max(2.5, 0.007 * short)
    tol_ang = math.radians(2.5)
    for k in order:
        n = len(members)
        if n:
            dth = np.abs(th_c[:n] - th[k])
            dth = np.minimum(dth, math.pi - dth)
            r2 = -mx[k] * np.sin(th_c[:n]) + my[k] * np.cos(th_c[:n])
            ok = np.flatnonzero((dth < tol_ang)
                                & (np.abs(r2 - rho_c[:n]) < rho_tol))
            if ok.size:
                members[ok[0]].append(k)
                continue
        th_c[n] = th[k]
        rho_c[n] = -mx[k] * math.sin(th[k]) + my[k] * math.cos(th[k])
        members.append([k])
    lines = []
    for mem in members:
        pts = np.concatenate([segs[mem][:, :2], segs[mem][:, 2:]], axis=0)
        p0, u = _fit_line(pts)
        t = (segs[mem][:, :2] - p0) @ u, (segs[mem][:, 2:] - p0) @ u
        lo = np.minimum(t[0], t[1])
        hi = np.maximum(t[0], t[1])
        o = np.argsort(lo)
        lo, hi = lo[o], hi[o]
        covered, c0, c1 = 0.0, lo[0], hi[0]
        for a_, b_ in zip(lo[1:], hi[1:]):
            if a_ <= c1 + 0.02 * short:
                c1 = max(c1, b_)
            else:
                covered += c1 - c0
                c0, c1 = a_, b_
        covered += c1 - c0
        lines.append(_Line(p0, u, float(lo.min()), float(hi.max()),
                           float(covered)))
    lines.sort(key=lambda l: -l.length)
    return lines[:max_lines]


def _line_quads(lines, w, h, max_quads=160):
    """Two pairs of parallel lines at right angles -> candidate quads."""
    N = len(lines)
    if N < 4:
        return []
    short = float(min(w, h))
    P = np.array([l.p for l in lines], np.float32)
    U = np.array([l.u for l in lines], np.float32)
    Nn = np.array([l.n for l in lines], np.float32)
    T0 = np.array([l.t0 for l in lines], np.float32)
    T1 = np.array([l.t1 for l in lines], np.float32)
    TH = np.array([l.theta for l in lines], np.float32)
    LEN = np.array([l.length for l in lines], np.float32)
    MID = np.array([l.mid for l in lines], np.float32)

    I, J = np.triu_indices(N, 1)
    dth = np.abs(TH[I] - TH[J])
    dth = np.minimum(dth, math.pi - dth)
    m = dth < math.radians(12.0)
    I, J = I[m], J[m]
    if I.size == 0:
        return []
    d = (np.abs(((MID[J] - P[I]) * Nn[I]).sum(1))
         + np.abs(((MID[I] - P[J]) * Nn[J]).sum(1))) / 2.0
    m = (d >= 0.07 * short) & (d <= 0.95 * short)
    I, J, d = I[m], J[m], d[m]
    if I.size == 0:
        return []
    # the two lines must face each other: extents overlap along u
    u = U[I]
    sgn = np.sign((U[I] * U[J]).sum(1))
    sgn[sgn == 0] = 1.0
    ai = np.stack([((P[I] + U[I] * T0[I, None]) * u).sum(1),
                   ((P[I] + U[I] * T1[I, None]) * u).sum(1)], 1)
    bj = np.stack([((P[J] + U[J] * T0[J, None]) * u).sum(1),
                   ((P[J] + U[J] * T1[J, None]) * u).sum(1)], 1)
    a0, a1 = ai.min(1), ai.max(1)
    b0, b1 = bj.min(1), bj.max(1)
    ov = np.minimum(a1, b1) - np.maximum(a0, b0)
    m = ov >= 0.5 * np.minimum(a1 - a0, b1 - b0)
    I, J, d = I[m], J[m], d[m]
    if I.size < 2:
        return []
    sup = LEN[I] + LEN[J]
    order = np.argsort(-sup)[:420]
    I, J, d, sup = I[order], J[order], d[order], sup[order]
    thp = TH[I]
    M = I.size

    # all pair-of-pairs that are perpendicular with a card-like ratio
    ang = np.abs(thp[:, None] - thp[None, :])
    ang = np.minimum(ang, math.pi - ang)
    perp = ang >= math.radians(64.0)
    dmin = np.minimum(d[:, None], d[None, :])
    dmax = np.maximum(d[:, None], d[None, :])
    ratio = dmin / np.maximum(dmax, 1e-6)
    ok = perp & (ratio >= MIN_ASPECT) & (ratio <= MAX_ASPECT)
    distinct = ((I[:, None] != I[None, :]) & (I[:, None] != J[None, :])
                & (J[:, None] != I[None, :]) & (J[:, None] != J[None, :]))
    ok &= distinct
    ok = np.triu(ok, 1)
    xs, ys = np.nonzero(ok)
    if xs.size == 0:
        return []
    tot = sup[xs] + sup[ys]
    o = np.argsort(-tot)[:700]
    xs, ys = xs[o], ys[o]

    out = []
    for x, y in zip(xs, ys):
        i, j, k, l = I[x], J[x], I[y], J[y]
        la, lb, lc, ld = lines[i], lines[j], lines[k], lines[l]
        c_ik = _intersect(la.p, la.u, lc.p, lc.u)
        c_il = _intersect(la.p, la.u, ld.p, ld.u)
        c_jl = _intersect(lb.p, lb.u, ld.p, ld.u)
        c_jk = _intersect(lb.p, lb.u, lc.p, lc.u)
        if c_ik is None or c_il is None or c_jl is None or c_jk is None:
            continue
        quad = np.array([c_ik, c_il, c_jl, c_jk], np.float32)
        cover = []
        for ln_, pa, pb in ((la, quad[0], quad[1]), (lb, quad[3], quad[2]),
                            (lc, quad[0], quad[3]), (ld, quad[1], quad[2])):
            ta = float((pa - ln_.p) @ ln_.u)
            tb = float((pb - ln_.p) @ ln_.u)
            lo, hi = min(ta, tb), max(ta, tb)
            side = max(hi - lo, 1e-3)
            inter = min(hi, ln_.t1) - max(lo, ln_.t0)
            cover.append(max(0.0, inter) / side)
        cs = sorted(cover)
        if cs[1] < 0.35 or sum(cover) < 1.9:
            continue
        out.append((float(tot[list(xs).index(x)] if False else 0) + 100.0 * sum(cover), quad))
        if len(out) >= max_quads * 3:
            break
    out.sort(key=lambda t: -t[0])
    return [q for _, q in out[:max_quads]]


# ------------------------------------------------------------------
#  image views
# ------------------------------------------------------------------

def _views(small):
    """Binary masks that may contain the card outline + scoring context."""
    h, w = small.shape[:2]
    short = min(h, w)
    lab = cv2.cvtColor(small, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)
    k3 = np.ones((3, 3), np.uint8)
    k5 = np.ones((5, 5), np.uint8)
    views = []

    # -- edge-contour view (plain luminance: no CLAHE noise boost) ---
    Ls = cv2.GaussianBlur(L, (0, 0), 1.4)
    gx = cv2.Sobel(Ls, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(Ls, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy) / 4.0
    hi = float(np.clip(np.percentile(mag, 93), 14, 90))
    e = cv2.Canny(Ls, hi * 0.5, hi)
    # drop tiny texture debris
    n, lab_cc, stats, _ = cv2.connectedComponentsWithStats(e, connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= max(20, int(0.06 * short))
    e = (keep[lab_cc].astype(np.uint8)) * 255
    views.append(("edge", cv2.dilate(e, k3)))
    views.append(("edge_closed",
                  cv2.morphologyEx(e, cv2.MORPH_CLOSE, k5, iterations=2)))

    # -- distance from the background colour ------------------------
    labf = cv2.GaussianBlur(lab, (0, 0), 2.0).astype(np.float32)
    bw = max(3, int(0.06 * short))
    strip = np.concatenate([
        labf[:bw].reshape(-1, 3), labf[-bw:].reshape(-1, 3),
        labf[:, :bw].reshape(-1, 3), labf[:, -bw:].reshape(-1, 3)])
    bg = np.median(strip, axis=0)
    dist = np.sqrt(((labf - bg) ** 2).sum(axis=2))
    dmax = float(dist.max())
    if dmax > 8:
        d8 = np.clip(dist * (255.0 / dmax), 0, 255).astype(np.uint8)
        t, m = cv2.threshold(d8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k5)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        views.append(("bgdist", m))
        m2 = (d8 > max(10, 0.55 * t)).astype(np.uint8) * 255
        m2 = cv2.morphologyEx(m2, cv2.MORPH_OPEN, k5)
        m2 = cv2.morphologyEx(m2, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        views.append(("bgdist_lo", m2))

    # -- light / dark regions ---------------------------------------
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    Lb = cv2.GaussianBlur(clahe.apply(L), (0, 0), 2.0)
    _, m = cv2.threshold(Lb, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    for name, mm in (("light", m), ("dark", 255 - m)):
        mm = cv2.morphologyEx(mm, cv2.MORPH_OPEN, k5)
        mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        views.append((name, mm))

    # -- straight-line evidence --------------------------------------
    segs = _segments(L, short)
    seg_mask = np.zeros((h, w), np.uint8)
    for x0, y0, x1, y1 in segs:
        if np.hypot(x1 - x0, y1 - y0) >= 0.05 * short:
            cv2.line(seg_mask, (int(round(x0)), int(round(y0))),
                     (int(round(x1)), int(round(y1))), 255, 1)
    ctx = {
        "lab": cv2.GaussianBlur(lab, (0, 0), 1.0).astype(np.float32),
        "edge_map": cv2.dilate(seg_mask, k5),
        "segs": segs,
        "w": w, "h": h,
    }
    return views, ctx


# ------------------------------------------------------------------
#  scoring
# ------------------------------------------------------------------

def _side_samples(q, n_per_px=0.5, max_n=60):
    """Sample points along each side (inside 8-92 % of its length)."""
    out = []
    for i in range(4):
        a, b = q[i], q[(i + 1) % 4]
        length = float(np.linalg.norm(b - a))
        n = int(min(max_n, max(8, length * n_per_px)))
        t = np.linspace(0.08, 0.92, n, dtype=np.float32)[:, None]
        out.append(a[None, :] + (b - a)[None, :] * t)
    return out


def _evaluate(q, pts, ctx, source):
    """Score a canonical quad. Returns a Detection or None."""
    w, h = ctx["w"], ctx["h"]
    if not _is_convex(q):
        return None
    area = abs(float(cv2.contourArea(q.reshape(4, 1, 2))))
    img_area = float(w * h)
    area_ratio = area / img_area
    if area_ratio < MIN_AREA_RATIO or area_ratio > MAX_AREA_RATIO:
        return None

    s = _side_lengths(q)           # top, right, bottom, left
    horiz = (s[0] + s[2]) / 2.0
    vert = (s[1] + s[3]) / 2.0
    if min(horiz, vert) < 12:
        return None
    aspect_app = horiz / vert
    ra, ortho = _rectified_aspect(q, w, h)
    if ra is None:
        return None
    aspect = ra
    opp = min(s[0] / max(s[2], 1e-3), s[2] / max(s[0], 1e-3),
              s[1] / max(s[3], 1e-3), s[3] / max(s[1], 1e-3))
    if aspect_app < MIN_ASPECT or aspect_app > 0.98:
        return None
    if aspect < 0.52 or aspect > 0.92 or opp < MIN_OPPOSITE_RATIO:
        return None
    angs = _angles(q)
    angle_dev = max(abs(a - 90.0) for a in angs)
    if angle_dev > MAX_ANGLE_DEV:
        return None

    # card cut off by the frame?
    out_x = max(0.0, float((-q[:, 0]).max()), float((q[:, 0] - (w - 1)).max()))
    out_y = max(0.0, float((-q[:, 1]).max()), float((q[:, 1] - (h - 1)).max()))
    out_frac = max(out_x / w, out_y / h)
    if out_frac > MAX_CORNER_OUTSIDE:
        return None
    clipped = out_frac > 0.004

    diag = float(np.linalg.norm(q[2] - q[0]))
    # how much of the quad's outline does the contour it came from
    # explain? (measured on the quad, so a finger bump on the contour
    # does not count against a quad whose four sides are all real)
    fit = None
    if pts is not None:
        tol = max(2.5, 0.022 * diag)
        sub = pts if len(pts) <= 700 else pts[:: max(1, len(pts) // 700)]
        per = np.concatenate(_side_samples(q, n_per_px=0.35, max_n=40), axis=0)
        dd = np.sqrt(((per[:, None, :] - sub[None, :, :]) ** 2).sum(axis=2))
        fit = float((dd.min(axis=1) <= tol).mean())

    # inside-vs-outside colour contrast and edge support, side by side
    centre = q.mean(axis=0)
    short = min(horiz, vert)
    delta = max(3.0, 0.045 * short)
    lab = ctx["lab"]
    emap = ctx["edge_map"]
    contrasts, supports = [], []
    for side in _side_samples(q):
        e = side[-1] - side[0]
        nrm = np.array([-e[1], e[0]], np.float32)
        nrm /= max(float(np.linalg.norm(nrm)), 1e-6)
        if float(nrm @ (centre - side.mean(axis=0))) < 0:
            nrm = -nrm                     # make it point inwards
        pin = side + nrm * delta
        pout = side - nrm * delta
        valid = ((pout[:, 0] >= 0) & (pout[:, 0] <= w - 1)
                 & (pout[:, 1] >= 0) & (pout[:, 1] <= h - 1)
                 & (pin[:, 0] >= 0) & (pin[:, 0] <= w - 1)
                 & (pin[:, 1] >= 0) & (pin[:, 1] <= h - 1))
        if int(valid.sum()) < 6:
            contrasts.append(0.0)
            supports.append(0.0)
            continue
        pin, pout, sd = pin[valid], pout[valid], side[valid]
        li = lab[pin[:, 1].round().astype(int), pin[:, 0].round().astype(int)]
        lo = lab[pout[:, 1].round().astype(int), pout[:, 0].round().astype(int)]
        contrasts.append(float(np.median(np.linalg.norm(li - lo, axis=1))))
        sup = emap[sd[:, 1].round().astype(int), sd[:, 0].round().astype(int)]
        supports.append(float((sup > 0).mean()))
    contrasts.sort(reverse=True)
    supports.sort(reverse=True)
    contrast = float(np.mean(contrasts[:3]))          # tolerate 1 hidden side
    weak_contrast = float(contrasts[-1])
    support = float(np.mean(supports[:3]))
    weakest = float(supports[-1])

    # ---- combine -------------------------------------------------
    s_aspect = math.exp(-0.5 * ((aspect - CARD_ASPECT) / 0.055) ** 2)
    s_rect = max(0.0, 1.0 - 0.5 * angle_dev / 34.0 - 0.5 * min(1.0, ortho / 0.25))
    s_opp = max(0.0, (opp - 0.5) / 0.5)
    s_contrast = (0.65 * min(1.0, contrast / 38.0)
                  + 0.35 * min(1.0, weak_contrast / 26.0))
    s_support = support
    if fit is None:                      # line-built quads: edges ARE the fit
        fit = support
    s_fit = fit
    # Cards in a webcam frame are mid-sized. Tiny is unreadable and
    # frame-sized is nearly always the table / mat / wall, not the card.
    if area_ratio <= 0.40:
        s_area = min(1.0, math.sqrt(area_ratio / 0.12))
    else:
        s_area = max(0.15, 1.0 - (area_ratio - 0.40) / 0.42 * 0.85)
    margin = min(float(q[:, 0].min()), float(q[:, 1].min()),
                 float(w - 1 - q[:, 0].max()), float(h - 1 - q[:, 1].max()))
    if margin < 0.012 * min(w, h):          # glued to the frame edge
        s_area *= 0.6
    score = (0.22 * s_aspect + 0.10 * s_rect + 0.05 * s_opp
             + 0.14 * s_fit + 0.22 * s_contrast + 0.17 * s_support
             + 0.10 * s_area)
    score *= 0.55 + 0.45 * min(1.0, weakest / 0.35 + 0.35)  # all 4 sides help
    if clipped:
        score *= 0.85
    det = Detection(q, score, area_ratio, aspect, contrast / 255.0, support,
                    fit, angle_dev, clipped, source)
    det.feat = {
        "aspect": aspect, "ortho": ortho, "angle_dev": angle_dev, "opp": opp,
        "fit": fit, "support": support, "weakest_support": weakest,
        "contrast": contrast, "weak_contrast": weak_contrast,
        "area_ratio": area_ratio, "margin": margin / float(min(w, h)),
        "clipped": float(clipped), "s_aspect": s_aspect, "s_area": s_area,
        "base_score": score,
    }
    return det


# ------------------------------------------------------------------
#  public API
# ------------------------------------------------------------------

def find_cards(image_bgr, max_candidates=3, max_dim=DETECT_MAX_DIM,
               return_all=False, min_score=None):
    """Return ranked card boundary candidates (best first).

    image_bgr : HxWx3 uint8 array (OpenCV BGR order). RGB works too - the
                detector only cares about colour DIFFERENCES.
    Corners are returned in the coordinates of the image passed in.
    """
    if image_bgr is None or image_bgr.ndim != 3:
        return []
    H0, W0 = image_bgr.shape[:2]
    if min(H0, W0) < 32:
        return []
    scale = min(1.0, float(max_dim) / max(H0, W0))
    small = (cv2.resize(image_bgr, None, fx=scale, fy=scale,
                        interpolation=cv2.INTER_AREA)
             if scale < 1.0 else image_bgr)
    views, ctx = _views(small)
    img_area = ctx["w"] * ctx["h"]

    cands = []
    lines = _merge_segments(ctx["segs"], min(ctx["w"], ctx["h"]))
    for quad in _line_quads(lines, ctx["w"], ctx["h"]):
        det = _evaluate(_canonical(quad), None, ctx, "lines")
        if det is not None:
            cands.append(det)
    for name, mask in views:
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST,
                                       cv2.CHAIN_APPROX_SIMPLE)
        sized = []
        for c in contours:
            a = cv2.contourArea(c)
            if MIN_AREA_RATIO * img_area * 0.8 <= a <= 1.05 * img_area:
                sized.append((a, c))
        sized.sort(key=lambda t: -t[0])
        for _, c in sized[:30]:
            pts = c.reshape(-1, 2).astype(np.float32)
            for quad in _quad_from_contour(c):
                q = _canonical(quad)
                det = _evaluate(q, pts, ctx, name)
                if det is not None:
                    cands.append(det)

    if not cands:
        return []

    # merge duplicates (keep the best-scoring of near-identical quads)
    cands.sort(key=lambda d: -d.score)
    kept = []
    for d in cands:
        if all(_quad_iou(d.corners, k.corners) < 0.85 for k in kept):
            kept.append(d)

    # Prefer the OUTER card outline over the printed frame inside it. A
    # candidate that tightly wraps another (inset of a few percent) and is
    # itself card-shaped and well supported is the physical card edge.
    for _ in range(2):
        for d in kept:
            for o in kept:
                if o is d:
                    continue
                ratio = o.area_ratio / max(d.area_ratio, 1e-6)
                if (1.06 < ratio < 1.9
                        and o.score >= 0.62 * d.score
                        and o.support >= 0.45
                        and abs(o.aspect - CARD_ASPECT) < 0.10
                        and _containment(d.corners, o.corners) > 0.90):
                    o.rank = max(o.rank, d.rank + 0.01)
    kept.sort(key=lambda d: -d.rank)

    thr = MIN_SCORE if min_score is None else min_score
    kept = [d for d in kept if d.score >= thr]
    for d in kept:                              # back to input coordinates
        d.corners = (d.corners / scale).astype(np.float32)
    return kept if return_all else kept[:max_candidates]


def find_card(image_bgr, **kwargs):
    """Best card boundary, or None."""
    found = find_cards(image_bgr, max_candidates=1, **kwargs)
    return found[0] if found else None
