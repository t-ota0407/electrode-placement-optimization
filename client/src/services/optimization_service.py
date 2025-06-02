import os
import json
import pandas as pd
from pathlib import Path
from functools import partial

import config as config
from model_data import ModelData
from custom_types.model_type import ModelType
from custom_types.domain_type import DomainType
from custom_types.optimization_mode import OptimizationMode
from errors.validation_error import ValidationError

class OptimizationService:
    def execute_optimization(self, model_type: ModelType, optimization_mode: OptimizationMode, optimization_condition, active_domain: DomainType):
        """最適化の実行"""
        if not config.USE_CACHE:
            return []

        try:
            solutions_df = self._load_solutions(model_type)
        except FileNotFoundError:
            raise FileNotFoundError('The solution file was not found')

        # Apply optimization conditions
        if optimization_mode == OptimizationMode.CONDITIONED_OPTIMIZATION:
            for constraint_domain, constraint_value in optimization_condition.constraints:
                solutions_df = solutions_df[solutions_df[constraint_domain.name] <= constraint_value]

        # Get top results
        result_df = solutions_df.nlargest(3, optimization_condition.target_domain.name)
        
        return self._process_results(result_df, model_type, active_domain)

    def _load_solutions(self, model_type: ModelType) -> pd.DataFrame:
        """ソリューションファイルの読み込み"""
        cache_paths = {
            ModelType.LOWER_LIMB: Path(config.LOWER_LIMB_CACHE_DIR_PATH, 'solutions.csv'),
            ModelType.UPPER_LIMB: Path(config.UPPER_LIMB_CACHE_DIR_PATH, 'solutions.csv'),
            ModelType.HEAD: Path(config.HEAD_CACHE_DIR_PATH, 'solutions.csv')
        }
        
        solutions_csv_path = cache_paths[model_type]
        return pd.read_csv(solutions_csv_path)

    def _process_results(self, result_df, model_type: ModelType, active_domain: DomainType):
        """結果の処理"""
        results = []
        cache_dir_path = self._get_cache_dir_path(model_type)

        for iter_idx, (index, row) in enumerate(result_df.iterrows()):
            anode = int(row.Anode)
            cathode = int(row.Cathode)
            
            model_data = self._load_result_model_data(cache_dir_path, anode, cathode, active_domain)
            if model_data is None:
                continue

            result_text = f'Solution{iter_idx+1}  Anode:{anode}, Cathode:{cathode}'
            results.append((result_text, model_data))

        return results

    def _get_cache_dir_path(self, model_type: ModelType) -> Path:
        """キャッシュディレクトリパスの取得"""
        cache_paths = {
            ModelType.LOWER_LIMB: config.LOWER_LIMB_CACHE_DIR_PATH,
            ModelType.UPPER_LIMB: config.UPPER_LIMB_CACHE_DIR_PATH,
            ModelType.HEAD: config.HEAD_CACHE_DIR_PATH
        }
        return cache_paths[model_type]

    def _load_result_model_data(self, cache_dir_path: Path, anode: int, cathode: int, active_domain: DomainType) -> ModelData:
        """結果のモデルデータの読み込み"""
        for file in os.listdir(cache_dir_path):
            if f'{anode}-{cathode}-{active_domain.name}' in file:
                cache_path = Path(cache_dir_path, file)
                with open(cache_path, 'r', encoding='utf-8') as file:
                    cached_data = file.read()
                cached_data = json.loads(cached_data)
                return ModelData.from_json(cached_data)
        return None 