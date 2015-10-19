
myApp.controller('RecruitmentCtrl',
    ['$scope', '$modal', '$http', '$log', 'Etape', 'Ec', 'PersonneDsi', 'EtatHeure', 'Invitation',
    function ($scope, $modal, $http, $log, Etape, Ec, PersonneDsi, EtatHeure, Invitation) {
    $scope.agents = [];
    $scope.monEtape = null;


    var getAgent = function(ec){
        EtatHeure.search(ec.code_ec).success(function(data){
            ec.agents = data;
        });
    };
    $scope.filter_invit=function(invitation){
            return invitation.date_acceptation==null;
    };
    var getInvitation = function(ec){
        Invitation.search(ec.code_ec).success(function(data){
            ec.invitations = data;
        });
    };
    $scope.listEc = function(etape){
        Ec.ec_by_etape(etape).success(function(data){
            $scope.ecs = data.results;
            ecs = $scope.ecs;
            for (var i = 0, length=ecs.length; i<length; i++){
               getAgent(ecs[i]);
               getInvitation(ecs[i]);
            }
        }).error(function(data, status, headers, config) {
            $scope.ecs = 'Erreur de chargement, serveur indisponible';
        });
    };
    $scope.etapes = Etape.query(function(data){
        console.log(data);
        $scope.monEtape = $scope.etapes[0];
         $scope.listEc({id: $scope.etapes[0].id });
    });
    $scope.$on('addPersonneDone', function(event, ec){
        getAgent(ec);

    });
    $scope.$on('addInvitationDone', function(event, ec){
        getAgent(ec);
        getInvitation(ec);
    });
    $scope.$on('createInvidation', function(event, ec){

        $scope.createInvitation(ec)
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
    $scope.createInvitation =  function(ec){
            var modalInstance = $modal.open({
            templateUrl: '/static/recruitment/app/partials/createInvitation.html',
                controller: 'InvitationCtrl',
                resolve: {
                     ec: function(){return ec}
                }
            });
        };
    $scope.valider_agent = function(agent){
        agent.valider = true;
        i = EtatHeure.resource().save(agent, function(){agent=i});
    };
    $scope.valider_invitation = function(invitation){
        invitation.valider = true;
        i = Invitation.resource().save(invitation, function(){invitation=i});
    };

    $scope.delete_invitation = function(invitation, ec){
        if (!invitation.valider) {
            var idx = ec.invitations.indexOf(invitation);
            i = Invitation.resource().get({InvitationEcId: invitation.id}, function () {
                i.$delete(function () {
                    ec.invitations.splice(idx, 1);
                });});}};


    $scope.delete_agent = function(agent, ec){
        if (!agent.valider) {
            var idx = ec.agents.indexOf(agent);
            i = EtatHeure.resource().get({EtatHeureId: agent.id}, function () {
                i.$delete(function () {
                    ec.agents.splice(idx, 1);
                });
            });
        }
    };
}]);


myApp.controller('SearchCtrl',
    ['$rootScope', '$scope', '$modalInstance', 'ec', '$modal', '$http', '$log', 'PersonneDsi', 'Agent', 'EtatHeure',
    function ($rootScope, $scope, $modalInstance, ec, $modal, $http, $log, PersonneDsi, Agent, EtatHeure) {

        $scope.ec = ec;
        $scope.forfaitaire = true;
        $scope.getPersonne =  function(value){
            return PersonneDsi.search(value).then(function(response){return response.data.results});
        };
        $scope.addPersonne = function(personne, ec){
            Agent.resource().save({individu_id:personne.numero, type: personne.type, annee:'2015', code_ec:ec.code_ec,
                forfaitaire: $scope.forfaitaire, heure: $scope.nb_heure}).$promise.then(function(){
                $scope.message = 'Opération réussi';
                $scope.pers = null;
            }, function(){
               $scope.errors = {Erreur: 'Il y a eu une erreur'};

            }).then(function(){
                $rootScope.$broadcast('addPersonneDone', ec);

            });
        };
        $scope.createInvitation =  function(ec){
            $modalInstance.close();
            $rootScope.$broadcast('createInvidation', ec);
        };

}]);


myApp.controller('InvitationCtrl',
    ['$rootScope', '$scope', '$modalInstance', 'ec', 'Invitation',
    function ($rootScope, $scope, $modalInstance, ec, Invitation) {

        $scope.ec = ec;
        $scope.forfaitaire = true;
        $scope.createInvitation =  function(){
            Invitation.resource().save({ec: ec.code_ec, email: $scope.email,
                forfaitaire: $scope.forfaitaire, nombre_heure_estime: $scope.nb_heure}).$promise.then(function(){
                $rootScope.$broadcast('addInvitationDone', ec);
                $scope.errors = null;
                $scope.message = "L'invitation a bien été envoyé à l'adresse : " + $scope.email

            }, function(request){
                $scope.errors = request.data;
                    $scope.message = null;
                $rootScope.$broadcast('addInvitationDone', ec);
            });
        };

}]);