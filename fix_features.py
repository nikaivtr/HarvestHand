p = 'cardscan/features.py'
lines = open(p).read().split('\n')
new = []
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.strip() == 'w, h = card.get_size()':
        i += 1
        continue
    if ln.strip().startswith('small = pygame.transform.smoothscale'):
        new.append(ln)
        new.append("    buf = pygame.image.tobytes(small, 'RGB')")
        new.append('    w, h = small.get_size()')
        i += 1
        continue
    new.append(ln)
    i += 1
open(p, 'w').write('\n'.join(new))
