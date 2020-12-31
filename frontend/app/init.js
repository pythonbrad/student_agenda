// This script init datas and load datas in the loading of the page
App = {
	// I can inspired me of Django mvc
	views: {
		// For the moment load just the pages
		base: function (next=function () {}) {
			$('#main').load('app/templates/base.html');
			setTimeout(function () {
				next();
			}, 100);
		},
		splash: function () {
			// We clean last error and delete all events
			App.vars.errors = [];
			App.vars.can_pass = 0;
			for (var i = 0; i < 100; i++) {
				clearInterval(App.events[i]);
			};
			$('#main').load('app/templates/splash.html');
		},
		index: function () {
			App.views.splash();
			// We config it to permit to splash screen should be showed if the datas are fast loaded
			App.vars.can_pass = 0;
			App.events[0] = setTimeout(function () {
				App.vars.can_pass = 1;
			}, 3000);
			// We perform operation
			// We verify if already login
			Addons.request('/api/auth/login', null, function (d) {
				if (d.code == 200) {
					App.vars.is_login = 1;
					App.models.user = {username: d.result.username, pk: d.result.pk};
				} else {
					App.vars.is_login = 0;
				}
				// We load the next view
				App.events[1] = setInterval(function () {
					if (App.vars.can_pass) {
						clearInterval(App.events[1]);
						if (App.vars.is_login) {
							// We verify if least 1 timetable is already follow
							Addons.request('/api/user/timetable/follow', null, function (d) {
								if (d.code == 200 && d.result.length) {
									// We load the home view
									App.models.timetables = d.result;
									App.views.home();
								} else {
									App.views.choose_timetable();
								}
							})
						} else {
							// We load the login view
							App.views.login();
						}
					}
				}, 100);
			}, false)
		},
		choose_timetable: function (timetable_pk) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/choose_timetable.html');
				}
			}, 100);

			if (timetable_pk) {
				Addons.request('/api/user/timetable/'+timetable_pk+'/follow', null, function (d) {
					if (d.code != 200) {
						App.vars.errors = [d.error];
						App.vars.can_pass = 1;
					} else {
						App.views.choose_timetable();
					}
				}, false);
			} else {
				// We load timetable
				Addons.request('/api/user/timetable', null, function (d) {
					if (d.code == 200) {
						App.models.timetables = d.result;
						// We load the page
						App.vars.can_pass = 1;
					} else {
						alert('error: code '+d.code);
					}
				}, false);
			}
		},
		add_timetable: function (name, description) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/add_timetable.html');
				}
			}, 100);
			// We send data
			if (name && description) {
				Addons.request('/api/admin/timetable/add',
					{name: name, description: description},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.choose_timetable();
						}
					}, false);
			} else {
				// We load the template
				App.vars.can_pass = 1;
			};
		},
		add_lesson: function (description,status,begin,end,location_pk,course_pk) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/add_lesson.html');
				}
			}, 100);
			// We send data
			if (description && status && begin && end && location_pk && course_pk) {
				Addons.request('/api/admin/timetable/course/'+course_pk+'/lesson/add',
					{description:description, status:status, begin:begin, end:end, location_pk:location_pk},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.add_lesson();
						}
					}, false);
			} else {
				// We should load location and course
				// We load the template
				App.vars.can_pass = 1;
			}
		},
		add_lecturer: function (name,timetable_pk) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/add_lecturer.html');
				}
			}, 100);
			// We send data
			if (name && timetable_pk) {
				Addons.request('admin/timetable/'+timetable_pk+'/lecturer/add',
					{name:name},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.add_lecturer();
						}
					}, false);
			} else {
				// We load the template
				App.vars.can_pass = 1;
			}
		},
		add_location: function (name,description,timetable_pk) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/add_location.html');
				}
			}, 100);
			// We send data
			if (name && description && timetable_pk) {
				Addons.request('admin/timetable/'+timetable_pk+'/location/add',
					{name:name,description:description},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.add_location();
						}
					}, false);
			} else {
				// We load the template
				App.vars.can_pass = 1;
			}
		},
		home: function () {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					// We load the home page
					App.views.base(
						function () {
							$('#contains').load('app/templates/home.html');
							$('#header').load('app/templates/home_header.html');
						}
					);
				}
			}, 100);
			// We get datas
			App.models.classes = [];
			for (var i = 0; i < App.models.timetables.length; i++) {
				Addons.request('/api/user/timetable/'+App.models.timetables[i].pk+'/classe', null, function (d) {
					if (d.code == 200) {
						for (var ii = 0; ii < d.result.length; ii++) {
							App.models.classes.push(d.result[ii]);
						}
					};
					if (i+1 == App.models.timetables.length) {
						App.vars.can_pass = 1;
					};
				}, false);
			};
		},
		supports: function () {
			App.views.splash();
			// We perform operation
			// We load the template
			App.views.base(
				function () {
					$('#contains').load('app/templates/supports.html');
					$('#header').load('app/templates/supports_header.html');
				}
			);
		},
		events: function () {
			App.views.splash();
			// We perform operation
			// We load the template
			App.views.base(
				function () {
					$('#contains').load('app/templates/events.html');
					$('#header').load('app/templates/events_header.html');
				}
			);
		},
		notifications: function () {
			App.views.splash();
			// We perform operation
			// We load the template
			App.views.base(
				function () {
					$('#contains').load('app/templates/notifications.html');
					$('#header').load('app/templates/notifications_header.html');
				}
			);
		},
		login: function (username, password) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/login.html');
				}
			}, 100);
			if (username && password) {
				Addons.request('/api/auth/login',
					{username: username, password: password},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.index();
						}
					},false
				);
			} else {
				// We load the template
				App.vars.can_pass = 1;
			}
		},
		signin: function (username, email, password, password2) {
			App.views.splash();
			// We perform operation
			App.vars.can_pass = 0;
			App.events[0] = setInterval(function () {
				if (App.vars.can_pass) {
					clearInterval(App.events[0]);
					$('#main').load('app/templates/signin.html');
				}
			}, 100);
			if (password != password2) {
				App.vars.errors = ['The passwords not match'];
			} else if (username && email && password && password2) {
				Addons.request('/api/auth/signin',
					{username: username, email: email, password: password, password2: password2},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							App.vars.can_pass = 1;
						} else {
							App.views.login();
						}
					},
					false
				);
			} else {
				// We load the template
				App.vars.can_pass = 1;
			}
		},
		profil: function () {
			App.views.splash();
			// We perform operation
			// We load the template
			App.views.base(
				function () {
					$('#contains').load('app/templates/profil.html');
					$('#header').load('app/templates/profil_header.html');
				}
			);
		},
		logout: function () {
			App.views.splash();
			// We perform operation
			Addons.request('/api/auth/logout',null,
				function (d) {
					setTimeout(function () {
						App.views.index();
					}, 200);
				},false
			);
		},
		admin: function () {
			App.views.splash();
			// We perform operation
			// We load the template
			$('#main').load('app/templates/admin.html');
		},
	},
	models: {},
	events: {},
	vars: {
		errors: [],
		is_login: 0,
	},
};

// We launch the default page
App.views.index();