from google import genai
from google.genai import types
from py_singleton import singleton
import json
import os
from dataclasses import dataclass
from typing import Any
from ACacheManager import ACacheManager

@dataclass
class TuningWrapper:
    tuning: genai.types.TuningJob
    training_dataset: str = ""
    
    @property
    def name(self):
        return self.tuning.name
        
    @property
    def state(self):
        state = str(self.tuning.state)
        if state.startswith('JobState.JOB_STATE_'):
            state = state[len('JobState.JOB_STATE_'):].capitalize()
        return state
        
    @property
    def info(self):
        to_ret = {}
        to_ret['name'] = self.tuning.name
        to_ret['create_time'] = self.tuning.create_time.strftime("%Y-%m-%d %H:%M:%S")
        return "\n".join([f"{k}: {v}" for k, v in to_ret.items()])

        return to_ret

    @property
    def training_dataset_formatted(self):
        if not self.training_dataset:
            return "No dataset available"

        if isinstance(self.training_dataset, str):
            try:
                data = json.loads(self.training_dataset)
            except json.JSONDecodeError:
                return self.training_dataset
        else:
            data = self.training_dataset

        examples = data.get('examples', [])
        return json.dumps(examples, indent=2)

@singleton
class AGenaiManager:
    def __init__(self):
        self.cache_manager = ACacheManager()
        api_key = self.cache_manager.get_api_key()
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
            
        self.client = genai.Client()
        self.training_datasets = self.cache_manager.load_training_datasets()
        
    def list_tunings(self):
        wrapped_tunings = []

        try:
            tunings = list(self.client.tunings.list())
            for tuning in tunings:
                dataset = self.training_datasets.get(tuning.name, "NONE")
                wrapped_tunings.append(TuningWrapper(tuning, dataset))
        except Exception:
            pass
        
        return wrapped_tunings
        
    def get_tuning(self, name):
        tuning = self.client.tunings.get(name=name)
        dataset = self.training_datasets[tuning.name]
        return TuningWrapper(tuning, dataset)
    
    def delete_model(self, model_name):
        self.client.models.delete(model=model_name)
        if model_name in self.training_datasets:
            del self.training_datasets[model_name]
            self.cache_manager.save_training_datasets(self.training_datasets)
        
    def create_tuning(self, base_model, training_dataset, config):
        tuning = self.client.tunings.tune(
            base_model=base_model,
            training_dataset=training_dataset,
            config=config
        )
        
        dataset_json = {
            "examples": [
                {
                    "input": example.text_input,
                    "output": example.output
                }
                for example in training_dataset.examples
            ]
        }

        self.training_datasets[tuning.name] = dataset_json
        self.cache_manager.save_training_datasets(self.training_datasets)
        return TuningWrapper(tuning, dataset_json)
        
    def generate_content(self, model, content):
        return self.client.models.generate_content(
            model=model,
            contents=content
        )

