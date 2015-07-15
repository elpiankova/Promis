'use strict';

/* Controllers */
var requestKNA = angular.module('requestKNA', []);

requestKNA.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});



requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('behavior/appliance.json').success(function(data, status, headers, config) {
        $scope.appliance = data;
    });

    $http.get('behavior/behavior.json').success(function(data, status, headers, config) {
        $scope.behavior = data;
    });

    $http.get('behavior/branches.json').success(function(data, status, headers, config) {
        $scope.branches = data;
    });



}]);

requestKNA.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [];

    todoList.addTodo = function() {
        todoList.todos.push({todoList});
    };

});