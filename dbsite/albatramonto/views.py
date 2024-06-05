from django.shortcuts import render
from .models import OreLuce

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import re

matplotlib.use('agg')

def albatramonto_home(request):
    query = 'SELECT * FROM albatramonto_oreluce'

    condizione = ""
    data_inizio = None
    data_fine = None

    if "data-inizio" in request.GET:
        data_inizio = request.GET["data-inizio"]
        if controlla_data(data_inizio):
            condizione += f'data >= "{data_inizio}"'
        else:
            data_inizio = None
    if "data-fine" in request.GET:
        data_fine = request.GET["data-fine"]
        if controlla_data(data_fine):
            if condizione:
                condizione += " AND "
            condizione += f'data <= "{data_fine}"'
        else:
            data_fine = None

    if condizione:
        query += " WHERE " + condizione

    dati = OreLuce.objects.raw(query)
    aggiorna_immagine_grafico(dati)

    if data_inizio is not None:
        pass
    elif len(dati) != 0:
        data_inizio = min([giorno.data for giorno in dati]).strftime("%Y-%m-%d")
    else:
        data_inizio = ""

    if data_fine is not None:
        pass
    elif len(dati) != 0:
        data_fine = max([giorno.data for giorno in dati]).strftime("%Y-%m-%d")
    else:
        data_fine = ""

    return render(
        request,
        'albatramonto_home.html',
        {
            "dati": dati,
            "data_inizio": data_inizio,
            "data_fine": data_fine,
        }
    )


def controlla_data(data):
    return re.fullmatch(r'\d{4}-[01]\d-[0-3]\d', data) is not None


def time_in_minutes(time, dst):
    hours, minutes = time.split(":")
    hours = int(hours)
    minutes = int(minutes)
    if dst:
        hours -= 1
    return hours * 60 + minutes


def fix_hours(ls, ds_times):
    for idx in range(len(ls)):
        ls[idx] = time_in_minutes(ls[idx], ds_times[idx])
    return ls


def aggiorna_immagine_grafico(dati):
    dates = [giorno.data.strftime("%d/%m/%Y") for giorno in dati]
    sunrises = [giorno.ora_alba.strftime("%H:%M") for giorno in dati]
    sunsets = [giorno.ora_tramonto.strftime("%H:%M") for giorno in dati]
    ds_times = [giorno.ora_legale for giorno in dati]


    sunrises = fix_hours(sunrises, ds_times)
    sunsets = fix_hours(sunsets, ds_times)
    day_durations = []
    for i in range(len(sunrises)):
        day_durations.append(sunsets[i] - sunrises[i])

    sunrises_array = np.array(sunrises)
    sunsets_array = np.array(sunsets)
    day_durations_array = np.array(day_durations)

    _, ax = plt.subplots(figsize=(12, 8))

    ax.plot(sunrises_array, label="Alba")
    ax.plot(sunsets_array, label="Tramonto")
    ax.plot(day_durations_array, label="Durata giorno")

    ax.set_xlabel("Data", fontsize="18")
    ax.set_ylabel("Ora o durata in ore", fontsize="18")
    ax.legend(loc=1, fontsize=10)
    ax.grid(True)

    for i in range(len(dates)):
        dates[i] = dates[i].removesuffix('/2023')

    def minutes_to_y_label(minutes):
        hours, mod_minutes = divmod(minutes, 60)
        if hours == 24:
            hours = 0
        if hours < 10:
            hours = "0" + str(hours)
        else:
            hours = str(hours)
        if mod_minutes < 10:
            mod_minutes = "0" + str(mod_minutes)
        else:
            mod_minutes = str(mod_minutes)
        return str(hours) + ":" + str(mod_minutes)

    y_labels = []
    for i in range(0, 60 * 25, 60):
        y_labels.append(minutes_to_y_label(i))

    ax.set_xticks(list(range(0, len(dates), 20)), labels=dates[::20], rotation=45)
    ax.set_yticks(list(range(0, 60 * 25, 60)), labels=y_labels)

    plt.savefig("dbsite/albatramonto/static/albatramonto_graph.png")
