import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
deltatime = 0
running = True

#Player Values
player = {
  "x": 5, 
  "y": 5,
  "width": 25,
  "height": 25,
  "speed": 5
}

def key_presses(keys):
  if keys[pygame.K_d]:
    player["x"] += player.get("speed")
  elif keys[pygame.K_a]:
    player["x"] -= player.get("speed")
  if keys[pygame.K_s]:
    player["y"] += player.get("speed")
  if keys[pygame.K_w]:
    player["y"] -= player.get("speed")
  
def mouse_click():
  mx,my=pygame.mouse.get_pos()
  bullet = {
    "x": player.get("x"),
    "y": player.get("y"),
    "target_x": mx,
    "target_y": my
	}

while running:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONUP:
      mouse_click()
    if event.type == pygame.QUIT:
      running = False

  screen.fill("white")
  
  key_presses(pygame.key.get_pressed())

  square = pygame.Rect(player.get("x"), player.get("y"), player.get("width"), player.get("height"))
  pygame.draw.rect(screen, "black", square)

  pygame.display.flip()
  deltatime = clock.tick(60) / 1000
  
pygame.quit()