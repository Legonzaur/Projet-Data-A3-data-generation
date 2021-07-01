from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.api as sms
from scipy import stats
import pylab as py
from statsmodels.graphics import tsaplots
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
client = MongoClient('82.65.170.87',27017)
db = client["DataProject"]
collection_trafic = db['vehicles']
vehicles_stamped = db['vehicles_stamped']

vehicules_par_arete = list(db.vehicles_stamped.aggregate([
    {"$project":{"num_arete":1, "heures":{"$hour":"$date"}, "nb_vehicules":1}},
    {"$match":{"heures":{"$lte":9, "$gte":7}}},
    {"$group":{"_id":"$num_arete", 
               "nb_vehicules":{"$avg":"$nb_vehicules"}}},
    {"$sort":{"nb_vehicules":-1}}
]))

arete_mediane = vehicules_par_arete[249]["_id"]
arete_max, arete_min = vehicules_par_arete[0]["_id"], vehicules_par_arete[-1]["_id"]
vehicules_arete_mediane = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_mediane}}},
    {"$project":{"temps":{"heures":{"$hour":"$date"},
                          "minutes":{"$minute":"$date"}},
                "nb_vehicules":1}},
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}},
     {"$sort":{"temps":1}}])
vehicules_arete_max = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_max}}},
    {"$project":{"temps":{"heures":{"$hour":"$date"},
                          "minutes":{"$minute":"$date"}},
                "nb_vehicules":1}},
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}},
     {"$sort":{"temps":1}}])
vehicules_arete_min = db.vehicles_stamped.aggregate([
    {"$match":{"num_arete":{"$eq":arete_min}}},
    {"$project":{"temps":{"heures":{"$hour":"$date"}, 
                          "minutes":{"$minute":"$date"}},
                "nb_vehicules":1}},
    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}},
     {"$sort":{"temps":1}}])

# Traitements relatif a l'arete la plus congestionnée
# Extraction des dates
xs = \
    pd.date_range("2020-01-01 07:01", "2020-01-01 09:00", freq = "min").to_pydatetime().tolist(
# Duplication des dates sur les 5 jours
xs = \
    [e for sub in zip(xs, xs, xs, xs, xs) for e in sub] 
# Données de trafic pour l'arete la plus congestionnée
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_max]
# Données matinales
ys = \
    trafics[:600]
# Affichage relatif a l'arete la plus congestionnée
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set(title="Trafic de l'arete la plus congestionnée.", xlabel="temps", ylabel="trafic")
ax.plot(xs,ys,"o")

# Traitements relatif a l'arete médiane
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_mediane]
ys = \
    trafics[:600]
# Affichage relatif a l'arete médiane
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set(title="Trafic de l'arete la moins congestionnée.", xlabel="temps", ylabel="trafic")
ax.plot(xs,ys,"o")

# Traitements relatif a l'arete la moins congestionnée
trafics = \
    [trafic["nb_vehicules"] for trafic in vehicules_arete_min]
ys = \
    trafics[:600]
# Affichage relatif a l'arete la moins congestionnée
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 15))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set(title="Trafic de l'arete la moins congestionnée.", xlabel="temps", ylabel="trafic")
ax.plot(xs,ys,"o")

plt.show()


# En premier lieu le modèle devra etre entrainé avant de l'évaluer
# Les données au format date sont converties en minutes
X = [(date.hour-7)*60+date.minute for date in xs]
# Ajout de la colonne correspondant à la constante
X = \
    np.append(arr = np.ones((len(X), 1)).astype(int), values = np.array([X]).T, axis = 1)
# Entrainement du modèle
regressor_OLS = \
    sm.OLS(endog = ys, exog = X).fit()
# Predictions avec le modèle
y_pred = \
    regressor_OLS.params[0]+regressor_OLS.params[1]*X[:,1]

# Affichage des résidus
fig, ax = plt.subplots()
ax.scatter(X[:,1], #Les résidus
           regressor_OLS.resid, alpha=0.3)
ax.set(title="Résidus de la régression linéaire.", xlabel="Temps", ylabel="Residus")
plt.show()

print("Test d'homogeneite (H0 : La variance des residus est homogène)")
print('p valeur de Goldfeld–Quandt test est: ',
      sms.het_goldfeldquandt(ys, regressor_OLS.model.exog)[1])
print('p valeur of Breusch–Pagan test est: ', 
        sms.het_breuschpagan(regressor_OLS.resid,
        regressor_OLS.model.exog)[1])
print('p valeur de White test est: ', 
      sms.het_white(regressor_OLS.resid**2, 
      regressor_OLS.model.exog)[1])

sm.qqplot(regressor_OLS.resid_pearson, line ='45')
py.show()




# Affichage de la fonction d'autocorrelation
fig = tsaplots.plot_acf(regressor_OLS.resid, lags=40)
plt.show()

print("Resultat du test d'auto-correlation (H0 : pas d'autocorrelation)")
print(sm.stats.acorr_ljungbox(regressor_OLS.resid, return_df=True))

fig, ax = plt.subplots()
# Affichage du nuage de point
ax.scatter(X[:,1], ys, alpha=0.3)
ax.set(title="Régression linéaire l'arete la moins congéstionnée.", xlabel="Temps", ylabel="Trafic")
# Affichage du nuage de point
ax.plot(X[:,1], y_pred, linewidth=3)
plt.show()


