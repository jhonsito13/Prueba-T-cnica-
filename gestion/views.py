from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse  
from django.contrib.auth import authenticate 
from .models import Acta, Compromiso, Gestion, Usuario, Compromiso
import json


@csrf_exempt
def login(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        return response
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                
                usuario = Usuario.objects.get(id=user.id)
                return JsonResponse({
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id,  
                    'rol': usuario.rol   
                })
            else:
                return JsonResponse({'error': 'Credenciales inválidas'})
        
        except Exception as e:
            return JsonResponse({'error': 'Error procesando datos'})

    return JsonResponse({'error': 'Solo POST'})
@csrf_exempt
def acta(request, id):
    try:
        acta = Acta.objects.get(id=id)
        
        compromisos = []
        for comp in acta.compromisos.all():
           
            gestiones = []
            
            for gest in comp.gestiones.all():
                gestiones.append({
                    'id': gest.id,
                    'descripcion': gest.descripcion,
                    'fecha': gest.fecha.strftime('%Y-%m-%d %H:%M')
                })
            
            compromisos.append({
                'id': comp.id,
                'descripcion': comp.descripcion,
                'fecha_limite': comp.fecha_limite.strftime('%Y-%m-%d'),
                'responsable': comp.responsable.username,
                'estado': comp.estado,
                'gestiones': gestiones
            })
        
        data = {
            'id': acta.id,
            'titulo': acta.titulo,
            'descripcion': acta.descripcion,
            'estado': acta.estado,
            'fecha': acta.fecha.strftime('%Y-%m-%d %H:%M'),
            'creador': acta.creador.username,
            'compromisos': compromisos,
            'archivo_pdf': acta.archivo_pdf.url if acta.archivo_pdf else None
        }
        
        response = JsonResponse({'success': True, 'acta': data})
        response['Access-Control-Allow-Origin'] = '*'  
        return response
        
    except Acta.DoesNotExist:
        response = JsonResponse({'error': 'Acta no encontrada'}, status=404)
        response['Access-Control-Allow-Origin'] = '*' 
        return response


@csrf_exempt
def crear_gestion(request):
    if request.method == 'POST':
        try:
            compromiso_id = request.POST.get('compromiso_id')
            descripcion = request.POST.get('descripcion')
            archivo = request.FILES.get('archivo')
            
            user = Usuario.objects.first()
            
            compromiso = Compromiso.objects.get(id=compromiso_id)
            
            gestion = Gestion.objects.create(
                compromiso=compromiso,
                descripcion=descripcion,
                creador=user
            )
            
            if archivo:
                ext = archivo.name.split('.')[-1].lower()
                if ext not in ['pdf', 'jpg']:
                    gestion.delete()
                    return JsonResponse({'error': 'Solo se permiten archivos PDF o JPG'}, status=400)
                
                if archivo.size > 5 * 1024 * 1024:
                    gestion.delete()
                    return JsonResponse({'error': 'El archivo no puede superar 5MB'}, status=400)
                
                gestion.archivo_adjunto = archivo
                gestion.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Gestión creada exitosamente',
                'gestion_id': gestion.id
            })
            
        except Compromiso.DoesNotExist:
            return JsonResponse({'error': 'Compromiso no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Solo POST'}, status=405)

@csrf_exempt
def actas_list(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method == 'GET':
        
        estado = request.GET.get('estado')
        titulo = request.GET.get('titulo')
        fecha = request.GET.get('fecha')
        
       
        user_id = request.GET.get('user_id')
        rol = request.GET.get('rol')
        
       
        if rol == 'ADMIN':
            
            actas = Acta.objects.all()
        elif rol == 'BASE' and user_id:
           
            from django.db.models import Q
            actas = Acta.objects.filter(
                Q(creador_id=user_id) |  
                Q(participantes__id=user_id) |  
                Q(compromisos__responsable_id=user_id)  
            ).distinct()  
        else:
           
            actas = Acta.objects.none()

        
        if estado:
            actas = actas.filter(estado__iexact=estado)
        if titulo:
            actas = actas.filter(titulo__icontains=titulo)
        if fecha:
            actas = actas.filter(fecha__date=fecha)

        data = []
        for acta in actas:
            data.append({
                'id': acta.id,
                'titulo': acta.titulo,
                'estado': acta.estado,
                'fecha': acta.fecha.strftime('%Y-%m-%d %H:%M'),
                'compromisos': acta.compromisos.count(),
            })

        response = JsonResponse({
            'success': True,
            'actas': data,
            'total': len(data)
        })
        response['Access-Control-Allow-Origin'] = '*'
        return response

    response = JsonResponse({'error': 'Método no permitido'})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def gestiones_por_compromiso(request, compromiso_id):
    if request.method == 'GET':
        try:
            gestiones = Gestion.objects.filter(compromiso_id=compromiso_id).order_by('-id')
            data = [
                {
                    'id': g.id,
                    'descripcion': g.descripcion,
                    'fecha_creacion': g.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
                    'creador': g.creador.username if g.creador else '',
                    'archivo_adjunto': g.archivo_adjunto.url if g.archivo_adjunto else None,
                }
                for g in gestiones
            ]
            return JsonResponse({'success': True, 'gestiones': data})
        except Compromiso.DoesNotExist:
            return JsonResponse({'error': 'Compromiso no encontrado'}, status=404)