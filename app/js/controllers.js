'use strict';

/* Controllers */
var requestKNA = angular.module('requestKNA', []);

requestKNA.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});



requestKNA.controller('claimInfoCtrl',['$scope','$http', function($scope, $http) {
    $http.get('behavior/appliance.json').success(function(data, status, headers, config) {
        console.log('This is Data:',data,'\n\nThis is Status:',status,'\n\nThis is Headers:',headers,'\n\nThis is config:',config);
        $scope.appliance = data;
    });

    $http.get('behavior/behavior.json').success(function(data, status, headers, config) {
        console.log('This is Data:',data,'\n\nThis is Status:',status,'\n\nThis is Headers:',headers,'\n\nThis is config:',config);
        $scope.behavior = data;
    });

    $http.get('behavior/branches.json').success(function(data, status, headers, config) {
        console.log('This is Data:',data,'\n\nThis is Status:',status,'\n\nThis is Headers:',headers,'\n\nThis is config:',config);
        $scope.branches = data;
    });

}]);
