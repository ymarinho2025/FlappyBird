import pygame
import os
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

screenWidth = 500
screenHeight = 800

pipeImage = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
floorImage = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'floor.png')))
backgroundImage = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
birdImage = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png'))),
]

pointsFonts = pygame.font.SysFont('arial', 50)

class Bird:
    img = birdImage
    # animações de rotação
    maxRotation = 25
    fastRotation = 20
    animationTime = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.countImage = 0
        self.image = self.img[0]
        
    def jump(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
       
        # Usar formula do sorvete # S = Vo * t + (1/2) * a * t²
        
    def move(self):
        
        # Calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        
        # Reestringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
            
        self.y += deslocamento
            
        # Angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.maxRotation:
                self.angulo = self.fastRotation
            else:
                if self.angulo > -90:
                    self.angulo -= self.fastRotation
                    
    def draw(self, screen):
        # definir qual imagem do passaro usar    
        self.countImage += 1
    
        if self.countImage < self.animationTime:
            self.image = self.img[0]
        elif self.countImage < self.animationTime*2:
            self.image = self.img[1]
        elif self.countImage < self.animationTime*3:
            self.image = self.img[2]
        elif self.countImage < self.animationTime*4:
            self.image = self.img[1]
        elif self.countImage >= self.animationTime*4 + 1:
            self.image = self.img[0]
            self.countImage = 0
            
        # se o passaro tiver caindo não bater asa
        if self.angulo <= -80:
            self.image = self.img[1]
            self.countImage = self.animationTime*2
            
        # desenhar a imagem
        routationImage = pygame.transform.rotate(self.image, self.angulo)
        imageCenter = self.image.get_rect(topleft=(self.x, self.y)).center
        retangle = routationImage.get_rect(center=imageCenter)
        screen.blit(routationImage, retangle.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    distance = 200
    speed = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        # pos para position
        self.posTop = 8
        self.posBottom = 8
        self.pipeTop = pygame.transform.flip(pipeImage, False, True)
        self.pipeBottom = pipeImage
        self.passed = False
        self.defineHeight()
        
    def defineHeight(self):
        self.height = random.randrange(50, 450)
        self.posTop = self.height - self.pipeTop.get_height()
        self.posBottom = self.height + self.distance
        
    def move(self):
        self.x -= self.speed
        
    def draw(self, screen):
        screen.blit(self.pipeTop, (self.x, self.posTop))
        screen.blit(self.pipeBottom, (self.x, self.posBottom))
        
    def crash(self, bird):
        birdMask = bird.get_mask()
        maskTop = pygame.mask.from_surface(self.pipeTop)
        maskBottom = pygame.mask.from_surface(self.pipeBottom)
        
        distanceTop = (self.x - round(bird.x), self.posTop - round(bird.y))
        distanceBottom = (self.x - round(bird.x), self.posBottom - round(bird.y))
        
        # verdadeiro ou falso
        pointTop = birdMask.overlap(maskTop, distanceTop)
        pointBottom = birdMask.overlap(maskBottom, distanceBottom)
        
        if pointBottom or pointTop:
            return True
        else:
            return False
        
class Floor:
    speed = 5
    width = floorImage.get_width()
    image = floorImage
    
    def __init__(self, y):
        self.y = y
        # x1 = chão 1 e x2 = chão 2
        self.x1 = 0
        self.x2 = self.width
        
    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        elif self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
            
    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))
        
def drawScreen(screen, birds, pipes, floor, points, game_over, tempo_restante):
    screen.blit(backgroundImage, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    
    text = pointsFonts.render(f"Pontuação: {points}", 1, (0, 255, 0))
    screen.blit(text, (screenWidth - 10 - text.get_width(), 10))

    if game_over:
        text = pointsFonts.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (screenWidth//2 - text.get_width()//2, screenHeight//2))

        timer_text = pointsFonts.render(f"Reiniciando em {tempo_restante}", True, (255, 255, 255))
        screen.blit(timer_text, (screenWidth//2 - timer_text.get_width()//2, screenHeight//2 + 60))
    
    floor.draw(screen)
    pygame.display.update()
    
def main():
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.03)  # 0.0 a 1.0
    
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode([screenWidth, screenHeight])
    points = 0
    clock = pygame.time.Clock()
    
    running = True
    game_over = False
    game_over_time = 0
    
    while running:
        clock.tick(30)
        # interação do usúario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
                        
        # mover as coisas
        for bird in birds:
            bird.move()
        floor.move()
        
        addPipe = False
        removePipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.crash(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    addPipe = True
            pipe.move()
            if pipe.x + pipe.pipeTop.get_width() < 0:
                removePipes.append(pipe)
        
        if addPipe:
            points += 1
            pipes.append(Pipe(600))
        for pipe in removePipes:
            pipes.remove(pipe)
            
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
        
        if len(birds) == 0 and not game_over:
            game_over = True
            game_over_time = pygame.time.get_ticks()
        
        tempo_restante = 0

        if game_over:
            tempo_atual = pygame.time.get_ticks()
            tempo_passado = (tempo_atual - game_over_time) // 1000
            tempo_restante = max(0, 3 - tempo_passado)

            if tempo_atual - game_over_time > 3000:
                return
    
        drawScreen(screen, birds, pipes, floor, points, game_over, tempo_restante)
        
if __name__ == '__main__':
    while True:
        main()