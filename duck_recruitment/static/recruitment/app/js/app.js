var myApp = angular.module('myApp', [
    'ngRoute',
    'servicesRecrutement',
    'ui.bootstrap'
]);

myApp.config(['$routeProvider', '$httpProvider',
    function ($routeProvider, $httpProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/recruitment/app/partials/home.html',
                controller: 'RecruitmentCtrl'
            }).
            when('/etapes/', {
                templateUrl: '/static/recruitment/app/partials/edit_etape.html',
                controller: 'EtapesCtrl'
            }).
            when('/etat_heure/', {
                templateUrl: '/static/recruitment/app/partials/etat_heure/list_etat_heure.html',
                controller: 'ListEtatHeureCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);
myApp.run(['$rootScope', '$http', function($rootScope, $http){
    $http.get('/recruitment/v1/users').success(function(data){
       if(data.length == 1){
           $rootScope.user = data[0];
       }
    });
}]);
