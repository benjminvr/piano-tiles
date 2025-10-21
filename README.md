# Piano Tiles en Python

Este proyecto implementa una versión simplificada del juego **Piano Tiles** en **Python** usando **Pygame** para la interfaz gráfica.  
La solución se estructura con una **arquitectura en capas** y sigue una **topología cliente-servidor**

---

## Estructura del Proyecto

```plaintext
piano_tiles/
├── app.py
├── src/
│   ├── presentation/                # Capa de Presentación (UI con Pygame)
│   │   ├── game_view.py
│   │   └── input_controller.py
│   ├── application/                 # Casos de uso (lógica de aplicación)
│   │   ├── start_game.py
│   │   ├── update_game.py
│   │   └── submit_score.py
│   ├── domain/                      # Reglas de negocio puras
│   │   ├── entities.py              # Entidades: Tile, Board, GameState, Score
│   │   ├── services.py              # Generación de tiles, validación de jugadas
│   │   └── ports.py                 # Interfaces
│   └── infrastructure/              
│       ├── leaderboard_api.py       # Cliente HTTP para Leaderboard remoto
│       ├── leaderboard_local.py     # Persistencia local alternativa (JSON/SQLite)
│       ├── pygame_audio.py          # Implementación de AudioPort
│       └── system_clock.py          # Implementación de ClockPort
└── server/
    ├── main.py                      # Servidor FastAPI/Flask (leaderboards)
    └── repositories.py              # Repositorios en memoria o SQLite
```

##  Arquitectura en Capas

- **Capa de Presentación (`presentation/`)**  David, rodrigo, antonio 
  - Interfaz con el usuario: dibuja la pantalla, captura teclas.  
  - Nunca contiene reglas de negocio, solo interacción gráfica.  

- **Capa de Aplicación (`application/`)**  
  - Casos de uso que coordinan al dominio.  
  - Ejemplos: iniciar partida, procesar ticks, registrar puntaje.  

- **Capa de Dominio (`domain/`)**  
  - Reglas puras del juego (entidades y servicios).  
  - Independiente de librerías externas (testable sin Pygame ni HTTP).  

- **Capa de Infraestructura (`infrastructure/`)**  
  - Adaptadores concretos a puertos (Pygame, API REST, JSON, etc.).  

- **Servidor (`server/`)**  
  - Exposición REST del leaderboard.  
  - Implementación sencilla para pruebas y despliegue local.
 
 ## Equipo y Roles

En este proyecto se identificó un **líder de equipo** y cada integrante tiene un rol definido asociado a una capa o módulo de la arquitectura.

| Integrante                | Rol / Responsabilidad                         | Capa o Módulo Asociado |
|----------------------------|-----------------------------------------------|-------------------------|
| Benjamin Vergara        | **Líder del proyecto**: coordinación general, revisiones y entregas | Global |
| David Hernandez / Antonio Pelayo / Rodrigo Leon  | Desarrollo de la interfaz (UI y control de entrada) | Presentation |
| [Santiago Ortiz]      | Implementación de casos de uso y lógica de orquestación | Application |
| daniel, Santiago      | Definición de entidades y reglas del negocio (tiles, puntuación) | Domain |
| [Nombre integrante 4]      | Adaptadores: leaderboard local/API, audio, reloj | Infrastructure |
| Luis Acosta / Benjamin Vergara      | Implementación y despliegue del servidor FastAPI/Flask | Server |
