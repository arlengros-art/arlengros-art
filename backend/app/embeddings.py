from functools import lru_cache
from typing import List

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


@lru_cache()
def _load_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

def image_embedding(path: str) -> List[float]:
    model, processor = _load_model()
    image = Image.open(path)
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)
    return embedding[0].cpu().tolist()

def text_embedding(text: str) -> List[float]:
    model, processor = _load_model()
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding = model.get_text_features(**inputs)
    embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)
    return embedding[0].cpu().tolist()
