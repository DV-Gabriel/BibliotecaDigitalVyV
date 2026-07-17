from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recursos_digitales.models import Categoria, Etiqueta, RecursoDigital

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Crea usuarios, categorías, etiquetas y 10 recursos de prueba para el catálogo.'

    def handle(self, *args, **options):
        ana, _ = Usuario.objects.get_or_create(
            username='ana',
            defaults={'email': 'ana@example.com', 'rol': Usuario.Rol.DOCENTE},
        )
        ana.set_password('demo1234')
        ana.save()

        luis, _ = Usuario.objects.get_or_create(
            username='luis',
            defaults={'email': 'luis@example.com', 'rol': Usuario.Rol.ESTUDIANTE},
        )
        luis.set_password('demo1234')
        luis.save()

        nombres_categorias = ['Matemática', 'Historia', 'Programación', 'Biología']
        categorias = [Categoria.objects.get_or_create(nombre=n)[0] for n in nombres_categorias]

        nombres_etiquetas = ['básico', 'avanzado', 'práctica', 'teoría', 'examen']
        etiquetas = [Etiqueta.objects.get_or_create(nombre=n)[0] for n in nombres_etiquetas]

        Tipo = RecursoDigital.Tipo
        Vis = RecursoDigital.Visibilidad
        Estado = RecursoDigital.Estado

        recursos_data = [
            dict(titulo='Introducción al Álgebra Lineal',
                 descripcion='Conceptos básicos de vectores, matrices y sistemas de ecuaciones.',
                 categoria=categorias[0], tipo=Tipo.ORIGINAL, propietario=ana, autor_usuario=ana,
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 contenido='Un vector es una magnitud con dirección y sentido...',
                 etiquetas=[etiquetas[0], etiquetas[3]]),
            dict(titulo='Cien Años de Soledad',
                 descripcion='Novela emblemática del realismo mágico latinoamericano.',
                 categoria=categorias[1], tipo=Tipo.EXTERNO, propietario=luis,
                 autor_texto='Gabriel García Márquez',
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 etiquetas=[etiquetas[3]]),
            dict(titulo='Guía de Python para Principiantes',
                 descripcion='Sintaxis básica, tipos de datos y estructuras de control.',
                 categoria=categorias[2], tipo=Tipo.ORIGINAL, propietario=luis, autor_usuario=luis,
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 contenido='print("Hola mundo") es el clásico primer programa...',
                 etiquetas=[etiquetas[0], etiquetas[2]]),
            dict(titulo='La Célula: Estructura y Función',
                 descripcion='Resumen sobre organelos celulares y sus funciones.',
                 categoria=categorias[3], tipo=Tipo.EXTERNO, propietario=ana,
                 autor_texto='Neil Campbell',
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 etiquetas=[etiquetas[3], etiquetas[1]]),
            dict(titulo='Ejercicios de Derivadas',
                 descripcion='Guía de práctica con ejercicios resueltos de derivación.',
                 categoria=categorias[0], tipo=Tipo.ORIGINAL, propietario=ana, autor_usuario=ana,
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 contenido='Ejercicio 1: deriva f(x) = x^2 + 3x...',
                 etiquetas=[etiquetas[1], etiquetas[2]]),
            dict(titulo='La Segunda Guerra Mundial: Resumen',
                 descripcion='Línea de tiempo y causas principales del conflicto.',
                 categoria=categorias[1], tipo=Tipo.EXTERNO, propietario=luis,
                 autor_texto='Ministerio de Educación',
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 etiquetas=[etiquetas[0]]),
            dict(titulo='Apuntes de POO en Python (borrador)',
                 descripcion='Notas de clase sobre clases, herencia y polimorfismo.',
                 categoria=categorias[2], tipo=Tipo.ORIGINAL, propietario=luis, autor_usuario=luis,
                 visibilidad=Vis.PRIVADO, estado=Estado.BORRADOR,
                 contenido='Trabajo en progreso...',
                 etiquetas=[]),
            dict(titulo='Genética Mendeliana',
                 descripcion='Leyes de Mendel y ejercicios de cruzamientos.',
                 categoria=categorias[3], tipo=Tipo.ORIGINAL, propietario=ana, autor_usuario=ana,
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 contenido='La primera ley de Mendel establece la segregación...',
                 etiquetas=[etiquetas[3], etiquetas[4]]),
            dict(titulo='Estructuras de Datos en Python',
                 descripcion='Listas, tuplas, diccionarios y sets explicados con ejemplos.',
                 categoria=categorias[2], tipo=Tipo.EXTERNO, propietario=ana,
                 autor_texto='Real Python',
                 visibilidad=Vis.PUBLICO, estado=Estado.PUBLICADO,
                 etiquetas=[etiquetas[0], etiquetas[1]]),
            dict(titulo='Simulacro de Examen de Historia (privado)',
                 descripcion='Banco de preguntas para practicar antes del examen.',
                 categoria=categorias[1], tipo=Tipo.ORIGINAL, propietario=luis, autor_usuario=luis,
                 visibilidad=Vis.PRIVADO, estado=Estado.PUBLICADO,
                 contenido='1) ¿En qué año comenzó la Segunda Guerra Mundial?...',
                 etiquetas=[etiquetas[4]]),
        ]

        creados = 0
        for data in recursos_data:
            etiquetas_del_recurso = data.pop('etiquetas')
            recurso, created = RecursoDigital.objects.get_or_create(
                titulo=data['titulo'], defaults=data
            )
            if created:
                recurso.etiquetas.set(etiquetas_del_recurso)
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f'{creados} recurso(s) nuevo(s) creado(s) (de {len(recursos_data)} definidos).\n'
            f'Usuarios demo -> usuario: ana / luis, password: demo1234'
        ))
