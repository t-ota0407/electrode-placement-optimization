from enum import Enum
from pathlib import Path

class ModelType(Enum):
    
    LOWER_LIMB = 1
    UPPER_LIMB = 2
    HEAD = 3

    @staticmethod
    def from_str(model_type_str):
        str_to_model_type = {
            'LOWER_LIMB': ModelType.LOWER_LIMB,
            'UPPER_LIMB': ModelType.UPPER_LIMB,
            'HEAD': ModelType.HEAD
        }
        
        if not (model_type_str in str_to_model_type.keys()):
            raise ValueError('Provided string has no corresponding ModelType.')
        return str_to_model_type[model_type_str]
    
    @staticmethod
    def to_icon_img_path(model_type) -> Path:
        model_to_icon_img_path = {
            ModelType.LOWER_LIMB: Path('../resources/images/lower_limb.png'),
            ModelType.UPPER_LIMB: Path('../resources/images/upper_limb.png'),
            ModelType.HEAD: Path('../resources/images/head.png')
        }

        if not (model_type in model_to_icon_img_path.keys()):
            raise ValueError('Invalid ModelType was provided.')
        return model_to_icon_img_path[model_type]
    
    @staticmethod
    def to_initial_model_cache_path(model_type) -> Path:
        model_to_initial_model_cache_path = {
            ModelType.LOWER_LIMB: Path('../resources/model_data_cache/initial_lower_limb_model.txt'),
            ModelType.UPPER_LIMB: Path('../resources/model_data_cache/initial_upper_limb_model.txt'),
            ModelType.HEAD: Path('../resources/model_data_cache/initial_head_model.txt')
        }

        if not (model_type in model_to_initial_model_cache_path):
            raise ValueError('Invalid ModelType was provided.')
        return model_to_initial_model_cache_path[model_type].resolve()
