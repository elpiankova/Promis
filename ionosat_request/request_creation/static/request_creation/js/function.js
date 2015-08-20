/**
 * Created by mammut on 8/19/15.
 */

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

						claim.todos[ index ][ "data_amount" ] = data_amount;
						var text_data_amount;
						var Ki = 1024;
						var Mi = Ki * 1024;
						var Gi = Mi * 1024;
						if ( data_amount <= Ki ) {
							text_data_amount = data_amount + " Байт";
						}
						else if ( data_amount > Ki ) {
							text_data_amount = data_amount / Mi;
							text_data_amount = text_data_amount.toFixed ( 1 );
							console.log ( text_data_amount );
							text_data_amount = text_data_amount + " Килобайт";
						}
						else if ( data_amount > Mi ) {
							text_data_amount = data_amount / Mi;
							text_data_amount = text_data_amount.toFixed ( 1 );
							console.log ( text_data_amount );
							text_data_amount = text_data_amount + " Мегабайт";

						}
						else if ( data_amount > Gi ) {
							text_data_amount = data_amount / Gi;
							text_data_amount = text_data_amount.toFixed ( 1 );
							console.log ( text_data_amount );
							text_data_amount = text_data_amount + " Гигиабайт";

						}
						claim.todos[ index ].data_amount = text_data_amount;

						if ( data_amount == 0 ) {
							claim.todos[ index ].data_amount = "0";
						}

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