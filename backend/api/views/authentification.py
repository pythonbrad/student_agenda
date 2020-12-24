from task.models import User, Student
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .tools import apiResponse


@csrf_exempt
def signin_view(request):
    if request.POST:
        data = request.POST
        if User.objects.filter(
            Q(
                username=data.get('username', None)
            ) | Q(
                email=data.get('email', None)
            )
        ):
            return apiResponse(code=401)
        else:
            user = User(
                username=data.get('username', None),
                email=data.get('email', None),
                password=data.get('password', None))
            try:
                user.full_clean()
                user.set_password(user.password)
                user.save()
                Student.objects.create(user=user)
                return apiResponse()
            except ValidationError:
                return apiResponse(code=501)
    else:
        return apiResponse(code=101)


@csrf_exempt
def login_view(request):
    if not request.user.is_anonymous:
        return apiResponse()
    elif request.POST:
        data = request.POST
        user = authenticate(
            request,
            username=data.get('username', None),
            password=data.get('password', None))
        if user is not None:
            login(request, user)
            return apiResponse()
        else:
            return apiResponse(code=502)
    else:
        return apiResponse(code=102)


def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return apiResponse()
