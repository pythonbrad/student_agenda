from task.models import User, Student
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

CODES = {
    100: 'Method not allow',
    200: '',
    400: 'Unique field violation',
    500: 'Data invalid',
}

def apiResponse(result=None, code=200, info=None):
    error = CODES[int(code/100)*100]
    return JsonResponse({'result': result, 'code': code, 'error': error, 'info': info})

# Create your views here.
@csrf_exempt
def signin_view(request):
    if request.POST:
        data = request.POST
        if User.objects.filter(
            Q(username=data.get('username', None)) | Q(email=data.get('email', None))
        ):
            return apiResponse(code=401)
        else:
            for i in ['username', 'email', 'password']:
                if not i in data or not data[i]:
                    return apiResponse(code=501)
            user = User(username=data.get('username', None), email=data.get('email', None), password=data.get('password', None))
            error = None
            try:
                user.full_clean()
                user.set_password(user.password)
                user.save()
                Student.objects.create(user=user)
                return apiResponse()
            except:
                return apiResponse(code=502)
    else:
        return apiResponse(code=101)

@csrf_exempt
def login_view(request):
    if not request.user.is_anonymous:
        return apiResponse()
    elif request.POST:
        data = request.POST
        user = authenticate(request, username=data.get('username', None), password=data.get('password', None))
        if user is not None:
            login(request, user)
            return apiResponse()
        else:
            return apiResponse(code=503)
    else:
        return apiResponse(code=101)

def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return apiResponse()