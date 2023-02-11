from PIL import Image


def blue_shift():
    picture = Image.open("assets/ground.png")

    width, height = picture.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = picture.getpixel((x, y))
            picture.putpixel((x, y), (r - 75, g - 50, b, a))

    picture.save("assets/ground-new.png")


def crop_tiles():
    picture = Image.open("assets/tileSheet.png")
    size = 65
    idx = 1
    for i in range(4):
        for j in range(10):
            im = Image.new(mode="RGBA", size=(size, size))
            for r in range(size):
                for c in range(size):
                    x = min(r + j * size, 648)
                    im.putpixel((r, c), picture.getpixel((x, c + i * size)))
            im.save(f"assets/tile-{idx}.png")
            idx += 1


if __name__ == "__main__":
    crop_tiles()
