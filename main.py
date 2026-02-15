from Model import BertLinear, predict
from PreprocessText import URLParser
import pandas as pd


df = pd.read_csv("data/test_url.csv")

print(df.columns)

model = BertLinear()
model.load_weight()

parser = URLParser()

links = df['max(page)'][99:100].to_list()
links.append('https://www.gloster.com/en-us/products/collections/kasha/kasha-round-dining-table/sand_matt/natural_teak')
input_texts = parser.parse(links)

for text, link in zip(input_texts, links):
    print(f'{link} found {len(text)} lines')

print(input_texts)

outputs = predict(input_texts, model, True)
for lines, output, link in zip(input_texts, outputs, links):
    print(f"\n{link}")
    for line, label in zip(lines, output):
        if label:
            print(f"{line} = {label}")
    print()
