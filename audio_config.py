SONGS = {
    'c_major': {
        'name': 'Do Mayor',
        'notes': ['C4', 'E4', 'G4', 'C5'],
        'description': 'Acorde de Do Mayor (C-E-G-C) - Alegre y brillante'
    },

    'g_major': {
        'name': 'Sol Mayor',
        'notes': ['G3', 'B3', 'D4', 'G4'],
        'description': 'Acorde de Sol Mayor (G-B-D-G) - Cálido y resonante'
    },

    'f_major': {
        'name': 'Fa Mayor',
        'notes': ['F4', 'A4', 'C5', 'F5'],
        'description': 'Acorde de Fa Mayor (F-A-C-F) - Suave y armonioso'
    },

    'd_major': {
        'name': 'Re Mayor',
        'notes': ['D4', 'F4', 'A4', 'D5'],
        'description': 'Acorde de Re Mayor (D-F#-A-D) - Energético'
    },

    'a_minor': {
        'name': 'La Menor',
        'notes': ['A3', 'C4', 'E4', 'A4'],
        'description': 'Acorde de La Menor (A-C-E-A) - Melancólico y suave'
    },

    'e_minor': {
        'name': 'Mi Menor',
        'notes': ['E4', 'G4', 'B4', 'E5'],
        'description': 'Acorde de Mi Menor (E-G-B-E) - Oscuro y profundo'
    },

    'd_minor': {
        'name': 'Re Menor',
        'notes': ['D4', 'F4', 'A4', 'D5'],
        'description': 'Acorde de Re Menor (D-F-A-D) - Dramático'
    },

    'pentatonic': {
        'name': 'Pentatónica',
        'notes': ['C4', 'D4', 'E4', 'G4'],
        'description': 'Escala Pentatónica - Sonido asiático/oriental'
    },

    'chromatic': {
        'name': 'Cromática',
        'notes': ['C4', 'D4', 'E4', 'F4'],
        'description': 'Escala Cromática ascendente - Progresión suave'
    },

    'ascending': {
        'name': 'Ascendente',
        'notes': ['C4', 'E4', 'G4', 'B4'],
        'description': 'Melodía ascendente - Sensación de elevación'
    },

    'descending': {
        'name': 'Descendente',
        'notes': ['C5', 'A4', 'F4', 'C4'],
        'description': 'Melodía descendente - Sensación de calma'
    },

    'twinkle': {
        'name': 'Estrellita',
        'notes': ['C4', 'C4', 'G4', 'G4'],
        'description': 'Inspirada en "Twinkle Twinkle Little Star"'
    },

    'ode_to_joy': {
        'name': 'Himno a la Alegría',
        'notes': ['E4', 'E4', 'F4', 'G4'],
        'description': 'Inspirada en Beethoven - Himno a la Alegría'
    },

    'happy_birthday': {
        'name': 'Cumpleaños Feliz',
        'notes': ['C4', 'C4', 'D4', 'C4'],
        'description': 'Inspirada en "Happy Birthday"'
    },

    'bass_rhythm': {
        'name': 'Ritmo Bajo',
        'notes': ['C3', 'C3', 'G3', 'G3'],
        'description': 'Patrón de bajo - Sonido grave y potente'
    },

    'high_energy': {
        'name': 'Alta Energía',
        'notes': ['C5', 'D5', 'E5', 'G5'],
        'description': 'Notas agudas - Energético y brillante'
    },

    'blues': {
        'name': 'Blues',
        'notes': ['C4', 'E4', 'F4', 'G4'],
        'description': 'Escala de Blues - Sonido característico'
    },

    'jazz': {
        'name': 'Jazz',
        'notes': ['C4', 'E4', 'G4', 'B4'],
        'description': 'Acorde de séptima mayor - Sonido jazzy'
    },
}

NOTE_FREQUENCIES = {
    'C3': 130.81,
    'D3': 146.83,
    'E3': 164.81,
    'F3': 174.61,
    'G3': 196.00,
    'A3': 220.00,
    'B3': 246.94,

    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,

    'C5': 523.25,
    'D5': 587.33,
    'E5': 659.25,
    'F5': 698.46,
    'G5': 783.99,
    'A5': 880.00,
    'B5': 987.77,
}

ACTIVE_SONG = 'c_major'

def get_active_notes():

    if ACTIVE_SONG in SONGS:
        return SONGS[ACTIVE_SONG]['notes']
    else:
        print(f"⚠️ Canción '{ACTIVE_SONG}' no encontrada. Usando 'c_major' por defecto.")
        return SONGS['c_major']['notes']

def get_active_song_info():

    if ACTIVE_SONG in SONGS:
        return SONGS[ACTIVE_SONG]
    else:
        return SONGS['c_major']

def list_available_songs():

    categories = {
        'Acordes Mayores': ['c_major', 'g_major', 'f_major', 'd_major'],
        'Acordes Menores': ['a_minor', 'e_minor', 'd_minor'],
        'Escalas y Melodías': ['pentatonic', 'chromatic', 'ascending', 'descending'],
        'Canciones Populares': ['twinkle', 'ode_to_joy', 'happy_birthday'],
        'Patrones Rítmicos': ['bass_rhythm', 'high_energy'],
        'Experimental': ['blues', 'jazz'],
    }

    for category, songs in categories.items():
        print(f"\n📁 {category}:")
        for song_id in songs:
            if song_id in SONGS:
                song = SONGS[song_id]
                notes_str = ' - '.join(song['notes'])
                print(f"   {song_id:15} | {song['name']:20} | {notes_str}")
                print(f"                   {song['description']}")

if __name__ == "__main__":
    list_available_songs()

    active = get_active_song_info()