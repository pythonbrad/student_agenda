from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=STATUS_CHOICES[0][0])
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
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
    description = models.CharField(max_length=1024, default='')
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    interested = models.ManyToManyField('Student')
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=STATUS_CHOICES[0][0])
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
    receivers = models.ManyToManyField('Student')
    description = models.CharField(max_length=1024, default='')

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.description

    def get_as_json(self):
        return {
            'pk': self.pk,
            'description': self.description,
        }

# Signals
# Delete file when media delete
@receiver(pre_delete, sender=Asset)
def delete_media(sender, instance, **kwargs):
    instance.media.file.delete()