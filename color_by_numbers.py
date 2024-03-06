# color_by_numbers.py
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pydantic import BaseModel, FilePath, PositiveInt, StrictBool
import math 

class ColorByNumbersConfig(BaseModel):
    image_path: FilePath
    pixel_size: PositiveInt
    colors: PositiveInt = 12
    outline: StrictBool
    fill: StrictBool

def enhance_image(img):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.8)  # Adjust the saturation
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Adjust the contrast
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # Adjust the brightness
    return img

def resize_image(img, pixel_size):
    width, height = img.size
    new_width = width // pixel_size
    new_height = height // pixel_size
    img = img.resize((new_width, new_height), resample=Image.BILINEAR)
    img = img.resize((width, height), resample=Image.NEAREST)
    return img

def quantize_colors(img, colors):
    img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
    palette = img.getpalette()[:colors * 3]
    palette = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]
    return img, palette

def adjust_font_size_to_fit(font_name, initial_font_size, max_width, max_height, text):
    font_size = initial_font_size
    temp_image = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)

    while True:
        font = ImageFont.truetype(font_name, font_size)
        text_width, text_height = temp_draw.textsize(text, font)

        if text_width <= max_width and text_height <= max_height:
            break

        font_size -= 1
        if font_size <= 1:
            break

    final_font = ImageFont.truetype(font_name, font_size)
    return final_font

def draw_color_by_numbers(img, palette, pixel_size, outline_option, fill_option):
    color_by_numbers = Image.new('RGB', img.size, color='white')
    draw = ImageDraw.Draw(color_by_numbers)
    font = ImageFont.truetype('Arial', 16)  # Adjust path as necessary
    block_size = pixel_size

    for x in range(0, img.size[0], block_size):
        for y in range(0, img.size[1], block_size):
            color_index = img.getpixel((x, y))
            color = palette[color_index]

            # Determine fill color
            fill_color = color if fill_option else None

            # Determine outline
            outline_color = 'black' if outline_option else None

            draw.rectangle(
                (x, y, x + block_size, y + block_size),
                fill=fill_color,
                outline=outline_color,
                width=1 if outline_option else 0
            )
          # Adjust font size to fit within the block
            #font = adjust_font_size_to_fit('Arial', 16, block_size - 4, block_size - 4, str(color_index + 1))
           # draw.text((x + 4, y + 4), str(color_index + 1), font=font, fill='black')

            draw.text((x + 4, y + 4), str(color_index + 1), font=font, fill='black')

    return color_by_numbers

def create_color_by_numbers(config):
    print(config)
    img = Image.open(config.image_path)
    img = enhance_image(img)
    img = resize_image(img, config.pixel_size)
    img, palette = quantize_colors(img, config.colors)
    color_by_numbers = draw_color_by_numbers(
        img, 
        palette, 
        config.pixel_size, 
        config.outline,
        config.fill)
    return color_by_numbers, palette


def create_color_palette_image(color_palette):
    # Parameters for each color block and text
    block_size = 16  # Size of the color block
    text_height = 16  # Space for the text
    padding = 2  # Space between color blocks and text

    # Calculate grid size
    num_colors = len(color_palette)
    cols = int(math.ceil(math.sqrt(num_colors)))
    rows = math.ceil(num_colors / cols)

    # Image size
    image_width = cols * block_size
    image_height = rows * (block_size + text_height + padding)
    color_palette_image = Image.new('RGB', (image_width, image_height), color='white')

    # Load a font for the color index
    font = ImageFont.truetype('Arial', 12)  # Adjust font size as needed

    # Draw the color blocks and index numbers
    draw = ImageDraw.Draw(color_palette_image)
    for i, color in enumerate(color_palette):
        col = i % cols
        row = i // cols
        x = col * block_size
        y = row * (block_size + text_height + padding)

        draw.rectangle((x, y, x + block_size, y + block_size), fill=color)
        draw.text((x + padding, y + block_size + padding), str(i + 1), font=font, fill='black')

    return color_palette_image
