'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('behavior/appliance.json').success(function(data, status, headers, config) {
        $scope.appliance = data;
        console.log(data);
    });
    $http.get('behavior/branches.json').success(function(data, status, headers, config) {
        $scope.branches = data;
        console.log(data);
    });
}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});