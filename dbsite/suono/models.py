from django.db import models

FREQUENZE = [
    16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500,
    630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000,
    10000, 12500, 16000, 20000
]


class Suono(models.Model):
    data_e_ora = models.DateTimeField(auto_now=False, auto_now_add=False)
    laeq = models.FloatField()

    @staticmethod
    def load_from_file(path, encoding='utf8', skiprows=1):
        with open(path, encoding=encoding) as f:
            contents = f.read()

        contents = contents.replace('\r\n', '\n').replace('\r', '\n').strip()
        rows = contents.split('\n')[skiprows:]

        for i, row in enumerate(rows):
            data, ora, laeq, *intensita = row.split()
            assert len(intensita) == len(FREQUENZE)
            print(f"Creazione suono {i + 1}/{len(rows)}")
            suono = Suono.objects.create(data_e_ora=f"{data} {ora}", laeq=float(laeq))
            for intens, freq in zip(intensita, FREQUENZE):
                Intensita.objects.create(frequenza=float(freq), intensita=float(intens), suono=suono)


class Intensita(models.Model):
    frequenza = models.FloatField()
    intensita = models.FloatField()
    suono = models.ForeignKey(Suono, on_delete=models.CASCADE)
