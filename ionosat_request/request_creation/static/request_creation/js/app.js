//Created by mammut
'use strict';

/* App Module */
var requestKNA = angular.module('requestKNA', []);

requestKNA.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});