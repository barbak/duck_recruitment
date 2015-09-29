myApp.controller('RecruitmentCtrl', ['$scope', '$modal', '$http', '$log', function ($scope, $modal, $http, $log) {
    $scope.agents = [];
    $scope.open = function (what, agent) {

        var templateUrl = '';

        switch (what) {
            case 'ied':
                templateUrl = '/static/recruitment/app/partials/agent-ied-detail.html';
                break;

            case 'dsi':
                templateUrl = '/static/recruitment/app/partials/agent-dsi-detail.html';
                break;
        }
        var modalInstance = $modal.open({
            animation: true,
            templateUrl: templateUrl,
            controller: 'AgentCtrl',
            size: 'sm',
            resolve: {
                what: function() {
                    return what;
                },
                recruitmentCtrlScope: function() {
                    return $scope;
                },
                agent: function() {
                    return agent;
                }
            }
        });
        modalInstance.result.then(null,
            function () {
                alert("BLOP");
            })
    };
    $scope.loadAgents = function () {
        var url = "/recruitment/agents";
        $http.get(url)
            .success(function(data, status, headers, config) {
                $log.log(data);
                $scope.agents = data;
                // $scope.isLoading = false;
            })
            .error(function(data, status, headers, config) {
                alert("Ajax Failed !");
                // $scope.isLoading = false;
            });
    };
    $scope.editAgent = function (agent) {
        $scope.open('ied', agent);
    };
    $scope.delAgent = function (agentId) {
        var url = "/recruitment/delete_agent/?pk=" + agentId;
        $http.get(url)
            .success(function(data, status, headers, config) {
                $scope.loadAgents();
            })
            .error(function(data, status, headers, config) {
                alert("AJAX FAILED !");
            })
    };
    $scope.loadAgents();
}]);

myApp.controller('AgentCtrl',
    ['$scope', '$modalInstance', 'what', 'recruitmentCtrlScope', 'agent', '$http', '$log',
        function ($scope, $modalInstance, what, recruitmentCtrlScope, agent, $http, $log) {

//            $scope.items = items;
//            $scope.selected = {
//                item: $scope.items[0]
//            };
            $scope.isLoading = true;
            $scope.what = what;
            $scope.agent = typeof agent === 'undefined' ? {} : agent;

            if ($scope.agent.birthday) { // Changing "%Y-%m-%d" to "%d/%m/%Y"
                elems = $scope.agent.birthday.split('-');
                $scope.agent.birthday = elems[2] + '/' + elems[1] + '/' + elems[0];
            }

            $scope.ok = function () {
                $modalInstance.close($scope.what); //$scope.selected.item);
                recruitmentCtrlScope.loadAgents();
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
                recruitmentCtrlScope.loadAgents();
            };

            $scope.addAgent = function () { //? finally the same as addDsiAgent
                // Check
                var url = "/recruitment/add_agent/";
                $http.post(url, $scope.agent )
                    .success(function(data, status, headers, config) {
                        $log.log($scope.agent);
                        recruitmentCtrlScope.loadAgents();
                    })
                    .error(function(data, status, headers, config) {
                        alert("Ajax Failed !");
                        $scope.isLoading = false;
                    });
            };

            function convertTimedmYtoYmd(dateStr) {
                if (dateStr) { // Changing "%d/%m/%Y" to "%Y-%m-%d"
                    elems = dateStr.split('/');
                    dateStr = elems[2] + '-' + elems[1] + '-' + elems[0];
                    return dateStr;
                }
            }

            function convertTimeYmdtodmY(dateStr) {
                if (dateStr) { // Changing "%Y-%m-%d" to "%d/%m/%Y"
                    elems = dateStr.split('-');
                    dateStr = elems[2] + '/' + elems[1] + '/' + elems[0];
                    return dateStr;
                }
            }

            $scope.modifyAgent = function () {
                var url = "/recruitment/modify_agent/";

                if ($scope.agent.birthday) { // Changing "%d/%m/%Y" to "%Y-%m-%d"
                    $scope.agent.birthday = convertTimedmYtoYmd($scope.agent.birthday);
                }
                $http.post(url, $scope.agent)
                    .success(function(data, status, headers, config) {
                        $log.log($scope.agent);
                        recruitmentCtrlScope.loadAgents();
                        if ($scope.agent.birthday) { // Changing "%Y-%m-%d" to "%d/%m/%Y"
                            $scope.agent.birthday = convertTimeYmdtodmY($scope.agent.birthday);
                        }
                    })
                    .error(function(data, status, headers, config) {
                        alert("Ajax Failed !");
                        $log.log(data);
                        $log.log(status);
                        $log.log(headers);
                        $log.log(config);
                        $scope.isLoading = false;
                        if ($scope.agent.birthday) { // Changing "%Y-%m-%d" to "%d/%m/%Y"
                            $scope.agent.birthday = convertTimeYmdtodmY($scope.agent.birthday);
                        }
                    });
            };

            function loadIndividusDSI(query) {
                var url = "/recruitment/dsi-individus"; //?page=" + page + "&last_name=" + query;
                $http.get(url)
                    .success(function(data, status, headers, config) {
                        $scope.dsi_agents = data;
                        $scope.isLoading = false;
                    })
                    .error(function(data, status, headers, config) {
                        alert("Ajax Failed !");
                        $scope.isLoading = false;
                    });
            };

            $scope.onQueryChange = function () {
                $scope.isLoading = true;
                loadIndividusDSI($scope.query);
            };

            $scope.addDsiAgent = function (agent) {
                var url = "/recruitment/add_agent/";
                $http.post(url, agent)
                    .success(function(data, status, headers, config) {
                        $log.log(agent);
                        recruitmentCtrlScope.loadAgents();
                        //$scope.dsi_agents = data;
                        //$scope.isLoading = false;
                    })
                    .error(function(data, status, headers, config) {
                        alert("Ajax Failed !");
                        $log.log(data);
                        $log.log(status);
                        $log.log(headers);
                        $log.log(config);
                        $scope.isLoading = false;
                    });
            };

            loadIndividusDSI();
        }]);
