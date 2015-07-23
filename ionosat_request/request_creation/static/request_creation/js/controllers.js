'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('/devices').success(function(data, status, headers, config) {
        $scope.appliance = data;
    });
    $http.get('behavior/branches.json').success(function(data, status, headers, config) {
        $scope.branches = data;
    });
}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});