# this allows us to use code from
# the open-source pygame library
# throughout this file

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot


def main():
    def reset_game():
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()

        asteroid_field = AsteroidField()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        return False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    paused = False
    p_key_pressed = False
    game_over = False

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Shot.containers = (shots, drawable, updatable)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not p_key_pressed and not game_over:
            paused = not paused
            print("Game is " + ("paused" if paused else "unpaused"))
        p_key_pressed = keys[pygame.K_p]

        if game_over and keys[pygame.K_RETURN]:
            game_over = reset_game()
            paused = False
            continue

        if not paused and not game_over:
            for obj in updatable:
                obj.update(dt)

            for asteroid in asteroids:
                if asteroid.is_colliding(player):
                    game_over = True
                for shot in shots:
                    if asteroid.is_colliding(shot):
                        asteroid.split()
                        shot.kill()

            dt = clock.tick(60) / 1000
        else:
            clock.tick(60)
            dt = 0

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        if paused:
            font = pygame.font.Font(None, 74)
            text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, text_rect)

        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, text_rect)

            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press RETURN to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
