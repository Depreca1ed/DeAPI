from __future__ import annotations

import base64
import copy
import datetime
from io import BytesIO

from litestar import post
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from _types import SpotifyData, SpotifyInput  # noqa: PLC2701

BASE_IMAGE_SIZE = (512, 512)
BACKGROUND_IMAGE_SIZE = (1024, 1024)

BRIGHTNESS = 0.25

IMAGE_COVER_PASTE_AREA = (256, 256, 768, 768)

FONT = ImageFont.truetype('assets/DejaVuSans-Bold.ttf')

TITLE_COORDS = (512, 832)
ARTISTS_COORDS = (512, 896)
ALBUM_COORDS = (512, 960)


def spotify_img(spotify_icon: BytesIO, data: SpotifyData) -> BytesIO:
    image = Image.open(spotify_icon, mode='r').resize(BASE_IMAGE_SIZE)

    _image_resized = image.resize((1, 1)).getpixel((0, 0))

    bg = Image.open(spotify_icon).resize(BACKGROUND_IMAGE_SIZE)

    e = ImageEnhance.Brightness(bg)
    bg = e.enhance(BRIGHTNESS).filter(ImageFilter.BLUR)

    bg.paste(image, IMAGE_COVER_PASTE_AREA)

    draw = ImageDraw.Draw(bg)

    font = copy.copy(FONT)
    font.size = 48
    draw.text(TITLE_COORDS, text=data.title, font=FONT, fill=_image_resized, anchor='mm')

    font2 = copy.copy(FONT)
    font2.size = 48
    draw.text(ARTISTS_COORDS, text='By ' + ', '.join(data.artists), font=font2, fill=_image_resized, anchor='mm')
    if data.album:
        draw.text(ALBUM_COORDS, text='On ' + data.album, font=font2, fill=_image_resized, anchor='mm')
    buffer = BytesIO()
    bg.save(buffer, 'png')
    buffer.seek(0)

    return buffer


@post(path='/spotify/', sync_to_thread=True)
def spotify_route(data: SpotifyInput) -> dict[str, str]:

    spotify_icon = BytesIO(base64.b64decode(data.icon))
    title = data.title
    artist = data.artist
    album = data.album

    value = spotify_img(
        spotify_icon,
        SpotifyData(title, artist, album, datetime.datetime.now()),
    )
    return {'image_bytes': base64.b64encode(value.getvalue()).decode()}
