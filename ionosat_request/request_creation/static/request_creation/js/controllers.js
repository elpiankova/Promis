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
        $scope.branches = data;
        console.log(data);
        console.log(status);
        console.log(headers);
        console.log(config);
    }).
  error(function(data, status, headers, config) {
        console.log(status);
        console.log(headers);
        console.log(config);
  });

}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});