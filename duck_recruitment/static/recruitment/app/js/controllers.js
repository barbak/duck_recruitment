
myApp.controller('RecruitmentCtrl',
    ['$scope', '$modal', '$http', '$log', 'Etape', 'Ec', 'PersonneDsi',
    function ($scope, $modal, $http, $log, Etape, Ec, PersonneDsi) {
    $scope.agents = [];
    $scope.ecs = Ec.ec_by_etape({id: '10' }).success(function(data){
            $scope.ecs = data.results
        });
    $scope.etapes = Etape.query();

    $scope.listEc = function(etape){
        Ec.ec_by_etape(etape).success(function(data){
            $scope.ecs = data.results
        }).error(function(data, status, headers, config) {
            $scope.ecs = 'Erreur de chargement, serveur indisponible';
        });
    };

    $scope.searchPersonne = function(code_ec){
        console.log(code_ec);
        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/addPersonne.html',
            controller: 'SearchCtrl',
            resolve: {
                code_ec: function(){return code_ec}
            }
        });
    };

}]);


myApp.controller('SearchCtrl',
    ['$scope', '$modalInstance', 'code_ec',  '$http', '$log', 'PersonneDsi', 'Agent',
    function ($scope, $modalInstance, code_ec, $http, $log, PersonneDsi, Agent) {
        $scope.code_ec = code_ec;
        $scope.getPersonne =  function(value){
            return PersonneDsi.search(value).then(function(response){return response.data.results});
        };
        $scope.addPersonne = function(personne, code_ec){
            Agent.resource().save({individu_id:personne.numero,type:'charge', annee:'2015' }).$promise.then(function(){
                console.log('reussi');
                $scope.message = 'Opération réussi';
            }, function(){
                console.log('merde');
               $scope.message = 'Echec';
            });
        }

}]);
