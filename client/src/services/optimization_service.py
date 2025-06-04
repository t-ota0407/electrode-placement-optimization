import os
import json
import pandas as pd
from pathlib import Path
from functools import partial
from typing import List, Tuple, Callable

import config
from model_data import ModelData
from custom_types.model_type import ModelType
from custom_types.optimization_mode import OptimizationMode
from errors.validation_error import ValidationError

class OptimizationService:
    def __init__(self):
        pass

    def execute_optimization(self, 
                           selected_model: ModelType,
                           optimization_mode: OptimizationMode,
                           optimization_condition: any,
                           active_domain: any,
                           draw_model_callback: Callable[[ModelData, bool, bool], None]) -> List[Tuple[str, Callable]]:
        try:
            solutions_csv_path = (Path(config.LOWER_LIMB_CACHE_DIR_PATH, 'solutions.csv') if selected_model == ModelType.LOWER_LIMB
                            else Path(config.UPPER_LIMB_CACHE_DIR_PATH, 'solutions.csv') if selected_model == ModelType.UPPER_LIMB
                            else Path(config.HEAD_CACHE_DIR_PATH, 'solutions.csv'))
            solutions_df = pd.read_csv(solutions_csv_path)
        except FileNotFoundError as e:
            raise ValidationError('The solution file was not found')

        if optimization_mode == OptimizationMode.CONDITIONED_OPTIMIZATION:
            for constraint_domain, constraint_value in optimization_condition.constraints:
                solutions_df = solutions_df[solutions_df[constraint_domain.name] <= constraint_value]

        result_df = solutions_df.nlargest(3, optimization_condition.target_domain.name)

        results = []
        for iter_idx, (index, row) in enumerate(result_df.iterrows()):
            anode = int(row.Anode)
            cathode = int(row.Cathode)
            
            cache_dir_path = (config.LOWER_LIMB_CACHE_DIR_PATH if selected_model == ModelType.LOWER_LIMB
                              else config.UPPER_LIMB_CACHE_DIR_PATH if selected_model == ModelType.UPPER_LIMB
                              else config.HEAD_CACHE_DIR_PATH)

            for file in os.listdir(cache_dir_path):
                if f'{anode}-{cathode}-{active_domain.name}' in file:
                    cache_path = Path(cache_dir_path, file)
                    with open(cache_path, 'r', encoding='utf-8') as file:
                        cached_data = file.read()
                    cached_data = json.loads(cached_data)
                    model_data = ModelData.from_json(cached_data)
                    
                    if iter_idx == 0:
                        draw_model_callback(model_data, True, False)

                    results.append((
                        f'Solution{iter_idx+1}  Anode:{anode}, Cathode:{cathode}',
                        partial(draw_model_callback, model_data, True, True)
                    ))

        return results

    def load_model(self, model_type: ModelType, tcpip_communication=None) -> ModelData:
        if config.USE_CACHE:
            cache_path = ModelType.to_initial_model_cache_path(model_type)            
            with open(cache_path, 'r', encoding='utf-8') as file:
                cached_data = file.read()
            cached_data = json.loads(cached_data)
            return ModelData.from_json(cached_data)
        else:
            model_data_json = tcpip_communication.load_model(model_type)
            return ModelData.from_json(model_data_json) 