from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.name

class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default='')
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Absent"
        verbose_name_plural = "Absents"

    def __str__(self):
        return self.student
    

class Timetable(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Timetable"
        verbose_name_plural = "Timetables"

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"

    def __str__(self):
        return name

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
        return code

class Classe(models.Model):
    STATUS_CHOICES = (
        ('w', 'Waiting'),
        ('s', 'Started'),
        ('c', 'Cancelled'),
        ('e', 'Ended'),
    )
    description = models.CharField(max_length=255, default='')
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=STATUS_CHOICES[0][0])
    absents = models.ManyToManyField('Absent')
    time = models.DateTimeField()
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.course

class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    readers = models.ManyToManyField('Student')

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return self.course + ':' + self.category

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    interested = models.ManyToManyField('Student')
    time = models.DateTimeField()
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    receivers = models.ManyToManyField('Student')
    description = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.description
