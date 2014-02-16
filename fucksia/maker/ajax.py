# Python imports
import json

# Third part imports
from dajaxice.decorators import dajaxice_register

# Project imports
from fucksia.maker.models import Materia, Paralelo, Periodo

@dajaxice_register
def combinacion(request, lista):
	simbolos = lista
	simbolos = simbolos.split(';')
	materias = list(m[:7] for m in simbolos)
	materias = list(set(materias))
	combinaciones = combinacionMaterias(simbolos, materias)

	listgen = list()
	diasT = ('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO')
	horasT = (8,10,12,14,16,18,20)
	sw = True
	for combinacion in combinaciones:
		genhorario = [ [""] * 6 for x in [''] * 7]
		for mat in combinacion:
			sw = True
			nombre_mat = mat[:7]
			materia = Materia.objects.get(sigla = nombre_mat)
			sigla_par = mat[7:]
			paralelo = Paralelo.objects.get(id_materia = materia, sigla_paralelo = sigla_par)
			periodo = Periodo.objects.filter(id_paralelo = paralelo)
			for hora in periodo:
				if genhorario[horasT.index(hora.hora_inicio.hour)][diasT.index(hora.dia)] == '':
					genhorario[horasT.index(hora.hora_inicio.hour)][diasT.index(hora.dia)] = nombre_mat
				else:
					sw = False
					break
			if not sw:
				break
		if sw:
			listgen.append(genhorario)
	return json.dumps({'listgen':listgen})

def combinacionMaterias(simbolos, materias):
	S = materias
	# S = ['a','b','c','d']
	num_materias = len(S)
	l = simbolos
	res = list()
	for x in combinations(l, num_materias):
		sw = True;
		cad = ' '.join(list(x))
		for mats in S:
			if cad.count(mats) != 1:
				sw = False
				break
		if sw:
			res.append(x)
	return res

def combinations(iterable, r):
    pool = iterable
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

@dajaxice_register
def horario(request, mat, par):
	print 'horario'
	materia = Materia.objects.get(sigla=mat)
	print materia
	paralelo = Paralelo.objects.get(id_materia=materia, sigla_paralelo=par)
	print paralelo
	periodo = Periodo.objects.filter(id_paralelo = paralelo)
	list_periodo = list()
	for pe in periodo:
		list_periodo.append({'per':'%s%s-%s' % (pe.dia[:2],pe.hora_inicio.hour, pe.hora_final.hour)})
	return json.dumps({'periodos':list_periodo, 'mat':mat})