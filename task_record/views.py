# core/views.py
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Task
from django.shortcuts import render


@csrf_exempt
def home(request):
    if request.method == 'GET':
        try:
            return render(request, 'task_record/index.html', {'data': ''})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User(
                name=data['name'],
                email=data['email'],
                mobile_number=data['mobile_number'],
                password=make_password(data['password']),
                address=data['address'],
                latitude=data['latitude'],
                longitude=data['longitude'],
            )
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse(status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(email=data['email'])
            if check_password(data['password'], user.password):
                return JsonResponse({'message': 'Login successful', 'user_id': user.id}, status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=data['assigned_to'])
            task = Task(
                name=data['name'],
                date_time=data['date_time'],
                assigned_to=user
            )
            task.save()
            return JsonResponse({'message': 'Task added successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Assigned user does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def view_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().values('name', 'date_time', 'assigned_to__name', 'status')
        task_list = list(tasks)
        return JsonResponse(task_list, safe=False, status=200)
    return HttpResponse(status=405)
