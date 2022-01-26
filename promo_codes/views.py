from django.shortcuts import render
from django.http import JsonResponse

def validate(request):
    return JsonResponse({
        'name': 'Test',
        'job': 'Demos',
        'courses': [
            {'title': 'Python'}
        ]
    })
