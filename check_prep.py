import sys; sys.path.insert(0,'.')
import cardscan.preprocess as p
import glob
for folder in ['pechay_plant','monggo_plant','chemical_fertilizer']:
    files = glob.glob('data/card_samples/%s/*.jpg' % folder)
    im = p.load_image(files[0])
    c = p.prepare(im)
    buf = p.pygame.image.tobytes(c, 'RGB')
    nonblack = sum(1 for i in range(0, len(buf), 3) if buf[i] > 30 or buf[i+1] > 30 or buf[i+2] > 30)
    print(folder, c.get_size(), 'nonblack frac %.3f' % (nonblack / (120*168)))
