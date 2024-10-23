import networkx as nx
import matplotlib.pyplot as plt
import random
from tabulate import tabulate

def create_connected_graph(num_nodes, probability):
    G = nx.erdos_renyi_graph(num_nodes, probability)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(num_nodes, probability)
    return G

def initialize_routing_tables(graph):
    return {node: {} for node in graph.nodes()}

def generate_random_routing_tables(graph, routing_tables):
    for node in graph.nodes():
        for dest in graph.nodes() - {node}:
            neighbors = list(graph.neighbors(node))
            next_hop = random.choice(neighbors)
            hop_count = nx.shortest_path_length(graph, source=node, target=dest)
            distance = nx.shortest_path_length(graph, source=node, target=dest, weight='weight')
            routing_tables[node][dest] = {'next_hop': next_hop, 'hop_count': hop_count, 'distance': distance}

def simulate_node_failure(graph, node_to_fail):
    graph.remove_node(node_to_fail)

def update_routing_table(graph, routing_tables, current_node, next_node, path, reverse=False):
    destination = path[0] if reverse else path[-1]
    hop_count = len(path) if reverse else len(path) + 1
    distance = nx.shortest_path_length(graph, source=current_node, target=destination, weight='weight')

    if destination not in routing_tables[current_node] or routing_tables[current_node][destination]['hop_count'] > hop_count:
        routing_tables[current_node][destination] = {'next_hop': next_node, 'hop_count': hop_count, 'distance': distance}

def route_discovery_aodv(graph, source, destination, routing_tables):
    if source not in graph.nodes() or destination not in graph.nodes():
        raise ValueError("Source or destination node is not in the graph.")

    visited, queue = set(), [(source, [source])]

    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            neighbors = list(graph.neighbors(node))
            visited.add(node)

            for neighbor in neighbors:
                if node != source:
                    update_routing_table(graph, routing_tables, node, path[-2], path, reverse=True)
                    print(f"Broadcasting RREQ from {node} to {neighbor}")
                if neighbor == destination:
                    update_routing_table(graph, routing_tables, neighbor, node, path + [neighbor], reverse=True)
                    return path + [neighbor]  # Return the full path
                else:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    if neighbor not in visited:
                        print(f"Broadcasting RREQ from {node} to {neighbor}")

    # If the destination node is not reachable, return an empty list
    return []

def update_routing_table_on_failure(graph, routing_tables, node_to_fail):
    for source_node, dest_node in [(s, d) for s in routing_tables for d in routing_tables[s] if routing_tables[s][d]['next_hop'] == node_to_fail]:
        try:
            if dest_node != node_to_fail:
                rreq_path = route_discovery_aodv(graph, source_node, dest_node, routing_tables)
                if rreq_path:  # Only update the routing table if a new path is found
                    print(f"Updated route after failure: {rreq_path}")
        except Exception as e:
            print(f"Failed to update route after failure: {e}")

def aodv(graph, source, destination, routing_tables):
    print("Initiating AODV Route Discovery...")
    try:
        rreq_path = route_discovery_aodv(graph, source, destination, routing_tables)
        if rreq_path:
            print(f"AODV Route found: {rreq_path}")
            return rreq_path
        else:
            print("AODV Route not found")
            return []
    except Exception as e:
        print(f"AODV Route Discovery failed: {e}")
        return []

def visualize_network(graph, path):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, edge_color="gray", width=1.0, alpha=0.7)
    edges = [(path[i], path[i+1]) for i in range(len(path)-1)] if path else []
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color="red", width=2)
    plt.show()

def print_routing_tables(routing_tables):
    print("\nRouting Tables:")
    for node, routes in routing_tables.items():
        if routes:
            print(f"Node {node}:")
            table_data = [(dest, info['next_hop'], info['hop_count'], info['distance']) for dest, info in routes.items()]
            headers = ['Destination', 'Next Hop', 'Hop Count', 'Distance']
            print(tabulate(table_data, headers=headers, tablefmt='fancy_grid'))

# Create a connected graph with 10 nodes and a connection probability of 0.3
graph = create_connected_graph(10, 0.3)

# Initialize empty routing tables
routing_tables = initialize_routing_tables(graph)

# Generate random routing tables
generate_random_routing_tables(graph, routing_tables)

# Print the initial routing tables
print_routing_tables(routing_tables)

# Run the AODV protocol for source node 0 and destination node 8
source = 0
destination = 8
path = aodv(graph, source, destination, routing_tables)

# Visualize the network and the discovered path
visualize_network(graph, path)