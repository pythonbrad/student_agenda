from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save, m2m_changed
from django.dispatch import receiver

STATUS_CHOICES = (
    ('w', 'Waiting'),
    ('s', 'Started'),
    ('c', 'Cancelled'),
    ('e', 'Ended'),
)

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return str(self.user)

    def get_as_json(self):
        return {
            'pk': self.user.pk,
            'username': self.user.username,
            'email': self.user.email,
            'last_login': self.user.last_login,
            'date_joined': self.user.date_joined,
        }

class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    description = models.TextField(max_length=1024)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Absent"
        verbose_name_plural = "Absents"

    def __str__(self):
        return str(self.student)

    def get_as_json(self):
        return {
            'pk': self.pk,
            'user': self.student.pk,
            'description': self.description,
            'time': self.time,
        }
    

class Timetable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1024)
    owner = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='Owner')
    moderators = models.ManyToManyField('Student', related_name='Moderators')
    followers = models.ManyToManyField('Student')

    class Meta:
        verbose_name = "Timetable"
        verbose_name_plural = "Timetables"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'moderators': [moderator.pk for moderator in self.moderators.all()],
            'followers': self.followers.count(),
            'owner': self.owner.get_as_json()
        }

class Lecturer(models.Model):
    name = models.CharField(max_length=64)
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'timetable_pk': self.timetable.pk,
        }

class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    code = models.CharField(max_length=10)
    lecturers = models.ManyToManyField('Lecturer')
    followers = models.ManyToManyField('Student')

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.code

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'lecturers': self.lecturers.count(),
            'followers': self.followers.count(),
        }

class Classe(models.Model):
    description = models.TextField(max_length=1024)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    absents = models.ManyToManyField('Absent')
    attendance_done = models.BooleanField(default=0)
    begin = models.TimeField(default=timezone.now)
    end = models.TimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        return str(self.course)

    def get_as_json(self):
        return {
            'pk': self.pk,
            'description': self.description,
            'location': self.location.get_as_json(),
            'course': self.course.get_as_json(),
            'date': self.date,
            'status': self.status,
            'attendance_done': self.attendance_done,
            'absents': self.absents.count(),
            'begin': self.begin,
            'end': self.end,
            'updated': self.updated,
            'timetable_pk': self.location.timetable.pk,
        }

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)

class Location(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'timetable_pk': self.timetable.pk,
        }

class Media(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/%I_%M_%p')
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('Student', on_delete=models.CASCADE)

class Asset(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    readers = models.ManyToManyField('Student')
    media = models.ForeignKey('Media', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return str(self.course) + ':' + str(self.category)

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'category': self.category.get_as_json(),
            'course': self.course.get_as_json(),
            'readers': self.readers.count(),
            'pub_date': self.pub_date,
            'url': self.media.file.url,
        }

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'timetable_pk': self.timetable.pk,
        }

class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    interested = models.ManyToManyField('Student')
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    date = models.DateField(default=timezone.now)
    begin = models.TimeField(default=timezone.now)
    end = models.TimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'location': self.location.get_as_json(),
            'interested': self.interested.count(),
            'status': self.status,
            'date': self.date,
            'begin': self.begin,
            'end': self.end,
            'updated': self.updated,
            'timetable_pk': self.location.timetable.pk,
        }

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)

    
class Notification(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    receivers = models.ManyToManyField('Student')
    description = models.TextField(max_length=1024)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.description

    def get_as_json(self):
        return {
            'timetable': self.timetable.name,
            'created_date': self.created_date,
            'description': self.description,
        }


class Announce(models.Model):
    message = models.TextField(max_length=1024) 
    audience = models.IntegerField(default=0) # 0 for all users
    receivers = models.ManyToManyField(Student)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Announce for USER_ID %s' % self.audience

    def get_as_json(self):
        return {
            'message': self.message,
            'created_date': self.created_date
        }


class Feedback(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(max_length=1024)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Feedback from %s' % author.username

# Signals
# Delete file when
@receiver(pre_delete, sender=Asset)
def delete_media(sender, instance, **kwargs):
    instance.media.file.delete()

# Create notification when
@receiver(post_save, sender=Classe)
def update_classe(instance, created, **kwargs):
    if created:
        message = "A class of %s has been added for %s %s."
    else:
        message = "The class of %s at %s %s has been updated."
    Notification.objects.create(
        description=message % (
            instance.course.code,
            instance.date,
            instance.begin
        ),
        timetable=instance.location.timetable,
    )

@receiver(post_save, sender=Asset)
def update_asset(instance, created, **kwargs):
    if created:
        message = "The asset <%s> of %s has been added."
    else:
        message = "The asset <%s> of %s has been updated."
    Notification.objects.create(
        description=message % (
            instance.name,
            instance.course.code
        ),
        timetable=instance.category.timetable,
    )

@receiver(post_save, sender=Event)
def update_event(instance, created, **kwargs):
    if created:
        message = "An event has been added for %s %s."
    else:
        message = "The event at %s %s has been updated."
    Notification.objects.create(
        description=message % (
            instance.date,
            instance.begin
        ),
        timetable=instance.location.timetable,
    )

# Create announce when
@receiver(post_save, sender=User)
def new_user(instance, created, **kwargs):
    if created:
        Announce.objects.create(audiance=instance.pk, message="Hello %s and welcome, to Student's Agenda." % instance.username)

@receiver(m2m_changed, sender=Timetable.moderators.through)
def update_moderator(instance, action, pk_set, **kwargs):
    if action == 'post_remove':
        for i in pk_set:
            Announce.objects.create(audience=i, message="From %s, you lost your status of moderator." % instance.name)
    elif action == 'post_add':
        for i in pk_set:
            Announce.objects.create(audience=i, message="From %s, you have been granted to moderator." % instance.name)
    else:
        pass