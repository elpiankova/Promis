//Created by mammut
'use strict';

/* Controllers */
requestKNA.controller(
	'claimInfoCtrl', function ($http) {
		var claim = this;
		$http.get('/devices').success(
			function (data) {
				claim.appliance = data;
			}
		);
		$http.get('/orbit_flag').success(
			function (data) {
				claim.branches = data;
			}
		);

		$http.get('/number').success(
			function (data) {
				claim.number = parseInt(data);
				claim.user =
				{
					"number": claim.number
				};
			}
		);

		claim.todos = [];
		claim.addTodo = function () {
			claim.todos.push({});
		};

		claim.dataReqest = function () {

			var request = claim.user;
			console.log(request);
			var index;
			for (index = 0; index < claim.todos.length; ++index) {
				claim.todos[index]["request_number"] = claim.user.number;
			}

			var devswitch = claim.todos;
			console.log(devswitch);

			$http.post('/request/', request).
				success(
				function (data) {
					var index;
					for (index = 0; index < devswitch.length; ++index) {
						$http.post('/devswitch/', devswitch[index])
					}
					var get_file = 'get_file/' + data.request_file;
					$http.get(get_file);
					$http.get(get_file).success(
						function (data) {
							console.log(data);
						}
					);
					console.log(get_file)
				}
			).
				error(
				function (status) {
				}
			);
		};
		claim.timeModes = function () {

			var index;
			for (index = 0; index < claim.todos.length; ++index) {
				var time_modes = claim.todos[index].time_duration.split(':');
				var hh = Number(time_modes[0]);
				var mm = Number(time_modes[1]);
				var ss = Number(time_modes[2]);
				var time = hh * 3600 + mm * 60 + ss;
				var index_device;
				for (index_device = 0; index_device < claim.appliance.length; ++index_device) {
					if (claim.todos[index].device == claim.appliance[index_device].name) {
						var modes = claim.appliance[index_device].modes;
						var index_modes;
						for (
							index_modes = 0; index_modes < modes.length;
							++index_modes
						) {
							if (claim.todos[index].mode == modes[index_modes].name) {

								var data_amount = modes[index_modes].data_speed * time / 8;
								claim.todos[index]["data_amount"] = data_amount;
								claim.todos[index].data_amount = data_amount;

								var power_amount = modes[index_modes].power * time / 3600;
								claim.todos[index]["power_amount"] = power_amount;
								claim.todos[index].power_amount = power_amount;

							}
						}
					}
				}
			}
		};
	}
);

