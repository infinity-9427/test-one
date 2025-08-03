"""
Weights configuration loader for design analysis scoring.
"""
import yaml
from pathlib import Path
from typing import Dict, Any
from ..core.settings import settings


class WeightsConfig:
    """Configuration loader for analysis weights and thresholds."""
    
    def __init__(self, config_path: str = "weights.yaml"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load weights configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {self.config_path} not found, using default weights")
            self._config = self._get_default_config()
        except Exception as e:
            print(f"Error loading weights config: {e}, using defaults")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration if file is not available."""
        return {
            "weights": {
                "typography": 0.25,
                "color": 0.20,
                "layout": 0.25,
                "responsiveness": 0.15,
                "accessibility": 0.15
            },
            "thresholds": {
                "excellent": 90,
                "good": 70,
                "fair": 50,
                "poor": 0
            },
            "version": "1.0"
        }
    
    def get_weights(self) -> Dict[str, float]:
        """Get scoring weights."""
        return self._config.get("weights", {})
    
    def get_thresholds(self) -> Dict[str, int]:
        """Get scoring thresholds."""
        return self._config.get("thresholds", {})
    
    def get_score_category(self, score: float) -> str:
        """Get score category based on thresholds."""
        thresholds = self.get_thresholds()
        
        if score >= thresholds.get("excellent", 90):
            return "excellent"
        elif score >= thresholds.get("good", 70):
            return "good"
        elif score >= thresholds.get("fair", 50):
            return "fair"
        else:
            return "poor"
    
    def get_version(self) -> str:
        """Get configuration version."""
        return self._config.get("version", "unknown")


# Global instance
weights_config = WeightsConfig()
