# main.py
import argparse
from color_by_numbers import ColorByNumbersConfig, create_color_by_numbers, create_color_palette_image
from PIL import Image

def save_image(img, filename):
    img.save(filename)
    print(f"Image saved as {filename}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Create a color-by-numbers image from an input image.")
    parser.add_argument("image_path", type=str, help="Path to the input image file")
    parser.add_argument("-p", "--pixel-size", type=int, default=20, help="Size of each pixel in the pixel art image (default: 20)")
    parser.add_argument("-c", "--colors", type=int, default=8, help="Number of colors to reduce the image to (default: 8)")
    parser.add_argument("-o", "--outline", action=argparse.BooleanOptionalAction, default=False,  help="Do not draw an outline around each pixel")
    parser.add_argument("-f", "--fill", action=argparse.BooleanOptionalAction, default=False,  help="Fill each pixel with color instead of drawing an outline")
    return parser.parse_args()

def main():
    args = parse_arguments()
    print(args)
    config = ColorByNumbersConfig(
        image_path=args.image_path,
        pixel_size=args.pixel_size,
        colors=args.colors,
        outline=args.outline,
        fill=args.fill
    )

    color_by_numbers_image, color_palette = create_color_by_numbers(config)
    save_image(color_by_numbers_image, "images/color_by_numbers.png")
    color_palette_image = create_color_palette_image(color_palette)
    save_image(color_palette_image, "images/color_palette.png")

if __name__ == "__main__":
    main()