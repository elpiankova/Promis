'use strict';

/* Controllers */
requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('behavior/appliance.json').success(function(data, status, headers, config) {
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

requestKNA.controller('FormController', function($scope) {
    $scope.schema = {
        type: "object",
        properties: {
            name: { type: "string", minLength: 2, title: "Name", description: "Name or alias" },
            title: {
                type: "string",
                enum: ['dr','jr','sir','mrs','mr','NaN','dj']
            }
        }
    };

    $scope.form = [
        "*",
        {
            type: "submit",
            title: "Save"
        }
    ];

    $scope.model = {};
});