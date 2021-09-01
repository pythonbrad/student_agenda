from task.models import Timetable, User
from task.models import Location, Course, Lecturer, Category
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .tools import apiResponse
import time, random, string


@csrf_exempt
def add_timetable_view(request, timetable_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if timetable_pk:
                timetable = Timetable.objects.filter(pk=timetable_pk)
            if Timetable.objects.filter(name=data.get('name', None)):
                return apiResponse(code=401, info=["Timetable's name already used"])
            else:
                timetable = timetable[0] if timetable_pk else Timetable()
                timetable.update(
                    name=data.get('name', None),
                    description=data.get('description', None),
                    owner=request.user,
                    code=''.join([random.choices(string.ascii_letters, k=10)[10%(int(i)+1)] for i in str(time.time_ns())])
                )
                try:
                    timetable.full_clean()
                    timetable.save()
                    timetable.moderators.add(request.user)
                    timetable.followers.add(request.user)
                    timetable.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=501, info=err.messages)
        else:
            return apiResponse(code=101)
    else:
        return apiResponse(code=601)

@csrf_exempt
def update_timetable_view(request, timetable_pk):
    return add_timetable_view(request, timetable_pk=timetable_pk)

def delete_timetable_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user)
        if timetable:
            timetable = timetable[0]
            timetable.delete()
            return apiResponse()
        else:
            return apiResponse(code=502)
    else:
        return apiResponse(code=602)

def add_timetable_moderator_view(request, timetable_pk, user_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user)
        user = User.objects.filter(pk=user_pk)
        if timetable and user:
            timetable = timetable[0]
            timetable.moderators.add(user[0])
            return apiResponse()
        else:
            return apiResponse(code=504)
    else:
        return apiResponse(code=604)


def remove_timetable_moderator_view(request, timetable_pk, user_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user)
        user = User.objects.filter(pk=user_pk)
        if timetable and user:
            timetable = timetable[0]
            print(timetable.name)
            timetable.moderators.remove(user[0])
            return apiResponse()
        else:
            return apiResponse(code=505)
    else:
        return apiResponse(code=605)



def get_timetable_follower_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=[follower.student_set.get().get_as_json() for follower in timetable.followers.all()])
        else:
            return apiResponse(code=522)
    else:
        return apiResponse(code=624)


@csrf_exempt
def add_timetable_lecturer_view(request, timetable_pk=None, lecturer_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if lecturer_pk:
                lecturer = Lecturer.objects.filter(pk=lecturer_pk)
            timetable = lecturer[0].timetable if lecturer else Timetable.objects.filter(
                pk=timetable_pk, owner=request.user)
            lecturer = lecturer[0] if lecturer else Lecturer()
            lecturer.update(name=data.get('name', None))
            if timetable:
                lecturer.timetable = timetable[0]
                try:
                    lecturer.full_clean()
                    lecturer.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=506, info=err.messages)
            else:
                return apiResponse(code=507)
        else:
            return apiResponse(code=102)
    else:
        return apiResponse(code=606)

@csrf_exempt
def update_timetable_lecturer_view(request, lecturer_pk):
    return add_timetable_lecturer_view(request, lecturer_pk=lecturer_pk)

def delete_timetable_lecturer_view(request, lecturer_pk):
    if request.user.is_authenticated:
        lecturer = Lecturer.objects.filter(pk=lecturer_pk, owner=request.user)
        if lecturer:
            lecturer = lecturer[0]
            lecturer.delete()
            return apiResponse()
        else:
            return apiResponse(code=508)
    else:
        return apiResponse(code=607)


@csrf_exempt
def add_timetable_course_view(request, course_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if course_pk:
                course = Course.objects.filter(pk=course_pk)
            course = course[0] if course else Course()
            course.update(
                name=data.get('name', None),
                description=data.get('description', None),
                code=data.get('code', None)
            )
            try:
                course.full_clean()
                course.save()
                course.followers.add(request.user)
                for pk in data.get('lecturers[]', []):
                    lecturer = Lecturer.objects.filter(pk=pk, timetable__owner=request.user)
                    if lecturer:
                        course.lecturers.add(lecturer[0])
                    else:
                        return apiResponse(code=528)
                return apiResponse()
            except ValidationError as err:
                return apiResponse(code=509, info=err.messages)
        else:
            return apiResponse(code=103)
    else:
        return apiResponse(code=608)

@csrf_exempt
def update_timetable_course_view(request, course_pk):
    return add_timetable_course_view(request, course_pk=course_pk)

def delete_timetable_course_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk, owner=request.user)
        if course:
            course.delete()
            return apiResponse()
        else:
            return apiResponse(code=510)
    else:
        return apiResponse(code=609)

@csrf_exempt
def add_timetable_location_view(request, timetable_pk=None, location_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if location_pk:
                location = Location.objects.filter(pk=location_pk)
            timetable = location[0].timetable if location else Timetable.objects.filter(
                pk=timetable_pk, owner=request.user)
            if timetable:
                location = location[0] if location else Location()
                location.update(name=data.get('name', None), description=data.get('description', None))
                location.timetable = timetable[0]
                try:
                    location.full_clean()
                    location.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=516, info=err.messages)
            else:
                return apiResponse(code=517)
        else:
            return apiResponse(code=105)
    else:
        return apiResponse(code=614)

@csrf_exempt
def update_timetable_location_view(request, location_pk):
    return add_timetable_location_view(request, location_pk=location_pk)

def delete_timetable_location_view(request, location_pk):
    if request.user.is_authenticated:
        location = Location.objects.filter(pk=location_pk, timetable__owner=request.user)
        if location:
            location = location[0]
            location.delete()
            return apiResponse()
        else:
            return apiResponse(code=518)
    else:
        return apiResponse(code=615)


@csrf_exempt
def add_timetable_category_view(request, timetable_pk=None, category_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if category_pk:
                category = Category.objects.filter(pk=category_pk)
            timetable = category[0].timetable if category else Timetable.objects.filter(
                pk=timetable_pk, owner=request.user)
            if timetable:
                category = category[0] if category else Category()
                category.update(name=data.get('name', None), description=data.get('description', None))
                category.timetable = timetable[0]
                try:
                    category.full_clean()
                    category.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=519, info=err.messages)
            else:
                return apiResponse(code=520)
        else:
            return apiResponse(code=106)
    else:
        return apiResponse(code=616)

@csrf_exempt
def update_timetable_category_view(request, category_pk):
    return add_timetable_category_view(request, category_pk=category_pk)

def delete_timetable_category_view(request, category_pk):
    if request.user.is_authenticated:
        category = Category.objects.filter(pk=category_pk, timetable__owner=request.user)
        if category:
            category = category[0]
            category.delete()
            return apiResponse()
        else:
            return apiResponse(code=521)
    else:
        return apiResponse(code=617)
