import pygame



def main():
    x = 0
    y = 0
    width = 50
    height = 50
    thickness = 5
    color = (255, 255, 255)
    pygame.init()
    # clock = pygame.time.Clock()

    screen = pygame.display.set_mode((500, 500))
    end_game = False

    while not end_game:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                end_game = True
        
        screen.fill((0, 0, 0))
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, color, (i*width,j*height,width,height), thickness)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
