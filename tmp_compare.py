"""Compare pechay vs monggo raw images across all samples."""
import os, sys
sys.path.insert(0, r'D:\HarvestHand')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
from PIL import Image
import numpy as np
pygame.init()

PECHAY_DIR = r'D:\HarvestHand\data\card_samples\pechay_plant'
MONGGO_DIR = r'D:\HarvestHand\data\card_samples\monggo_plant'
EXTS = ('.jpg', '.jpeg', '.png')

def list_imgs(d):
    return sorted(
        os.path.join(d, f) for f in os.listdir(d)
        if f.lower().endswith(EXTS) and os.path.isfile(os.path.join(d, f))
    )

def band_stats(path):
    im = Image.open(path).convert('RGB')
    arr = np.array(im, dtype=np.float64)
    h, w = arr.shape[:2]
    y_top = int(h * 0.25)
    y_ill = int(h * 0.75)
    top = arr[:y_top, :, :]
    ill = arr[y_top:y_ill, :, :]
    bot = arr[y_ill:, :, :]
    cy, cx = h // 2, w // 2
    dy, dx = int(h * 0.1), int(w * 0.1)
    center = arr[cy-dy:cy+dy, cx-dx:cx+dx, :]
    side_w = int(w * 0.1)
    left = arr[:, :side_w, :]
    right = arr[:, -side_w:, :]
    side = np.concatenate([left, right], axis=1)
    return {
        'file': os.path.basename(path),
        'size': (w, h),
        'top_lum': (0.299*top[:,:,0] + 0.587*top[:,:,1] + 0.114*top[:,:,2]).mean(),
        'ill_lum': (0.299*ill[:,:,0] + 0.587*ill[:,:,1] + 0.114*ill[:,:,2]).mean(),
        'bot_lum': (0.299*bot[:,:,0] + 0.587*bot[:,:,1] + 0.114*bot[:,:,2]).mean(),
        'center_lum': (0.299*center[:,:,0] + 0.587*center[:,:,1] + 0.114*center[:,:,2]).mean(),
        'side_lum': (0.299*side[:,:,0] + 0.587*side[:,:,1] + 0.114*side[:,:,2]).mean(),
        'ill_green_frac': float((ill[:,:,1] > ill[:,:,0] + 10).mean()),
        'center_green_frac': float((center[:,:,1] > center[:,:,0] + 10).mean()),
        'ill_red_minus_green': float((ill[:,:,0] - ill[:,:,1]).mean()),
        'center_red_minus_green': float((center[:,:,0] - center[:,:,1]).mean()),
    }

def print_table(rows, label):
    print(f'\n=== {label} ===')
    print(f"{'file':30s} {'top_lum':>8s} {'ill_lum':>8s} {'bot_lum':>8s} {'ctr_lum':>8s} {'side_lum':>8s} {'illG%':>6s} {'ctrG%':>6s} {'illR-G':>7s} {'ctrR-G':>7s}")
    for r in rows:
        print(f"{r['file']:30s} {r['top_lum']:8.1f} {r['ill_lum']:8.1f} {r['bot_lum']:8.1f} {r['center_lum']:8.1f} {r['side_lum']:8.1f} {r['ill_green_frac']*100:6.1f} {r['center_green_frac']*100:6.1f} {r['ill_red_minus_green']:7.1f} {r['center_red_minus_green']:7.1f}")

pechay_imgs = list_imgs(PECHAY_DIR)
monggo_imgs = list_imgs(MONGGO_DIR)
pechay_stats = [band_stats(p) for p in pechay_imgs]
monggo_stats = [band_stats(p) for p in monggo_imgs]
print_table(pechay_stats, 'PECHAY')
print_table(monggo_stats, 'MONGGO')

def agg(stats):
    keys = ['top_lum', 'ill_lum', 'bot_lum', 'center_lum', 'side_lum', 'ill_green_frac', 'center_green_frac', 'ill_red_minus_green', 'center_red_minus_green']
    out = {}
    for k in keys:
        vals = [s[k] for s in stats]
        out[k] = (np.mean(vals), np.std(vals))
    return out

pa = agg(pechay_stats)
ma = agg(monggo_stats)
print('\n=== AGGREGATE (mean +/- std) ===')
print(f"{'metric':25s} {'pechay':>20s} {'monggo':>20s} {'diff':>10s}")
for k in pa:
    p_mean, p_std = pa[k]
    m_mean, m_std = ma[k]
    print(f"{k:25s} {p_mean:7.2f}+/-{p_std:6.2f} {m_mean:7.2f}+/-{m_std:6.2f} {m_mean-p_mean:10.2f}")