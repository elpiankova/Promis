/**
 * Created by mammut on 8/13/15.
 */
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