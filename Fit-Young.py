#!/bin/python
# -*- coding: utf-8 -*-

"""
14 février 2017, version 1.

Ceci est un exemple de fit sur des données expérimentales et de graphique en
python. 

Pour l'éxécuter, simplement exécuter "python Fit-Young.py" dans le dossier 
contenant "Fit-Young.py", "Young_fente3_2260mm_zero"txt. et "maxfit.py".
On peut aussi l'exécuter dans une fenêtre interactive ipython via la commande
"run -i Fit-Young.py" pour ensuite jouer avec les variables et fonctions.

Les résultats du fit s'afficheront dans le terminal ou la console.

Pour bien comprendre comment le programme fonctionnne, je suggère d'exécuter
"Fit-Young.py" dans une fenêtre ipython et d'ensuite accéder à la 
documentation des différentes fonction en tapant leur nom suivi de "?".
e.g., In[1]: fit?


Jean Olivier Simoneau
"""


########################
# IMPORTS / LIBRAIRIES #
########################

from pylab import genfromtxt, linspace, plt, show
from numpy import sinc as np_sinc, pi, cos
from maxfit import fit


###############
# DÉFINITIONS #
###############

data_filename = 'Young_fente3_2260mm_zero.txt'

# On défini la fonction sinc à la manière des mathématiciens
# Le sinc de numpy est défini sin(πx)/(πx) plutôt que sin(x)/x
def sinc(x):
    return np_sinc(x/pi)

def model(x,p):
    a,b,c = p   # Équivalent à: a=p[0]; b=p[1]; c=p[2];
    return a*(sinc(b*x)*cos(c*x))**2   # Le modèle sur lequel on va fitter


#################
# ANALYSE / FIT #
#################

# On charge les données
data = genfromtxt(data_filename).T  # data[i] est la iême colonne

# On fait le fit
param_init = [1, 0.2, 0.7]  # Paramètres initiaux du fit
monFit = fit(data[0], data[1], param_init, model)   # On prépare le fit
monFit.leastsq()    # Effectue le fit et affiche les résultats à l'écran
                    # Les résultats sont accessibles via monFit.para

###########################
# GRAPHIQUE DES RÉSULTATS #
###########################

# On veut afficher le fit avec plus de points que les données
x = linspace(data[0,0], data[0,-1], 1001)

f = plt.figure()    # On créé une figure
ax = f.add_subplot(111) # On créé un axe sur la figure 
                        # 1-1-1 -> #rangées-#colonnes-"index de l'axe créé"
# On afficher les données brutes
ax.plot(data[0], data[1], '.', label=u'Données', markersize=10.) # Gros points
                                #    ^ le u indique unicode (pour l'accent)

# On affiche le fit via monFit qui, après le lissage, s'utilise comme la 
# fonction "model" optimisée via les paramètres de fit. 
ax.plot(x, monFit(x), '-', label='Fit', linewidth=2.) 

# Texte sur axes
ax.set_xlabel(u'Déplacement (u.a.)') # Je ne connais pas les unités
ax.set_ylabel('Amplitude (u.a.)')   # Idem

# On ajuste les limites de la figure
ax.set_xlim(-40,40)
ax.set_ylim(0,11)

# On affiche la légende
ax.legend(loc='upper right', frameon=False)   # On enlève le pourtour

# On force la figure à s'afficher
f.show()

# Commenter les deux prochaines lignes pour ne pas sauvegarder la figure
extension='pdf' # pdf, png, eps, ... au choix!
f.savefig('Fit-Young_Python.{ext}'.format(ext=extension), bbox_inches='tight')
    # bbox_inches='tight' ajuste les marges de la figure automatiquement
    # si on sauve en png, utiliser dpi=200 pour une belle définision


