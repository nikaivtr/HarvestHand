import os, glob
from PIL import Image

root = 'data/card_samples'
for folder in sorted(os.listdir(root)):
    p = os.path.join(root, folder)
    if not os.path.isdir(p):
        continue
    imgs = []
    for ext in ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.webp'):
        imgs += glob.glob(os.path.join(p, ext))
    if not imgs:
        print(f'{folder}: (no images)')
        continue
    im = Image.open(imgs[0])
    print(f'{folder}: {len(imgs)} imgs, first={os.path.basename(imgs[0])} size={im.size} mode={im.mode}')
