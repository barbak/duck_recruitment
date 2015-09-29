var myApp = angular.module('myApp', [
    'ui.bootstrap',
    'ngRoute'
]);

myApp.config(['$routeProvider', '$httpProvider',
    function ($routeProvider, $httpProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/recruitment/app/partials/home.html',
                controller: 'RecruitmentCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);
