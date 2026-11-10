import os, sys
sys.path.insert(0, 'D:\HarvestHand')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
from PIL import Image
import numpy as np
pygame.init()

pechay_dir = 'D:\HarvestHand\data\card_samples\pechay_plant'
monggo_dir = 'D:\HarvestHand\data\card_samples\monggo_plant'

def get_first_image(d):
    for f in sorted(os.listdir(d)):
        if f.lower().endswith(('.jpg','.jpeg','.png')):
            return os.path.join(d, f)
    return None

for label, d in [('pechay', pechay_dir), ('monggo', monggo_dir)]:
    p = get_first_image(d)
    if p:
        im = Image.open(p)
        print(f'{label}: {os.path.basename(p)} size={im.size} mode={im.mode}')
        w, h = im.size
        cx, cy = w//2, h//2
        crop = im.crop((cx-50, cy-50, cx+50, cy+50))
        arr = np.array(crop)
        print(f'  center mean RGB: R={arr[:,:,0].mean():.1f} G={arr[:,:,1].mean():.1f} B={arr[:,:,2].mean():.1f}')
        top = im.crop((0, 0, w, int(h*0.25)))
        arrt = np.array(top)
        print(f'  top band mean RGB: R={arrt[:,:,0].mean():.1f} G={arrt[:,:,1].mean():.1f} B={arrt[:,:,2].mean():.1f}')
        ill = im.crop((0, int(h*0.25), w, int(h*0.75)))
        arri = np.array(ill)
        print(f'  ill band mean RGB: R={arri[:,:,0].mean():.1f} G={arri[:,:,1].mean():.1f} B={arri[:,:,2].mean():.1f}')
        bot = im.crop((0, int(h*0.75), w, h))
        arrb = np.array(bot)
        print(f'  bot band mean RGB: R={arrb[:,:,0].mean():.1f} G={arrb[:,:,1].mean():.1f} B={arrb[:,:,2].mean():.1f}')