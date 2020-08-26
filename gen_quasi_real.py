
#_____________________________________________________________________________
# Quasi-real photoproduction at low Q^2
#
# d^2 sigma / dxdy is Eq. II.6 in Amaldi, ed., Study on ep facility, 1979, page 320,
# Conf.Proc. C790402 (1979) 1-474, http://inspirehep.net/record/151135
#
# The procedure was used in S. Levonian, H1LUMI, H1-04/93-287 (1993),
# https://www-h1.desy.de/~levonian/papers/h1lumi.ps.gz
#
# The total gamma-proton cross section is from Donnachie, Landshoff, Total cross sections,
# Phys.Lett. B296 (1992) 227-232, http://inspirehep.net/record/337839
# 
#_____________________________________________________________________________

import math
from math import pi

import ROOT as rt
from ROOT import TF2, Double, TMath, TRandom3, gROOT, AddressOf, TDatabasePDG

from electron import electron

#_____________________________________________________________________________
class gen_quasi_real:
    #_____________________________________________________________________________
    def __init__(self, parse, tree):

        #electron and proton beam energy, GeV
        self.Ee = parse.getfloat("lgen", "Ee")
        self.Ep = parse.getfloat("lgen", "Ep")
        print "Ee =", self.Ee
        print "Ep =", self.Ep

        #electron mass
        self.me = TDatabasePDG.Instance().GetParticle(11).Mass()

        #center-of-mass squared s, GeV^2
        self.s = self.get_s(self.Ee, self.Ep)

        #range in x and y, max 4 orders of magnitude for the range of x
        xmin = parse.getfloat("lgen", "xmin")
        xmax = parse.getfloat("lgen", "xmax")
        print "xmin =", xmin
        print "xmax =", xmax

        #range in y
        ymin = parse.getfloat("lgen", "ymin")
        ymax = parse.getfloat("lgen", "ymax")
        print "ymin =", ymin
        print "ymax =", ymax

        #constant term in the cross section
        self.const = (1./137)/(2.*math.pi)

        #cross section formula for d^2 sigma / dxdy, Eq. II.6
        self.eq = TF2("d2SigDxDyII6", self.eq_II6, xmin, xmax, ymin, ymax)

        #number of points for function evaluation to generate
        #the values of x and y down to x = 1e-7
        self.eq.SetNpx(10000) # max for npx allowed in ROOT

        #uniform generator for azimuthal angles
        self.rand = TRandom3()
        self.rand.SetSeed(5572323)

        #generator event variables in output tree
        tnam = ["gen_x", "gen_y", "gen_Q2", "gen_theta", "gen_E", "gen_phi"]

        #create the tree variables
        tcmd = "struct gen_out { Double_t "
        for i in tnam:
            tcmd += i + ", "
        tcmd = tcmd[:-2] + ";};"
        gROOT.ProcessLine( tcmd )

        #set the variables in the tree
        if tree is not None:
            self.out = rt.gen_out()
            for i in tnam:
                tree.Branch(i, AddressOf(self.out, i), i+"/D")

        #total integrated cross section
        self.sigma_tot = self.eq.Integral(xmin, xmax, ymin, ymax)
        print "Total integrated cross section for a given x and y range:", self.sigma_tot, "mb"

        print "Quasi-real photoproduction initialized"

    #_____________________________________________________________________________
    def generate(self, add_particle):

        #electron polar angle theta and energy E
        theta = -1.
        E = 0.
        while theta < 0. or theta > pi or E**2 < self.me**2:

            #values of the x and y from the cross section
            x = Double(0)
            y = Double(0)
            self.eq.GetRandom2(x, y)

            #electron angle and energy
            theta = math.sqrt( x*y*self.s/((1.-y)*self.Ee**2) )
            E = self.Ee*(1.-y)

        #tree output with generator kinematics
        self.out.gen_x = x
        self.out.gen_y = y
        self.out.gen_Q2 = x*y*self.s

        self.out.gen_theta = theta
        self.out.gen_E = E

        #uniform azimuthal angle
        phi = 2. * TMath.Pi() * self.rand.Rndm()
        self.out.gen_phi = phi

        #put the electron to the event
        el = add_particle( electron(E, theta, phi) )
        el.pxyze_prec = 9

    #_____________________________________________________________________________
    def eq_II6(self, val):

        #II.6
        x = val[0]
        y = val[1]

        #print "x:", x, "y:", y

        sig = self.const*( (1.+(1.-y)**2)/y )*(1.-x)/x

        #term of the total gamma-p cross section by Donnachie, Landshoff, 1992
        sig *= 0.0677*(y*self.s)**0.0808 + 0.129*(y*self.s)**-0.4525 # mb

        return sig

    #_____________________________________________________________________________
    def get_s(self, Ee, Ep):

        #calculate the CMS squared s

        #proton mass
        mp = TDatabasePDG.Instance().GetParticle(2212).Mass()

        #CMS energy squared s, GeV^2
        s = 2.*Ee*Ep + self.me**2 + mp**2
        s += 2*TMath.Sqrt(Ee**2 - self.me**2) * TMath.Sqrt(Ep**2 - mp**2)

        #print "sqrt(s):", TMath.Sqrt(s)

        return s















