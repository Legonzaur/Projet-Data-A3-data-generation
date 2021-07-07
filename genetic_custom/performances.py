import numpy  as np
import matplotlib.pyplot as plt
import json
import matplotlib.pyplot as plt

i = 0

with open("DATA/stats_graph_size (1).json", "r") as f:
  data = json.load(f)
  execs = []
  sizes = []
  sizes2 = []
for datapoint in data:
  if i < 70:
    execs.append(float(datapoint["exec_time"]))
    sizes.append(datapoint["iterations"])  
    sizes2.append(datapoint["graph_size"])
    i = i + 1
  
# plotting the points 

# plotting the points 
plt.scatter(sizes2,execs)
  
# naming the x axis
plt.xlabel("Taille du graphe")
# naming the y axis
plt.ylabel("Temps d'exécution(s)")

# giving a title to my graph
plt.title('Data')
  
# function to show the plot
plt.show()