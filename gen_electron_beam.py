
#_____________________________________________________________________________
# Beam electrons with a given energy for simulations testing
#
#_____________________________________________________________________________

from ROOT import TMath, TDatabasePDG

from particle import particle

#_____________________________________________________________________________
class gen_electron_beam:
    #_____________________________________________________________________________
    def __init__(self, parse):

        #electron beam energy, GeV
        Ee = parse.getfloat("lgen", "Ee")
        print "Ee =", Ee

        #electron mass
        me = TDatabasePDG.Instance().GetParticle(11).Mass()

        #momentum along z
        pz = -TMath.Sqrt(Ee**2 - me**2)

        #beam Lorentz vector
        self.beam = particle(11)
        self.beam.vec.SetPxPyPzE(0, 0, pz, Ee)
        self.beam.stat = 1
        self.beam.pxyze_prec = 9

        print "Electron beam initialized"

    #_____________________________________________________________________________
    def generate(self, add_particle):

        #put the electron to the event
        add_particle( self.beam )

















