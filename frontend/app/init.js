/*! Agenda's Student | (c) fomegnemeudje@outlook.com */
// This script init datas and load datas in the loading of the page
App = {
	// I can inspired me of Django mvc
	views: {
		// For the moment load just the pages
		base: function (next=function () {}) {
			$('#main').empty();
			$('#main').load('app/templates/base.html', next);
		},
		splash: function (next=function () {}) {
			$('#main').empty();
			// We clean last error, delete all events and tmp datas
			App.vars.errors = [];
			App.vars.tmp = {};
			for (var i = 0; i < 100; i++) {
				clearInterval(App.events[i]);
			};
			$('#main').load('app/templates/splash.html',next);
		},
		error: function () {
			$('#main').empty();
			$('#main').html('<div class="splash-image" align="center"><i class="fas fa-6x fa-disease text-warning"></i><h4><b>Error unexpected.</b></h4><i style="font-size: 75%">If persist, you can contact the webmaster.<br>Email: fomegnemeudje@outlook.com</i><hr size="#"><h5></div>');
		},
		index: function () {
			App.views.splash(
				function () {
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
							App.vars.now = d.result.last_login;
						} else {
							App.vars.is_login = 0;
						}
						// We load the next view
						App.events[1] = setInterval(function () {
							// We verify if all the operations are finished
							if (App.vars.can_pass) {
								clearInterval(App.events[1]);
								if (App.vars.is_login) {
									// We load c0nstant
								    Addons.request('/api/user/status/choice', null, function (d) {
								        if(d.code == 200) {
								            App.vars.STATUS_CHOICES = d.result;
								            App.vars.STATUS_CHOICES_DICT = {};
								            for(i=0;i<d.result.length;i++) {
								                App.vars.STATUS_CHOICES_DICT[d.result[i][0]] = d.result[i][1];
								            }
								        }
								    }, true);
									// We verify if least 1 timetable is already follow
									Addons.request('/api/user/timetable/follow', null, function (d) {
										if (d.code == 200 && d.result.length) {
											// We load the home view
											App.models.timetables = d.result;
											App.views.home();
										} else {
											App.views.choose_timetable();
										}
									}, true);
								} else {
									// We load the login view
									App.views.login();
								};
							};
						}, 100);
					}, false);
				}
			);
		},
		choose_timetable: function (timetable_pk, reverse) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/choose_timetable.html');
						};
					}, 100);
					if (timetable_pk) {
						Addons.request(
							'/api/user/timetable/'+timetable_pk+'/'+(reverse?'unfollow':'follow'),
							null,
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.choose_timetable();
								};
							},
							false
						);
					} else {
						// We load timetable
						Addons.request('/api/user/timetable', null, function (d) {
							if (d.code == 200) {
								App.models.timetables = d.result;
								// We load the page
								App.vars.can_pass = 1;
							} else {
								alert('error: code '+d.code);
							};
						}, false);
					};
				}
			);
		},
		add_timetable: function (name, description) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_timetable.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description};
					// We send data
					if (name && description) {
						Addons.request('/api/admin/timetable/add',
							{name: name, description: description},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.index();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		add_event: function (name,description,status,date,begin,end,location_pk,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_event.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description,status:status,date:date,begin:begin,end:end,location_pk:location_pk, timetable_pk:timetable_pk};
					// We send data
					if (name && description && status && date && begin && end && location_pk) {
						Addons.request('/api/admin/timetable/event/add',
							{name:name,description:description,status:status,date:date,begin:begin,end:end,location:location_pk},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		delete_event: function (event_pk) {
			App.views.splash(
				function () {
					// We perform operation
					Addons.request('/api/admin/timetable/event/'+event_pk+'/delete',null,
						function (d) {
							App.views.events();
						},false
					);
				}
			);
		},
		update_event: function (event_id,name,description,status,date,begin,end,location_pk,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We convert add event to update event
							$('#main').load('app/templates/add_event.html', function () {
								$('#header').html($('#header').html().replace('Add', 'Update'));
								$('#main').html($('#main').html().replace('views.add_event(', 'views.update_event(App.vars.tmp.form.event_id,'));
							});
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {event_id:event_id,name:name,description:description,status:status,date:date,begin:begin,end:end,location_pk:location_pk,timetable_pk:timetable_pk};
					// We send data
					if (event_id != null) {
						if (name && description && status && date && begin && end && location_pk) {
							Addons.request('/api/admin/timetable/event/'+App.models.events[event_id].pk+'/update',
								{name:name,description:description,status:status,date:date,begin:begin,end:end,location:location_pk},
								function (d) {
									if (d.code != 200) {
										App.vars.errors = [d.error];
										App.vars.can_pass = 1;
									} else {
										App.views.events();
									};
								}, false);
						} else {
							// We save the event data in the form
					        App.vars.tmp.form = {
					        	name:App.models.events[event_id].name,
					        	description:App.models.events[event_id].description,
					        	status:App.models.events[event_id].status,
					        	date:App.models.events[event_id].date,
					        	begin:App.models.events[event_id].begin,
					        	end:App.models.events[event_id].end,
					        	location_pk:App.models.events[event_id].location.pk,
					        	timetable_pk:App.models.events[event_id].location.timetable.pk,
					        	event_id:event_id
					        };
							// We load the template
							App.vars.can_pass = 1;
						};
					} else {
						App.views.events();
					};
				}
			);
		},
		add_lesson: function (description,attendance_done,status,date,begin,end,location_pk,course_pk,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_lesson.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {description:description,attendance_done:attendance_done,status:status,date:date,begin:begin,end:end,location_pk:location_pk,course_pk:course_pk,timetable_pk:timetable_pk};
					// We send data
					if (description && attendance_done && status && date && begin && end && location_pk && course_pk) {
						Addons.request('/api/admin/timetable/course/'+course_pk+'/classe/add',
							{description:description, attendance_done:attendance_done, status:status, date:date, begin:begin, end:end, location:location_pk, course:course_pk},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We should load location and course
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		delete_lesson: function (classe_pk) {
			App.views.splash(
				function () {
					// We perform operation
					Addons.request('/api/admin/timetable/classe/'+classe_pk+'/delete',null,function (d) {
						App.views.home();
					}, false);
				}
			);
		},
		update_lesson: function (lesson_id,description,attendance_done,status,date,begin,end,location_pk,course_pk,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We convert add lesson to update lesson
							$('#main').load('app/templates/add_lesson.html', function () {
								$('#header').html($('#header').html().replace('Add', 'Update'));
								$('#main').html($('#main').html().replace('views.add_lesson(', 'views.update_lesson(App.vars.tmp.form.lesson_id,'));
							});
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {description:description,attendance_done:attendance_done,status:status,date:date,begin:begin,end:end,location_pk:location_pk,course_pk:course_pk,timetable_pk:timetable_pk,lesson_id:lesson_id};
					// We send data
					if (lesson_id != null) {
						if (description && attendance_done && status && date && begin && end && location_pk && course_pk) {
							Addons.request('/api/admin/timetable/classe/'+App.models.classes[lesson_id].pk+'/update',
								{description:description, attendance_done:attendance_done, status:status, date:date, begin:begin, end:end, location:location_pk, course:course_pk},
								function (d) {
									if (d.code != 200) {
										App.vars.errors = [d.error];
										App.vars.can_pass = 1;
									} else {
										App.views.home();
									};
								}, false);
						} else {
							// We save the lesson data in the form
					        App.vars.tmp.form = {
					        	description:App.models.classes[lesson_id].description,
					        	attendance_done:App.models.classes[lesson_id].attendance_done ? 1 : 0,
					        	status:App.models.classes[lesson_id].status,
					        	date:App.models.classes[lesson_id].date,
					        	begin:App.models.classes[lesson_id].begin,
					        	end:App.models.classes[lesson_id].end,
					        	location_pk:App.models.classes[lesson_id].location.pk,
					        	course_pk:App.models.classes[lesson_id].course.pk,
					        	timetable_pk:App.models.classes[lesson_id].location.timetable.pk,
					        	lesson_id:lesson_id
					        };
							// We load the template
							App.vars.can_pass = 1;
						};
					} else {
						App.views.home();
					};
				}
			);
		},
		add_lecturer: function (name,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_lecturer.html');
						}
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,timetable_pk:timetable_pk};
					// We send data
					if (name && timetable_pk) {
						Addons.request('/api/admin/timetable/'+timetable_pk+'/lecturer/add',
							{name:name},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		add_location: function (name,description,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_location.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description,timetable_pk:timetable_pk};
					// We send data
					if (name && description && timetable_pk) {
						Addons.request('/api/admin/timetable/'+timetable_pk+'/location/add',
							{name:name,description:description},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		add_category: function (name,description,timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_category.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description,timetable_pk:timetable_pk};
					// We send data
					if (name && description && timetable_pk) {
						Addons.request('/api/admin/timetable/'+timetable_pk+'/category/add',
							{name:name,description:description},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		add_course: function (name,code,description,lecturer_pks, timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_course.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,code:code,description:description,timetable_pk:timetable_pk,lecturer_pks:lecturer_pks};
					// We send data
					if (name && code && description && lecturer_pks.length) {
						Addons.request('/api/admin/timetable/course/add',
							{name:name,code:code,description:description,lecturers:lecturer_pks},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.admin();
								};
							}, false);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		add_asset: function (name, description, category_pk, course_pk, files, timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					MAX_SIZE = 1024*1024*10;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/add_asset.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description,category_pk:category_pk,course_pk:course_pk,timetable_pk:timetable_pk};
					// We send data
					if (name && description && category_pk && course_pk && files.length) {
						if (files[0].size < MAX_SIZE) {
							media_data = new FormData();
							media_data.append('file', files[0]);
							$.ajax({
								url: '/api/admin/media/add',
								type: 'post',
								data: media_data,
								contentType: false,
								processData: false,
								success: function(response){
									if(response.code == 200){
										media_pk = response.result;
										Addons.request(
											'/api/admin/timetable/course/'+course_pk+'/asset/add',
											{name:name,description:description,category:category_pk,media:media_pk},
											function (d) {
												if (d.code != 200) {
													App.vars.errors = [d.error];
													App.vars.can_pass = 1;
												} else {
													App.views.admin();
												};
											},
											false
										);
									} else {
										App.vars.errors = [response.error];
										App.vars.can_pass = 1;
									};
								},
								async: false,
							});
						} else {
							App.vars.errors = ['The file is too large, maximun '+MAX_SIZE/(1024*1024)+' MB'];
							App.vars.can_pass = 1;
						};
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		delete_asset: function (asset_pk) {
			App.views.splash(
				function () {
					// We perform operation
					Addons.request('/api/admin/timetable/asset/'+asset_pk+'/delete',null,
						function (d) {
							App.views.supports();
						},false
					);
				}
			);
		},
		update_asset: function (asset_id, name, description, category_pk, course_pk, files, timetable_pk) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We convert add asset to update asset
							$('#main').load('app/templates/add_asset.html', function () {
								$('#asset_media').parent().hide();
								$('#header').html($('#header').html().replace('Add', 'Update'));
								$('#main').html($('#main').html().replace('views.add_asset(', 'views.update_asset(App.vars.tmp.form.asset_id,'));
							});
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {name:name,description:description,category_pk:category_pk,course_pk:course_pk,timetable_pk:timetable_pk,asset_id:asset_id};
					// We send data
					if (asset_id != null) {
						if (name && description && category_pk && course_pk) {
							Addons.request('/api/admin/timetable/asset/'+App.models.assets[asset_id].pk+'/update',
								{name:name,description:description,category:category_pk,course:course_pk},
								function (d) {
									if (d.code != 200) {
										App.vars.errors = [d.error];
										App.vars.can_pass = 1;
									} else {
										App.views.supports();
									};
								}, false);
						} else {
							// We save the lesson data in the form
					        App.vars.tmp.form = {
					        	name:App.models.assets[asset_id].name,
					        	description:App.models.assets[asset_id].description,
					        	category_pk:App.models.assets[asset_id].category.pk,
					        	course_pk:App.models.assets[asset_id].course.pk,
					        	timetable_pk:App.models.assets[asset_id].category.timetable.pk,
					        	asset_id:asset_id
					        };
							// We load the template
							App.vars.can_pass = 1;
						};
					} else {
						App.views.supports();
					};
				}
			);
		},
		home: function (next_day=0) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We load the home page
							App.views.base(
								function () {
									$('#header').load('app/templates/home_header.html');
									$('#contains').load('app/templates/home.html', function () {
										$('#next_day').click(function () {
											App.views.home(next_day+1);
										});
										$('#next_day').text('now + '+(next_day+1)+' day'+(next_day?'s':''));
									});
								}
							);
						};
					}, 100);
					// We get data
					App.vars.get_lessons(next_day);
				}
			);
		},
		supports: function () {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We load the page
							App.views.base(
								function () {
									$('#contains').load('app/templates/supports.html');
									$('#header').load('app/templates/supports_header.html');
								}
							);
						};
					}, 100);
					// We get datas
					App.models.assets = [];
					for (var i = 0; i < App.models.timetables.length; i++) {
						Addons.request('/api/user/timetable/'+App.models.timetables[i].pk+'/asset', null, function (d) {
							if (d.code == 200) {
								for (var ii = 0; ii < d.result.length; ii++) {
									App.models.assets.push(d.result[ii]);
								};
							};
							if (i+1 == App.models.timetables.length) {
								App.vars.can_pass = 1;
							};
						}, false);
					};
				}
			);
		},
		events: function (next_day=0) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							// We load the page
							App.views.base(
								function () {
									$('#header').load('app/templates/events_header.html');
									$('#contains').load('app/templates/events.html', function () {
										$('#next_day').click(function () {
											App.views.events(next_day+1);
										});
										$('#next_day').text('now + '+(next_day+1)+' day'+(next_day?'s':''));
									});
								}
							);
						};
					}, 100);
					// We get data
					App.vars.get_events(next_day);
				}
			);
		},
		notifications: function () {
			App.views.splash(
				function () {
					// We perform operation
					// We load the template
					App.views.base(
						function () {
							$('#contains').load('app/templates/notifications.html');
							$('#header').load('app/templates/notifications_header.html');
						}
					);
				}
			);
		},
		login: function (username, password) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/login.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {username:username};
					// We send data
					if (username && password) {
						Addons.request('/api/auth/login',
							{username: username, password: password},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.index();
								};
							},false
						);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};
				}
			);
		},
		signin: function (username, email, password, password2) {
			App.views.splash(
				function () {
					// We perform operation
					App.vars.can_pass = 0;
					App.events[0] = setInterval(function () {
						// We verify if all the operations are finished
						if (App.vars.can_pass) {
							clearInterval(App.events[0]);
							$('#main').load('app/templates/signin.html');
						};
					}, 100);
					// We save the data form
			        App.vars.tmp.form = {username:username,email:email};
					if (password != password2) {
						App.vars.errors = ['The passwords not match'];
						App.vars.can_pass = 1;
					} else if (username && email && password && password2) {
						Addons.request('/api/auth/signin',
							{username: username, email: email, password: password, password2: password2},
							function (d) {
								if (d.code != 200) {
									App.vars.errors = [d.error];
									App.vars.can_pass = 1;
								} else {
									App.views.login();
								};
							},
							false
						);
					} else {
						// We load the template
						App.vars.can_pass = 1;
					};		
				}
			);
		},
		profil: function () {
			App.views.splash(
				function () {
					// We perform operation
					// We load the template
					App.views.base(
						function () {
							$('#contains').load('app/templates/profil.html');
							$('#header').load('app/templates/profil_header.html');
						}
					);
				}
			);
		},
		logout: function () {
			App.views.splash(
				function () {
					// We perform operation
					Addons.request('/api/auth/logout',null,
						function (d) {
							App.views.index();
						},false
					);
				}
			);
		},
		admin: function () {
			App.views.splash(
				function () {
					// We perform operation
					// We load the template
					App.views.base(
						function () {
							$('#contains').load('app/templates/admin.html');
							$('#header').load('app/templates/admin_header.html');
						}
					);
				}
			);
		},
		calendar: function () {
			App.views.splash(function () {
				// We load datas
				App.vars.get_lessons();
				App.vars.get_events();
				// We config the calendar
				moment.locale('en');
				var datas = App.models.classes;
                for (var i = 0; i < App.models.events.length; i++) {
                    datas.push(App.models.events[i]);
                };
                // We config the calendar
                moment.locale('en');
                /**
                    * Many events
                */
                var events = [
                    /*{
                        start: now.startOf('week').add(9, 'h').format('X'),
                        end: now.startOf('week').add(10, 'h').format('X'),
                        title: '1',
                        content: 'Hello World! <br> <p>Foo Bar</p>',
                        category:'Professionnal'
                    },*/
                ];
                for (var i=0; i < datas.length; i++) {
                    var now = moment(datas[i].date);
                    var begin = datas[i].begin.split(':');
                    var end = datas[i].end.split(':');
                    events.push({
                        start: now.startOf('day').add(begin[0], 'h').add(begin[1], 'm').format('X'),
                        end: now.startOf('day').add(end[0], 'h').add(end[1], 'm').format('X'),
                        title: datas[i].course ? datas[i].course.name : datas[i].name,
                        content: "<b>Status:</b> "+App.vars.STATUS_CHOICES_DICT[datas[i].status]+"<br>\
                        "+(datas[i].attendance_done ? ("<b>Attendance Done:</b> "+datas[i].attendance_done+"<br>") : "")+"\
                        <b>Venue:</b> "+datas[i].location.name+"<br>\
                        <b>Last update:</b> "+datas[i].updated+"<br>\
                        <b>Description:</b> "+datas[i].description+"<br>",
                        category: datas[i].course ? datas[i].course.code : "Event"
                    });
                };
			    /**
		      		* A daynote
		       	*/
		      	var daynotes = [
			        /*{
			        	time: now.startOf('week').add(15, 'h').add(30, 'm').format('X'),
			          	title: 'Leo\'s holiday',
			          	content: 'yo',
			          	category: 'holiday'
			        },*/
		      	];
			    /**
			    * Init the calendar
			    */
		      	var calendar = $('#main').Calendar({
		        	locale: 'en',
		        	weekday: {
		        		timeline: {
		            		intervalMinutes: 30,
		            		fromHour: 7
		        		},
		        	},
		        	events: events,
		        	daynotes: daynotes
		      	}).init();
			});
		},
	},
	models: {},
	events: {},
	vars: {
		errors: [],
		tmp: {},
		is_login: 0,
		get_lessons: function (next_day) {
			// We get datas
			App.models.classes = [];
			for (var i = 0; i < App.models.timetables.length; i++) {
				Addons.request('/api/user/timetable/'+App.models.timetables[i].pk+'/classe'+((next_day != null)?'/'+next_day:''), null, function (d) {
					if (d.code == 200) {
						for (var ii = 0; ii < d.result.length; ii++) {
							App.models.classes.push(d.result[ii]);
						};
					};
					if (i+1 == App.models.timetables.length) {
						App.vars.can_pass = 1;
					};
				}, false);
			};
		},
		get_events: function (next_day) {
			// We get datas
			App.models.events = [];
			for (var i = 0; i < App.models.timetables.length; i++) {
				Addons.request('/api/user/timetable/'+App.models.timetables[i].pk+'/event'+((next_day != null)?'/'+next_day:''), null, function (d) {
					if (d.code == 200) {
						for (var ii = 0; ii < d.result.length; ii++) {
							App.models.events.push(d.result[ii]);
						};
					};
					if (i+1 == App.models.timetables.length) {
						App.vars.can_pass = 1;
					};
				}, false);
			};
		},
	},
};

// We config global ajax configuration to manage error
$(document).ajaxError(function () {
	App.views.error();
})

// We launch the default page
App.views.index();