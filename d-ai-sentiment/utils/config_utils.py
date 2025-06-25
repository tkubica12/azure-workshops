from typing import Dict


class ConfigUtils:
    """Utility class for loading and validating configuration files."""
    
    @staticmethod
    def load_yaml_config(config_path: str) -> Dict:
        """
        Load YAML configuration file.
        
        Args:
            config_path: Path to YAML config file
            
        Returns:
            Dict: Configuration data
        """
        try:
            import yaml
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except ImportError:
            raise ImportError("PyYAML is required. Install with: pip install pyyaml")
        except Exception as e:
            raise Exception(f"Error loading config from {config_path}: {str(e)}")
    
    @staticmethod
    def load_simple_config(config_path: str) -> Dict:
        """
        Load simple key=value configuration file (fallback if PyYAML not available).
        
        Args:
            config_path: Path to config file
            
        Returns:
            Dict: Configuration data
        """
        config = {'dataset_files': {}}
        
        try:
            with open(config_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            if key in ['train', 'test', 'validation']:
                                config['dataset_files'][key] = value
                            elif key == 'text_column':
                                config['text_column'] = value
            
            return config
        except Exception as e:
            raise Exception(f"Error loading config from {config_path}: {str(e)}")
    
    @staticmethod
    def load_config(config_path: str) -> Dict:
        """
        Load configuration from file, trying YAML first, then simple format.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dict: Configuration data
        """
        try:
            # Try YAML first
            return ConfigUtils.load_yaml_config(config_path)
        except ImportError:
            print("PyYAML not available, trying simple config format...")
            return ConfigUtils.load_simple_config(config_path)
        except Exception as e:
            print(f"Error loading YAML config: {e}")
            print("Trying simple config format...")
            return ConfigUtils.load_simple_config(config_path)
    @staticmethod
    def validate_dataset_config(config: Dict) -> None:
        """
        Validate dataset configuration structure.
        
        Args:
            config: Configuration dictionary
            
        Raises:
            ValueError: If configuration is invalid
        """
        required_keys = ['dataset_files', 'text_column']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
        
        # Check for minimum required datasets (train, test, validation)
        required_datasets = ['train', 'test', 'validation']
        for dataset in required_datasets:
            if dataset not in config['dataset_files']:
                raise ValueError(f"Missing required dataset file mapping: {dataset}")
        
        # Optional datasets that may or may not be present
        optional_datasets = ['train_100', 'train_1000', 'train_all']
        missing_optional = []
        for dataset in optional_datasets:
            if dataset not in config['dataset_files']:
                missing_optional.append(dataset)
        
        if missing_optional:
            print(f"Note: Optional datasets not configured: {', '.join(missing_optional)}")
            print("Run dataset_trim.py to create these files if needed.")
    
    @staticmethod
    def validate_config(config: Dict, required_keys: list = None, required_datasets: list = None) -> None:
        """
        Generic configuration validation.
        
        Args:
            config: Configuration dictionary
            required_keys: List of required top-level keys
            required_datasets: List of required dataset types
            
        Raises:
            ValueError: If configuration is invalid
        """
        if required_keys is None:
            required_keys = ['dataset_files', 'text_column']
        
        if required_datasets is None:
            required_datasets = ['train', 'test', 'validation']
        
        # Check required top-level keys
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
        
        # Check required dataset files if dataset_files is required
        if 'dataset_files' in required_keys and required_datasets:
            for dataset in required_datasets:
                if dataset not in config['dataset_files']:
                    raise ValueError(f"Missing dataset file mapping: {dataset}")
