# Student's agenda

![Image](https://github.com/pythonbrad/student_agenda/blob/master/snapshot.gif)

## Problem description
Many students of UB (University of BUEA) match problems of information (often caused by the disturbance of the network):
- When the timetable has been changed or not
- When a lecturer has cancelled or programmed a course
- When the attendance has been done or not
- When the lecturer is present of not
- When an assignment, tutorial or other document has been given or not
- To have information after an absence (history of activities who has been or not)
- To find past information (documents, events,...)
Hence have the good information at good instant, it is not easy.

## Features
- Display the updated timetable
- Notify on changed timetable (creating and deleting of events)
- Notify on changed information (new ressource, updating of time, status, venue,... of an event or course)
- Cloud storage and media management
- Limit the redundancy of information 

## Installation
- Clone the project
```sh
git clone https://github.com/pythonbrad/student_agenda.git
```
- Install the requirements
```sh
pip install --upgrade pip
pip install -r requirements_raw.txt
```
- Config the environement (.env file)
```sh
cp .env_example .env
python manage.py makemigrations
python manage.py migrate
```

## Backup
Source: https://www.coderedcorp.com/blog/how-to-dump-your-django-database-and-load-it-into-/
```bash
mkdir -p backup
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 -o backup/$(date +%F).json
```
##### NB: To evict error like "matching query does not exist", you should organise each model by order of priority
	eg: auth.user before task.student

## How to contrib?
Feel you free to make issues and pull requests.
