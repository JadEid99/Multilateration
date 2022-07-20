import yaml
import os


class ConfigLoader:
    def __init__(self, target_file, file_content=""):
        self.target_file = target_file
        self.file_content = file_content

    def load_config(self) -> dict:
        if os.path.isfile(self.target_file):
            with open(self.target_file, encoding="utf-8") as config_file:
                self.file_content = yaml.load(config_file, Loader=yaml.SafeLoader)
        return self.file_content
