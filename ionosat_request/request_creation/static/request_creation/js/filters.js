'use strict';

/* Filters */
requestKNA.filter (
	'formatText', function () {
		return function ( name ) {
			var text_data_amount;
			var Ki = 1024;
			var Mi = Ki * 1024;
			var Gi = Mi * 1024;
			if ( name <= Ki ) {
				text_data_amount = name + " Байт";
			}
			else if ( name > Ki ) {
				text_data_amount = name / Mi;
				text_data_amount = text_data_amount.toFixed ( 1 );
				text_data_amount = text_data_amount + " Килобайт";
			}
			else if ( name > Mi ) {
				text_data_amount = name / Mi;
				text_data_amount = text_data_amount.toFixed ( 1 );
				text_data_amount = text_data_amount + " Мегабайт";

			}
			else if ( name > Gi ) {
				text_data_amount = name / Gi;
				text_data_amount = text_data_amount.toFixed ( 1 );
				text_data_amount = text_data_amount + " Гигиабайт";

			}
			return text_data_amount;
		}
	}
);