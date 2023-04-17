import random
import time
from utils import getTeamById


def calcular_probabilidad_ganador(ranking_local, ranking_visitante):
    """Calcula la probabilidad de que el equipo con menor ranking gane."""
    diferencia_ranking = ranking_local - ranking_visitante

    if ranking_local < ranking_visitante:
        if abs(diferencia_ranking) > 10:
            probabilidad_local = 0.7  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.3  # Probabilidad de gol visitante más baja
        elif abs(diferencia_ranking) > 20:
            probabilidad_local = 0.8  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.2  # Probabilidad de gol visitante más baja
        else:
            probabilidad_local = 0.6  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.4  # Probabilidad de gol visitante más baja


    elif ranking_local > ranking_visitante:
        if abs(diferencia_ranking) > 10:
            probabilidad_local = 0.3  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.7  # Probabilidad de gol visitante más baja
        elif abs(diferencia_ranking) > 20:
            probabilidad_local = 0.2  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.8  # Probabilidad de gol visitante más baja
        else:
            probabilidad_local = 0.4  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.6  # Probabilidad de gol visitante más baja
    else:
        probabilidad_local = 0.5  # Probabilidad de gol local igual a la del visitante
        probabilidad_visitante = 0.5  # Probabilidad de gol visitante igual a la del local
    return probabilidad_local, probabilidad_visitante


def simular_partido(equipo_local, equipo_visitante):
    """Simula un partido entre dos equipos y determina el ganador."""
    # Obtener el ranking FIFA de los equipos
    probalidad_gol = 0.01
    jsonLocal = getTeamById(equipo_local)
    jsonVisita = getTeamById(equipo_visitante)
    ranking_local = jsonLocal[0]['fifa_nation_rank']
    ranking_visitante = jsonVisita[0]['fifa_nation_rank']

    # Calcular la probabilidad de que el equipo con menor ranking gane
    probabilidad_local, probabilidad_visitante = calcular_probabilidad_ganador(ranking_local, ranking_visitante)
    probabilidad_gol_local = probabilidad_local * probalidad_gol
    probabilidad_gol_visita = probabilidad_visitante * probalidad_gol
    # Inicializar los goles de cada equipo
    goles_local = 0
    goles_visitante = 0

    # Simular el tiempo transcurrido en el partido (90 segundos)
    tiempo_transcurrido = 0
    while tiempo_transcurrido < 90:
        # Generar un evento aleatorio basado en las probabilidades de los equipos
        evento = random.choices([0, 1, 2], [probabilidad_gol_local, probabilidad_gol_visita,
                                            1 - (probabilidad_gol_local - probabilidad_gol_visita)])[0]

        # Si el evento es un gol local
        if evento == 0:
            # Incrementar el marcador del equipo local
            goles_local += 1
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Gol Local ({}) {} - {}'.format(tiempo_transcurrido,goles_local,goles_visitante))

        # Si el evento es un gol visitante
        elif evento == 1:
            # Incrementar el marcador del equipo visitante
            goles_visitante += 1
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Gol Visita ({}) {} - {}'.format(tiempo_transcurrido,goles_local,goles_visitante))

        # Si el evento es un sin gol
        else:
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Sin gol. ({})'.format(tiempo_transcurrido))

        # Dormir el programa por 0.9 segundos para simular el tiempo real del partido
        time.sleep(0.9)

    return {'local': goles_local, 'visita': goles_visitante}
