
from ROOT import TLorentzVector, TDatabasePDG

#generic particle

#_____________________________________________________________________________
class particle:
    #_____________________________________________________________________________
    def __init__(self, pdg):
        #particle Lorentz vector
        self.vec = TLorentzVector()
        #index in particle list
        self.idx = 0
        #status code
        self.stat = 0
        #pdg code
        self.pdg = pdg
        #particle database for pass and codes
        self.pdgdat = TDatabasePDG.Instance()
        #mass, GeV
        self.mass = self.pdgdat.GetParticle(self.pdg).Mass()
        #parent particle id
        self.parent_id = 0
        #vertex coordinates, mm
        self.vx = 0.
        self.vy = 0.
        self.vz = 0.
        #precision for momentum and energy
        self.pxyze_prec = 6


    #_____________________________________________________________________________
    def write(self, out):
        #put event output line
        #index, status and pdg
        out.write("{0:10d}{1:11d}{2:11d}".format(self.idx, self.stat, self.pdg))
        #parent particle id
        out.write("{0:11d}".format(self.parent_id))
        #placeholder for daughter indices
        out.write("          0          0")
        #px, py, pz, energy
        pxyze_form = "{0:16."+str(self.pxyze_prec)+"f}"
        out.write( pxyze_form.format( self.vec.Px() ) )
        out.write( pxyze_form.format( self.vec.Py() ) )
        out.write( pxyze_form.format( self.vec.Pz() ) )
        out.write( pxyze_form.format( self.vec.E() ) )
        #mass
        out.write( "{0:16.6f}".format(self.mass) )
        #out.write("        0.000000")
        #vertex
        out.write( "{0:16.6f}".format(self.vx) )
        out.write( "{0:16.6f}".format(self.vy) )
        out.write( "{0:16.6f}".format(self.vz) )
        #end of line
        out.write("\n")

    #_____________________________________________________________________________
    def write_tx(self, track_list):

        #output line in TX format

        #Geant code and momentum
        lin = "TRACK:  "+str(self.pdgdat.ConvertPdgToGeant3(self.pdg))
        pxyz_form = " {0:."+str(self.pxyze_prec)+"f}"
        lin += pxyz_form.format( self.vec.Px() )
        lin += pxyz_form.format( self.vec.Py() )
        lin += pxyz_form.format( self.vec.Pz() )

        #track id
        lin += " " + str(len(track_list))

        #start and stop vertex and pdg
        lin += " 1 0 " + str(self.pdg)

        track_list.append(lin)

    #_____________________________________________________________________________
    def write_tparticle(self, particles, ipos):

        #write to TParticle clones array

        p = particles.ConstructedAt(ipos)

        p.SetMomentum(self.vec)
        p.SetPdgCode(self.pdg)
        p.SetProductionVertex(self.vx, self.vy, self.vz, 0)















