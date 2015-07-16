'use strict';

/* Filters */
requestKNA.filter('numberFilter',function(){
    return function(date) {
        return ("0000" + date).slice(-4);
    };
});

