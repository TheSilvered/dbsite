from django.shortcuts import render
from .models import Suono, Intensita, FREQUENZE

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('agg')

def suono_home(request):
    suoni = Suono.objects.all()
    crea_grafico_suono(suoni)
    return render(request, "suono_home.html")


def crea_grafico_suono(suoni):
    griglia_intensita = []
    for suono in suoni:
        intensita = Intensita.objects.raw(f"SELECT * FROM suono_intensita WHERE suono_id == {suono.pk}")
        intensita = [(intens.frequenza, intens.intensita) for intens in intensita]
        intensita.sort(key=lambda x: x[0])
        intensita = [x[1] for x in intensita]
        griglia_intensita.append(intensita)

    data = np.array(griglia_intensita, dtype=np.float64)
    data = np.rot90(data, k=-1)
    _, ax = plt.subplots(figsize=(12, 8))

    ax.pcolormesh(data)
    ax.set_ylabel("Frequenza (Hz)", fontsize="18")
    ax.set_yticks([i + 0.5 for i in range(32)], labels=[str(freq) for freq in FREQUENZE])

    plt.savefig("dbsite/suono/static/suono_graph.png")
