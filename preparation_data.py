import pandas as pd


df = pd.read_csv("data/train_label.csv")
print(df.describe())
print(df.info())
print(df["label"].nunique())

# df = pd.read_csv("data/URL_list.csv")
# print(df.head(3))
# print(df.info())
# print(df.describe())
# df = df.sample(frac=1, random_state=999).reset_index(drop=True)
# print(df.head(3))
# df.to_csv("data/shacked_URLs.csv")
# train_df = df[:100]
# test_df = df[100:]
# test_df.to_csv("data/test_url.csv", index=False)
# train_df.to_csv("data/train_urs.csv", index=False)
#
# print(test_df.iloc[0].iloc[0])


# Testimonials поменять на 00000
# чекнуть с s на конце