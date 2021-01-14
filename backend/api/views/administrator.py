from task.models import Timetable, Classe, Asset
from task.models import Location, Course, Lecturer, Category
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .tools import apiResponse



@csrf_exempt
def add_timetable_view(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if Timetable.objects.filter(name=data.get('name', None)):
                return apiResponse(code=401)
            else:
                timetable = Timetable(
                    name=data.get('name', None),
                    description=data.get('description', None),
                    owner=request.user.student_set.get())
                try:
                    timetable.full_clean()
                    timetable.save()
                    timetable.moderators.add(request.user.student_set.get())
                    timetable.followers.add(request.user.student_set.get())
                    timetable.save()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=501)
        else:
            return apiResponse(code=101)
    else:
        return apiResponse(code=601)


def delete_timetable_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user.student_set.get())
        if timetable:
            timetable = timetable[0]
            timetable.delete()
            return apiResponse()
        else:
            return apiResponse(code=502)
    else:
        return apiResponse(code=602)

def get_timetable_moderator_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user.student_set.get())
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=timetable.moderators_set.get_as_json())
        else:
            return apiResponse(code=503)
    else:
        return apiResponse(code=603)

def add_timetable_moderator_view(request, timetable_pk, user_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user.student_set.get())
        user = User.objects.filter(pk=user_pk)
        if timetable and user:
            timetable = timetable[0]
            timetable.moderators.add(user[0].student_set.get())
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=504)
    else:
        return apiResponse(code=604)


def remove_timetable_moderator_view(request, timetable_pk, user_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, owner=request.user.student_set.get())
        user = User.objects.filter(pk=user_pk)
        if timetable and user:
            timetable = timetable[0]
            timetable.moderators.remove(user[0].student_set.get())
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=505)
    else:
        return apiResponse(code=605)


@csrf_exempt
def add_timetable_lecturer_view(request, timetable_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            timetable = Timetable.objects.filter(
                pk=timetable_pk, owner=request.user.student_set.get())
            if timetable:
                lecturer = Lecturer(name=data.get('name', None))
                lecturer.timetable = timetable[0]
                try:
                    lecturer.full_clean()
                    lecturer.save()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=506)
            else:
                return apiResponse(code=507)
        else:
            return apiResponse(code=102)
    else:
        return apiResponse(code=606)


def delete_timetable_lecturer_view(request, lecturer_pk):
    if request.user.is_authenticated:
        lecturer = Lecturer.objects.filter(pk=lecturer_pk, owner=request.user.student_set.get())
        if lecturer:
            lecturer = lecturer[0]
            lecturer.delete()
            return apiResponse()
        else:
            return apiResponse(code=508)
    else:
        return apiResponse(code=607)


@csrf_exempt
def add_timetable_course_view(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            course = Course(
                name=data.get('name', None),
                description=data.get('description', None),
                code=data.get('code', None)
            )
            try:
                course.full_clean()
                course.save()
                course.followers.add(request.user.student_set.get())
                for pk in data.get('lecturers[]', []):
                    lecturer = Lecturer.objects.filter(pk=pk, timetable__owner=request.user.student_set.get())
                    if lecturer:
                        course.lecturers.add(lecturer[0])
                    else:
                        return apiResponse(code=528)
                return apiResponse()
            except ValidationError:
                return apiResponse(code=509)
        else:
            return apiResponse(code=103)
    else:
        return apiResponse(code=608)


def delete_timetable_course_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk, owner=request.user.student_set.get())
        if course:
            course.delete()
            return apiResponse()
        else:
            return apiResponse(code=510)
    else:
        return apiResponse(code=609)


@csrf_exempt
def add_course_lecturer_view(request, course_pk, lecturer_pk):
    if request.user.is_authenticated:
        lecturer = Lecturer.objects.filter(pk=lecturer_pk, timetable__owner=request.user.student_set.get())
        course = Course.objects.filter(pk=course_pk)
        if course and lecturer:
            course = course[0]
            course.lecturers.add(lecturer[0])
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=511)
    else:
        return apiResponse(code=610)


@csrf_exempt
def remove_course_lecturer_view(request, course_pk, lecturer_pk):
    if request.user.is_authenticated:
        lecturer = Lecturer.objects.filter(pk=lecturer_pk, timetable__owner=request.user.student_set.get())
        course = Course.objects.filter(pk=course_pk)
        if course and lecturer:
            course = course[0]
            course.lecturers.remove(lecturer[0])
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=512)
    else:
        return apiResponse(code=611)

