from pygame import *
import random
 
init()
screen = display.set_mode((0,0), FULLSCREEN)
sx, sy = screen.get_size()
 
wx, wy = 4000, 4000
worldmap = Surface((wx, wy))
 
worldmap.fill((40, 40, 40))
for _ in range(1000):
        c = random.randint(20, 60)
        x = random.randint(0, wx)
        y = random.randint(0, wy)
        r = random.randint(wx // 20, wx // 10)
        draw.circle(worldmap, (c, c, c), (x, y), r)
 
playing = True
px, py = wx // 2, wy // 2
clock = time.Clock()
f = font.Font(None, 64)
while not any(e.type == KEYDOWN and e.key == K_ESCAPE for e in event.get()):
        dt = 0.001 * clock.tick()
        k = key.get_pressed()
       
        # Player position in world coordinates
        px += (k[K_RIGHT] - k[K_LEFT]) * 1000 * dt
        py += (k[K_DOWN] - k[K_UP]) * 1000 * dt
        px = min(max(px, 0), wx)
        py = min(max(py, 0), wy)
 
        # Camera position (ie center of the screen in world coordinates)
        cx = min(max(px, sx//2), wx-sx//2)
        cy = min(max(py, sy//2), wy-sy//2)
 
        # draw world map
        screen.blit(worldmap, (sx//2 - cx, sy//2 - cy))
        # draw player
        draw.circle(screen, (0, 0, 100), (int(sx//2 + px - cx), int(sy//2 + py - cy)), 20)
        # fps counter
        screen.blit(f.render("%.1ffps" % clock.get_fps(), True, (255, 255, 255)), (0, 0))
 
        display.flip()
 
quit()
