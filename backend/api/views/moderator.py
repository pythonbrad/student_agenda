from task.models import Course, Event, Classe, Location, Media, Asset, Category
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .tools import apiResponse

@csrf_exempt
def add_timetable_classe_view(request, course_pk=None, classe_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if classe_pk:
                classe = Classe.objects.filter(pk=classe_pk)
                classe = classe[0] if classe else None
            else:
                classe = Classe()
            location = Location.objects.filter(
                pk=data.get('location', None), timetable__owner=request.user)
            course = Course.objects.filter(
                pk=data.get('course') if classe_pk else course_pk)
            if location and course and classe:
                classe.description = data.get('description', None)
                classe.attendance_done = data.get('attendance_done', None) == '1'
                classe.status = data.get('status', None)
                classe.date = data.get('date', None)
                classe.begin = data.get('begin', None)
                classe.end = data.get('end', None)
                classe.location = location[0]
                classe.course = course[0]
                try:
                    classe.full_clean()
                    classe.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=513, info=err.messages)
            else:
                return apiResponse(code=514)
        else:
            return apiResponse(code=104)
    else:
        return apiResponse(code=612)

@csrf_exempt
def update_timetable_classe_view(request, classe_pk):
    return add_timetable_classe_view(request, classe_pk=classe_pk)


def delete_timetable_classe_view(request, classe_pk):
    if request.user.is_authenticated:
        classe = Classe.objects.filter(pk=classe_pk, location__timetable__owner=request.user)
        if classe:
            classe.delete()
            return apiResponse()
        else:
            return apiResponse(code=515)
    else:
        return apiResponse(code=613)


@csrf_exempt
def add_media_view(request):
    if request.user.is_authenticated:
        if request.FILES:
            media = Media.objects.create(file=request.FILES['file'], author=request.user)
            return apiResponse(result=media.pk)
        else:
            return apiResponse(code=529)
    else:
        return apiResponse(code=622)



@csrf_exempt
def add_course_asset_view(request, course_pk=None, asset_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if asset_pk:
                asset = Asset.objects.filter(pk=asset_pk)
                asset = asset[0] if asset else None
            else:
                asset = Asset()
            category = Category.objects.filter(
                pk=data.get('category', None), timetable__owner=request.user)
            if not asset_pk:
                media = Media.objects.filter(
                    pk=data.get('media', None))
            course = Course.objects.filter(
                pk=data.get('course', None) if asset_pk else course_pk)
            if category and (asset_pk or media) and course and asset:
                asset.name=data.get('name', None)
                asset.description=data.get('description', None)
                asset.category = category[0]
                if not asset_pk:
                    asset.media = media[0]
                else:
                    pass
                asset.course = course[0]
                try:
                    asset.full_clean()
                    asset.save()
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=522, info=err.messages)
            else:
                return apiResponse(code=523)
        else:
            return apiResponse(code=107)
    else:
        return apiResponse(code=618)


def delete_course_asset_view(request, asset_pk):
    if request.user.is_authenticated:
        asset = Asset.objects.filter(pk=asset_pk, category__timetable__owner=request.user)
        if asset:
            asset[0].delete()
            return apiResponse()
        else:
            return apiResponse(code=524)
    else:
        return apiResponse(code=619)


@csrf_exempt
def update_course_asset_view(request, asset_pk):
    return add_course_asset_view(request, asset_pk=asset_pk)

@csrf_exempt
def add_timetable_event_view(request, event_pk=None):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            if event_pk:
                event = Event.objects.filter(pk=event_pk)
                event = event[0] if event else None
            else:
                event = Event()
            location = Location.objects.filter(
                pk=data.get('location', None), timetable__owner=request.user)
            if location and event:
                event.name=data.get('name', None)
                event.description=data.get('description', None)
                event.status=data.get('status', None)
                event.date=data.get('date', None)
                event.begin=data.get('begin', None)
                event.end=data.get('end', None)
                event.location = location[0]
                try:
                    event.full_clean()
                    event.save()
                    event.interested.add(request.user)
                    return apiResponse()
                except ValidationError as err:
                    return apiResponse(code=525, info=err.messages)
            else:
                return apiResponse(code=526)
        else:
            return apiResponse(code=108)
    else:
        return apiResponse(code=620)

def delete_timetable_event_view(request, event_pk):
    if request.user.is_authenticated:
        event = Event.objects.filter(pk=event_pk, location__timetable__owner=request.user)
        if event:
            event.delete()
            return apiResponse()
        else:
            return apiResponse(code=527)
    else:
        return apiResponse(code=621)

@csrf_exempt
def update_timetable_event_view(request, event_pk):
    return add_timetable_event_view(request, event_pk=event_pk)
