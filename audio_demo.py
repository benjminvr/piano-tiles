

import pygame
import sys
import time

from src.infrastructure.pygame_audio import PygameAudio
from audio_config import SONGS, list_available_songs

def demo_single_song(song_id):
    if song_id not in SONGS:
        print(f"❌ Canción '{song_id}' no encontrada")
        return

    song = SONGS[song_id]
    print(f"\n🎵 Reproduciendo: {song['name']}")
    print(f"   Notas: {' - '.join(song['notes'])}")
    print(f"   {song['description']}")
    print("\n   Escuchando...")

    audio = PygameAudio(note_sequence=song['notes'])

    for i in range(4):
        print(f"   ♪ Nota {i+1}: {song['notes'][i]}")
        audio.play_note_for_column(i)
        time.sleep(0.6)

    print("   ♫ Acorde completo...")
    for i in range(4):
        audio.play_note_for_column(i)

    time.sleep(1.5)
    print("   ✓ Completado\n")

def demo_all_songs():
    print("\n" + "="*70)
    print("🎼 DEMO DE TODAS LAS CANCIONES")
    print("="*70)
    print("\nEsto puede tomar algunos minutos...")
    print("Presiona Ctrl+C para cancelar\n")

    try:
        for song_id in SONGS.keys():
            demo_single_song(song_id)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo cancelada por el usuario")

def interactive_demo():
    pygame.init()

    while True:
        print("\n" + "="*70)
        print("🎹 PIANO TILES - DEMO INTERACTIVO DE AUDIO")
        print("="*70)
        print("\nOpciones:")
        print("  1. Ver lista de canciones disponibles")
        print("  2. Escuchar una canción específica")
        print("  3. Demo de todas las canciones")
        print("  4. Modo prueba de teclado (tocar libremente)")
        print("  0. Salir")
        print()

        try:
            opcion = input("Selecciona una opción (0-4): ").strip()

            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break

            elif opcion == "1":
                list_available_songs()
                input("\nPresiona Enter para continuar...")

            elif opcion == "2":
                list_available_songs()
                song_id = input("\nIngresa el ID de la canción: ").strip()
                demo_single_song(song_id)
                input("Presiona Enter para continuar...")

            elif opcion == "3":
                confirm = input("\n⚠️  Esto reproducirá todas las canciones. ¿Continuar? (s/n): ")
                if confirm.lower() == 's':
                    demo_all_songs()
                input("\nPresiona Enter para continuar...")

            elif opcion == "4":
                keyboard_test_mode()

            else:
                print("\n❌ Opción no válida")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(2)

def keyboard_test_mode():
    print("\n" + "="*70)
    print("⌨️  MODO PRUEBA DE TECLADO")
    print("="*70)

    list_available_songs()
    song_id = input("\nIngresa el ID de la canción (o Enter para 'c_major'): ").strip()

    if not song_id or song_id not in SONGS:
        song_id = 'c_major'

    song = SONGS[song_id]
    print(f"\n🎵 Canción seleccionada: {song['name']}")
    print(f"   Notas: {' - '.join(song['notes'])}")

    audio = PygameAudio(note_sequence=song['notes'])

    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption(f"Piano Tiles - {song['name']}")

    font = pygame.font.SysFont("arial", 24)

    print("\n📖 Instrucciones:")
    print("   Teclas 1-4: Tocar notas 1-4")
    print("   ESC: Salir")
    print("\n🎹 ¡Toca el piano!\n")

    running = True
    last_notes = ["", "", "", ""]

    while running:

        screen.fill((30, 30, 30))

        title = font.render(song['name'], True, (255, 255, 255))
        screen.blit(title, (200 - title.get_width()//2, 20))

        keys = ["1", "2", "3", "4"]
        key_width = 80
        key_height = 100
        gap = 10
        start_x = (400 - (key_width * 4 + gap * 3)) // 2

        for i, (key, note) in enumerate(zip(keys, song['notes'])):
            x = start_x + i * (key_width + gap)
            y = 70

            color = (200, 200, 200)
            if last_notes[i]:
                color = (100, 255, 100)

            pygame.draw.rect(screen, color, (x, y, key_width, key_height))
            pygame.draw.rect(screen, (50, 50, 50), (x, y, key_width, key_height), 2)

            key_text = font.render(key, True, (0, 0, 0))
            note_text = font.render(note, True, (0, 0, 0))

            screen.blit(key_text, (x + key_width//2 - key_text.get_width()//2, y + 20))
            screen.blit(note_text, (x + key_width//2 - note_text.get_width()//2, y + 60))

        pygame.display.flip()

        for i in range(4):
            if last_notes[i]:
                last_notes[i] = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_1:
                    audio.play_note_for_column(0)
                    last_notes[0] = "active"
                    print(f"♪ Nota 1: {song['notes'][0]}")

                elif event.key == pygame.K_2:
                    audio.play_note_for_column(1)
                    last_notes[1] = "active"
                    print(f"♪ Nota 2: {song['notes'][1]}")

                elif event.key == pygame.K_3:
                    audio.play_note_for_column(2)
                    last_notes[2] = "active"
                    print(f"♪ Nota 3: {song['notes'][2]}")

                elif event.key == pygame.K_4:
                    audio.play_note_for_column(3)
                    last_notes[3] = "active"
                    print(f"♪ Nota 4: {song['notes'][3]}")

        pygame.time.Clock().tick(60)

    pygame.quit()
    print("\n✓ Modo teclado finalizado\n")

def main():
    try:
        interactive_demo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()