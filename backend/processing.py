import pandas as pd

# upload > checked and processed > stored in redis db

df = pd.read_excel("test_uploads/dummy_narvis_001.xlsx")
print(df.head())