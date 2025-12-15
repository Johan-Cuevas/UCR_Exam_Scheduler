"""Repository for exam data access from JSON file."""

import json
from pathlib import Path
from functools import lru_cache


class ExamRepository:
    """Repository for accessing exam data from JSON storage."""
    
    def __init__(self, data_path: str | Path | None = None):
        """Initialize the repository with the path to the data file.
        
        Args:
            data_path: Path to the exams.json file. If not provided,
                      defaults to backend/data/exams.json.
        """
        if data_path is None:
            # Default path relative to this file's location
            base_dir = Path(__file__).parent.parent.parent
            data_path = base_dir / "data" / "exams.json"
        
        self._data_path = Path(data_path)
        self._cache: list[dict] | None = None
    
    def get_all_exams(self) -> list[dict]:
        """Get all exams from the data file.
        
        Returns:
            List of exam dictionaries.
            
        Note:
            Results are cached after the first read for performance.
        """
        if self._cache is not None:
            return self._cache
        
        return self._load_exams()
    
    def _load_exams(self) -> list[dict]:
        """Load exams from the JSON file.
        
        Returns:
            List of exam dictionaries.
            
        Raises:
            FileNotFoundError: If the data file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        if not self._data_path.exists():
            raise FileNotFoundError(f"Exam data file not found: {self._data_path}")
        
        with open(self._data_path, "r", encoding="utf-8") as f:
            self._cache = json.load(f)
        
        return self._cache
    
    def clear_cache(self) -> None:
        """Clear the cached exam data.
        
        This forces a fresh read from the file on the next access.
        """
        self._cache = None
