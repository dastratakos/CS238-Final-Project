for i in range (10):
    with open(f"maps-orig/{i}.prop", "r") as f:
        width, height, hue = [int(line.split(":")[1].strip()) for line in f.readlines()]
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