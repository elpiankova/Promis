//Created by mammut
requestKNA.directive(
	'datepicker', function () {
		return {
			require: 'ngModel',
			link: function (scope, element, attrs, ngModelCtrl) {
				$(
					function () {
						$("#from").datepicker(
							{
								dateFormat: 'yy-mm-dd',
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

requestKNA.directive(
	'timespinner', function () {
		return {
			require: 'ngModel',
			link: function (scope, element, attrs, ngModelCtrl) {
				$.widget(
					"ui.timespinner", $.ui.spinner, {
						options: {
							// seconds
							step: 60 * 1000,
							// hours
							page: 60
						},

						_parse: function (value) {
							if (typeof value === "string") {
								// already a timestamp
								if (Number(value) == value) {
									return Number(value);
								}
								return +Globalize.parseDate(value);
							}
							return value;
						},

						_format: function (value) {
							return Globalize.format(new Date(value), "t", "de-DE");
						}
					}
				);

				$(
					function () {
						$("#spinner").timespinner();
						Globalize.culture("de-DE");

					}
				);
			}
		}
	}
);
