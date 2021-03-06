from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.api as sms

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
client = MongoClient('82.65.170.87',27017)
db = client["DataProject"]
collection_trafic = db['vehicles']
vehicles_stamped = db['vehicles_stamped']


vehicules_par_arete = list(db.vehicles_stamped.aggregate([
    {"$project":{"num_arete":1, "heures":{"$hour":"$date"}, "nb_vehicules":1}}, #SOLUTION
    {"$match":{"heures":{"$lte":9, "$gte":7}}}, #SOLUTION
    {"$group":{"_id":"$num_arete",  #SOLUTION
               "nb_vehicules":{"$avg":"$nb_vehicules"}}}, #SOLUTION
    {"$sort":{"nb_vehicules":-1}} #SOLUTION
]))
print("Le résultat retourné par la requete (max,median,min):")
print(vehicules_par_arete[0], vehicules_par_arete[249], vehicules_par_arete[-1])

arete_mediane = vehicules_par_arete[249]["_id"]
arete_max, arete_min = vehicules_par_arete[0]["_id"], vehicules_par_arete[-1]["_id"]
vehicules_arete_mediane = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_mediane}}}, #SOLUTION
    {"$project":{"temps":{"heures":{"$hour":"$date"}, #SOLUTION
                          "minutes":{"$minute":"$date"}}, #SOLUTION
                "nb_vehicules":1}}, #SOLUTION
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}}, #SOLUTION
     {"$sort":{"temps":1}}]) #SOLUTION
vehicules_arete_max = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_max}}}, #SOLUTION
    {"$project":{"temps":{"heures":{"$hour":"$date"}, #SOLUTION
                          "minutes":{"$minute":"$date"}}, #SOLUTION
                "nb_vehicules":1}}, #SOLUTION
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}}, #SOLUTION
     {"$sort":{"temps":1}}]) #SOLUTION
vehicules_arete_min = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_min}}}, #SOLUTION
    {"$project":{"temps":{"heures":{"$hour":"$date"}, #SOLUTION 
                          "minutes":{"$minute":"$date"}}, #SOLUTION
                "nb_vehicules":1}}, #SOLUTION
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}}, #SOLUTION
     {"$sort":{"temps":1}}]) #SOLUTION

# Traitements relatif a l'arete la plus congestionnée
# Extraction des dates
xs = \
    pd.date_range("2020-01-01 07:01", "2020-01-01 09:00", freq = "min").to_pydatetime().tolist()#SOLUTION
# Duplication des dates sur les 5 jours
xs = \
    [e for sub in zip(xs, xs, xs, xs, xs) for e in sub] #SOLUTION 
# Données de trafic pour l'arete la plus congestionnée
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_max] #SOLUTION
# Données matinales
ys = \
    trafics[:600] #SOLUTION
# Affichage relatif a l'arete la plus congestionnée
fig, ax = plt.subplots() #SOLUTION
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1)) #SOLUTION
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15)) #SOLUTION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) #SOLUTION
ax.set(title="Trafic de l'arete la plus congestionnée.", xlabel="temps", ylabel="trafic") #SOLUTION
ax.plot(xs,ys,"o") #SOLUTION

# Traitements relatif a l'arete médiane
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_mediane] #SOLUTION
ys = \
    trafics[:600] #SOLUTION
# Affichage relatif a l'arete médiane
fig, ax = plt.subplots() #SOLUTION
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1)) #SOLUTION
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15)) #SOLUTION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) #SOLUTION
ax.set(title="Trafic de l'arete la moins congestionnée.", xlabel="temps", ylabel="trafic") #SOLUTION
ax.plot(xs,ys,"o") #SOLUTION

# Traitements relatif a l'arete la moins congestionnée
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_min] #SOLUTION
ys = \
    trafics[:600] #SOLUTION
# Affichage relatif a l'arete la moins congestionnée
fig, ax = plt.subplots() #SOLUTION
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1)) #SOLUTION
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15)) #SOLUTION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) #SOLUTION
ax.set(title="Trafic de l'arete la moins congestionnée.", xlabel="temps", ylabel="trafic") #SOLUTION
ax.plot(xs,ys,"o") #SOLUTION

plt.show()


def generate_gene(vrp):
    a = list(range(1, len(vrp)))
    random.shuffle(a)
    return a
