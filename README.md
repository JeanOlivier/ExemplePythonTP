# Exemple Python TP

## Description
Ceci est un exemple de fit sur des données expérimentales et de graphique en
python. Les données sont une gracieuseté de Guy Bernier, coordonnateur de laboratoire au département de Physique de l'Université de Sherbrooke.

## Utilisation
Pour l'éxécuter, simplement exécuter `python Fit-Young.py` dans le dossier 
contenant *Fit-Young.py*, *Young_fente3_2260mm_zero.txt* et *maxfit.py*.
On peut aussi l'exécuter dans une fenêtre interactive ipython via la commande
`run -i Fit-Young.py` pour ensuite jouer avec les variables et fonctions.

Les résultats du fit s'afficheront dans le terminal ou la console.

Pour bien comprendre comment le programme fonctionnne, je suggère d'exécuter
*Fit-Young.py* dans une fenêtre ipython et d'ensuite accéder à la 
documentation des différentes fonction en tapant leur nom suivi de *?*.
e.g., `In[1]: fit?`

**Outpout Typique**
```
In [1]: run -i Fit-Young.py

--- FIT ON FUNCTION model ---

Fit parameters are [ 10.85968508   0.21240333   0.76450081]
Fit errors are [ 0.02007594  0.00040676  0.00034704]
Fit covariance
[[  3.69577155e-02   3.87662206e-04  -1.30732007e-07]
 [  3.87662206e-04   1.51715595e-05  -5.71271355e-09]
 [ -1.30732007e-07  -5.71271355e-09   1.10434042e-05]]
Fit correlation matrix
[[  1.00000000e+00   5.17709090e-01  -2.04634044e-04]
 [  5.17709090e-01   1.00000000e+00  -4.41342601e-04]
 [ -2.04634044e-04  -4.41342601e-04   1.00000000e+00]]
Reduced chi2 is 0.0109055316205
```

![Graphique obtenu](Example/Fit-Young_Python.png)


Jean Olivier Simoneau, février 2017

