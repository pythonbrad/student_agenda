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
        }

class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default='')
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Absent"
        verbose_name_plural = "Absents"

    def __str__(self):
        return str(self.student)

    def get_as_json(self):
        return {
            'pk': str(self.pk),
            'user': self.student.get_as_json(),
            'description': self.description,
            'time': self.time,
        }
    

class Timetable(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, default='')
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
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'moderators': [moderator.get_as_json() for moderator in self.moderators.all()],
            'followers': [follower.get_as_json() for follower in self.followers.all()],
            'owner': self.owner.get_as_json()
        }

class Lecturer(models.Model):
    name = models.CharField(max_length=50)
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': str(self.pk),
            'name': self.name,
            'timetable': self.timetable.get_as_json(),
        }

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
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
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'lecturers': [lecturer.get_as_json() for lecturer in self.lecturers.all()],
            'followers': [follower.get_as_json() for follower in self.followers.all()],
        }

class Classe(models.Model):
    description = models.CharField(max_length=255, default='')
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
            'pk': str(self.pk),
            'description': self.description,
            'location': self.location.get_as_json(),
            'course': self.course.get_as_json(),
            'date': self.date,
            'status': self.status,
            'attendance_done': self.attendance_done,
            'absents': [absent.get_as_json() for absent in self.absents.all()],
            'begin': self.begin,
            'end': self.end,
            'updated': self.updated,
        }

class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'timetable': self.timetable.get_as_json(),
        }

class Media(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/%I_%M_%p')
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('Student', on_delete=models.CASCADE)

class Asset(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
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
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'category': self.category.get_as_json(),
            'course': self.course.get_as_json(),
            'readers': [reader.get_as_json() for reader in self.readers.all()],
            'pub_date': self.pub_date,
            'url': self.media.file.url,
        }

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_as_json(self):
        return {
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'timetable': self.timetable.get_as_json(),
        }

class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
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
            'pk': str(self.pk),
            'name': self.name,
            'description': self.description,
            'location': self.location.get_as_json(),
            'interested': [i.get_as_json() for i in self.interested.all()],
            'status': self.status,
            'date': self.date,
            'begin': self.begin,
            'end': self.end,
            'updated': self.updated,
        }

    
class Notification(models.Model):
    receivers = models.ManyToManyField('Student')
    description = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.description

    def get_as_json(self):
        return {
            'pk': str(self.pk),
            'description': self.description,
        }

# Signals
# Delete file when media delete
@receiver(pre_delete, sender=Asset)
def delete_media(sender, instance, **kwargs):
    instance.media.file.delete()