# Django imports
from django.contrib import admin

# Project imports
from fucksia.maker.models import (
    Estudiante,
    Materia,
    Modulo,
    Paralelo,
    Periodo,
    RecordAcademico
)


class MateriaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nombre', 'modulo')
    list_filter = ('modulo',)
    filter_horizontal = ('pre_requisito','materias_inscritas')

admin.site.register(Materia, MateriaAdmin)


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'avatar', 'social_network', 'cod_estudiante')

admin.site.register(Estudiante, EstudianteAdmin)

admin.site.register([Modulo, Paralelo, Periodo, RecordAcademico])
