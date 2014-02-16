# Django imports
from django.db import models

class Estudiante(models.Model):
    uid = models.IntegerField()
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    avatar = models.URLField()
    social_network = models.CharField(max_length=20)
    cod_estudiante = models.CharField(max_length=10, blank=True)
    is_config = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre


class Modulo(models.Model):
    nombre = models.CharField(max_length=25)

    def __unicode__(self):
        return self.nombre


class Materia(models.Model):
    sigla = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=60)
    pre_requisito = models.ManyToManyField('Materia', blank=True, null=True)
    modulo = models.ForeignKey(Modulo)
    record_academico = models.ManyToManyField('Estudiante', through='RecordAcademico')
    materias_inscritas = models.ManyToManyField('Estudiante', related_name='inscripcion')
    notas = models.ManyToManyField('Estudiante', through='Apunte', related_name='notas_de_clase')

    def __unicode__(self):
        return self.nombre


class Paralelo(models.Model):
    nombre_docente = models.CharField(max_length=40)
    sigla_paralelo = models.CharField(max_length=1)
    id_materia = models.ForeignKey(Materia)

    def __unicode__(self):
        return self.nombre_docente


class Periodo(models.Model):
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField(max_length=6)
    hora_final = models.TimeField(max_length=6)
    aula = models.CharField(max_length=15)
    id_paralelo = models.ForeignKey(Paralelo)

    def __unicode__(self):
        return self.aula


class RecordAcademico(models.Model):
    estudiante = models.ForeignKey('Estudiante')
    materia = models.ForeignKey(Materia)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    gestion = models.CharField(max_length=6)

    def __unicode__(self):
        return '%s - %s' % (self.estudiante.nombre, self.materia.sigla)


class Apunte(models.Model):
    materia = models.ForeignKey(Materia)
    estudiante = models.ForeignKey('Estudiante')
    texto_apuntado = models.CharField(max_length=140)


#-------------------------------------------------------------------------------


class Comentario(models.Model):
    estudiante = models.ForeignKey('Estudiante')
    materia = models.ForeignKey('Materia')
    titulo = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.titulo

class Respuestas(models.Model):
    comentario = models.ForeignKey('Comentario')
    titulo = models.CharField(max_length=255)

    def __unicode__(self):
        return self.titulo