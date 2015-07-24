'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('/devices').success(function(data, status, headers, config) {
        $scope.appliance = data;
    });
    $http.get('/orbit_flag').success(function(data, status, headers, config) {
        $scope.branches = data;

        console.log(data);
    });

    $http.get('/number').success(function(data, status, headers, config) {
        $scope.number = data;
  });

}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});