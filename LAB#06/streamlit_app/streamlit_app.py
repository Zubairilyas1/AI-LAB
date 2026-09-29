import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from searchAlgos import a_star, gbfs, hospital_graph, locations

# Set Page Config
st.set_page_config(page_title="Informed Search Visualizer", layout="wide")

st.title("Interactive Search Visualization")
st.write(
    "Select a **start node**, a **goal node** and a **search algorithm** "
    "(Greedy Best-First Search or A*), then run the search to see the solution "
    "path highlighted on the hospital network."
)

# Define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# Selectboxes for start and goal nodes
start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))

# Selectbox for the search algorithm
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

path = None
cost = 0.0

if st.button("Run Search"):
    if algorithm == "GBFS":
        path, cost, expanded = gbfs(start, goal, hospital_graph)
    else:
        path, cost, expanded = a_star(start, goal, hospital_graph)

    if path is None:
        st.error(
            f"No path found from {start} to {goal} with {algorithm}. "
            "Check the graph connections."
        )
    else:
        # Display result
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Nodes Expanded:** {len(expanded)}")

    # Visualize NetworkX graph
    G = nx.DiGraph()
    for node, neighbors in hospital_graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = locations
    fig, ax = plt.subplots(figsize=(10, 6))

    nx.draw_networkx_nodes(G, pos, node_color="#ffd9a0", node_size=1200, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)
    nx.draw_networkx_edges(G, pos, arrows=True, edge_color="#888888", ax=ax)
    nx.draw_networkx_edge_labels(
        G, pos, nx.get_edge_attributes(G, "weight"), font_size=8, ax=ax
    )

    if path is not None:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=3, ax=ax
        )

    ax.set_title(f"{algorithm} Solution Path")
    ax.axis("off")
    st.pyplot(fig)
