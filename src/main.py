import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'domain'))
from song import SongManager

pygame.init()

WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tiles - Song Mode")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)

TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 150
TILE_SPEED = 4

clock = pygame.time.Clock()
tiles = []
running = True
game_over = False
score = 0
speed = TILE_SPEED
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 36)

song_manager = SongManager(os.path.join(os.path.dirname(__file__), '..', 'songs.json'))
game_start_time = 0
game_state = "menu"
selected_song_index = 0
available_songs = song_manager.get_available_songs()

def spawn_tile_from_song():
    current_song = song_manager.get_current_song()
    if not current_song or not current_song.has_more_notes():
        return False
    
    current_time = (pygame.time.get_ticks() - game_start_time) / 1000.0
    next_note = None
    
    for i in range(current_song.current_note_index, len(current_song.notes)):
        note = current_song.notes[i]
        spawn_time = note['time'] - 2.0
        
        if current_time >= spawn_time:
            if i == current_song.current_note_index:
                next_note = current_song.get_next_note()
                break
        else:
            break
    
    if next_note:
        column = next_note['column']
        for i in range(4):
            color = BLACK if i == column else WHITE
            rect = pygame.Rect(i * TILE_WIDTH, -TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
            tiles.append({"rect": rect, "color": color, "clicked": False, "note_time": next_note['time']})
        return True
    return False

def draw_menu():
    SCREEN.fill(WHITE)
    title = big_font.render("Piano Tiles - Song Mode", True, BLACK)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    instructions = font.render("Selecciona una cancion:", True, BLACK)
    SCREEN.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 150))
    
    for i, song_id in enumerate(available_songs):
        song = song_manager.songs[song_id]
        color = BLUE if i == selected_song_index else BLACK
        song_text = font.render(f"{i+1}. {song.name}", True, color)
        difficulty_text = font.render(f"[{song.difficulty}]", True, color)
        
        y_pos = 200 + i * 50
        SCREEN.blit(song_text, (50, y_pos))
        SCREEN.blit(difficulty_text, (50, y_pos + 25))
    
    controls1 = font.render("Flechas: Navegar | Enter: Seleccionar", True, GRAY)
    controls2 = font.render("Durante el juego: Click en tiles negros", True, GRAY)
    SCREEN.blit(controls1, (WIDTH//2 - controls1.get_width()//2, HEIGHT - 80))
    SCREEN.blit(controls2, (WIDTH//2 - controls2.get_width()//2, HEIGHT - 50))

def draw_tiles():
    for tile in tiles:
        pygame.draw.rect(SCREEN, tile["color"], tile["rect"])
        pygame.draw.rect(SCREEN, GRAY, tile["rect"], 2)

def reset_game():
    global tiles, score, speed, game_over, game_start_time
    tiles.clear()
    score = 0
    speed = TILE_SPEED
    game_over = False
    game_start_time = pygame.time.get_ticks()
    current_song = song_manager.get_current_song()
    if current_song:
        current_song.reset()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_song_index = (selected_song_index - 1) % len(available_songs)
                elif event.key == pygame.K_DOWN:
                    selected_song_index = (selected_song_index + 1) % len(available_songs)
                elif event.key == pygame.K_RETURN:
                    song_id = available_songs[selected_song_index]
                    song_manager.select_song(song_id)
                    game_state = "playing"
                    reset_game()

        elif game_state == "playing":
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                    elif event.key == pygame.K_m:
                        game_state = "menu"
                        game_over = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for tile in tiles:
                    if tile["rect"].collidepoint(x, y) and not tile["clicked"]:
                        if tile["color"] == BLACK:
                            tile["color"] = GREEN
                            tile["clicked"] = True
                            score += 10
                        else:
                            game_over = True
                        break

    if game_state == "menu":
        draw_menu()
    
    elif game_state == "playing":
        SCREEN.fill(WHITE)
        
        if game_over:
            current_song = song_manager.get_current_song()
            song_name = current_song.name if current_song else "Cancion"
            
            text = big_font.render("Game Over!", True, RED)
            score_text = font.render(f"Puntuacion: {score}", True, BLACK)
            song_text = font.render(f"Cancion: {song_name}", True, BLACK)
            restart_text = font.render("R: Reiniciar | M: Menu", True, GRAY)
            
            SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
            SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))
            SCREEN.blit(song_text, (WIDTH//2 - song_text.get_width()//2, HEIGHT//2))
            SCREEN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
        else:
            spawn_tile_from_song()

            for tile in tiles:
                tile["rect"].y += speed

            for tile in tiles:
                if tile["rect"].bottom >= HEIGHT and tile["color"] == BLACK and not tile["clicked"]:
                    game_over = True
                    break

            tiles = [t for t in tiles if t["rect"].top < HEIGHT]

            draw_tiles()
            
            current_song = song_manager.get_current_song()
            song_name = current_song.name if current_song else "Sin cancion"
            
            score_text = font.render(f"Puntuacion: {score}", True, BLACK)
            song_text = font.render(f"Cancion: {song_name}", True, BLACK)
            SCREEN.blit(score_text, (10, 10))
            SCREEN.blit(song_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()