//Created by mammut
'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl', function ($http) {
    var claim = this;
    $http.get('/devices').success(function (data, status, headers, config) {
        claim.appliance = data;
    });
    $http.get('/orbit_flag').success(function (data, status, headers, config) {
        claim.branches = data;
    });

    $http.get('/number').success(function (data, status, headers, config) {
        claim.number = data;
    });

    claim.dataReqest = function () {
        var datareqest = {
            "number": $scope.number,
            "date_start": "2015-07-15",
            "date_end": "2015-07-16",
            "orbit_flag": "y",
            "latitude_start": "30.0",
            "longitude_left": "0.0",
            "longitude_right": "359.0",
            "switches": [
                {
                    "time_delay": "00:00:01",
                    "time_duration": "00:00:30",
                    "argument_part": "qwe",
                    "device": "Wave probe WP(count3)",
                    "mode": "ojjkm"
                }
            ]
        };
        $http.post('/request/', datareqest).
            success(function (data, status, headers, config) {
            }).
            error(function (data, status, headers, config) {

            });
        console.warn(claim.user);
    }

});

requestKNA.controller('TodoListController', function () {
    var todoList = this;
    todoList.todos = [];
    todoList.addTodo = function () {
        todoList.todos.push({});
    };

    todoList.Save = function () {
        var save = this.switches;
        console.log(save);


        console.log(claim.number);
    };
});