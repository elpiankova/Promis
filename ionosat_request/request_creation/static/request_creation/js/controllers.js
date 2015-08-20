//Created by mammut
'use strict';

/* Controllers */
requestKNA.controller (
	'claimInfoCtrl', function ( $http ) {
		var claim = this;
		$http.get ( '/devices' ).success (
			function ( data ) {
				claim.appliance = data;
			}
		);
		$http.get ( '/orbit_flag' ).success (
			function ( data ) {
				claim.branches = data;
			}
		);

		$http.get ( '/number' ).success (
			function ( data ) {
				claim.number = parseInt ( data );
				claim.user =
				{
					"number": claim.number
				};
			}
		);

		var timeModes = function () {
			var index;
			for ( index = 0; index < claim.todos.length; ++index ) {

				//Count time in seconds
				var time_modes = claim.todos[ index ].time_duration.split ( ':' );
				var hhh = Number ( time_modes[ 0 ] );
				var mm = Number ( time_modes[ 1 ] );
				var ss = Number ( time_modes[ 2 ] );
				var time = hhh * 3600 + mm * 60 + ss;
				if ( time > 999999 ) {
					claim.todos[ index ].time_duration = 'Неверная длительность';
					return;

				}

				var index_device;
				for (
					index_device = 0; index_device < claim.appliance.length; ++index_device
				) {
					if ( claim.todos[ index ].device
					     == claim.appliance[ index_device ].name ) {
						var modes = claim.appliance[ index_device ].modes;
						var index_modes;
						for (
							index_modes = 0;
							index_modes < modes.length;
							++index_modes
						) {
							if ( claim.todos[ index ].mode == modes[ index_modes ].name ) {

								var data_amount = modes[ index_modes ].data_speed * time / 8;
								console.log ( claim.todos[ index ][ "data_amount" ] );

								claim.todos[ index ][ "data_amount" ] = data_amount;
								claim.todos[ index ].data_amount = data_amount;

								if ( data_amount == 0 ) {
									claim.todos[ index ].data_amount = "0 Байт";
								}

								claim.todos[ index ][ "data_amount" ] = data_amount;
								var alldatamount;
								if ( isNaN ( alldatamount ) ) {
									alldatamount = 0;
								}
								alldatamount = alldatamount + data_amount;

								claim.data_amount = alldatamount;
								var power_amount = modes[ index_modes ].power * time / 3600;
								claim.todos[ index ][ "power_amount" ] = power_amount;
								claim.todos[ index ].power_amount = power_amount;
								if ( power_amount == 0 ) {
									claim.todos[ index ].power_amount = "0";
								}
								var allpoweramount;
								if ( isNaN ( allpoweramount ) ) {
									allpoweramount = 0;
								}
								allpoweramount = allpoweramount + power_amount;
								claim.power_amount = allpoweramount;

								claim.Reqest = true;
							}
						}
					}
				}
			}
		};
		claim.todos = [];
		claim.addTodo = function () {
			claim.todos.push ( {} );
			claim.Reqest = false;
		};

		claim.dataReqest = function () {
			var request = claim.user;
			var index;
			for ( index = 0; index < claim.todos.length; ++index ) {
				claim.todos[ index ][ "request_number" ] = claim.user.number;
			}

			var devswitch = claim.todos;

			$http.post ( '/request/', request ).
				success (
				function ( data ) {
					var index;
					for ( index = 0; index < devswitch.length; ++index ) {
						$http.post ( '/devswitch/', devswitch[ index ] ).success (
							claim.hash = 'get_file/' + data.request_file
						).error (
							function () {

								console.log ( devswitch[ index ] );
							}
						);
					}

				}
			).
				error (
				function ( status ) {
					console.log ( status.number );
				}
			);
		};
		claim.timeModes = timeModes;
	}
);



