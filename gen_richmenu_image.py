from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

font_path = "temp/TanukiMagic.ttf"
illust_path = "temp/smartphone_map_app_woman.png"
richmenu_size = (2500, 843)

richmenu_image_path = Path("asset/richmenu/default.png")

im = Image.new("RGBA", richmenu_size, (200, 255, 200, 255))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype(font_path, 320)

text_options = {
    "text": "位置情報を\n送信する",
    "align": "center",
    "font": font,
    "anchor": "mm",
}
bbox = draw.textbbox((0, 0), **text_options)
draw.text((bbox[2]+100, 843/2), **text_options, fill=(0,0,0,255))

im_illust=Image.open(illust_path)
im_illust.thumbnail(richmenu_size)
im_illust2 = Image.new("RGBA", richmenu_size)
im_illust2.paste(im_illust, (richmenu_size[0] - im_illust.size[0], 0))

im = Image.alpha_composite(im, im_illust2)
# im = im_illust

richmenu_image_path.parent.mkdir(parents=True, exist_ok=True)
im.convert("RGB")
im.save(richmenu_image_path)
