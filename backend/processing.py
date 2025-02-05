import json
import pyvis as pv
from pyvis.network import Network
import pandas as pd


df = pd.read_excel("test_uploads/dummy_narvis_graph.xlsx")
print(df.head())

net = Network(height="1800px", width="100%", notebook=True)

for _, row in df.iterrows():
    net.add_node(row['id'], label=row['name'])

for i, row_1 in df.iterrows():
    for j, row_2 in df.iterrows():
        if i < j:
            if row_1['category'] == row_2['category']:
                net.add_edge(row_1['id'], row_2['id'], color="green")
            if row_1['interaction_type'] == row_2['interaction_type']:
                net.add_edge(row_1['id'], row_2['id'], color="red")


net.force_atlas_2based()
net.show("interactive_network.html")