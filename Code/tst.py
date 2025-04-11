import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import powerlaw

DGM_G = nx.dorogovtsev_goltsev_mendes_graph(10)

print(f"Number of nodes: {DGM_G.number_of_nodes()}")
print(f"Number of edges: {DGM_G.number_of_edges()}")

degrees = [d for _, d in DGM_G.degree()]
unique, counts = np.unique(degrees, return_counts=True)

# Fit the degree distribution to a power-law
fit = powerlaw.Fit(degrees, xmin=9)
alpha = fit.power_law.alpha
xmin = fit.power_law.xmin

print(f"Power-law alpha: {alpha}")
print(f"Power-law xmin: {xmin}")

plt.figure(figsize=(8, 6))
plt.loglog(unique, counts, 'bo', markersize=4, label="Raw Degree Distribution")
plt.xlabel("Degree (k)")
plt.ylabel("P(k)")
plt.title("Degree Distribution of DGM Graph")
plt.legend()
plt.show()