from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SearchState:
    """Holds the shared state of the search process."""
    properties: List[Dict[str, Any]] = field(default_factory=list)
    total: int = 0
    processed: int = 0
    status: str = "initializing" # initializing, processing, complete
