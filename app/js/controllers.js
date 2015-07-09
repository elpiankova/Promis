'use strict';

/* Controllers */
var requestKNA = angular.module('requestKNA', []);

requestKNA.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});



requestKNA.controller('claimInfoCtrl', function($scope, $http){

    $http.get('behavior/appliance.json').success(function(data, status, headers, config){
        console.log('Data:',data,'\n\n Status:',status,'\n\n Headers:', headers,'\n\nConfig:',config);
        $scope.appliance = data;
    }).error(function(){
        console.log('Error');
    });
    /*$scope.maindata =
        {   'kna' : 'KNA',
            'appnumber' : '0003'
        }
    $scope.branches = [
        {   'name' : 'Восходящая',
            'atr' : 'v'},
        {   'name' : 'Нисходящая',
            'atr' : 'n'},
        {   'name' : 'Не имеет значения',
            'atr' : 'p'}
    ];
    $scope.appliance = [
        {   'name' : 'Волновые зонды WP',
            'atr' : 'WP0000'},
        {   'name' : 'Электрический зонд',
            'atr' : 'EP0000'},
        {   'name' : 'Радиочастотный анализатор',
            'atr' : 'RFA000'},
        {   'name' : 'Датчик нейтрального компонента плазмы',
            'atr' : 'DN0000'},
        {   'name' : 'Блок датчиков электронного компонента плазмы',
            'atr' : 'DE0000'},
        {   'name' : 'Феррозондовый магнитометр постоянного поля',
            'atr' : 'FGM000'},
        {   'name' : 'Измеритель полного электронного содержания',
            'atr' : 'PES000'},
        {   'name' : 'Система сбора научной информации',
            'atr' : 'SSNI00'},
    ];
    $scope.behavior = [
        {   'name' : 'Моніторинг',
            'atr' : 'M'},
        {   'name' : 'MONITOR1',
            'atr' : 'MONITOR1'},
        {   'name' : 'M10',
            'atr' : 'M10'},
        {   'name' : 'M10',
            'atr' : 'M10'},
        {   'name' : 'SPECTRUM',
            'atr' : 'SPECTRUM'},
    ];*/
});