from PreprocessText import URLParser
import pandas as pd


df = pd.read_csv("data/train_urs.csv")

train_labels_df = pd.read_csv("data/train_label.csv")
print(train_labels_df.info())
parser = URLParser()
index = train_labels_df["url_id"].max() + 1
while index < len(df):
    print(f"\ncurrent url - {index}")
    choice = int(input("1-continue, 2-check DataFrame, 3-save, 0-finish"))
    match choice:
        case 0:
            train_labels_df.to_csv("data/train_label.csv", index=False)
            break
        case 1:
            print(f"==== URL number - {index} ====")
            print(df.iloc[index, 0])
            labels = parser.parse_one(df.iloc[index, 0])
            print(f"Start choose (total:{len(labels)})\n")

            isAllZeroClass = False
            for i, label in enumerate(labels):
                isFurniture = 0
                if not isAllZeroClass:
                    isFurniture = int(input(f"({i}/{len(labels)})Furniture(1-yes/0-no/999-all-is-0):    {label}"))
                if isFurniture == 999:
                    isAllZeroClass = True
                    isFurniture = 0
                train_labels_df.loc[len(train_labels_df)] = [index, label, isFurniture]
            index += 1
            continue
        case 2:
            print(train_labels_df)
            continue
        case 3:
            train_labels_df.to_csv("data/train_label.csv", index=False)
            continue



