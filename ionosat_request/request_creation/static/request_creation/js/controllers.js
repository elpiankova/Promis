'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('/devices').success(function(data, status, headers, config) {
        $scope.appliance = data;
    });
    $http.get('/orbit_flag').success(function(data, status, headers, config) {
        $scope.branches = data;
    });

    $http.get('/number').success(function(data, status, headers, config) {
        $scope.number = data;
  });
    $scope.name = {};
    var datareqest = {
     "number": "12",
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
    var req = {
 method: 'POST',
 url: '/request/',
 headers: {
   'Content-Type' : 'application/json'
 },
 data: datareqest
}
    $http(req).
  success(function(data, status, headers, config) {
          console.log(status);
           console.log(headers);
  }).
  error(function(data, status, headers, config) {
           console.warn(status);
            console.warn(headers);
  });

}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});