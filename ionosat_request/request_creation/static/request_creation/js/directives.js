//Created by mammut
requestKNA.directive (
	'datepicker', function () {
		return {
			require: 'ngModel',
			link: function ( scope, element, attrs, ngModelCtrl ) {
				$ (
					function () {
						$ ( "#from" ).datepicker (
							{
								dateFormat: 'yy-mm-dd',
								defaultDate: "+1w",
								changeMonth: true,
								numberOfMonths: 1,
								onClose: function ( selectedDate ) {
									$ ( "#to" ).datepicker (
										"option", "minDate", selectedDate
									);
								}
							}
						);
						$ ( "#to" ).datepicker (
							{
								dateFormat: 'yy-mm-dd',
								defaultDate: "+1w",
								changeMonth: true,
								numberOfMonths: 1,
								onClose: function ( selectedDate ) {
									$ ( "#from" ).datepicker (
										"option", "maxDate", selectedDate
									);
								}
							}
						);
					}
				);
			}
		}
	}
);

requestKNA.directive (
	'timespinner', function () {
		return {
			require: 'ngModel',
			link: function ( scope, element, attrs, ngModelCtrl ) {
				jQuery (
					function ( $ ) {
						$ ( ".fromtime" ).mask ( "99:99:99:99" );
					}
				);
			}
		}
	}
);

requestKNA.directive (
	'modeTime', function () {
		return {
			require: 'ngModel',
			link: function ( scope, element, attrs, ngModelCtrl ) {

			}
		}
	}
);