/**
 * Created by paulguichon on 11/02/2016.
 */
myApp.controller('ListEtatHeureCtrl', ['$scope', 'Etape', '$filter','Ec','$modal', 'RecrutementService',
    function($scope, Etape, $filter, Ec, $modal, RecrutementService){
         RecrutementService.all_ec_annuel.query(function(data){
            $scope.all_etats_heures = data;
         });

    $scope.info_agent = function(all_ec_annuel){
        var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/etat_heure/agent.html',
            controller: 'AgentCtrl',
            resolve: {
                all_ec_annuel: function() { return all_ec_annuel }
            },
            size: "lg",
            windowClass: 'my-modal-popup'
        });
    };

}]);
myApp.controller('AgentCtrl', ['$rootScope', '$scope','all_ec_annuel', 'Etape', '$filter','Ec','$modal', 'RecrutementService',
    function($rootScope, $scope, all_ec_annuel, Etape, $filter, Ec, $modal, RecrutementService){
        RecrutementService.agent.get({id:all_ec_annuel.agent}, function(data){
            $scope.agent = data;

        });
        $scope.all_ec_annuel = all_ec_annuel;
        angular.forEach(all_ec_annuel.ec, function(element){
           angular.forEach(element, function(element) {
               RecrutementService.etat_heure.get({id: element.id}, function(data){
                  element.id = data;
               });
           });
        });

        $scope.reset = function(id){
            id.date_validation_rattrapage=null;
            id.$update();
        };
        $scope.all_ec_annuel_udpdate = function(all_ec_annuel){
            var list_ec = all_ec_annuel.list_ec;
            all_ec_annuel.$update(function(data){
                data.list_ec = list_ec;
                all_ec_annuel = data;
            })
        };

}]);