
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
        self.Ee = parse.getfloat("lgen", "Ee")
        print "Ee =", self.Ee

        #electron mass
        me = TDatabasePDG.Instance().GetParticle(11).Mass()

        #momentum along z
        self.pz = -TMath.Sqrt(self.Ee**2 - me**2)

        print "Electron beam initialized"

    #_____________________________________________________________________________
    def generate(self, add_particle):

        #beam Lorentz vector
        beam = particle(11)
        beam.vec.SetPxPyPzE(0, 0, self.pz, self.Ee)
        beam.stat = 1
        beam.pxyze_prec = 9

        #put the beam electron to the event
        add_particle( beam )

















