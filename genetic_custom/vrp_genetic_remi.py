from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
client = MongoClient('82.65.170.87',27017)
db = client["DataProject"]
collection_trafic = db['vehicles']
vehicles_stamped = db['vehicles_stamped']


# Execution de la requete en utilisant python et datetime.datetime
# Extraction des dates dinstinctes
dates = list(\
             vehicles_stamped.distinct("date"))
# Initialisation de vehicules_par_minutes
vehicules_par_minutes = dict(\
                             [(date.strftime("%H:%M"), 0) for date in dates]) 

# Parcours de la collection et calcul de la somme du trafic
for trafic in vehicles_stamped.find():
    date = trafic["date"].strftime("%H:%M") 
    vehicules_par_minutes[date] += trafic["nb_vehicules"] 

nb_jours = 5
nb_data_points = nb_jours*len(vehicles_stamped.distinct("num_arete"))
trafics = \
    [vehicules_par_minutes[date]/nb_data_points for date in vehicules_par_minutes.keys()]
print("Traffic pour les 4 premières minutes :", trafics[0:4])

# Les dates du matin
xs = \
    pd.date_range("2020-01-01 07:01", "2020-01-01 09:00", freq = "min").to_pydatetime().tolist() 
# Le données de trafic au matin
ys = \
    trafics[:120] 
fig, axes = plt.subplots(2)
# Traitements sur l'affichage au matin
axes[0].xaxis.set_major_locator(mdates.HourLocator(interval = 1))
axes[0].xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15))
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes[0].set(ylabel="trafic")
axes[0].plot(xs,ys,"o")

# Les dates du soir
xs = \
    pd.date_range("2020-01-01 17:01", "2020-01-01 19:00", freq = "min").to_pydatetime().tolist()# Les données de trafic au soir
ys = \
    trafics[120:] 
# Traitements sur l'affichage au soir
axes[1].xaxis.set_major_locator(mdates.HourLocator(interval = 1)) 
axes[1].xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15)) 
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 
axes[1].set(xlabel="temps", ylabel="trafic") 
axes[1].plot(xs,ys,"o") 

fig.suptitle('Trafic moyen au matin et au soir.')
plt.show()



vehicules_par_arete = list(db.vehicles_stamped.aggregate([
    {"$project":{"num_arete":1, "heures":{"$hour":"$date"}, "nb_vehicules":1}}, 
    {"$match":{"heures":{"$lte":9, "$gte":7}}}, 
    {"$group":{"_id":"$num_arete",  
               "nb_vehicules":{"$avg":"$nb_vehicules"}}},
    {"$sort":{"nb_vehicules":-1}}
]))
print("Le résultat retourné par la requete (max,median,min):")
print(vehicules_par_arete[0], vehicules_par_arete[249], vehicules_par_arete[-1])



def generate_gene(vrp):
    a = list(range(1, len(vrp)))
    random.shuffle(a)
    return a
