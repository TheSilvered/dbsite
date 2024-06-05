from django.shortcuts import render

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('agg')

def suono_home(request):
    return render(request, "suono_home.html")

