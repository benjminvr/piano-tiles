

import pygame
from src.presentation.game_view import GameView, Color
from src.presentation.input_controller import InputController, GameAction

def ejemplo_1_basico():

    view = GameView(400, 600)
    clock = view.get_clock()

    view.draw_start_screen()
    view.update_display()

    running = True
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.time.get_ticks() - start_time > 3000:
            running = False

        clock.tick(60)

    view.quit()

def ejemplo_2_renderizado_tiles():
    view = GameView(400, 600)
    clock = view.get_clock()
    controller = InputController()

    tiles = [
        {
            'rect': pygame.Rect(0, 100, 100, 150),
            'color': Color.BLACK,
            'clicked': False
        },
        {
            'rect': pygame.Rect(100, 100, 100, 150),
            'color': Color.WHITE,
            'clicked': False
        },
        {
            'rect': pygame.Rect(200, 100, 100, 150),
            'color': Color.WHITE,
            'clicked': False
        },
        {
            'rect': pygame.Rect(300, 100, 100, 150),
            'color': Color.WHITE,
            'clicked': False
        },
    ]

    running = True
    while running:

        actions = controller.process_events()
        for action, data in actions:
            if action == GameAction.QUIT:
                running = False
            elif action == GameAction.CLICK:

                clicked_tile = controller.check_tile_click(data, tiles)
                if clicked_tile:
                    clicked_tile['clicked'] = True
                    print(f"Tile clickeada en posición: {clicked_tile['rect'].x}")

        view.clear_screen()
        view.draw_grid_lines()
        view.draw_tiles(tiles)
        view.draw_score(10)
        view.update_display()

        clock.tick(60)

    view.quit()

def ejemplo_3_animacion_tiles():
    view = GameView(400, 600)
    clock = view.get_clock()
    controller = InputController()

    tile = {
        'rect': pygame.Rect(0, -150, 100, 150),
        'color': Color.BLACK,
        'clicked': False
    }

    tiles = [tile]
    speed = 5
    score = 0

    running = True
    while running and tile['rect'].top < 600:

        actions = controller.process_events()
        for action, data in actions:
            if action == GameAction.QUIT:
                running = False
            elif action == GameAction.CLICK:
                clicked_tile = controller.check_tile_click(data, tiles)
                if clicked_tile and not clicked_tile['clicked']:
                    clicked_tile['clicked'] = True
                    score += 1
                    print(f"¡Click correcto! Score: {score}")

        tile['rect'].y += speed

        view.clear_screen()
        view.draw_grid_lines()
        view.draw_tiles(tiles)
        view.draw_score(score)
        view.update_display()

        clock.tick(60)

    view.quit()

def ejemplo_4_estados_juego():
    view = GameView(400, 600)
    clock = view.get_clock()
    controller = InputController()

    estado = "MENU"
    score = 42
    high_score = 100
    tiles = []

    running = True
    while running:

        actions = controller.process_events()
        for action, data in actions:
            if action == GameAction.QUIT:
                running = False
            elif action == GameAction.START:
                estado = "PLAYING"
            elif action == GameAction.PAUSE:
                if estado == "PLAYING":
                    estado = "PAUSED"
                elif estado == "PAUSED":
                    estado = "PLAYING"
            elif action == GameAction.RESTART:
                estado = "MENU"

        if estado == "PLAYING":

            pass

        if estado == "MENU":
            view.draw_start_screen()
        elif estado == "PLAYING":
            view.clear_screen()
            view.draw_grid_lines()
            view.draw_tiles(tiles)
            view.draw_score(score)
            view.draw_speed_indicator(2.5)
        elif estado == "PAUSED":
            view.clear_screen()
            view.draw_grid_lines()
            view.draw_tiles(tiles)
            view.draw_pause_screen(score)
        elif estado == "GAME_OVER":
            view.clear_screen()
            view.draw_grid_lines()
            view.draw_tiles(tiles)
            view.draw_game_over_screen(score, high_score)

        view.update_display()
        clock.tick(60)

    view.quit()

