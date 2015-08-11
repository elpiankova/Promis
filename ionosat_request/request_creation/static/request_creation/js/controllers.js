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

		claim.dataReqest = function () {
			var request = claim.user;
			console.log(request);
			var devswitch = [
				{
					"request_number": claim.number,

					"time_delay": "00:00:01",

					"time_duration": "00:00:30",

					"argument_part": "qwe",

					"device": "Wave probe WP(count3)",

					"mode": "400 Hz mode",

					"power_amount": 0,

					"data_amount": 0
				},
				{
					"request_number": claim.number,

					"time_delay": "00:00:01",

					"time_duration": "00:00:30",

					"argument_part": "qwe",

					"device": "Electric  probe",

					"mode": "700 Hz Frequency",

					"power_amount": 0,

					"data_amount": 0
				}, {
					"request_number": claim.number,

					"time_delay": "00:00:01",

					"time_duration": "00:00:30",

					"argument_part": "qwe",

					"device": "Radio frequency analyser",

					"mode": "5KHz Frequency",

					"power_amount": 0,

					"data_amount": 0
				}
			];
			var index;
			for (index = 0; index < devswitch.length; ++index) {
			}
			$http.post('/request/', request).
				success(
				function () {
					var index;
					for (index = 0; index < devswitch.length; ++index) {
						$http.post('/devswitch/', devswitch[index]);
					}
				}
			).
				error(
				function (status) {
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
	}
);