@csrf_exempt
def add_timetable_classe_view(request, course_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            classe = Classe(
                description=data.get('description', None),
                status=data.get('status', None),
                begin=data.get('begin', None),
                end=data.get('end', None)
            )
            location = Location.objects.filter(
                pk=data.get('location', None), owner=request.user.student_set.get())
            course = Course.objects.filter(
                pk=course_pk)
            if location and course:
                classe.location = location[0]
                classe.course = course[0]
                try:
                    classe.full_clean()
                    classe.save()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=513)
            else:
                return apiResponse(code=514)
        else:
            return apiResponse(code=104)
    else:
        return apiResponse(code=612)


def delete_timetable_classe_view(request, classe_pk):
    if request.user.is_authenticated:
        classe = Classe.objects.filter(pk=classe_pk, owner=request.user.student_set.get())
        if classe:
            classe.delete()
            return apiResponse()
        else:
            return apiResponse(code=515)
    else:
        return apiResponse(code=613)


@csrf_exempt
def add_timetable_location_view(request, timetable_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            timetable = Timetable.objects.filter(
                pk=timetable_pk, owner=request.user.student_set.get())
            if timetable:
                location = Location(name=data.get('name', None), description=data.get('description', None))
                location.timetable = timetable[0]
                try:
                    location.full_clean()
                    location.save()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=516)
            else:
                return apiResponse(code=517)
        else:
            return apiResponse(code=105)
    else:
        return apiResponse(code=614)


def delete_timetable_location_view(request, location_pk):
    if request.user.is_authenticated:
        location = Location.objects.filter(pk=location_pk, timetable__owner=request.user.student_set.get())
        if location:
            location = location[0]
            location.delete()
            return apiResponse()
        else:
            return apiResponse(code=518)
    else:
        return apiResponse(code=615)


@csrf_exempt
def add_timetable_category_view(request, timetable_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            timetable = Timetable.objects.filter(
                pk=timetable_pk, owner=request.user.student_set.get())
            if timetable:
                category = Category(name=data.get('name', None), description=data.get('description', None))
                category.timetable = timetable[0]
                try:
                    category.full_clean()
                    category.save()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=519)
            else:
                return apiResponse(code=520)
        else:
            return apiResponse(code=106)
    else:
        return apiResponse(code=616)


def delete_timetable_category_view(request, category_pk):
    if request.user.is_authenticated:
        category = Category.objects.filter(pk=category_pk, timetable__owner=request.user.student_set.get())
        if category:
            category = category[0]
            category.delete()
            return apiResponse()
        else:
            return apiResponse(code=521)
    else:
        return apiResponse(code=617)

@csrf_exempt
def add_course_asset_view(request, course_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            asset = Asset(
                name=data.get('name', None),
                description=data.get('description', None))
            category = Category.objects.filter(
                pk=data.get('category', None), timetable__owner=request.user.student_set.get())
            course = Course.objects.filter(
                pk=course_pk)
            if category and course:
                asset.category = category[0]
                asset.course = course[0]
                try:
                    asset.full_clean()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=522)
            else:
                return apiResponse(code=523)
        else:
            return apiResponse(code=107)
    else:
        return apiResponse(code=618)


def delete_course_asset_view(request, asset_pk):
    if request.user.is_authenticated:
        asset = Asset.objects.filter(pk=asset_pk, category__timetable__owner=request.user.student_set.get())
        if asset:
            asset.delete()
            return apiResponse()
        else:
            return apiResponse(code=524)
    else:
        return apiResponse(code=619)

@csrf_exempt
def add_timetable_event_view(request, location_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            event = Event(
                name=data.get('name', None),
                description=data.get('description', None))
            location = Location.objects.filter(
                pk=location_pk, timetable__owner=request.user.student_set.get())
            if location:
                event.location = location[0]
                try:
                    event.full_clean()
                    return apiResponse()
                except ValidationError:
                    return apiResponse(code=525)
            else:
                return apiResponse(code=526)
        else:
            return apiResponse(code=108)
    else:
        return apiResponse(code=620)

def delete_timetable_event_view(request, event_pk):
    if request.user.is_authenticated:
        event = Event.objects.filter(pk=event_pk, location__timetable__owner=request.user.student_set.get())
        if event:
            event.delete()
            return apiResponse()
        else:
            return apiResponse(code=527)
    else:
        return apiResponse(code=621)