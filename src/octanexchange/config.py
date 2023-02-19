from pathlib import Path
import yaml


class Config:
    def __init__(self):
        conf_path = Path(__file__).parent/'conf.yaml'
        with open(conf_path) as f:
            self.doc = yaml.safe_load(f)

    def get(self, key:str):
        return self.doc.get(key)

    @property
    def exchanges_api_url(self):
        return self.doc.get('exchanges_api_url')

    @property
    def default_currency(self):
        return self.doc.get('default_currency')
