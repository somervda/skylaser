import json

class SettingsManager:
    def __init__(self, settings_file_path):
        self.settings_file_path = settings_file_path
        self.settings = {}
        self._load_settings()

    def _load_settings(self):
        try:
            with open(self.settings_file_path, 'r') as file:
                self.settings = json.load(file)
            print("Settings loaded successfully.")
        except FileNotFoundError:
            print(f"Error: The settings file '{self.settings_file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The settings file '{self.settings_file_path}' is not a valid JSON file.")

    def get_setting(self, key):
        """
        Returns the value for the requested setting.
        
        Args:
        key (str): The key of the setting to retrieve.
        
        Returns:
        any: The value associated with the key if it exists, None otherwise.
        """
        return self.settings.get(key, None)