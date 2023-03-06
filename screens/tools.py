import csv
from PIL import Image


def blue_shift():
    picture = Image.open("assets/ground.png")

    width, height = picture.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = picture.getpixel((x, y))
            picture.putpixel((x, y), (r - 75, g - 50, b, a))

    picture.save("assets/ground-new.png")


def crop_elements():
    picture = Image.open("assets/elements/element-sheet.png")
    size = 65
    idx = 1
    for i in range(4):
        for j in range(10):
            im = Image.new(mode="RGBA", size=(size, size))
            for r in range(size):
                for c in range(size):
                    x = min(r + j * size, 648)
                    im.putpixel((r, c), picture.getpixel((x, c + i * size)))
            im.save(f"assets/elements/element-{idx}.png")
            idx += 1


def crop_players():
    picture = Image.open("assets/players/player-sheet.png")
    size = 60
    border = 1
    idx = 1
    for i in range(2):
        for j in range(10):
            im = Image.new(mode="RGBA", size=(size, size))
            for r in range(size):
                for c in range(size):
                    im.putpixel(
                        (r, c),
                        picture.getpixel(
                            (r + j * (size + border), c + i * (size + border))
                        ),
                    )
            im.save(f"assets/players/player-{idx}.png")
            idx += 1


def convert_map():
    for i in range(10):
        with open(f"maps-orig/{i}.prop", "r") as f:
            width, height, hue = [
                int(line.split(":")[1].strip()) for line in f.readlines()
            ]
        with open(f"maps-orig/{i}.save", "r") as f:
            map = [[0 for _ in range(width)] for _ in range(height)]
            cell = 0
            for line in f.readlines():
                value = int(line.strip())
                # map[cell % height][cell // height] = value
                map[cell // width][cell % width] = value
                cell += 1
        with open(f"maps/{i}.csv", "w") as f:
            for row in map:
                f.write(",".join([str(value) for value in row]) + "\n")


def crop_map(infile, outfile, start_col, end_col):
    with open(infile) as f:
        reader = csv.reader(f)
        map = []
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map.append(r)

    with open(outfile, "w") as f:
        for row in map:
            f.write(",".join([str(value) for value in row[start_col:end_col]]) + "\n")


def join_maps(infile1, infile2, outfile):
    with open(infile1) as f:
        reader = csv.reader(f)
        map = []
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map.append(r)

    with open(infile2) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map[i].extend(r)
            i += 1

    with open(outfile, "w") as f:
        for row in map:
            f.write(",".join([str(value) for value in row]) + "\n")
            
def remove_col(infile, outfile, col):
    with open(infile) as f:
        reader = csv.reader(f)
        map = []
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map.append(r)

    with open(outfile, "w") as f:
        for row in map:
            row.pop(col)
            f.write(",".join([str(value) for value in row]) + "\n")


if __name__ == "__main__":
    remove_col("maps/2-easy.csv", "maps/2-easy-2.csv", 250)
