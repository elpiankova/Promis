'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('behavior/appliance.json').success(function(data, status, headers, config) {
        $scope.appliance = data;
    });

    $http.get('behavior/behavior.json').success(function(data, status, headers, config) {
        $scope.behavior = data;
    });

    $http.get('behavior/branches.json').success(function(data, status, headers, config) {
        $scope.branches = data;
        console.log(data);
    });

    $scope.numberval = '1';
    $scope.startPointval = '1';

    $scope.borderLeftval = '1';
    $scope.borderRightval = '1';
}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({ todoList });
    };
});

