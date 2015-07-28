'use strict';

/* App Module */
var requestKNA = angular.module('requestKNA', ['schemaForm']);

requestKNA.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});