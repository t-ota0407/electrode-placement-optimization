import pandas as pd
from enum import Enum

STR_OPTIMIZATION_MODE = 'OptimizationMode'
STR_STRING_EXPRESSION = 'StringExpression'
STR_DESCRIPTION = 'Description'
STR_IDENTICAL_NUMBER = 'IdenticalNumber'

class OptimizationMode(Enum):

    SIMPLE_OPTIMIZATION = 1
    CONDITIONED_OPTIMIZATION = 2

    @staticmethod
    def _definition() -> pd.DataFrame:
        return pd.DataFrame([
            [OptimizationMode.SIMPLE_OPTIMIZATION, 'SIMPLE_OPTIMIZATION', 'Optimization of a target domain', 1],
            [OptimizationMode.CONDITIONED_OPTIMIZATION, 'CONDITIONED_OPTIMIZATION', 'Conditioned optimization of a target domain', 2]
        ], columns=[STR_OPTIMIZATION_MODE, STR_STRING_EXPRESSION, STR_DESCRIPTION, STR_IDENTICAL_NUMBER])
    
    @staticmethod
    def _exists(target_column_str, value) -> bool:
        return (value in OptimizationMode._definition()[target_column_str].values)
    
    @staticmethod
    def _convert(original_value, original_column_str, converted_column_str):
        return OptimizationMode._definition().loc[OptimizationMode._definition()[original_column_str] == original_value,
                                                  converted_column_str].values[0]

    @staticmethod
    def from_str(optimization_mode_str: str):
        if not OptimizationMode._exists(STR_STRING_EXPRESSION, optimization_mode_str):
            raise ValueError('Provided string has no corresponding OptimizationMode.')
        
        return OptimizationMode._convert(optimization_mode_str, STR_STRING_EXPRESSION, STR_OPTIMIZATION_MODE)
    
    @staticmethod
    def to_description(optimization_mode):
        if not OptimizationMode._exists(STR_OPTIMIZATION_MODE, optimization_mode):
            raise ValueError('Invalid OptimizationMode was provided.')

        return OptimizationMode._convert(optimization_mode, STR_OPTIMIZATION_MODE, STR_DESCRIPTION)
    
    @staticmethod
    def to_identical_number(optimization_mode):
        if not OptimizationMode._exists(STR_OPTIMIZATION_MODE, optimization_mode):
            raise ValueError('Invalid OptimizationMode was provided.')

        return OptimizationMode._convert(optimization_mode, STR_OPTIMIZATION_MODE, STR_IDENTICAL_NUMBER)
    
    @staticmethod
    def from_identical_number(identical_number):
        if not OptimizationMode._exists(STR_IDENTICAL_NUMBER, identical_number):
            raise ValueError('Provided number has no corresponding OptimizationMode.')

        return OptimizationMode._convert(identical_number, STR_IDENTICAL_NUMBER, STR_OPTIMIZATION_MODE)
