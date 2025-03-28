import random
import time
from utils import getTeamById, diferencia_alta, diferencia_extrema, diferencia_media, diferencia_ultra


def calcular_probabilidad_ganador(ranking_local, ranking_visitante):
    """Calcula la probabilidad de que el equipo con menor ranking gane."""

    if ranking_local < ranking_visitante:
        if diferencia_media(ranking_local, ranking_visitante):
            probabilidad_local = 0.65  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.35  # Probabilidad de gol visitante más baja
        elif diferencia_alta(ranking_local, ranking_visitante):
            probabilidad_local = 0.7  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.3  # Probabilidad de gol visitante más baja
        elif diferencia_extrema(ranking_local, ranking_visitante):
            probabilidad_local = 0.8  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.2  # Probabilidad de gol visitante más baja
        elif diferencia_ultra(ranking_local, ranking_visitante):
            probabilidad_local = 0.9  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.1  # Probabilidad de gol visitante más baja
        else:
            probabilidad_local = 0.6  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.4  # Probabilidad de gol visitante más baja


    elif ranking_local > ranking_visitante:
        if diferencia_media(ranking_local, ranking_visitante):
            probabilidad_local = 0.35  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.65  # Probabilidad de gol visitante más baja
        elif diferencia_alta(ranking_local, ranking_visitante):
            probabilidad_local = 0.3  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.7  # Probabilidad de gol visitante más baja
        elif diferencia_extrema(ranking_local, ranking_visitante):
            probabilidad_local = 0.2  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.8  # Probabilidad de gol visitante más baja
        elif diferencia_ultra(ranking_local, ranking_visitante):
            probabilidad_local = 0.1  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.9  # Probabilidad de gol visitante más baja
        else:
            probabilidad_local = 0.4  # Probabilidad de gol local más alta
            probabilidad_visitante = 0.6  # Probabilidad de gol visitante más baja
    else:
        probabilidad_local = 0.5  # Probabilidad de gol local igual a la del visitante
        probabilidad_visitante = 0.5  # Probabilidad de gol visitante igual a la del local
    return probabilidad_local, probabilidad_visitante


