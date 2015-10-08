
myApp.controller('RecruitmentCtrl',
    ['$scope', '$modal', '$http', '$log', 'Etape', 'Ec', 'PersonneDsi', 'EtatHeure',
    function ($scope, $modal, $http, $log, Etape, Ec, PersonneDsi, EtatHeure) {
    $scope.agents = [];

    $scope.etapes = Etape.query();
    var getAgent = function(ec){
        EtatHeure.search(ec.code_ec).success(function(data){
            ec.agents = data;
        });
    };
    $scope.listEc = function(etape){
        Ec.ec_by_etape(etape).success(function(data){
            $scope.ecs = data.results;
            ecs = $scope.ecs;
            console.log('ici');
            for (var i = 0, length=ecs.length; i<length; i++){
               getAgent(ecs[i]);
            }
        }).error(function(data, status, headers, config) {
            $scope.ecs = 'Erreur de chargement, serveur indisponible';
        });
    };
    $scope.listEc({id: '10' });
    $scope.$on('addPersonneDone', function(event, ec){
        getAgent(ec);
    });

    $scope.searchPersonne = function(ec){
        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/addPersonne.html',
            controller: 'SearchCtrl',
            resolve: {
                ec: function(){return ec}
            }
        });
    };

}]);


myApp.controller('SearchCtrl',
    ['$rootScope', '$scope', '$modalInstance', 'ec',  '$http', '$log', 'PersonneDsi', 'Agent', 'EtatHeure',
    function ($rootScope, $scope, $modalInstance, ec, $http, $log, PersonneDsi, Agent, EtatHeure) {

        $scope.ec = ec;
        $scope.getPersonne =  function(value){
            return PersonneDsi.search(value).then(function(response){return response.data.results});
        };
        $scope.addPersonne = function(personne, ec){
            Agent.resource().save({individu_id:personne.numero, type: personne.type, annee:'2015', code_ec:ec.code_ec}).$promise.then(function(){
                $scope.message = 'Opération réussi';
            }, function(){
               $scope.message = 'Echec';
            }).then(function(){
                $rootScope.$broadcast('addPersonneDone', ec);

            });
        }

}]);
