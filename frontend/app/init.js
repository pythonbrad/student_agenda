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
			// We clean last error
			App.vars.errors = [];
			$('#main').load('app/templates/splash.html');
		},
		index: function () {
			App.views.splash()
			// We config it to permit to splash screen should be showed if the datas are fast loaded
			App.vars.can_pass = 0;
			App.events[0] = setTimeout(function () {
				App.vars.can_pass = 1;
			}, 3000);
			// We perform operation
			// We verify if already login
			Addons.request('/api/login', null, function (d) {
				if (d.code == 200) {
					App.vars.is_login = 1;
				}
				// We load the home view
				App.events[1] = setInterval(function () {
					if (App.vars.can_pass) {
						clearInterval(App.events[1]);
						App.views.home();
					}
				}, 100);
			}, false)
		},
		home: function () {
			App.views.splash()
			// We perform operation
			// ...
			// We load the home page
			if (App.vars.is_login) {
				App.views.base(
					function () {
						$('#contains').load('app/templates/home.html');
						$('#header').load('app/templates/home_header.html');
					}
				);
			} else {
				App.views.login();
			}
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
		login: function (username, password) {
			App.views.splash();
			// We perform operation
			if (username && password) {
				Addons.request('/api/login',
					{username: username, password: password},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							$('#main').load('app/templates/login.html');
						} else {
							App.vars.is_login = 1;
							App.views.home();
						}
					},false
				);
			} else {
				// We load the template
				$('#main').load('app/templates/login.html');
			}
		},
		signin: function (username, email, password, password2) {
			App.views.splash();
			// We perform operation
			if (password != password2) {
				App.vars.errors = ['The passwords not match'];
			} else if (username && email && password && password2) {
				Addons.request('/api/signin',
					{username: username, email: email, password: password, password2: password2},
					function (d) {
						if (d.code != 200) {
							App.vars.errors = [d.error];
							$('#main').load('app/templates/signin.html');
						} else {
							App.views.login();
						}
					},
					false
				);
			} else {
				// We load the template
				$('#main').load('app/templates/signin.html');
			}
		},
		logout: function () {
			App.views.splash();
			// We perform operation
			App.vars.is_login = 0;
			App.views.home();
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