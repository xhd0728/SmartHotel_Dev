import random

import redis
from PIL import ImageFilter, ImageFont, ImageDraw, Image

from SmartHotel_Dev.settings import BASE_DIR
from config import db

redis_conn = redis.Redis(db.REDIS_HOST, db.REDIS_PORT)


def cache_code(md5_str, code):
    redis_conn.set(md5_str, code, ex=300)


def check_code(md5_str, code):
    if not isinstance(code, str):
        return False
    if len(code) != 4:
        return False
    redis_code = redis_conn.get(md5_str)
    if not redis_code:
        return False
    res = bool(str(redis_conn.get(md5_str).decode('utf-8')) == code)
    return res


def gene_code(width=120, height=30, char_length=4, font_size=28):
    font_file = open('{}/pkg/Monaco.ttf'.format(BASE_DIR), 'rb')
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text((i * width / char_length, h), char, font=font, fill=rndColor())

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
