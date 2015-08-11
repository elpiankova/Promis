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

