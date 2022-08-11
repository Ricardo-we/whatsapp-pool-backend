from django.shortcuts import render

# Create your views here.
SUCCESS_MESSAGE = {'message': 'success'}
def ERROR_MESSAGE(error): return {'error': str(error)}
