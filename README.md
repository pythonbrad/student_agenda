# Student's agenda

![Image](https://github.com/pythonbrad/student_agenda/blob/master/snapshot.gif)

## Problem:
### Many students of UB (University of BUEA) match problems of information (often caused by the disturbance of the network):
- When the timetable has been changed or not
- When a lecturer has cancelled or programmed a course
- When the attendance has been done or not
- When the lecturer is present of not
- When an assignment, tutorial or other document has been given or not
- To have information after an absence (history of activities who has been or not)
- To find past information (documents, events,...)
### Hence have the good information at good instant, it is not easy.

## Solution:
### To solve this problem, we propose a fast and light application (and able send information to students offline) who will be managed by the course delegate or not and who will permit:
- To see the timetable the most update
- To be informed when the timetable has changed or not, the lecturer is present of not
- To find and download a document given (same after many months)
- At a student to inform the course delegate of his absence
- To evict the repetitive diffusion of the same information

# Installation
We recommanded to use https://github.com/pythonbrad/mega.py in the case where github.com/odwyersoftware/mega.py is not updated.
```sh
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

# Backup
Source: https://www.coderedcorp.com/blog/how-to-dump-your-django-database-and-load-it-into-/
NB: To evict error like "matching query does not exist", you should organise each model by order of priority
	eg: auth.user before task.student
```sh
python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 -o backup_$(date +%F).json
```

# Actor, Use case and entities
* An user can manage timetable
	+ View the lessons of today
		- Location
		- Time
		- Status (waiting, started, ended, cancelled)
		- Attendance status (done, not done)
	+ View the events of today
		- Location
		- Time
		- Status (waiting, started, ended, cancelled)
	+ View the full timetable
		- Lessons by day
		- Lessons by week
		- Lessons by month
	+ Follow a timetable
		- Required a shared code
	+ Unfollow a timetable
	+ If admin
	+ Create a timetable
	+ Delete a timetable
* An user can manage asset
	+ View an asset
		- Course
		- Descrition
		- Date of update
		- NB of downloading
		- Category
	+ Download an asset
	+ If moderator
	+ Create an asset
	+ Update an asset
	+ Delete an asset
* An user can manage lesson
	+ View the details about a lesson
	+ If moderator
	+ Create a lesson
	+ Update a lesson
	+ Delete a lesson
* An user can manage event
	+ View the details about a event
	+ If moderator
	+ Create a event
	+ Update a event
	+ Delete a event
* An user can manage data
	+ If admin
	+ Create a lecturer
	+ Create a location
	+ Create a category