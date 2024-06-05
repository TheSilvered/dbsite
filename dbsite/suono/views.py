from django.shortcuts import render
from .models import Suono, Intensita, FREQUENZE

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import re

matplotlib.use('agg')

def suono_home(request):
    # suoni = Suono.objects.all()
    # crea_grafico_suono(suoni)
    #return render(request, "suono_home.html")

    query = 'SELECT * FROM suono_suono'

    condizione = ""
    ora_inizio = None
    ora_fine = None

    if "ora-inizio" in request.GET:
        ora_inizio = request.GET["ora-inizio"]
        if controlla_ora(ora_inizio):
            condizione += f'ora >= "{ora_inizio}"'
        else:
            ora_inizio = None
    if "ora-fine" in request.GET:
        ora_fine = request.GET["ora-fine"]
        if controlla_ora(ora_fine):
            if condizione:
                condizione += " AND "
            condizione += f'ora <= "{ora_fine}"'
        else:
            ora_fine = None

    if condizione:
        query += " WHERE " + condizione

    dati = Suono.objects.raw(query)
    aggiorna_immagine_grafico(dati)

    if ora_inizio is not None:
        pass
    elif len(dati) != 0:
        ora_inizio = min([giorno.ora for giorno in dati]).strftime("%H:%M")
    else:
        ora_inizio = ""

    if ora_fine is not None:
        pass
    elif len(dati) != 0:
        ora_fine = max([giorno.ora for giorno in dati]).strftime("%H:%M")
    else:
        ora_fine = ""

    return render(
        request,
        'suono_home.html',
        {
            "dati": dati,
            "ora_inizio": ora_inizio,
            "ora_fine": ora_fine,
        }
    )


def controlla_ora(data):
    return re.fullmatch(r'\d\d:\d\d', data) is not None


def aggiorna_immagine_grafico(suoni):
    griglia_intensita = []
    ore = []
    time_step = max(int(len(suoni) * 0.0547), 1)

    for i, suono in enumerate(suoni):
        intensita = Intensita.objects.raw(f"SELECT * FROM suono_intensita WHERE suono_id == {suono.pk}")
        intensita = list(intensita)
        intensita.sort(key=lambda x: x.frequenza)
        if i % time_step == 0:
            ore.append(intensita[0].suono.ora.strftime("%H:%M:%S:%f")[:-3])
        intensita = [x.intensita for x in intensita]
        griglia_intensita.append(intensita)

    data = np.array(griglia_intensita, dtype=np.float64)
    if griglia_intensita:
        data = np.rot90(data, k=-1)
    _, ax = plt.subplots(figsize=(12, 8))

    if griglia_intensita:
        ax.pcolormesh(data)
    ax.set_ylabel("Frequenza (Hz)", fontsize="18")
    ax.set_yticks([i + 0.5 for i in range(32)], labels=[str(freq) for freq in FREQUENZE])
    ax.set_xlabel("Ora")

    if ore:
        ax.set_xticks(list(range(0, len(suoni), time_step)), labels=ore, rotation=45)

    plt.savefig("dbsite/suono/static/suono_graph.png")
