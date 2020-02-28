
import math
from math import pi

import ROOT as rt
from ROOT import TF2, Double, TMath, TRandom3, gROOT, AddressOf, TDatabasePDG

from electron import electron

#_____________________________________________________________________________
class gen_quasi_real_v2:
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

        #range in u = log_10(x)
        umin = TMath.Log10(xmin)
        umax = TMath.Log10(xmax)
        print "umin =", umin
        print "umax =", umax

        #range in y
        ymin = parse.getfloat("lgen", "ymin")
        ymax = parse.getfloat("lgen", "ymax")
        print "ymin =", ymin
        print "ymax =", ymax

        #range in v = log_10(y)
        vmin = TMath.Log10(ymin)
        vmax = TMath.Log10(ymax)
        print "vmin =", vmin
        print "vmax =", vmax

        #constant term in the cross section
        self.const = TMath.Log(10)*TMath.Log(10)*(1./137)/(2.*math.pi)

        #cross section formula for d^2 sigma / dxdy, Eq. II.6
        #transformed as x -> u = log_10(x) and y -> v = log_10(y)
        self.eq = TF2("d2SigDuDvII6", self.eq_II6_uv, umin, umax, vmin, vmax)

        #self.eq.SetNpy(10000)

        #uniform generator for azimuthal angles
        self.rand = TRandom3()
        self.rand.SetSeed(5572323)

        #generator event variables in output tree
        tnam = ["gen_u", "gen_v", "gen_x", "gen_y", "gen_Q2", "gen_theta", "gen_E", "gen_phi"]

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

        print "Quasi-real photoproduction version 2 initialized"

    #_____________________________________________________________________________
    def generate(self, add_particle):

        #electron polar angle theta and energy E
        theta = -1.
        E = 0.
        while theta < 0. or theta > pi or E**2 < self.me**2:

            #values of the u = log_10(x) and y from the cross section
            u = Double(0)
            v = Double(0)
            self.eq.GetRandom2(u, v)

            #x and y from the transformation
            x = 10.**u
            y = 10.**v

            #electron angle and energy
            theta = math.sqrt( x*y*self.s/((1.-y)*self.Ee**2) )
            E = self.Ee*(1.-y)

        #tree output with generator kinematics
        self.out.gen_u = u
        self.out.gen_v = v
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
    def eq_II6_uv(self, val):

        #II.6 transformed as x -> u = log_10(x)
        u = val[0]
        v = val[1]

        #sig = self.const*( y + 2.*(1.-y)/y )*(1.-10.**u)
        sig = self.const*( 1. + (1.-10**v)**2 )*(1.-10.**u)

        #term of the total gamma-p cross section by Donnachie, Landshoff, 1992
        #sig *= 0.0677*(y*self.s)**0.0808 + 0.129*(y*self.s)**-0.4525 # mb
        sig *= 0.0677*((10.**v)*self.s)**0.0808 + 0.129*((10.**v)*self.s)**-0.4525 # mb

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











