//Created by mammut
'use strict';

/* Controllers */
requestKNA.controller (
	'claimInfoCtrl', function ( $http ) {
		//Обявлення області видимості
		var claim = this;

		//Получення усіх даних методом get
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

		// Функція для підрахування кількості байт та ват, це все зберігається в json та
		// підраховується загальна інформація для всіх параметрів
		var timeModes = function () {
			var index;
			// Перебирається масив з пристроями та підраховується
			// для кожного пристрою окремо і загально
			for ( index = 0; index < claim.todos.length; ++index ) {

				// Розбивається масив з часом роботи та переводиться у секунди
				var time_modes = claim.todos[ index ].time_duration.split ( ':' );
				var hhh = Number ( time_modes[ 0 ] );
				var mm = Number ( time_modes[ 1 ] );
				var ss = Number ( time_modes[ 2 ] );
				var time = hhh * 3600 + mm * 60 + ss;
				// Якщо більше максимума не пропускає далі
				if ( time > 999999 ) {
					claim.todos[ index ].time_duration = 'Неверная длительность';
					return;
				}
				// Перебирається json та вибирається дані які ввів користувач
				var index_device;
				for ( index_device = 0; index_device < claim.appliance.length; ++index_device ) {

					// Якщо вибрано саме цей пристрій ми дивимось який режим вибрано
					if ( claim.todos[ index ].device == claim.appliance[ index_device ].name ) {

						// Дивимось який режим вибрано і надалі працюємо із ним
						var modes = claim.appliance[ index_device ].modes;
						var index_modes;
						for ( index_modes = 0; index_modes < modes.length; ++index_modes ) {
							if ( claim.todos[ index ].mode == modes[ index_modes ].name ) {

								// Переводимо дані у потрібний вигляд
								var data_amount = modes[ index_modes ].data_speed * time / 8;

								// Показуємо що у нас є на кожен пристрій
								claim.todos[ index ][ "data_amount" ] = data_amount;
								claim.todos[ index ].data_amount = data_amount;

								// Потрібно виводити якщо значення є нуль
								if ( data_amount == 0 ) {
									claim.todos[ index ].data_amount = "0 Байт";
								}
								// Загальна кількість даних
								var alldatamount;
								if ( isNaN ( alldatamount ) ) {
									alldatamount = 0;
								}
								alldatamount = alldatamount + data_amount;
								claim.data_amount = alldatamount;

								// Переводимо дані у потрібний вигляд
								var power_amount = modes[ index_modes ].power * time / 3600;
								claim.todos[ index ][ "power_amount" ] = power_amount;
								claim.todos[ index ].power_amount = power_amount;

								// Потрібно виводити якщо значення є нуль
								if ( power_amount == 0 ) {
									claim.todos[ index ].power_amount = "0";
								}
								// Загальна кількість даних
								var allpoweramount;
								if ( isNaN ( allpoweramount ) ) {
									allpoweramount = 0;
								}
								allpoweramount = allpoweramount + power_amount;
								claim.power_amount = allpoweramount;

								// Показуємо кнопку згенерувати заявку та добавити пристрій
								claim.Reqest = true;
							}
						}
					}
				}
			}
		};

		// Показуємо кнопку згенерувати заявку та добавити пристрій
		claim.Reqest = true;

		// Створюєтрься масив для майбутніх форм
		claim.todos = [];

		// При нажатті на кнопку створюється нова форма
		claim.addTodo = function () {
			claim.todos.push ( {} );
			claim.Reqest = false;
		};

		// Надсилання даних на сервер
		claim.dataReqest = function () {
			// json який надсилає
			var request = claim.user;
			var index;
			// Добавлення номеру заяви у devswitch
			for ( index = 0; index < claim.todos.length; ++index ) {
				claim.todos[ index ][ "request_number" ] = claim.user.number;
			}

			// Сам масив
			var devswitch = claim.todos;
			$http.post ( '/request/', request ).
				success (
				function ( data ) {
					var index;
					for ( index = 0; index < devswitch.length; ++index ) {
						$http.post ( '/devswitch/', devswitch[ index ] );
					}
					claim.hash = 'get_file/' + data.request_file;
				}
			).
				error (
				function ( status ) {
					console.log ( status.number );
				}
			);
		};
		// Виклик при нажатті на кнопку обрахувати
		claim.timeModes = timeModes;
	}
);



