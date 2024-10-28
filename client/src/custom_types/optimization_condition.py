from typing import List, Tuple, Optional
from dataclasses import dataclass

from custom_types.optimization_mode import OptimizationMode
from custom_types.domain_type import DomainType

@dataclass
class OptimizationCondition:
    optimization_mode: OptimizationMode
    target_domain: DomainType
    constraints: Optional[List[Tuple[DomainType, float]]] = None
