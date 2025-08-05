from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse  
from django.contrib.auth import authenticate 
from .models import Acta, Compromiso, Gestion, Usuario  
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                return JsonResponse({
                    'success': True,
                    'username': user.username,
                    'email': user.email
                })
            else:
                return JsonResponse({'error': 'Credenciales inválidas'})
        
        except:
            return JsonResponse({'error': 'Error procesando datos'})

    return JsonResponse({'error': 'Solo POST'})

def acta(request, id):
    try:
        acta = Acta.objects.get(id=id)
        
        compromisos = []
        for comp in acta.compromisos.all():
            compromisos.append({
                'id': comp.id,
                'descripcion': comp.descripcion,
                'fecha_limite': comp.fecha_limite.strftime('%Y-%m-%d'),
                'responsable': comp.responsable.username,
                'estado': comp.estado
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
        
        return JsonResponse({'success': True, 'acta': data})
        
    except Acta.DoesNotExist:
        return JsonResponse({'error': 'Acta no encontrada'}, status=404)  

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