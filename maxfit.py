#!/usr/bin/python
# -*- coding: utf-8 -*-

# Librairie de fit par Maxime Hardy et Jean Olivier Simoneau

from numpy import array,linspace,sqrt,diag
from scipy.optimize import leastsq
import scipy.odr as odr


class fit:
    '''
    La classe 'fit' crée un objet contenant deux méthodes de fit, soient
    fit.leastsq et fit.odr qui renvoient toutes deux le résultat dans
    fit.para avec comme erreurs fit.err. Si l'option verbose est activée
    (activée par défaut), le fit imprime à l'écran des valeurs importantes
    (dont la matrice de corrélation et chi^2).
    
    Elle s'utilise comme suit :
    def Fonction(x,P):
        return     La_fonction_de_la_variable_x_et_du_tableau_de_paramètres_p

    a = fit(ValeursDeX, ValeursDeY, ParamètresInitiaux, Fonction, xerr=ErreursEnX, yerr=ErreursEnY)
    a.leastsq() OU a.odr()

    Aussi, appeler l'objet de 'fit' correspond à appeler la fonction avec
    les paramètres stockés dans fit.para (paramètres initiaux au paramètres
    de fit)
    a(x) est absolument équivalent à Fonction(x,a.para)

    Aussi, on peut aller chercher directement les paramètres du fit en
    considérant l'objet comme un tableau:
    a[i] est absolument équivalen.let à a.para[i]

    Les classes 'lsqfit' et 'odrfit' sont absolument identiques à la classe
    'fit' (elles héritent de toutes ses méthodes et variables), sauf qu'elle
    performent la régression au moment de l'initialisation. Ainsi :
    def Fonction(x,P):
        return La_fonction_de_la_variable_x_et_du_tableau_de_paramètres_p

    a = odrfit(ValeursDeX, ValeursDeY, ParamètresInitiaux, Fonction, xerr=ErreursEnX, yerr=ErreursEnY)
    '''
    def __init__(self,x,y,p0,f,fullo=1,xerr=None,yerr=None,verbose=True,npts=1000):
        # Tableau des abscisses

        self.x = array(x)
        if xerr is None:
            self.xerr = [1.]*len(self.x)
        else:
            self.xerr = array(xerr)

        # Tableau des ordonnées
        self.y = y
        if yerr is None:
            self.yerr = [1.]*len(self.y)
        else:
            self.yerr = yerr
        self.para = p0         # Paramètres initiaux
        self.f = f        # Fonction pour la régression
        self.fullo = fullo     # 'Full output' de leastsq
        self.verbose = verbose    # Imprime des résultats importants à l'écran
        self.xFit = linspace(min(self.x),max(self.x),npts)



    # Appeler l'objet comme une fonction revient à évaluer la fonction avec les paramètres stockés dans
    # self.para (soit les paramètres du fit si celui-ci à déjà été fait)    
    def __call__(self,x=None):
        if x is None:
            x = self.xFit
        return self.f(x,self.para)
    
    def __getitem__(self,i):
        return self.para[i]

    def __len__(self):
        return len(self.para)

    def _residuals(self,p):
        return (self.y-self.f(self.x,p))/self.yerr

    def diff(self):
        return self.y - self.f(self.x,self.para)

    def leastsq(self):
        self.lsq = leastsq(self._residuals,self.para,full_output=self.fullo)
        if self.lsq[1] is None:
            if self.verbose: print '\n --- FIT DID NOT CONVERGE ---\n'
            self.err = None
            self.chi2r = None
            return False
        else:
            # Paramètres :
            self.para = self.lsq[0]
            self.cv = self.lsq[1]
            # Nombre d'itérations :
            self.it = self.lsq[2]['nfev'] 
            self.computevalues()
            self.err = self.sdcv*sqrt(self.chi2r)
#            self.donnee = []
#            for i in range(len(self.para)):
#                self.donnee.append(d.donnee(self.para[i],self.err[i]))
            if self.verbose:
                print self
            return True
        
    def fct(self,p,x):
        return self.f(x,p)
    
    def odr(self, **kwargs):
        self.model = odr.Model(self.fct)
        self.mydata = odr.Data(self.x,y=self.y,we=self.yerr,wd=self.xerr)
        self.myodr = odr.ODR(self.mydata,self.model,self.para)
        self.myoutput = self.myodr.run()
        self.cv = self.myoutput.cov_beta
        self.para = self.myoutput.beta
        self.computevalues()
        self.err = self.myoutput.sd_beta
#        self.donnee = []
#        for i in range(len(self.para)):
#            self.donnee.append(d.donnee(self.para[i],self.err[i]))
#        if kwargs.has_key('verbose'):
#            if kwargs['verbose']:
#                print self
#            else:
#                return
        if self.myodr.output.stopreason[0] in ['Iteration limit reached']:
            if self.verbose: print '\n --- FIT DID NOT CONVERGE ---\n'
            return False
        elif self.verbose:
            print self
            return True
            
    def computevalues(self):
        self.sdcv = sqrt(diag(self.cv))
        # Matrice de corrélation
        self.corrM = self.cv/self.sdcv/self.sdcv[:,None]
        self.chi2 = sum(((self.y-self.f(self.x,self.para))/self.yerr)**2.)
        # Chi^2 réduit
        self.chi2r = self.chi2/(len(self.y)-len(self.para))
        

    def __str__(self):
        return '\n--- FIT ON FUNCTION {} ---\n\nFit parameters are {}\nFit errors are {}\nFit covariance\n{}\nFit correlation matrix\n{}\nReduced chi2 is {}\n\n'.format(self.f.__name__,self.para,self.err,self.cv,self.corrM,self.chi2r)

    
    
class lsqfit(fit):
    def __init__(self,x,y,p0,f,fullo=1,xerr=None,yerr=None,verbose=True):
        fit.__init__(self,x,y,p0,f,fullo=fullo,xerr=xerr,yerr=yerr,verbose=verbose)
        self.leastsq()
    
class odrfit(fit):
    def __init__(self,x,y,p0,f,fullo=1,xerr=None,yerr=None,verbose=True):
        fit.__init__(self,x,y,p0,f,fullo=fullo,xerr=xerr,yerr=yerr,verbose=verbose)
        self.odr()
