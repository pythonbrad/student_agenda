from task.models import Course, Classe, Timetable, Notification, Feedback, Announce, Media
from task.models import Lecturer, Absent, Asset, Event, STATUS_CHOICES
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from .tools import apiResponse
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import _thread
import time
from mega import Mega

def get_timetable_view(request):
    if request.user.is_authenticated:
        result = []
        for timetable in Timetable.objects.all():
            _ = timetable.get_as_json()
            if timetable.owner == request.user:
                _.update({'code': timetable.code})
            result.append(_)
        return apiResponse(result=result)
    else:
        return apiResponse(code=601)

def get_timetable_follow_by_me_view(request):
    if request.user.is_authenticated:
        timetables = Timetable.objects.filter(followers=request.user)
        if timetables:
            return apiResponse(result=[timetable.get_as_json() for timetable in timetables])
        else:
            return apiResponse(result=[])
    else:
        return apiResponse(code=624)


def follow_timetable_view(request, timetable_pk, timetable_code=''):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk, code=timetable_code)
        if timetable:
            timetable = timetable[0]
            timetable.followers.add(request.user)
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=501)
    else:
        return apiResponse(code=602)


def unfollow_timetable_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            timetable.followers.remove(request.user)
            timetable.save()
            return apiResponse()
        else:
            return apiResponse(code=502)
    else:
        return apiResponse(code=603)


def get_timetable_lecturer_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=[lecturer.get_as_json() for lecturer in timetable.lecturer_set.all()])
        else:
            return apiResponse(code=503)
    else:
        return apiResponse(code=604)


def get_timetable_course_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            courses = Course.objects.filter(lecturers__timetable=timetable)
            return apiResponse(result=[course.get_as_json() for course in courses])
        else:
            return apiResponse(code=504)
    else:
        return apiResponse(code=605)


def get_course_lecturer_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            return apiResponse(result=[lecturer.get_as_json() for lecturer in course.lecturers.all()])
        else:
            return apiResponse(code=505)
    else:
        return apiResponse(code=606)


def get_course_follower_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            return apiResponse(result=[follower.get_as_json() for follower in course.followers.all()])
        else:
            return apiResponse(code=506)
    else:
        return apiResponse(code=607)


def set_course_follower_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            course.followers.add(request.user)
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=507)
    else:
        return apiResponse(code=608)


def unset_course_follower_view(request, course_pk):
    if request.user.is_authenticated:
        course = Course.objects.filter(pk=course_pk)
        if course:
            course = course[0]
            course.followers.remove(request.user)
            course.save()
            return apiResponse()
        else:
            return apiResponse(code=508)
    else:
        return apiResponse(code=609)


def get_status_choice_view(request):
    if request.user.is_authenticated:
        return apiResponse(result=STATUS_CHOICES)
    else:
        return apiResponse(code=611)


def get_timetable_classes_view(request, timetable_pk, next_day=None):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            current_date = timezone.now().date()
            classes = Classe.objects.filter(location__timetable=timetable[0])
            if next_day != None:
                classes = classes.filter(date=current_date+timezone.timedelta(next_day)).order_by('begin')
            return apiResponse(
                result=[classe.get_as_json() for classe in classes])
        else:
            return apiResponse(code=509)
    else:
        return apiResponse(code=610)

def get_classe_absent_view(request, classe_pk):
    if request.user.is_authenticated:
        classe = Classe.objects.filter(pk=classe_pk)
        if classe:
            classe = classe[0]
            return apiResponse(result=[absent.get_as_json() for absent in classe.absents.all()])
        else:
            return apiResponse(code=510)
    else:
        return apiResponse(code=611)


@csrf_exempt
def set_classe_absent_view(request, classe_pk):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            classe = Classe.objects.filter(pk=classe_pk)
            if classe:
                classe = classe[0]
                if not Absent.objects.filter(user=request.user):
                    absent = Absent.objects.create(
                        user=request.user,
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
    if request.user.is_authenticated:
        classe = Classe.objects.filter(pk=classe_pk)
        if classe:
            classe = classe[0]
            classe.absents.remove(request.user)
            classe.save()
            return apiResponse()
        else:
            return apiResponse(code=512)
    else:
        return apiResponse(code=613)


def get_timetable_location_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=[location.get_as_json() for location in timetable.location_set.all()])
        else:
            return apiResponse(code=513)
    else:
        return apiResponse(code=614)

def get_timetable_category_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            return apiResponse(result=[category.get_as_json() for category in timetable.category_set.all()])
        else:
            return apiResponse(code=514)
    else:
        return apiResponse(code=615)

def get_timetable_asset_view(request, timetable_pk):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            assets = Asset.objects.filter(course__lecturers__timetable=timetable[0])
            return apiResponse(
                result=[asset.get_as_json() for asset in assets])
        else:
            return apiResponse(code=509)
    else:
        return apiResponse(code=610)