def simular_partido(equipo_local, equipo_visitante, extraTime):
    """Simula un partido entre dos equipos y determina el ganador."""
    # Obtener el ranking FIFA de los equipos
    sleepTime = 0.1
    probalidad_gol = 0.03
    jsonLocal = getTeamById(equipo_local)
    jsonVisita = getTeamById(equipo_visitante)
    ranking_local = jsonLocal[0]['fifa_nation_rank']
    ranking_visitante = jsonVisita[0]['fifa_nation_rank']
    nombre_local = jsonLocal[0]['nation_name']
    nombre_visita = jsonVisita[0]['nation_name']

    # Calcular la probabilidad de que el equipo con menor ranking gane
    probabilidad_local, probabilidad_visitante = calcular_probabilidad_ganador(ranking_local, ranking_visitante)
    probabilidad_gol_local = probabilidad_local * probalidad_gol
    probabilidad_gol_visita = probabilidad_visitante * probalidad_gol
    # Inicializar los goles de cada equipo
    goles_local = 0
    goles_visitante = 0

    # Simular el tiempo transcurrido en el partido (90 segundos)
    tiempo_transcurrido = 0
    print(':::::::Comienza Partido::::::::::  {}  - {} ::::::::::::::::::: \n'.format(nombre_local, nombre_visita))
    while tiempo_transcurrido < 90:
        # Generar un evento aleatorio basado en las probabilidades de los equipos
        evento = random.choices(['L', 'V', '-'], [probabilidad_gol_local, probabilidad_gol_visita,
                                            1 - (probabilidad_gol_local - probabilidad_gol_visita)])[0]

        # Si el evento es un gol local
        if evento == 'L':
            # Incrementar el marcador del equipo local
            goles_local += 1
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Gol {} ({}) {} - {} \n'.format(nombre_local, tiempo_transcurrido, goles_local, goles_visitante))

        # Si el evento es un gol visitante
        elif evento == 'V':
            # Incrementar el marcador del equipo visitante
            goles_visitante += 1
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Gol {} ({}) {} - {} \n'.format(nombre_visita, tiempo_transcurrido, goles_local, goles_visitante))

        # Si el evento es un sin gol
        else:
            # Incrementar el tiempo transcurrido en 1 segundo
            tiempo_transcurrido += 1
            # Mostrar el evento en el partido
            print('Minuto ({}) \n'.format(tiempo_transcurrido))

        # Dormir el programa por 0.9 segundos para simular el tiempo real del partido
        time.sleep(sleepTime)

    print(':::::::::::::::Fin del Partido:::::::::::::::::: ---------> {} {} - {} {} \n'.format(nombre_local, goles_local, goles_visitante, nombre_visita))
    if extraTime and goles_local == goles_visitante:
        print('::::::::::::::Comienza Alargue::::::::::::::::: --------->  {} - {} \n'.format(nombre_local, nombre_visita))
        tiempo_transcurrido = 90
        penales_local = None
        penales_visita = None
        while tiempo_transcurrido < 120:
            # Generar un evento aleatorio basado en las probabilidades de los equipos
            evento = random.choices(['L', 'V', '-'], [probabilidad_gol_local, probabilidad_gol_visita,
                                                1 - (probabilidad_gol_local - probabilidad_gol_visita)])[0]

            # Si el evento es un gol local
            if evento == 'L':
                # Incrementar el marcador del equipo local
                goles_local += 1
                # Incrementar el tiempo transcurrido en 1 segundo
                tiempo_transcurrido += 1
                # Mostrar el evento en el partido
                print('Gol {} ({}) {} - {} \n'.format(nombre_local, tiempo_transcurrido, goles_local, goles_visitante))

            # Si el evento es un gol visitante
            elif evento == 'V':
                # Incrementar el marcador del equipo visitante
                goles_visitante += 1
                # Incrementar el tiempo transcurrido en 1 segundo
                tiempo_transcurrido += 1
                # Mostrar el evento en el partido
                print('Gol {} ({}) {} - {} \n'.format(nombre_visita, tiempo_transcurrido, goles_local, goles_visitante))

            # Si el evento es un sin gol
            else:
                # Incrementar el tiempo transcurrido en 1 segundo
                tiempo_transcurrido += 1
                # Mostrar el evento en el partido
                print('Minuto ({}) \n'.format(tiempo_transcurrido))

            # Dormir el programa por 0.9 segundos para simular el tiempo real del partido
            time.sleep(sleepTime)
        print(':::::::::::::::::::::Fin del Alargue:::::::::::::::: ---------> {} {} - {} {} \n'.format(nombre_local, goles_local, goles_visitante, nombre_visita))

        if goles_local == goles_visitante:
            penales = False
            count_penales = 0
            penales_local = 0
            penales_visita = 0
            array_pen_local = []
            array_pen_visita = []
            print('................::::::::::::: PENALES ::::::::::::::::::::................ \n')
            while penales == False:
                # Generar un evento aleatorio de penales basado en las probabilidades de los equipos
                eventoLocal = random.choices(['O', 'X'], [probabilidad_local, probabilidad_visitante])[0]

                # Si el evento es un gol local
                if eventoLocal == 'O':
                    # Incrementar el marcador del equipo local
                    penales_local += 1
                    # Incrementar el tiempo transcurrido en 1 segundo

                    # Mostrar el evento en el partido
                    array_pen_local.append("O")
                else:
                    array_pen_local.append("X")

                print('Penales {}   {} \n'.format(nombre_local, array_pen_local[-5:]))

                time.sleep(sleepTime)
                eventoVisita = random.choices(['O', 'X'], [probabilidad_visitante, probabilidad_local])[0]

                # Si el evento es un gol visitante
                if eventoVisita == 'O':
                    # Incrementar el marcador del equipo visitante
                    penales_visita += 1
                    # Incrementar el tiempo transcurrido en 1 segundo

                    # Mostrar el evento en el partido
                    array_pen_visita.append("O")
                else:
                    array_pen_visita.append("X")

                # Si el evento es un sin gol
                print('Penales {}   {} \n'.format(nombre_visita, array_pen_visita[-5:]))

                count_penales += 1
                if count_penales > 2 and count_penales < 5:
                    if (abs((5 - penales_local) - (5 - penales_visita))>(5 - count_penales)):
                        penales = True


                if count_penales >= 5:
                    if penales_local != penales_visita:
                        penales = True

                time.sleep(sleepTime)

            print('::::::::::::::::::::::Fin Penales ::::::::::::::::::::: ---------> {} {} - {} {} \n'.format(nombre_local, penales_local if penales_local > 0 else 0,
                                                     penales_visita if penales_visita > 0 else 0, nombre_visita))
        return {'local': goles_local, 'penales_local': penales_local if penales_local is not None else None,
                'visita': goles_visitante, 'penales_visita': penales_visita if penales_visita is not None else None}

    return {'local': goles_local, 'visita': goles_visitante}
