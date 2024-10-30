classdef ModelType
    enumeration
        LOWER_LIMB,
        UPPER_LIMB,
        HEAD
    end

   methods (Static)
       function modelType = fromString(modelTypeString)
           switch modelTypeString
               case 'LOWER_LIMB'
                   modelType = ModelType.LOWER_LIMB;
               case 'UPPER_LIMB'
                   modelType = ModelType.UPPER_LIMB;
               case 'HEAD'
                   modelType = ModelType.HEAD;
               otherwise
                   error('There is no ModelType represented by this string expression.')
           end
       end

       function modelPath = toModelPath(modelType)
           switch modelType
               case ModelType.LOWER_LIMB
                   modelPath = './models/lower_limb.mph';
               case ModelType.UPPER_LIMB
                   modelPath = './models/upper_limb.mph';
               case MOdelType.HEAD
                   modelPath = './models/head.mph';
               otherwise
                   error('Invalid ModelType was provided.');
           end
       end
   end
end
