from task.models import User, Student, Timetable, Classe
from task.models import Location, Course, Lecturer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from . import authentification
from . import administrator
from . import moderator
from . import user

CODES = {
    100: 'Method not allow',
    200: '',
    400: 'Unique field violation',
    500: 'Data invalid',
    600: 'Access Denied',
}


def apiResponse(result=None, code=200, info=None):
    error = CODES[int(code / 100) * 100]
    return JsonResponse({
        'result': result,
        'code': code,
        'error': error,
        'info': info})

