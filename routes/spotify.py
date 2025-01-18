from __future__ import annotations

import copy

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from _types import SpotifyData

BASE_IMAGE_SIZE = (512, 512)
BACKGROUND_IMAGE_SIZE = (1024, 1024)

BRIGHTNESS = 0.25

IMAGE_COVER_PASTE_AREA = (256, 256, 768, 768)

FONT = ImageFont.truetype('assets/DejaVuSans-Bold.ttf')

TITLE_COORDS = (512, 832)


_Ink = float | tuple[int, ...] | str


def spotify_img(spotify_icon: str, data: SpotifyData):
    image = Image.open(spotify_icon, mode='r').resize(BASE_IMAGE_SIZE)

    _image_resized: _Ink | None = image.resize((1, 1)).getpixel((1, 1))
    if _image_resized is None:
        msg = 'Expected a full image'
        raise TypeError(msg)

    bg = Image.open(spotify_icon).resize(BACKGROUND_IMAGE_SIZE)

    e = ImageEnhance.Brightness(bg)
    bg = e.enhance(BRIGHTNESS).filter(ImageFilter.BLUR)

    bg.paste(image, IMAGE_COVER_PASTE_AREA)

    draw = ImageDraw.Draw(bg)

    font = copy.copy(FONT)
    font.size = 48
    draw.text(TITLE_COORDS, text=data.title, font=FONT, fill=_image_resized, anchor='mm')


#    dr.text((512, 1024 - 256 + 128), text='By ' + ', '.join(act.artists), font=fntt, fill=x, anchor='mm')
#    dr.text((512, 1024 - 256 + 192), text='On ' + act.album, font=fntt, fill=x, anchor='mm')
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
#    buffer = BytesIO()
#    im.save(buffer, 'png')
#    buffer.seek(0)
#    return buffer
