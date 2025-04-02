import networkx as nx
import pickle
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def generate_dgm_graph(target_edges):
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    
    while G.number_of_edges() < target_edges:
        u, v = random.choice(list(G.edges()))
        new_node = G.number_of_nodes()
        G.add_edges_from([(new_node, u), (new_node, v)])
    
    return G

random.seed(42)

target_edges = 30000
DGM_G = generate_dgm_graph(target_edges)

filename = f"dgm_graph_{target_edges}_edges.gpickle"
with open(filename, "wb") as f:
    pickle.dump(DGM_G, f)

print(f"Number of nodes: {DGM_G.number_of_nodes()}")
print(f"Number of edges: {DGM_G.number_of_edges()}")

degrees = [d for _, d in DGM_G.degree()]
unique, counts = np.unique(degrees, return_counts=True)

plt.figure(figsize=(8, 6))
plt.loglog(unique, counts, 'bo', markersize=4, label="DGM Model")
plt.xlabel("Degree (k)")
plt.ylabel("P(k)")
plt.title("Degree Distribution of DGM Graph")
plt.legend()
plt.show()

log_degrees = np.log10(unique)
log_counts = np.log10(counts)
slope, intercept, r_value, p_value, std_err = linregress(log_degrees, log_counts)

print(f"Fitted power-law exponent (slope): {abs(slope):.2f}")

def log_bin_data(raw_degrees, bin_base=1.1):
    bins = [bin_base ** i for i in range(int(np.log(max(raw_degrees)) / np.log(bin_base)) + 1)]
    binned_degrees = []
    binned_counts = []
    for i in range(len(bins) - 1):
        bin_min, bin_max = bins[i], bins[i + 1]
        bin_mask = (raw_degrees >= bin_min) & (raw_degrees < bin_max)
        if np.any(bin_mask):
            binned_degrees.append(np.mean(raw_degrees[bin_mask]))
            binned_counts.append(np.sum(bin_mask))
    return np.array(binned_degrees), np.array(binned_counts)

raw_degrees = np.array([d for _, d in DGM_G.degree()])
binned_degrees, binned_counts = log_bin_data(raw_degrees)

plt.figure(figsize=(8, 6))
plt.loglog(binned_degrees, binned_counts, 'ro', markersize=4, label="Binned DGM Model")
plt.xlabel("Degree (k)")
plt.ylabel("P(k)")
plt.title("Log-Log Binned Degree Distribution of DGM Graph")
plt.legend()
plt.show()

log_binned_degrees = np.log10(binned_degrees)
log_binned_counts = np.log10(binned_counts)
slope_binned, intercept_binned, r_value_binned, p_value_binned, std_err_binned = linregress(log_binned_degrees, log_binned_counts)

print(f"Fitted power-law exponent (slope) for binned data: {abs(slope_binned):.2f}")