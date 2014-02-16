# Python imports
import json

# DJango imports
from django.contrib.auth import logout as social_logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

# Project imports
from fucksia.maker.utils import gestion_actual
from fucksia.maker.models import (
    Estudiante,
    Comentario,
    Respuestas,
    RecordAcademico,
    Materia,
    Paralelo
)
from fucksia.maker.forms import URLForm, EstudianteForm, PensumForm
from fucksia.maker.parser import (
    save_record,
    save_inscrito,
    save_horarios,
    save_pensum
)

@login_required
def perfil(request):
    estudiante = Estudiante.objects.get(uid=request.user.id)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EstudianteForm(instance=estudiante)

    return render_to_response('maker/perfil.html', {'estudiante':estudiante}, context_instance=RequestContext(request, locals()))

@login_required
def config(request):
    estudiante = Estudiante.objects.get(uid=request.user.id)
    if estudiante.is_config:
        return redirect('home')

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            for x in form:
                print x.value()
                if x.label == 'Record academico url' and x.value():
                    save_record(x.value(), estudiante)
                if x.label == 'Materias inscritas url' and x.value():
                    save_inscrito(x.value(), estudiante)
                if x.label == 'Horarios url' and x.value():
                    save_horarios(x.value(), estudiante)
                estudiante.is_config = True
                estudiante.save()
            return redirect('home')
    else:
        form = URLForm()
    return render_to_response('maker/config.html', {
        'form':form, 'estudiante': estudiante}
        ,context_instance=RequestContext(request))

# TODO -------------------------------------------------------------------------


def login(request):
    if not request.user.is_authenticated():
        return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        return redirect('home')

def config_pensum(request):
    if request.method == 'POST':
        form = PensumForm(request.POST)
        if form.is_valid():
            for x in form:
                save_pensum(x.value())
            return redirect('home')
    else:
        form = PensumForm()
        return render_to_response('config.html',{'form':form} ,context_instance=RequestContext(request))

@login_required
def home(request):
    comentario = Comentario.objects.all().order_by('-id')
    data = list()
    for comentario in comentario:
        data.append({ 'id': comentario.pk, 'titulo': comentario.titulo, 'materia': comentario.materia, 'estudiante': comentario.estudiante })

    estudiante = Estudiante.objects.get(uid=request.user.id)
    if estudiante.is_config:
        materias = [x.sigla for x in estudiante.inscripcion.all()]
        return render_to_response('home.html', {'comentarios':data, 'materias':materias, 'estudiante':estudiante}, context_instance=RequestContext(request))
    else:
        return redirect('estudiante:config')

@login_required
def logout(request):
    social_logout(request)
    return redirect('login')


@login_required
def generador(request):
    estudiante = Estudiante.objects.get(uid=request.user.id)
    materias = serializers.serialize('json', estudiante.inscripcion.all())
    data = list()
    for ins in estudiante.inscripcion.all():
        mat = json.loads(serializers.serialize('json', [ins,]))[0]
        data.append({
            'materia':mat,
            'paralelo':json.loads(serializers.serialize('json', Paralelo.objects.filter(id_materia=ins.pk)))})

    return render_to_response('generador.html', {'estudiante':estudiante, 'materias': data},context_instance=RequestContext(request))


@login_required
def horario(request):
    estudiante = Estudiante.objects.get(uid=request.user.id)
    materias = serializers.serialize('json', estudiante.inscripcion.all())
    data = list()
    for ins in estudiante.inscripcion.all():
        mat = json.loads(serializers.serialize('json', [ins,]))[0]
        data.append({
            'materia':mat,
            'paralelo':json.loads(serializers.serialize('json', Paralelo.objects.filter(id_materia=ins.pk)))})

    return render_to_response('horario.html', {'estudiante':estudiante, 'materias': data, 'gestion_actual':gestion_actual()}, context_instance=RequestContext(request))




@login_required
def guardar_comentario(request):
    if request.is_ajax():
        estudiante = Estudiante.objects.get(uid=request.user.id)

        if request.POST['comentario']:
            materia = Materia.objects.get(sigla=request.POST['sigla'])
            print type(materia)
            comentario = Comentario(titulo=request.POST['comentario'], estudiante=estudiante, materia=materia)
            comentario.save()

        comentario = Comentario.objects.all().order_by('-id')

        data = list()
        for comentario in comentario:
            data.append({ 'id': comentario.pk, 'titulo': comentario.titulo })

        return HttpResponse(
            json.dumps({ 'comentarios': data }),
            content_type="application/json; charset=uft8"
            )
    else:
        raise Http404

@login_required
def cargar_respuestas(request, id):
    if request.is_ajax():
        respuestas = Respuestas.objects.filter(comentario__id=id).order_by('-id')

        data = list()
        for respuesta in respuestas:
            data.append(respuesta.titulo)

        return HttpResponse(
            json.dumps({'respuestas': data, 'comentario': id}),
            content_type="application/json; charset=uft8"
            )
    else:
        raise Http404

@login_required
def guardar_respuesta(request):
    if request.is_ajax():

        if request.POST['respuesta']:
            respuesta = Respuestas(titulo=request.POST['respuesta'], comentario_id=request.POST['comentario'])
            respuesta.save()

        return cargar_respuestas(request, request.POST['comentario'])
