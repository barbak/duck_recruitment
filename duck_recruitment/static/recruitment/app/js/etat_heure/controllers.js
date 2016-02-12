/**
 * Created by paulguichon on 11/02/2016.
 */
myApp.controller('ListEtatHeureCtrl', ['$scope', 'Etape', '$filter','Ec','$modal', 'RecrutementService',
    function($scope, Etape, $filter, Ec, $modal, RecrutementService){
         RecrutementService.all_ec_annuel.query(function(data){
            $scope.all_etats_heures = data;
         });
    //$scope.monEtape = null;
    //$scope.choix_prop_ec = [
    //    {choix:'0', label: 'Annuel'},
    //    {choix: '1', label: 'Premier semestre'},
    //    {choix:'2', label: 'Seconde semestre'}
    //];
    //Etape.query(function(data) {
    //    $scope.etapes = $filter('filter')(data, {cod_vrs_vet:'5'}, false);
    //    if($scope.etapes.length >= 1) {
    //        $scope.monEtape = $scope.etapes[0];
    //
    //        $scope.listEc($scope.monEtape);
    //    }
    //});
    //$scope.listEc = function(etape){
    //    RecrutementService.type_ec.resource.query({etape:etape.id}, function(data){
    //       $scope.types_ec = data;
    //    });
    //    RecrutementService.ec.query_with_type_ec({etape:etape.id}, function(data){
    //        $scope.ecs = data;
    //    });
    //};
    //    $scope.update_ec= function(ec){
    //        var prop_ec = ec.prop_ec;
    //        ec.$update(function(){
    //           ec.prop_ec = prop_ec;
    //        });
    //    };
    //    $scope.$on('updateTypeEc', function(type_ec){
    //       RecrutementService.type_ec.resource.query({etape:$scope.monEtape.id}, function(data){
    //           $scope.types_ec = data;
    //        });
    //    });
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
myApp.controller('AgentCtrl', ['$scope','all_ec_annuel', 'Etape', '$filter','Ec','$modal', 'RecrutementService',
    function($scope, all_ec_annuel, Etape, $filter, Ec, $modal, RecrutementService){
        RecrutementService.agent.get({id:all_ec_annuel.agent}, function(data){
            $scope.agent = data;
        });


    //$scope.monEtape = null;
    //$scope.choix_prop_ec = [
    //    {choix:'0', label: 'Annuel'},
    //    {choix: '1', label: 'Premier semestre'},
    //    {choix:'2', label: 'Seconde semestre'}
    //];
    //Etape.query(function(data) {
    //    $scope.etapes = $filter('filter')(data, {cod_vrs_vet:'5'}, false);
    //    if($scope.etapes.length >= 1) {
    //        $scope.monEtape = $scope.etapes[0];
    //
    //        $scope.listEc($scope.monEtape);
    //    }
    //});
    //$scope.listEc = function(etape){
    //    RecrutementService.type_ec.resource.query({etape:etape.id}, function(data){
    //       $scope.types_ec = data;
    //    });
    //    RecrutementService.ec.query_with_type_ec({etape:etape.id}, function(data){
    //        $scope.ecs = data;
    //    });
    //};
    //    $scope.update_ec= function(ec){
    //        var prop_ec = ec.prop_ec;
    //        ec.$update(function(){
    //           ec.prop_ec = prop_ec;
    //        });
    //    };
    //    $scope.$on('updateTypeEc', function(type_ec){
    //       RecrutementService.type_ec.resource.query({etape:$scope.monEtape.id}, function(data){
    //           $scope.types_ec = data;
    //        });
    //    });
    //$scope.modify_etape = function(etape){
    //    var modalInstance = $modal.open({
    //        templateUrl: '/static/recruitment/app/partials/update_etape.html',
    //        controller: 'ModifyEtapeCtrl',
    //        resolve: {
    //            etape: function() { return etape }
    //        },
    //        size: "lg",
    //        windowClass: 'my-modal-popup'
    //    });
    //};

}]);