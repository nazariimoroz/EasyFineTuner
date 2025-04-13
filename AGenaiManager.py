from google import genai
from google.genai import types

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class AGenaiManager:
    def __init__(self):
        self.client = genai.Client()
        
    def list_tunings(self):
        return list(self.client.tunings.list())
        
    def delete_model(self, model_name):
        self.client.models.delete(model=model_name)
        
    def list_models(self):
        return list(self.client.models.list())
        
    def create_tuning(self, base_model, training_dataset, config):
        return self.client.tunings.tune(
            base_model=base_model,
            training_dataset=training_dataset,
            config=config
        )
        
    def get_tuning(self, name):
        return self.client.tunings.get(name=name)
        
    def generate_content(self, model, content):
        return self.client.models.generate_content(
            model=model,
            contents=content
        )
