"""Monte une pub 9:16 à partir d'images : fond flouté, image au centre avec léger zoom,
texte dans un bandeau turquoise en haut, fondus entre scènes. Usage : python3 make_video.py liste|histoire"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import imageio_ffmpeg

W, H, FPS, FADE = 1080, 1920, 30, 10
TURQ, INK = (27, 199, 194), (10, 30, 30)
IMG = '/home/user/claude/images/reliefroll/'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

# (image, recadrage en fractions (x0,y0,x1,y1) ou None, texte, durée en s)
VIDEOS = {
    'liste': [
        ('page/A1-probleme-main-sur-le-dos.png', None,
         'Die kleinen Dinge, die man morgens niemandem erzählt …', 3.2),
        ('page/A1-probleme-main-sur-le-dos.png', (0.05, 0.0, 0.95, 0.6),
         '… man steht in zwei Etappen auf.', 2.6),
        ('page/A1-probleme-main-sur-le-dos.png', (0.0, 0.45, 1.0, 1.0),
         '… die ersten Schritte fühlen sich an wie bei einem Roboter.', 2.8),
        ('page/B4-foam-roller-vs-lit.png', (0.0, 0.0, 0.5, 1.0),
         '… und die Faszienrolle? Da kommt man kaum wieder hoch.', 2.8),
        ('reserve/produit-en-main.png', None,
         'Bis man DAS entdeckt.', 2.4),
        ('reserve/de-dos-bord-du-lit-journee.png', None,
         '10 Minuten auf der Bettkante. Es rollt und klopft – ganz ohne Kraft.', 3.0),
        ('page/E1-petite-fille-jardin-CARRY.png', None,
         'Und der Morgen gehört wieder einem selbst.', 3.2),
        ('END', None, None, 3.0),
    ],
    'histoire': [
        ('page/A1-probleme-main-sur-le-dos.png', None,
         '7:02 Uhr. Der Rücken ist schon wach. Sie noch nicht.', 3.0),
        ('reserve/de-dos-bord-du-lit-journee.png', None,
         'Statt Wärmecreme: 10 Minuten auf der Bettkante.', 2.8),
        ('page/A2-solution-soulagee-bord-du-lit.png', None,
         'Es rollt. Es klopft. Sie muss nichts tun.', 2.6),
        ('page/F1-chaussures-petite-fille-porte-CARRY.png', None,
         '7:15 Uhr. Die Enkelin wartet schon an der Tür.', 2.8),
        ('page/E1-petite-fille-jardin-CARRY.png', None,
         'Und dieser Moment gehört wieder ihr.', 3.2),
        ('END', None, None, 3.0),
    ],
}


def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def wrap(draw, text, font, maxw):
    lines, cur = [], ''
    for word in text.split():
        t = (cur + ' ' + word).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def text_box(text, big):
    """Bandeau turquoise avec texte auto-ajusté (3 lignes max)."""
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    size = 74 if big else 62
    while True:
        font = ImageFont.truetype(BOLD, size)
        lines = wrap(d, text, font, W - 160)
        if len(lines) <= 3 or size <= 40:
            break
        size -= 4
    lh = int(size * 1.22)
    bh = lh * len(lines) + 56
    box = Image.new('RGBA', (W - 80, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 0, W - 81, bh - 1), radius=28, fill=TURQ + (255,))
    for i, line in enumerate(lines):
        tw = bd.textlength(line, font=font)
        bd.text(((W - 80 - tw) / 2, 26 + i * lh), line, font=font, fill=INK)
    return box


def scene_frames(path, crop, text, dur, first):
    im = Image.open(IMG + path).convert('RGB')
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    bg = cover(im, W, H).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.25)
    # image au premier plan : sous le bandeau, jamais cachée par le texte
    box = text_box(text, first)
    top = 250 + box.height + 30
    avail = H - 140 - top
    r = min(W / im.width, avail / im.height)
    fg = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    n = int(dur * FPS)
    for f in range(n):
        z = 1 + 0.07 * f / n
        fw, fh = round(fg.width * z), round(fg.height * z)
        z_im = fg.resize((fw, fh), Image.BILINEAR)
        # recadre au format d'origine pour garder la même taille à l'écran
        cx, cy = (fw - fg.width) // 2, (fh - fg.height) // 2
        z_im = z_im.crop((cx, cy, cx + fg.width, cy + fg.height))
        frame = bg.copy()
        frame.paste(z_im, ((W - fg.width) // 2, top + (avail - fg.height) // 2))
        frame.paste(box, (40, 250), box)
        yield frame


def end_frames(dur):
    frame = Image.new('RGB', (W, H), (255, 255, 255))
    prod = Image.open(IMG + 'reserve/produit-en-main.png').convert('RGB')
    prod = cover(prod, 860, 860)
    mask = Image.new('L', prod.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 859, 859), radius=48, fill=255)
    frame.paste(prod, (110, 330), mask)
    d = ImageDraw.Draw(frame)

    def center(t, y, font, fill):
        d.text(((W - d.textlength(t, font=font)) / 2, y), t, font=font, fill=fill)

    center('ReliefRoll™', 1250, ImageFont.truetype(BOLD, 96), INK)
    center('Rollt + klopft · 10 Minuten am Morgen', 1380, ImageFont.truetype(REG, 44), (60, 60, 60))
    d.rounded_rectangle((140, 1490, W - 140, 1620), radius=65, fill=TURQ)
    center('30 Tage in Ruhe testen', 1522, ImageFont.truetype(BOLD, 54), INK)
    center('Geld-zurück-Garantie · Versand mit Tracking', 1670, ImageFont.truetype(REG, 38), (60, 60, 60))
    for _ in range(int(dur * FPS)):
        yield frame


def build(name):
    out = f'/home/user/claude/images/reliefroll/pubs/{name}-9x16-DE.mp4'
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
           '-crf', '23', '-preset', 'medium', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    prev_tail = []
    for i, (path, crop, text, dur) in enumerate(VIDEOS[name]):
        frames = end_frames(dur) if path == 'END' else scene_frames(path, crop, text, dur, i == 0)
        for k, fr in enumerate(frames):
            if k < len(prev_tail):  # fondu avec la fin de la scène précédente
                fr = Image.blend(prev_tail[k], fr, (k + 1) / (FADE + 1))
            if k == 0:
                buf = []
            buf.append(fr)
            if len(buf) > FADE:
                p.stdin.write(buf.pop(0).tobytes())
        prev_tail = buf
    for fr in prev_tail:
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    print(out)


if __name__ == '__main__':
    build(sys.argv[1])
