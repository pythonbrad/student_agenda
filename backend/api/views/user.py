from task.models import Course, Classe, Timetable, Notification
from task.models import Lecturer, Absent, Asset, Event
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .tools import apiResponse



def get_timetable_view(request):
    if request.user.is_authentificated:
        return apiResponse(result=Timetable.objects.values())
    else:
        return apiResponse(code=601)

def get_timetable_follower_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=timetable.followers.values())
        else:
            return apiResponse(code=522)
    else:
        return apiResponse(code=624)


def follow_timetable_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            timetable.followers.add(request.user.student_set.get())
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=501)
    else:
        return apiResponse(code=602)


def unfollow_timetable_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            timetable.followers.remove(request.user.student_set.get())
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=502)
    else:
        return apiResponse(code=603)


def get_timetable_lecturer_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=timetable.lecturers_set.values())
        else:
            return apiResponse(code=503)
    else:
        return apiResponse(code=604)


def get_timetable_course_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=Course.objects.filter(lecturers__timetable=timetable).values())
        else:
            return apiResponse(code=504)
    else:
        return apiResponse(code=605)


def get_course_lecturer_view(request, course_pk):
    if request.user.is_authentificated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            return apiResponse(result=course.lecturers.values())
        else:
            return apiResponse(code=505)
    else:
        return apiResponse(code=606)


def get_course_follower_view(request, course_pk):
    if request.user.is_authentificated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            return apiResponse(result=course.followers.values())
        else:
            return apiResponse(code=506)
    else:
        return apiResponse(code=607)


def set_course_follower_view(request, course_pk):
    if request.user.is_authentificated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            course.followers.add(request.user.student_set.get())
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=507)
    else:
        return apiResponse(code=608)


def unset_course_follower_view(request, course_pk):
    if request.user.is_authentificated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            course.followers.remove(request.user.student_set.get())
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=508)
    else:
        return apiResponse(code=609)


def get_timetable_classes_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            return apiResponse(
                result=Classe.objects.filter(
                    location__timetable=timetable[0]).values())
        else:
            return apiResponse(code=509)
    else:
        return apiResponse(code=610)

def get_classe_absent_view(request, classe_pk):
    if request.user.is_authentificated:
        classe = Classe.objects.filter(pk=classe_pk)
        if classe:
            classe = classe[0]
            return apiResponse(result=classe.absents.values())
        else:
            return apiResponse(code=510)
    else:
        return apiResponse(code=611)


@csrf_exempt
def set_classe_absent_view(request, classe_pk):
    if request.user.is_authentificated:
        if request.POST:
            data = request.POST
            classe = Classe.objects.filter(pk=classe_pk)
            if classe:
                classe = classe[0]
                if not Absent.objects.filter(student__user=request.user):
                    absent = Absent.objects.create(
                        student=request.user.student_set.get(),
                        description=data.get('description', None))
                    classe.absents.add(absent)
                    classe.save()
                else:
                    pass
                return apiResponse()
            else:
                return apiResponse(code=511)
        else:
            return apiResponse(code=101)
    else:
        return apiResponse(code=612)


def unset_classe_absent_view(request, classe_pk):
    if request.user.is_authentificated:
        classe = Classe.objects.filter(pk=classe_pk)
        if classe:
            classe = classe[0]
            classe.absents.remove(request.user.student_set.get())
            classe.save()
            return apiResponse()
        else:
            return apiResponse(code=512)
    else:
        return apiResponse(code=613)


def get_timetable_location_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=timetable.locations_set.values())
        else:
            return apiResponse(code=513)
    else:
        return apiResponse(code=614)

def get_timetable_category_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=timetable.categorys_set.values())
        else:
            return apiResponse(code=514)
    else:
        return apiResponse(code=615)

def get_asset_reader_view(request, asset_pk):
    if request.user.is_authentificated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            return apiResponse(result=asset.readers.values())
        else:
            return apiResponse(code=515)
    else:
        return apiResponse(code=616)



def set_asset_reader_view(request, asset_pk):
    if request.user.is_authentificated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            asset.readers.add(request.user.student_set.get())
            asset.save()
            return apiResponse()
        else:
            return apiResponse(code=516)
    else:
        return apiResponse(code=617)


def unset_asset_reader_view(request, asset_pk):
    if request.user.is_authentificated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            asset.readers.remove(request.user.student_set.get())
            asset.save()
            return apiResponse()
        else:
            return apiResponse(code=517)
    else:
        return apiResponse(code=618)


def get_timetable_course_view(request, timetable_pk):
    if request.user.is_authentificated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=Events.objects.filter(location__timetable=timetable).values())
        else:
            return apiResponse(code=518)
    else:
        return apiResponse(code=619)


def get_event_follower_view(request, event_pk):
    if request.user.is_authentificated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            return apiResponse(result=event.followers.values())
        else:
            return apiResponse(code=521)
    else:
        return apiResponse(code=623)


def follow_event_view(request, event_pk):
    if request.user.is_authentificated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            event.interested.add(request.user.student_set.get())
            event.save()
            return apiResponse()
        else:
            return apiResponse(code=519)
    else:
        return apiResponse(code=620)


def unfollow_event_view(request, event_pk):
    if request.user.is_authentificated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            event.interested.remove(request.user.student_set.get())
            event.save()
            return apiResponse()
        else:
            return apiResponse(code=520)
    else:
        return apiResponse(code=621)


def get_notification(request):
    if request.user.is_authentificated:
        return apiResponse(result=Notification.objects.filter(receivers=request.user.student_set.get()).values())
    else:
        return apiResponse(code=622)