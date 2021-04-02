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
            return apiResponse(code=401, info=['username or email already used'])
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
            except ValidationError as err:
                return apiResponse(code=501, info=err.messages)
    else:
        return apiResponse(code=101)


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return apiResponse(result=request.user.student_set.get().get_as_json())
    elif request.POST:
        data = request.POST
        user = authenticate(
            request,
            username=data.get('username', None),
            password=data.get('password', None))
        if user is not None:
            login(request, user)
            return apiResponse(result=user.student_set.get().get_as_json())
        else:
            return apiResponse(code=502, info=['username or password invalid'])
    else:
        return apiResponse(code=102)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return apiResponse()
