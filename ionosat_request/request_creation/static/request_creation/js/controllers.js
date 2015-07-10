'use strict';

/* Controllers */
var phonecatApp = angular.module('phonecatApp', []);

phonecatApp.controller('PhoneListCtrl', function($scope, $http){

    //Масив даних
    $scope.title = "Телефони";
    $http.get('phones/phones.json').succsess(function() {

    }).error()

    //Дата
    var date = new Date();
    $scope.today = date;

    //Фільтр
    $scope.doneAddFilter = function(phoneItem) {
        return phoneItem.name && phoneItem.priority > 1 && phoneItem.status === true;
    }

    //Сортування
    $scope.sortFiled = undefined;
    $scope.reverse = false;

    $scope.sort = function(filedName){
        if ($scope.sortFiled === filedName) {
            $scope.sortFiled = !$scope.reverse;
        }
        else{
            $scope.sortFiled = filedName;
            $scope.reverse = false;
        }
    };

    //Іконка сортування яка показує напрямок сортування файлів

    $scope.isSortDown = function(filedName){
        return $scope.sortFiled === filedName && $scope.reverse;
    };
    $scope.isSortUp = function(filedName){
        return $scope.sortFiled === filedName && !$scope.reverse;
    };
});