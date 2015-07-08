'use strict';

/* Controllers */
var requestKNA = angular.module('requestKNA', []);

requestKNA.controller('claimInfoCtrl', function($scope){
    $scope.maindata =
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
    $scope.branches = [
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
    ];
});