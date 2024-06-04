from django.db import models

# Create your models here.
class OreLuce(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False)
    ora_alba = models.TimeField(auto_now=False, auto_now_add=False)
    ora_tramonto = models.TimeField(auto_now=False, auto_now_add=False)
    ora_legale = models.BooleanField()

    def __str__(self):
        return f"{self.data}, {self.ora_alba}, {self.ora_tramonto}, {self.ora_legale}"

    @classmethod
    def load_from_file(cls, path, encoding='utf8', skiprows=1):
        with open(path, encoding=encoding) as f:
            contents = f.read()

        contents = contents.replace('\r\n', '\n').replace('\r', '\n').strip()
        rows = contents.split('\n')[skiprows:]

        for row in rows:
            _, data, ora_alba, ora_tramonto, ora_legale = row.split()
            d, m, y = data.split('/')

            cls.objects.create(
                data=f"{y}-{m}-{d}",
                ora_alba=ora_alba,
                ora_tramonto=ora_tramonto,
                ora_legale=ora_legale == 'L'
            )
