classdef OptimizationCondition
    properties
        domain DomainType
        threshold double
    end
    
    methods
        function obj = OptimizationCondition(domain, threshold)
            if nargin == 2
                obj.domain = domain;
                obj.threshold = threshold;
            else
                error('Invalid number of input arguments for instantiating OptimizationCondition.');
            end
        end
    end
end
