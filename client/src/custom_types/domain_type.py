import pandas as pd
from enum import Enum

from custom_types.model_type import ModelType

STR_DOMAIN_TYPE = 'DomainType'
STR_DESCRIPTION = 'Description'
STR_TARGETABLE_LOWER_LIMB = 'TargetableLowerLimb'
STR_TARGETABLE_UPPER_LIMB = 'TargetableUpperLimb'
STR_TARGETABLE_HEAD = 'TargetableHead'
STR_VIEWABLE_LOWER_LIMB = 'ViewableLowerLimb'
STR_VIEWABLE_UPPER_LIMB = 'ViewableUpperLimb'
STR_VIEWABLE_HEAD = 'ViewableHead'

class DomainType(Enum):

    ALL = 0
    SKIN = 1
    BONE = 2
    CIRCULATORY = 3
    
    TA_MUSCLE = 101
    GAS_MUSCLE = 102
    PL_MUSCLE = 103
    FDL_MUSCLE = 104
    L_OTHER_MUSCLES = 105

    TA_TENDON = 106
    AC_TENDON = 107
    PL_TENDON = 108
    FDL_TENDON = 109

    DPN_NERVE = 110
    SPN_NERVE = 111
    TI_NERVE = 112
    SU_NERVE = 113
    L_OTHER_NERVES = 114

    FD_MUSCLE = 201
    EX_MUSCLE = 202
    U_OTHER_MUSCLES = 203

    FD_TENDON = 204
    EX_TENDON = 205

    RAD_NERVE = 206
    MED_NERVE = 207
    UL_NERVE = 208
    U_OTHER_NERVES = 209

    RIG_OPTICUS_NERVE = 301
    LEF_OPTICUS_NERVE = 302
    RIG_TRIGEMINAL_NERVE = 303
    LEF_TRIGEMINAL_NERVE = 304
    H_OTHER_NERVES = 305

    @staticmethod
    def _definition() -> pd.DataFrame:
        return pd.DataFrame([
            [DomainType.ALL, 'All domains', False, False, False, True, True, True],
            [DomainType.SKIN, 'Skin', False, False, False, True, True, True],
            [DomainType.BONE, 'Bone', False, False, False, True, True, True],
            [DomainType.CIRCULATORY, 'Vessel', False, False, False, True, True, True],
            [DomainType.TA_MUSCLE, 'Tibialis anterior muscle', True, False, False, True, False, False],
            [DomainType.GAS_MUSCLE, 'Gastrocnemius', True, False, False, True, False, False],
            [DomainType.PL_MUSCLE, 'Peroneus longus muscle', True, False, False, True, False, False],
            [DomainType.FDL_MUSCLE, 'Flexor digitorum longus', True, False, False, True, False, False],
            [DomainType.L_OTHER_MUSCLES, 'Other muscles (Lower limb)', True, False, False, True, False, False],
            [DomainType.TA_TENDON, 'Tibialis anterior muscle tendon', True, False, False, True, False, False],
            [DomainType.AC_TENDON, 'Achilles tendon', True, False, False, True, False, False],
            [DomainType.PL_TENDON, 'Peroneus longus tendon', True, False, False, True, False, False],
            [DomainType.FDL_TENDON, 'Flexor digitorum longus tendon', True, False, False, True, False, False],
            [DomainType.DPN_NERVE, 'Deep peroneal nerve', True, False, False, True, False, False],
            [DomainType.SPN_NERVE, 'Superficial peroneal nerve', True, False, False, True, False, False],
            [DomainType.TI_NERVE, 'Tibial nerve', True, False, False, True, False, False],
            [DomainType.SU_NERVE, 'Sural nerve', True, False, False, True, False, False],
            [DomainType.L_OTHER_NERVES, 'Other nerves (Lower limb)', True, False, False, True, False, False],
            [DomainType.FD_MUSCLE, 'Flexor digitorum superficialis', False, True, False, False, True, False],
            [DomainType.EX_MUSCLE, 'Extensor muscle', False, True, False, False, True, False],
            [DomainType.U_OTHER_MUSCLES, 'Other muscle (Upper limb)', False, True, False, False, True, False],
            [DomainType.FD_TENDON, 'Superficial digitorum flexor tendon', False, True, False, False, True, False],
            [DomainType.EX_TENDON, 'Extensor tendon', False, True, False, False, True, False],
            [DomainType.RAD_NERVE, 'Radial nerve', False, True, False, False, True, False],
            [DomainType.MED_NERVE, 'Median nerve', False, True, False, False, True, False],
            [DomainType.UL_NERVE, 'Ulnar nerve', False, True, False, False, True, False],
            [DomainType.U_OTHER_NERVES, 'Other nerves (Upper limb)', False, True, False, False, True, False],
            [DomainType.RIG_OPTICUS_NERVE, 'Right opticus nerve', False, False, True, False, False, True],
            [DomainType.LEF_OPTICUS_NERVE, 'Left opticus nerve', False, False, True, False, False, True],
            [DomainType.RIG_TRIGEMINAL_NERVE, 'Right trigeminal nerve', False, False, True, False, False, True],
            [DomainType.LEF_TRIGEMINAL_NERVE, 'Left trigeminal nerve', False, False, True, False, False, True],
            [DomainType.H_OTHER_NERVES, 'Other nerves (Head)', False, False, True, False, False, True],
        ], columns=[STR_DOMAIN_TYPE, STR_DESCRIPTION, STR_TARGETABLE_LOWER_LIMB, STR_TARGETABLE_UPPER_LIMB, STR_TARGETABLE_HEAD, STR_VIEWABLE_LOWER_LIMB, STR_VIEWABLE_UPPER_LIMB, STR_VIEWABLE_HEAD])

    @staticmethod
    def _exists(target_column_str, value) -> bool:
        return (value in DomainType._definition()[target_column_str].values)
    
    @staticmethod
    def _convert(original_value, original_column_str, converted_column_str):
        return DomainType._definition().loc[DomainType._definition()[original_column_str] == original_value,
                                                  converted_column_str].values[0]
    
    @staticmethod
    def get_targetable_descriptions(model_type):
        definition_df = DomainType._definition()
        str_in_selected_part = (
            STR_TARGETABLE_LOWER_LIMB if model_type == ModelType.LOWER_LIMB
            else STR_TARGETABLE_UPPER_LIMB if model_type == ModelType.UPPER_LIMB
            else STR_TARGETABLE_HEAD)
        filtered_df = definition_df[definition_df[str_in_selected_part] == True]
        return filtered_df[STR_DESCRIPTION].values

    @staticmethod
    def get_viewable_descriptions(model_type):
        definition_df = DomainType._definition()
        str_in_selected_part = (
            STR_VIEWABLE_LOWER_LIMB if model_type == ModelType.LOWER_LIMB
            else STR_VIEWABLE_UPPER_LIMB if model_type == ModelType.UPPER_LIMB
            else STR_VIEWABLE_HEAD)
        filtered_df = definition_df[definition_df[str_in_selected_part] == True]
        return filtered_df[STR_DESCRIPTION].values

    @staticmethod
    def to_description(domain_type):
        if not DomainType._exists(STR_DOMAIN_TYPE, domain_type):
            raise ValueError('Invalid DomainType was provided.')
        
        return DomainType._convert(domain_type, STR_DOMAIN_TYPE, STR_DESCRIPTION)
    
    # @deprecated Descriptionの値は重複する可能性があるため非推奨
    @staticmethod
    def from_description(description):
        if not DomainType._exists(STR_DESCRIPTION, description):
            raise ValueError('Provided description has no corresponding DomainType.')
        
        return DomainType._convert(description, STR_DESCRIPTION, STR_DOMAIN_TYPE)
