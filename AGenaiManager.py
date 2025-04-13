from google import genai
from google.genai import types
from py_singleton import singleton
import json
import os
import pathlib
from dataclasses import dataclass
from typing import Any

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
    CACHE_DIR = pathlib.Path.home() / '.cache' / 'easy_fine_tuner'
    DATASETS_CACHE = CACHE_DIR / 'training_datasets.json'

    def __init__(self):
        self.client = genai.Client()
        self.training_datasets = {}
        self._load_cache()
        
    def _load_cache(self):
        try:
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            if self.DATASETS_CACHE.exists():
                with open(self.DATASETS_CACHE, 'r') as f:
                    self.training_datasets = json.load(f)
        except Exception:
            self.training_datasets = {}
            
    def _save_cache(self):
        try:
            with open(self.DATASETS_CACHE, 'w') as f:
                json.dump(self.training_datasets, f)
        except Exception:
            pass
        
    def list_tunings(self):
        tunings = list(self.client.tunings.list())
        wrapped_tunings = []
        for tuning in tunings:
            dataset = self.training_datasets.get(tuning.name, "NONE")
            wrapped_tunings.append(TuningWrapper(tuning, dataset))
        return wrapped_tunings
        
    def get_tuning(self, name):
        tuning = self.client.tunings.get(name=name)
        dataset = self.training_datasets[tuning.name]
        return TuningWrapper(tuning, dataset)
    
    def delete_model(self, model_name):
        self.client.models.delete(model=model_name)
        if model_name in self.training_datasets:
            del self.training_datasets[model_name]
            self._save_cache()
        
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
        self._save_cache()
        return TuningWrapper(tuning, training_dataset)
        
    def generate_content(self, model, content):
        return self.client.models.generate_content(
            model=model,
            contents=content
        )
