from django.contrib import admin
from .models import (
    Atleta, Esporte, Torneio,
    DesempenhoFutebol, DesempenhoBasquete, DesempenhoVolei,
)

admin.site.register(Atleta)
admin.site.register(Esporte)
admin.site.register(Torneio)
admin.site.register(DesempenhoFutebol)
admin.site.register(DesempenhoBasquete)
admin.site.register(DesempenhoVolei)