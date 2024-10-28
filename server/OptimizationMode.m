classdef OptimizationMode
    enumeration
        SIMPLE_OPTIMIZATION,
        CONDITIONED_OPTIMIZATION
    end

    methods (Static)
        function optimizationMode = fromString(optimizationModeString)
            switch optimizationModeString
                case 'SIMPLE_OPTIMIZATION'
                    optimizationMode = OptimizationMode.SIMPLE_OPTIMIZATION;
                case 'CONDITIONED_OPTIMIZATION'
                    optimizationMode = OptimizationMode.CONDITIONED_OPTIMIZATION;
                otherwise
                    error('There is no OptimizationMode represented by this string expression');
            end
        end
    end
end