//Created by mammut
'use strict';

/* Controllers */
requestKNA.controller(
	'claimInfoCtrl', function ($http) {
		var claim = this;
		$http.get('/devices').success(
			function (data) {
				claim.appliance = data;
				console.log(data)
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
				console.log(claim.user.number);
			}
		);

		claim.dataReqest = function () {
			var request = {
				"number": claim.number,

				"date_start": "2015-07-15",

				"date_end": "2015-07-16",

				"orbit_flag": "y",

				"latitude_start": "30.0",

				"longitude_left": "0.0",

				"longitude_right": "359.0"
			};
			var devswitch = {
				"request_number": claim.number,

				"time_delay": "00:00:01",

				"time_duration": "00:00:30",

				"argument_part": "qwe",

				"device": "Wave probe WP(count3)",

				"mode": "5KHz Frequency",

				"power_amount": 0,

				"data_amount": 0
			};
			console.log
			$http.post('/request/', request).
				success(
				function (data) {
					$http.post('/devswitch/', devswitch).
						success(
						function (data) {

							console.log(data);
						}
					).
						error(
						function (status) {
							console.log('geg');
						}
					);
					console.log(data);
				}
			).
				error(
				function (status) {
					console.log(status);
				}
			);


		}

	}
);

requestKNA.controller(
	'TodoListController', function () {
		var todoList = this;
		todoList.todos = [];
		todoList.addTodo = function () {
			todoList.todos.push({});
		};

		todoList.Save = function () {
			var save = this.switches;
			console.log(save);
		};
	}
);