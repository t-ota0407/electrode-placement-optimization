classdef OptimizationConfig
    properties
        OptimizationMode OptimizationMode
        TargetDomain DomainType
        Conditions 
    end

    methods
        function obj = set.OptimizationMode(obj, optimizationMode)
            arguments
                obj
                optimizationMode OptimizationMode
            end
            obj.OptimizationMode = optimizationMode;
        end
    end
end