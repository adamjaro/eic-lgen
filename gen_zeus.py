
from ROOT import TDatabasePDG, TF1, TRandom3, gRandom, TMath

from photon import photon
from beam import beam

#_____________________________________________________________________________
class gen_zeus:
    #Bethe-Heitler bremsstrahlung photon according to ZEUS
    #Eur. Phys. J. C (2011) 71: 1574
    #_____________________________________________________________________________
    def __init__(self, Ee, Ep, parse):

        #electron beam, GeV
        self.Ee = Ee
        #proton beam, GeV
        self.Ep = Ep

        print "Ee =", self.Ee, "GeV"
        print "Ep =", self.Ep, "GeV"

        #minimal photon energy, GeV
        self.emin = parse.getfloat("lgen", "emin")
        print "emin =", self.emin

        #maximal photon angle
        self.tmax = 1.5e-3
        if parse.has_option("lgen", "tmax"):
            self.tmax = parse.getfloat("lgen", "tmax")

        #electron and proton mass
        self.me = TDatabasePDG.Instance().GetParticle(11).Mass()
        self.mp = TDatabasePDG.Instance().GetParticle(2212).Mass()
        self.mep = self.me * self.mp

        #normalization,  4 alpha r_e^2
        self.ar2 = 4*7.297*2.818*2.818*1e-2 # m barn

        #parametrizations for dSigma/dE_gamma and dSigma/dtheta
        gRandom.SetSeed(5572323)
        self.dSigDe = TF1("dSigDe", self.eq1, self.emin, self.Ee)

        self.theta_const = 1e-11 # constant term in theta formula
        self.dSigDtheta = TF1("dSigDtheta", self.eq2, 0, self.tmax)

        #uniform generator for azimuthal angles
        self.rand = TRandom3()
        self.rand.SetSeed(5572323)

        print("ZEUS parametrization initialized")
        print("Total cross section: "+str(self.dSigDe.Integral(self.emin, self.Ee))+" mb")

    #_____________________________________________________________________________
    def eq1(self, x):

        #E_gamma
        Eg = x[0]
        #electron and proton energy
        Ee = self.Ee
        Ep = self.Ep

        #scattered electron Ee'
        Escat = Ee - Eg
        #if Escat < 1e-5: return 0.

        t1 = Escat/(Eg*Ee)
        t2 = (Ee/Escat) + (Escat/Ee) - 2./3
        t3 = TMath.Log(4*Ep*Ee*Escat/(self.mep*Eg)) - 1./2

        return self.ar2*t1*t2*t3

    #_____________________________________________________________________________
    def eq2(self, x):

        #photon angular distribution
        t = x[0]

        #1e-11
        return self.theta_const * t/(( (self.me/self.Ee)**2 + t**2 )**2)

    #_____________________________________________________________________________
    def generate(self, add_particle):

        #initialize the scattered electron as a beam electron
        electron = add_particle( beam(self.Ee, 11, -1) )
        electron.stat = 1
        electron.pxyze_prec = 9

        #kinematics for the Bethe-Heitler bremsstrahlung photon
        #energy and polar angle
        en = self.dSigDe.GetRandom()
        theta = self.dSigDtheta.GetRandom()

        #azimuthal angle
        phi = 2. * TMath.Pi() * self.rand.Rndm()

        #put the Bethe-Heitler bremsstrahlung photon to the event
        phot = add_particle( photon(en, theta, phi) )
        phot.pxyze_prec = 9 # increase kinematics precision for the photon

        #constrain the scattered electron with the photon
        electron.vec -= phot.vec

























