import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# Load the dataset (assuming "maths dataset.csv" is in the working directory)
df = pd.read_csv("maths dataset.csv")

# Assume the congestion state column is located in the 5th column (index 4)
congestion_states = df.iloc[:, 4]

# Step 1: Create Transition Matrix
transition_matrix = {}
for (current_state, next_state) in zip(congestion_states[:-1], congestion_states[1:]):
    if current_state not in transition_matrix:
        transition_matrix[current_state] = {}
    if next_state not in transition_matrix[current_state]:
        transition_matrix[current_state][next_state] = 0
    transition_matrix[current_state][next_state] += 1

# Normalize the transition matrix
for current_state, transitions in transition_matrix.items():
    total = sum(transitions.values())
    for next_state in transitions:
        transitions[next_state] /= total

# Step 2: Visualize the Transition Matrix as a Heatmap
transition_df = pd.DataFrame(transition_matrix).fillna(0)

plt.figure(figsize=(8, 6))
sns.heatmap(transition_df, annot=True, cmap="Blues", fmt=".2f")
plt.title("Transition Probability Matrix (Traffic Congestion States)", fontsize=14)
plt.xlabel("Next State")
plt.ylabel("Current State")
plt.tight_layout()
plt.show()

# Step 3: Visualize Markov Chain as a Directed Graph
G = nx.DiGraph()

# Add edges with weights from the transition matrix
for from_state, transitions in transition_matrix.items():
    for to_state, prob in transitions.items():
        G.add_edge(from_state, to_state, weight=prob)

# Draw the graph
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)  # consistent layout
edges = G.edges(data=True)

nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
nx.draw_networkx_labels(G, pos, font_size=12)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, width=2)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in edges},
    font_color='gray'
)

plt.title("Markov Chain: State Transition Diagram", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()

# Step 4: Frequency of Congestion States (2020 vs 2023)
state_counts = congestion_states.value_counts()
state_mapping = {state: idx for idx, state in enumerate(state_counts.index)}
numerical_states = congestion_states.map(state_mapping)

plt.figure(figsize=(8, 6))
sns.barplot(x=state_counts.index, y=state_counts.values, color='skyblue', edgecolor='black')
plt.title("Frequency of Congestion States (2020 vs 2023)", fontsize=14)
plt.xlabel("Congestion State")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 5: Predict Future States using Markov Chain
def predict_next_state(current_state):
    if current_state not in transition_matrix:
        return random.choice(list(transition_matrix.keys()))
    next_states = list(transition_matrix[current_state].keys())
    probabilities = list(transition_matrix[current_state].values())
    return np.random.choice(next_states, p=probabilities)

def predict_future_states(start_state, steps=5):
    future_states = [start_state]
    current_state = start_state
    for _ in range(steps):
        next_state = predict_next_state(current_state)
        future_states.append(next_state)
        current_state = next_state
    return future_states

# Example prediction of future states
current_state = random.choice(congestion_states.tolist())
print(f"\nCurrent State: {current_state}")
future_states = predict_future_states(current_state, steps=5)
print(f"Predicted Future States: {future_states}")
