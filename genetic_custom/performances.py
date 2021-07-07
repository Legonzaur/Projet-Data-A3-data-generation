import numpy  as np
import matplotlib.pyplot as plt
import json
import matplotlib.pyplot as plt



with open("DATA/stats_iterations (1).json", "r") as f:
  data = json.load(f)
  execs = []
  sizes = []
  sizes2 = []
for datapoint in data:
  execs.append(float(datapoint["exec_time"]))
  sizes.append(datapoint["iterations"])  
  sizes2.append(datapoint["path_time"])  
  
# plotting the points 

# plotting the points 
plt.scatter(sizes,sizes2)
  
# naming the x axis
plt.xlabel("Nombre d'itérations")
# naming the y axis
plt.ylabel("Longueur du meilleur chemin trouvé")

# giving a title to my graph
plt.title('Data')
  
# function to show the plot
plt.show()