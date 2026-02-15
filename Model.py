from transformers import AutoModel, AutoTokenizer
import torch.nn as nn
import torch
from typing import List


class BertLinear(nn.Module):
    def __init__(self, bert_path=r'.\local_bert', freez_bert=True):
        super().__init__()
        self.bert = AutoModel.from_pretrained(bert_path)
        self.bert.requires_grad_(not freez_bert)
        self.tokenizer = AutoTokenizer.from_pretrained(bert_path)

        self.head = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(312, 256),
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(256, 2)
        )
        self.eval()

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids, attention_mask)
        cls = output.last_hidden_state[:, 0, :]
        return self.head(cls)

    def load_weight(self, path='furniture_model.pth'):
        self.load_state_dict(torch.load(path, map_location='cpu'))


def predict(texts: List[List[str,]], model, return_proba=False):
    output = []
    for text in texts:
        output.append(predict_one(text, model, return_proba))
    return output

def predict_one(text: List[str,], model, return_proba=False):
    if len(text) == 0:
        return []
    inputs = model.tokenizer(text, padding=True, truncation=True, return_tensors='pt', return_token_type_ids=False)
    output = model(**inputs)
    if return_proba:
        return output.softmax(dim=-1).tolist()
    return output.argmax(dim=-1).tolist()
