
from ROOT import TF1, TDatabasePDG, TMath, TRandom3, gRandom

#_____________________________________________________________________________
class gen_h1:
    #Bethe-Heitler bremsstrahlung photon generator according to H1
    #S. Levonian, H1LUMI, H1-04/93-287
    #_____________________________________________________________________________
    def __init__(self, Ee, Ep, emin = 8, tmax = 1.5e-3):

        #energy of electron beam, GeV
        self.Ee = Ee
        #proton beam, GeV
        self.Ep = Ep

        #minimal photon energy
        self.emin = float(emin)

        #electron and proton mass
        self.me = TDatabasePDG.Instance().GetParticle(11).Mass()
        self.mp = TDatabasePDG.Instance().GetParticle(2212).Mass()
        self.mep = self.me * self.mp

        #CMS energy squared, GeV^2
        self.s = 2*self.Ee*self.Ep + self.me**2 + self.mp**2
        self.s += 2*TMath.Sqrt(self.Ee**2 - self.me**2) * TMath.Sqrt(self.Ep**2 - self.mp**2)

        #normalization,  4 alpha r_e^2
        self.ar2 = 4*7.297*2.818*2.818*1e-2 # m barn

        #parametrizations for dSigma/dy and dSigma/dtheta
        gRandom.SetSeed(5572323)
        self.dSigDy = TF1("dSigDy", self.eq1, self.emin/self.Ee, 1)
        self.dSigDtheta = TF1("dSigDtheta", self.eq3, 0, tmax)

        #uniform generator for azimuthal angles
        self.rand = TRandom3()
        self.rand.SetSeed(5572323)

        print "H1 parametrization initialized"
        print("Total cross section: "+str(self.dSigDy.Integral(self.emin/self.Ee, 1))+" mb")

    #_____________________________________________________________________________
    def generate(self):

        #energy and polar angle
        en = self.dSigDy.GetRandom() * self.Ee
        #en = 0.1
        theta = self.dSigDtheta.GetRandom()

        #azimuthal angle
        phi = 2. * TMath.Pi() * self.rand.Rndm()

        return en, theta, phi

    #_____________________________________________________________________________
    def eq1(self, x):

        #formula for dSigma/dy with y = Eg/Ee

        y = x[0]

        t1 = self.ar2/y
        t2 = 1. + (1.-y)**2 - (2./3)*(1-y)
        t3 = TMath.Log( self.s*(1-y)/(self.mep*y) ) - 0.5

        return t1*t2*t3

    #_____________________________________________________________________________
    def eq3(self, x):

        #formula for angular distribution

        t = x[0] # rad
        return 1e-9 * t/( ((self.me/self.Ee)**2 + t*t)**2 )























