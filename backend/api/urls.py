from django.urls import path
from .views import authentification, user, administrator


urlpatterns = [
    path('auth/signin', authentification.signin_view),
    path('auth/login', authentification.login_view),
    path('auth/logout', authentification.logout_view),
    path('user/timetable/follow', user.get_timetable_follow_by_me_view),
    path('user/timetable/<int:timetable_pk>/follow', user.follow_timetable_view),
    path('user/timetable/<int:timetable_pk>/unfollow', user.unfollow_timetable_view),
    path('user/timetable', user.get_timetable_view),
    path('user/classe/status/choice', user.get_classe_status_choice_view),
    path('user/timetable/<int:timetable_pk>/classe', user.get_timetable_classes_view),
    path('user/timetable/<int:timetable_pk>/lecturer', user.get_timetable_lecturer_view),
    path('user/timetable/<int:timetable_pk>/location', user.get_timetable_location_view),
    path('user/timetable/<int:timetable_pk>/course', user.get_timetable_course_view),
    path('user/timetable/<int:timetable_pk>/category', user.get_timetable_category_view),
    path('admin/timetable/add', administrator.add_timetable_view),
    path('admin/timetable/course/<int:course_pk>/lesson/add', administrator.add_timetable_classe_view),
    path('admin/timetable/course/<int:course_pk>/asset/add', administrator.add_course_asset_view),
    path('admin/timetable/course/add', administrator.add_timetable_course_view),
    path('admin/timetable/<int:timetable_pk>/lecturer/add', administrator.add_timetable_lecturer_view),
    path('admin/timetable/<int:timetable_pk>/location/add', administrator.add_timetable_location_view),
    path('admin/timetable/<int:timetable_pk>/category/add', administrator.add_timetable_category_view),
]
