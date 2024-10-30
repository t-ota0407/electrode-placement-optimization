classdef DomainType
    enumeration
        SKIN,
        BONE,
        CIRCULATORY,

        TA_TENDON,
        AC_TENDON,
        FDL_TENDON,
        PL_TENDON,

        PERONEAL_NERVE,
        TIBIAL_NERVE,
        SURAL_NERVE,

        FLEXOR_DIGITORUM_SUPERFICIAL,
        EXTENSOR_DIGITORUM,

        RADIAN_NERVE,
        MEDIAL_NERVE,
        ULNAR_NERVE,

        LEFT_TRIGEMINAL_NERVE
        RIGHT_TRIGEMINAL_NERVE
    end

    methods (Static)
        function modelType = fromString(modelTypeString)
            switch modelTypeString
                case 'SKIN'
                    modelType = ModelType.SKIN;
                otherwise
                    error('There is no DomainType represented by this string expression.')
            end
        end
    end
end