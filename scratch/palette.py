import pygame

image = pygame.image.load("assets/palette.png")

w, h = image.get_size()
x_vals = []
for start in [567, 1000, 1434, 1867]:
    x_vals.extend(list(range(start, start + 350, 100)))
y_vals = []
for start in [463, 792]:
    y_vals.extend(list(range(start, start + 250, 100)))
for y in y_vals:
    for x in x_vals:
        r, g, b, a = image.get_at((x, y))
        print(f"    ({r}, {g}, {b}),")
        for r in range(-3, 4):
            for c in range(-3, 4):
                if abs(r) != 3 and abs(c) != 3:
                    continue
                image.set_at((x + r, y + c), pygame.Color(255, 0, 0, 255))

pygame.init()
size = image.get_size()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((43, 91, 168))

    screen.blit(image, (0, 0))

    pygame.display.flip()

pygame.quit()
exit()