def ejemplo_5_input_avanzado():
    view = GameView(400, 600)
    clock = view.get_clock()
    controller = InputController()

    tile_width = 100

    running = True
    while running:
        actions = controller.process_events()

        for action, data in actions:
            if action == GameAction.QUIT:
                running = False

            elif action == GameAction.CLICK:

                x, y = data
                column = controller.get_clicked_tile_column(data, tile_width)
                in_area = controller.is_within_game_area(data, 400, 600)

                print(f"Click en ({x}, {y})")
                print(f"  - Columna: {column}")
                print(f"  - Dentro del área: {in_area}")

            elif action == GameAction.START:
                print("¡Juego iniciado!")

            elif action == GameAction.PAUSE:
                print("Juego pausado")

            elif action == GameAction.RESTART:
                print("Reiniciando...")

                controller.reset()

        mouse_pos = controller.get_mouse_position()
        if mouse_pos:
            x, y = mouse_pos

        view.clear_screen()
        if mouse_pos:

            text = f"Mouse: ({x}, {y})"
            small_font = pygame.font.SysFont("arial", 16)
            text_surface = small_font.render(text, True, Color.BLACK)
            view.screen.blit(text_surface, (10, 570))

        view.update_display()
        clock.tick(60)

    view.quit()

def ejemplo_6_personalizacion_visual():
    view = GameView(400, 600)
    clock = view.get_clock()

    tiles = [
        {'rect': pygame.Rect(0, 100, 100, 150), 'color': Color.BLACK, 'clicked': False},
        {'rect': pygame.Rect(100, 100, 100, 150), 'color': Color.WHITE, 'clicked': False},
        {'rect': pygame.Rect(200, 100, 100, 150), 'color': Color.BLUE, 'clicked': False},
        {'rect': pygame.Rect(300, 100, 100, 150), 'color': Color.GREEN, 'clicked': False},
    ]

    running = True
    frames = 0

    while running and frames < 180:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        view.clear_screen(Color.LIGHT_GRAY)

        view.draw_tiles(tiles)

        view.draw_score(frames // 6, 10, 10)
        view.draw_speed_indicator(1.0 + frames / 180.0, 10, 50)

        view.update_display()
        clock.tick(60)
        frames += 1

    view.quit()

def main():
    print("=" * 50)
    print("Ejemplos de Uso - Capa de Presentación")
    print("=" * 50)
    print("\nSelecciona un ejemplo:")
    print("1. Pantalla de inicio básica")
    print("2. Renderizado de tiles")
    print("3. Animación de tiles cayendo")
    print("4. Estados del juego")
    print("5. Input avanzado")
    print("6. Personalización visual")
    print("0. Salir")
    print()

    while True:
        try:
            opcion = input("Opción (0-6): ")

            if opcion == "0":
                print("¡Hasta luego!")
                break
            elif opcion == "1":
                print("\n[Ejecutando Ejemplo 1: Pantalla de inicio]")
                ejemplo_1_basico()
            elif opcion == "2":
                print("\n[Ejecutando Ejemplo 2: Renderizado de tiles]")
                ejemplo_2_renderizado_tiles()
            elif opcion == "3":
                print("\n[Ejecutando Ejemplo 3: Animación]")
                ejemplo_3_animacion_tiles()
            elif opcion == "4":
                print("\n[Ejecutando Ejemplo 4: Estados del juego]")
                ejemplo_4_estados_juego()
            elif opcion == "5":
                print("\n[Ejecutando Ejemplo 5: Input avanzado]")
                ejemplo_5_input_avanzado()
            elif opcion == "6":
                print("\n[Ejecutando Ejemplo 6: Personalización]")
                ejemplo_6_personalizacion_visual()
            else:
                print("Opción no válida. Intenta de nuevo.")

            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()