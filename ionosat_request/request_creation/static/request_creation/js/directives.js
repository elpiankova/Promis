//Created by mammut
requestKNA.directive(
	'datepicker', function () {
		return {
			require: 'ngModel',
			link: function (scope, element, attrs, ngModelCtrl) {
				$(
					function () {
						$("#from").datepicker(
							{ dateFormat: 'yy-mm-dd',
								defaultDate: "+1w",
								changeMonth: true,
								numberOfMonths: 1,
								onClose: function (selectedDate) {
									$("#to").datepicker("option", "minDate", selectedDate);
								}
							}
						);
						$("#to").datepicker(
							{
								dateFormat: 'yy-mm-dd',
								defaultDate: "+1w",
								changeMonth: true,
								numberOfMonths: 1,
								onClose: function (selectedDate) {
									$("#from").datepicker("option", "maxDate", selectedDate);
								}
							}
						);
					}
				);
			}
		}
	}
);
