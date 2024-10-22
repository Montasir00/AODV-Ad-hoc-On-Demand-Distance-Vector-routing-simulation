# AODV-Ad-hoc-On-Demand-Distance-Vector-routing-simulation
A simulation using NetworkX in Python to illustrate the AODV routing algorithm in action.
### **About AODV**

AODV (Ad-hoc On-Demand Distance Vector) is an on-demand routing protocol for mobile ad-hoc networks. It operates dynamically, creating routes only when needed, and is based on the **distance vector algorithm.** When a node wants to send data to another and lacks a route, it initiates a route discovery process by broadcasting a Route Request (RREQ) packet. Nodes forward this request until it reaches the destination or a node with a known route. Once established, routes are maintained, and in case of failures, Route Error (RERR) messages update routing tables. AODV's efficiency lies in its adaptability to dynamic network topologies, minimizing continuous updates and conserving bandwidth.

**1. Overview:**
The simulation project illustrates the Ad-hoc On-Demand Distance Vector (AODV) routing algorithm using **Python, NetworkX,** and **Matplotlib, Tabulate.** This endeavor aimed to provide a practical understanding of AODV's route discovery process in dynamic ad-hoc networks.

**2. AODV Algorithm:**
The core of the simulation lies in the **`aodv`** function, which initiates the AODV route discovery by utilizing the **`route_discovery_aodv`** function. This function employs a breadth-first search mechanism, simulating the broadcast of Route Request (RREQ) packets and ultimately establishing a path from the source to the destination.

**3. Network Topology:**
To mimic a realistic ad hoc network, I generated a connected Watts-Strogatz graph using the `create_connected_graph`** function. Random edges were added in the `simulate_network_topology`** function to capture the dynamic nature of such networks.

**4. Visualization:**
Visualizing the network was achieved through the **`visualize_network`** function, which showcased the network graph with nodes and labels. The AODV route was highlighted in red, offering a clear representation of the route discovery process.

**4. Routing Tables:**

Routing tables are a crucial aspect of AODV. In the simulation, routing tables are initialized and updated dynamically. The the**'initialize_routing_tables`** function creates empty routing tables for each node, and the the**`update_routing_table`**

function modifies these tables during the route discovery process. The **`print_routing_tables`**function provides a detailed view of the routing tables.

**5. Simulation:**
The **`simulate_network_topology`** function created a network graph with a specified number of nodes and introduced randomness by adding edges. The main function then orchestrated the entire simulation, from network creation to AODV routing, routing table updates, and visualization.

**6. Results:**
The program effectively demonstrated the AODV route discovery process in action. It showcased the path from the source to the destination, emphasizing the network topology with the discovered route.
