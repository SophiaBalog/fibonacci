from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def fibonacci(request, n):
    a, b = 0, 1
    for _ in range(n):
            a, b = b, a + b
    return HttpResponse(f"Fibonacci sequence: {a}")