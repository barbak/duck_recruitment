/**
 * Created by paulguichon on 06/10/2015.
 */

var servicesRecrutement = angular.module('servicesRecrutement', ['ngResource']);

servicesRecrutement.factory('Etape', ['$resource',
    function($resource){
        return $resource('/recruitment/v1/etapes/:etapeId', {}, {
            query: {method: 'GET', params: {etapeId: '@etapeId'}, isArray: true}
        })
    }]);


servicesRecrutement.factory('Ec', ['$resource', '$http',
    function($resource, $http){
        var resource = function(){
            return $resource('/recruitment/v1/ecs/:ecId', {}, {
            query: {method: 'GET', params: {ecId: '@ecId'}, isArray: true},
                update: { method: 'PUT', params: {ecId:'@id'}}
            });
        };
        var ec_by_etape = function(etape){
            return $http.get('/recruitment/v1/ecs', {params: {etape: etape.id}, isArray: true});
        };
        return {resource: resource, ec_by_etape: ec_by_etape}
    }]);

servicesRecrutement.factory('PersonneDsi', ['$resource', '$http', function($resource, $http){
    var resource = function(){ return $resource('/recruitment/v1/dsi-individus/:individuId', {}, {
        query: {method: 'GET', params: {individuId: '@individuId'}, isArray: true}
    })};
    var search = function(val){
        return $http.get('/recruitment/v1/dsi-individus', {params: {nom_pat: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);

servicesRecrutement.factory('Agent', ['$resource', '$http', function($resource, $http){
    var resource = function(){
        return $resource('/recruitment/v1/agents/:agentId',{}, {
           query:  {method: 'GET', params: {agentId: '@agentId'}, isArray: true}
        });
    };
    return {resource: resource}
}]);

servicesRecrutement.factory('EtatHeure', ['$resource', '$http', function($resource, $http){
    var resource = function(){
        return $resource('/recruitment/v1/etat_heure/:EtatHeureId',{}, {
           query:  {method: 'GET', params: {EtatHeureId: '@EtatHeureId'}, isArray: true},
            delete: { method: 'DELETE', params: {EtatHeureId: '@id'} }
        });
    };
    var search = function(val){
        return $http.get('/recruitment/v1/etat_heure', {params: {ec: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);

servicesRecrutement.factory('Invitation', ['$resource', '$http', function($resource, $http){

    var resource = function(){
        return $resource('/recruitment/v1/invitations_ec/:InvitationEcId',{}, {
           query:  {method: 'GET', params: {InvitationEcId: '@InvitationEcId'}, isArray: true},
            delete: { method: 'DELETE', params: {InvitationEcId: '@id'} }
        });
    };
    var search = function(val){
        return $http.get('/recruitment/v1/invitations_ec', {params: {ec: val}, isArray: true});
    };
    return {resource: resource, search: search}
}]);

servicesRecrutement.factory('RecrutementService', ['$resource', '$http', function($resource, $http){
    var ec = $resource('/recruitment/v2/ecs/:id',{id:'@id'}, {
        update: { method: 'PUT', params: {id:'@id'}},
        query_with_type_ec: { method: 'GET', params: {id:'@id'}, isArray:true, interceptor: {
            response: function(response){
                var ecs = response.resource;
                var etape = response.config.params.etape;
                 prop_ec.resource.query({etape: etape}, function(data){
                    angular.forEach(ecs, function (ec) {
                     ec.prop_ec = data.find(function (proc_ec) {
                        if (proc_ec.ec == ec.id) {
                            return proc_ec;
                        }
                        return false;
                     });
                     });
                });
                return ecs;
            }
        }}
    });

    var type_ec = {
        resource:
            $resource('/recruitment/v1/type_ec/:id',{id:'@id'}, {
                update: { method: 'PUT', params: {id:'@id'}}
            })

    };
    var heure_forfait = {
        resource:
            $resource('/recruitment/v1/heure_forfait/:id',{id:'@id'}, {
                update: { method: 'PUT', params: {id:'@id'}}
            })

    };
    var prop_ec = {
        resource:
            $resource('/recruitment/v1/prop_ec/:id',{id:'@id'}, {
                update: { method: 'PUT', params: {id:'@id'}}
            })

    };
    var agent = $resource('/recruitment/v2/agents/:id',{id: '@id'});
    var etat_heure = $resource('/recruitment/v1/etat_heure/:id',{id: '@id'},{
                update: { method: 'PUT', params: {id:'@id'}}
            });
    var all_ec_annuel = $resource('/recruitment/v1/all_ec_annuel',{id:'@id'}, {
                update: { method: 'PUT', params: {id:'@id'}}
            });
    return {
        type_ec: type_ec,
        heure_forfait:heure_forfait,
        etat_heure: etat_heure,
        prop_ec: prop_ec,
        ec: ec,
        all_ec_annuel:all_ec_annuel,
        agent: agent
    }
}]);