def get_asset_reader_view(request, asset_pk):
    if request.user.is_authenticated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            return apiResponse(result=[reader.get_as_json() for reader in asset.readers.all()])
        else:
            return apiResponse(code=515)
    else:
        return apiResponse(code=616)



def set_asset_reader_view(request, asset_pk):
    if request.user.is_authenticated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            asset.readers.add(request.user)
            asset.save()
            return apiResponse()
        else:
            return apiResponse(code=516)
    else:
        return apiResponse(code=617)


def unset_asset_reader_view(request, asset_pk):
    if request.user.is_authenticated:
        asset = Asset.objects.filter(pk=asset_pk)
        if asset:
            asset = asset[0]
            asset.readers.remove(request.user)
            asset.save()
            return apiResponse()
        else:
            return apiResponse(code=517)
    else:
        return apiResponse(code=618)


def get_timetable_event_view(request, timetable_pk, next_day=None):
    if request.user.is_authenticated:
        timetable = Timetable.objects.filter(pk=timetable_pk)
        if timetable:
            timetable = timetable[0]
            current_date = timezone.now().date()
            events = Event.objects.filter(location__timetable=timetable)
            if next_day != None:
                events = events.filter(date=current_date+timezone.timedelta(next_day)).order_by('begin')
            return apiResponse(result=[event.get_as_json() for event in events])
        else:
            return apiResponse(code=518)
    else:
        return apiResponse(code=619)


def get_event_follower_view(request, event_pk):
    if request.user.is_authenticated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            return apiResponse(result=[follower.get_as_json() for followers in event.followers.all()])
        else:
            return apiResponse(code=521)
    else:
        return apiResponse(code=623)


def follow_event_view(request, event_pk):
    if request.user.is_authenticated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            event.interested.add(request.user)
            event.save()
            return apiResponse()
        else:
            return apiResponse(code=519)
    else:
        return apiResponse(code=620)


def unfollow_event_view(request, event_pk):
    if request.user.is_authenticated:
        event = Event.objects.filter(pk=event_pk)
        if event:
            event = event[0]
            event.interested.remove(request.user)
            event.save()
            return apiResponse()
        else:
            return apiResponse(code=520)
    else:
        return apiResponse(code=621)


def get_notification(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(timetable__followers=request.user, created_date__gte=request.user.date_joined).exclude(receivers=request.user).order_by('-pk')
        if not notifications:
            notifications = Notification.objects.filter(timetable__followers=request.user).order_by('-pk')[:5]
        results = []
        for notification in notifications:
            results.append(notification.get_as_json())
            notification.receivers.add(request.user)
        return apiResponse(result=results)
    else:
        return apiResponse(code=623)

def get_announce(request):
    if request.user.is_authenticated:
        announces = Announce.objects.filter(Q(audience=request.user.pk) | Q(audience=0), created_date__gte=request.user.date_joined).exclude(receivers=request.user).order_by('-pk')
        results = []
        for announce in announces:
            results.append(announce.get_as_json())
            announce.receivers.add(request.user)
        return apiResponse(result=results)
    else:
        return apiResponse(code=626)

@csrf_exempt
def feedback_view(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST
            feedback = Feedback(author=request.user, message=data.get('message', None))
            try:
                feedback.full_clean()
                feedback.save()
                return apiResponse()
            except ValidationError as err:
                return apiResponse(code=522, info=err.messages)
        else:
            return apiResponse(code=102)
    else:
        return apiResponse(code=625)

def download_media_view(request, media_pk):
    if request.user.is_authenticated:
        media = Media.objects.filter(pk=media_pk)
        if media:
            mega_api = Mega()

            class VirtualFile:
                def __init__(self):
                    self.data = None
                    self.readable = False
                    self.is_closed = False

                # We write if the reading is not active
                def write(self, x):
                    while self.readable:
                        time.sleep(0.1)
                    self.data = x
                    self.readable = True

                # We read if the writing is not active
                def read(self, x=None):
                    while not self.readable and not self.is_closed:
                        time.sleep(0.1)
                    data = self.data
                    # We clean the data after each reading
                    self.data = b''
                    self.readable = False
                    return data

                # If you don't call it, we will risk to have an infinite reading
                def close(self):
                    self.is_closed = True

            output_file = VirtualFile()

            _thread.start_new_thread(lambda:mega_api.download_url(media[0].cloud_url, output_file=output_file), ())

            response = HttpResponse(FileWrapper(output_file), content_type=media[0].origin_content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % media[0].origin_name
            response['Content-Length'] = media[0].origin_size
            return response
        else:
            return apiResponse(code=523)
    else:
        return apiResponse(code=625)