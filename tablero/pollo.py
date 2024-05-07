import matplotlib.pyplot as plt
import networkx as nx

def draw_neural_graph(data):
    G = nx.DiGraph()
    pos = {}
    layers = list(data.keys())
    
    for i, layer in enumerate(layers):
        states = list(data[layer].keys())
        for state in states:
            G.add_node(f"{layer}-{state}", label=str(state))
            pos[f"{layer}-{state}"] = (i, -state)  # (x,y) coordenadas
            
            next_layer = layer + 1
            if next_layer in data:  # Verificar si existe la siguiente capa
                for connection in data[layer][state]:
                    if connection in data[next_layer]:  # Verificar si el estado de conexión existe en la siguiente capa
                        G.add_edge(f"{layer}-{state}", f"{next_layer}-{connection}")

    labels = {node: G.nodes[node]['label'] for node in G.nodes()}

    # Dibuja el grafo
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, labels=labels, node_size=2000, node_color="skyblue", font_size=10, width=2, edge_color="gray")
    plt.title("Grafo tipo Red Neuronal")
    plt.show()

# Diccionario
data = {
    1: {1: {2, 5}},
    2: {2: {1, 3, 6}, 5: {1, 6, 9}},
    3: {1: {2, 5}, 3: {2, 4, 7}, 6: {2, 10, 5, 7}, 9: {10, 5, 13}},
    4: {2: {5, 7}, 5: {2, 10}, 4: {7}, 7: {2, 10, 4, 12}, 10: {5, 7, 13, 15}, 13: {10}},
    5: {5: {1, 6, 9}, 7: {8, 3, 11, 6}, 2: {1, 3, 6}, 10: {9, 11, 6, 14}, 4: {8, 3}, 12: {8, 16, 11}, 13: {9, 14}, 15: {16, 11, 14}}
}

# Dibuja el grafo
draw_neural_graph(data)
