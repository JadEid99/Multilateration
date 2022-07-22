import yaml
import os


class ConfigLoader:
    """
       A class that loads the configuration from yaml files.

       ...

       Attributes
       ----------
       target file : str
           path of config file
       file_content : dict of int/str
           configuration from yaml files
       """
    def __init__(self, target_file, file_content={}):
        self.target_file = target_file
        self.file_content = file_content

    def load_config(self) -> dict:
        """
        Loads data from yaml config files.

        Returns
        -------
        file_content : dict of str/int
        """
        if os.path.isfile(self.target_file):
            with open(self.target_file, encoding="utf-8") as config_file:
                self.file_content = yaml.load(config_file, Loader=yaml.SafeLoader)
        return self.file_content
