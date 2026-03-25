import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class InformationFusionEngine:
    def __init__(self):
        self.knowledge_graph = nx.DiGraph()
        self.data_sources = {}

    def register_data_source(self, name, data):
        self.data_sources[name] = data
        self.fuse_information()

    def fuse_information(self):
        for name, data in self.data_sources.items():
            for entity, attributes in data.items():
                if entity not in self.knowledge_graph:
                    self.knowledge_graph.add_node(entity, **attributes)
                else:
                    for attr, value in attributes.items():
                        self.knowledge_graph.nodes[entity][attr] = value

    def visualize_cartography(self, output_path):
        pos = nx.spring_layout(self.knowledge_graph)
        plt.figure(figsize=(12, 12))
        nx.draw(self.knowledge_graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10)
        plt.savefig(output_path)

if __name__ == '__main__':
    engine = InformationFusionEngine()
    engine.register_data_source('wikipedia', {
        'Albert Einstein': {'occupation': 'physicist', 'nationality': 'German'},
        'Nikola Tesla': {'occupation': 'inventor', 'nationality': 'Serbian'}
    })
    engine.register_data_source('wikidata', {
        'Albert Einstein': {'birth_year': 1879, 'death_year': 1955},
        'Nikola Tesla': {'birth_year': 1856, 'death_year': 1943}
    })
    engine.visualize_cartography('knowledge_graph.png')