print("Evaluation de la regression lineaire en utilisant la classe statsmodels :")
print("Les parametres de la regression sont ", 
      regressor_OLS.params)
print("La valeur du R2 est ", 
      regressor_OLS.rsquared)
print("Les test de Fischer sur la qualite globale de la regression ")
print("f_value ", 
      regressor_OLS.fvalue,
      " f_pvalue",
      regressor_OLS.f_pvalue)
print("Le resultat des t-tests ")
print("p valeurs ", 
      regressor_OLS.pvalues, 
      " t valeurs ", 
      regressor_OLS.tvalues)

print("\nEvaluation de la regression en utilisant les formules : ")
# Calcul manuel des paramètres de la regression
slope = \
    np.sum(np.multiply(X[:,1] - np.mean(X[:,1]), 
                           ys - np.mean(ys)))/np.sum((X[:,1] - np.mean(X[:,1]))**2)
intercept = \
    np.mean(ys)-slope*np.mean(X[:,1])
print("Terme constant et pente ", intercept, slope)

# Calcul de la statistique de fischer pour evaluer la regression
n_obs, k = len(X[:,1]), 1
# somme des ecarts expliques
sce = \
    np.sum((y_pred-np.mean(ys))**2)
# sommes des ecarts totaux
sct = \
    np.sum((ys-np.mean(ys))**2)
# somme des ecarts residuels
scr = \
    sct-sce
F = \
    (sce/k)/(scr/(n_obs-k-1))
print("Le coefficient de R2 ", sce/sct)
print("Valeur du F-test ", F)

se_x = np.sum((X[:,1] - np.mean(X[:,1]))**2)
temp = (1/n_obs + np.mean(X[:,1])**2 / se_x)
ecart_type0 = np.sqrt((scr/(n_obs-k-1)) * temp)
t0 = \
    intercept/ecart_type0
print("Valeur de t0 ", t0)

ecart_type1 = np.sqrt(
    (scr/(n_obs-k-1)) / se_x)
t1 = \
    slope/ecart_type1
print("Valeur du t1 ", t1)



# Nombre d'aretes dans la ville
nb_aretes = 500
# Nombre de modèles
nb_regression_models = 250
# Nombre d'aretes pris en charge par chaque modèle
nb_aretes_per_model = nb_aretes/ nb_regression_models
# Les modèles de regression
regression_models = [None]*nb_regression_models
for i in range(nb_regression_models):
    #print(i)
    num_premiere_arete, num_derniere_arete = i*nb_aretes_per_model, (i+1)*nb_aretes_per_model-1 
    # Lecture des données du trafic matinales sur les aretes dans l'intervalle
    # [num_premiere_arete, num_derniere_arete]
    X = list(db.vehicules_stamped.aggregate([
        {"$match":{"num_arete":{"$gte":num_premiere_arete, "$lte":num_derniere_arete}}},
        {"$project":{"temps":{"heures":{"$hour":"$date"}, 
                              "minutes":{"$minute":"$date"}},
                    "nb_vehicules":1,"num_arete":1}},
        {"$match":{"temps.heures":{"$lte":9, "$gte":7}}}]))
    # Conversion en minutes des données de trafic
    X = [[trafic["num_arete"],
                60*(trafic["temps"]["heures"]-7)+trafic["temps"]["minutes"], 
                trafic["nb_vehicules"]] for trafic in X]
    # Transformation de la colone "num_arete" en colonne binaire associée à chaque arete
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], 
                           remainder="passthrough")
    X = ct.fit_transform(X)
    if isinstance(X, np.ndarray) is False:
        X = X.toarray()
    else :
        X = np.array(X, dtype = int)
   # Vecteur du trafic réel par arete et par minute
    ys = X[:,-1]
    # Matrice contenant l'échantillon des données, les colonnes sont la minute et l'arete
    X = X[:, 1:-1]
    
    # Ajout de la constante dans la matrice
    X = \
        np.append(arr = np.ones((X.shape[0], 1)), values = X, axis = 1)
    # Entrainement du modèle
    regression_models[i] = \
        sm.OLS(endog = ys, exog = X).fit()
# seuil des tests
seuil = 0.05
# nombre de variables par modèle
nb_regressors = int(nb_aretes_per_model+1)
# Compteur du nombre de t-tests concluant de l'effet des variables par modèle
cpts_ts = [[0]*nb_regressors for i in range(nb_regression_models)]
# Compteur du nombre de F-tests conclusifs sur les modèles
cpts_f = [0]*nb_regression_models
for i in range(nb_regression_models):
    # Les p-valeurs des t-tests
    pvalues_t_test = \
        regression_models[i].pvalues
    # Les p-valeurs des F-tests
    pvalue_f_test = \
        regression_models[i].f_pvalue
    for j in range(len(pvalues_t_test)):
        if pvalues_t_test[j] < seuil:
            cpts_ts[i][j] += 1
            #print("p-valeur associee a la variable "+str(j)+" est "+str(pvalues_t_test [j]))
    if pvalue_f_test < seuil:
        cpts_f[i] += 1
        #print("p-valeur du f-test est "+str(pvalue_f_test))
print("Proportion de succes associee aux t-tests ", 
      [sum(
              [cpts_ts[i][j] for i in range(nb_regression_models)]
          )/nb_regression_models for j in range(nb_regressors)])
print("Proportion de succes associee aux f-tests ", sum(cpts_f)/nb_regression_models)
print("Tous les tests sont completees.")
