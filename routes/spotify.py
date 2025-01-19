from __future__ import annotations

import copy
import datetime
from io import BytesIO

from litestar import get
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from _types import SpotifyData  # noqa: PLC2701

BASE_IMAGE_SIZE = (512, 512)
BACKGROUND_IMAGE_SIZE = (1024, 1024)

BRIGHTNESS = 0.25

IMAGE_COVER_PASTE_AREA = (256, 256, 768, 768)

FONT = ImageFont.truetype('assets/DejaVuSans-Bold.ttf')

TITLE_COORDS = (512, 832)
ARTISTS_COORDS = (512, 896)
ALBUM_COORDS = (512, 960)


def spotify_img(spotify_icon: str, data: SpotifyData) -> BytesIO:
    image = Image.open(spotify_icon, mode='r').resize(BASE_IMAGE_SIZE)

    _image_resized = image.resize((1, 1)).getpixel((1, 1))

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

    #    dr.rounded_rectangle((128 - 16, 128 - 16, 1024 - 128 + 16, 128 + 16), fill=y, radius=45)
    #    val1 = datetime.datetime.now(tz=datetime.UTC) - act.start
    #    val2 = val1.seconds / act.duration.seconds
    #    dr.rounded_rectangle((128 - 16, 128 - 16, 128 + 16 + round(val2 * (1024 - 256)), 128 + 16), fill=x, radius=45)
    #    dr.text((128 - 16, 128 + 16 + 8), text=f'{round(val1.seconds / 60)}:{val1.seconds % 60}', fill=x, font=fntt, anchor='lt')
    #    dr.text(
    #        (1024 - 128 + 16, 128 + 16 + 8),
    #        text=f'{round(act.duration.seconds / 60)}:{act.duration.seconds % 60}',
    #        fill=x,
    #        font=fntt,
    #        anchor='rt',
    #    )
    buffer = BytesIO()
    bg.save(buffer, 'png')
    buffer.seek(0)
    return buffer


@get(path='/spotify/', sync_to_thread=True)
def spotify_route(spotify_icon: str, title: str, artist: str, album: str | None = None) -> dict[str, str]:
    value = spotify_img(
        spotify_icon,
        SpotifyData(title, artist, album, datetime.datetime.now()),
    )
    return {'image_bytes': str(value)}
