
import ConfigParser
from ROOT import TLorentzVector

from photon import photon
from beam import beam
from beam_effects import beam_effects
from file_io import file_io

from gen_h1 import gen_h1
from gen_zeus import gen_zeus

#_____________________________________________________________________________
class event:
    #lgen generated event
    #_____________________________________________________________________________
    def __init__(self, config):

        print "Generator configuration:", config

        parse = ConfigParser.RawConfigParser()
        parse.read(config)

        #electron and proton beam, GeV
        self.Ee = parse.getfloat("lgen", "Ee")
        self.Ep = parse.getfloat("lgen", "Ep")
        print "Ee =", self.Ee
        print "Ep =", self.Ep

        #photon generator
        par = parse.get("lgen", "par").strip("\"'")
        emin = parse.getfloat("lgen", "emin")
        print "emin =", emin
        if par == "h1":
            self.gen = gen_h1(self.Ee, self.Ep, emin)
        elif par == "zeus":
            self.gen = gen_zeus(self.Ee, self.Ep, emin)
        else:
            print "Invalid generator specified"
            exit()

        #beam effects, also reads config file
        self.beff = beam_effects(config)

        #tracks in the event
        self.tracks = []

        #output from lgen
        nam = parse.get("lgen", "nam").strip("\"'")
        print "Output name:", nam
        self.io = file_io(nam)

        #run
        nev = parse.getint("lgen", "nev")
        print "Number of events:", nev
        self.event_loop(nev)

    #_____________________________________________________________________________
    def event_loop(self, nev):

        for i in xrange(nev):
            self.generate()

        print "All done"

    #_____________________________________________________________________________
    def generate(self):
        #generate the event

        #clear tracks list
        self.tracks = []

        #beam particles
        self.add_particle( beam(self.Ee, 11, -1) )
        self.add_particle( beam(self.Ep, 2212, 1) )

        #intermediate particle, placehoder with zero energy photon
        intermediate = self.add_particle( photon(0.1, 1e-4, 0) )
        intermediate.stat = 21 # mark as not final
        intermediate.pdg = 23 # away from photon pdg

        #scattered electron, initialized as beam electron
        electron = self.add_particle( beam(self.Ee, 11, -1) )
        electron.stat = 1
        electron.parent_id = 1
        electron.pxyze_prec = 9

        #Bethe-Heitler bremsstrahlung photon
        en, theta, phi = self.gen.generate()
        phot = self.add_particle( photon(en, theta, phi) )
        phot.parent_id = 4
        phot.pxyze_prec = 9 # increase kinematics precision for the photon

        #apply beam effects to outgoing photon and electron
        self.beff.apply(phot, electron)

        #constrain scattered electron with the photon
        electron.vec -= phot.vec

        #ascii event output
        self.io.write_dat(self.tracks)
        self.io.write_tx(self.tracks)

        #ROOT output for the photon and scattered electron
        self.io.write_root(phot, electron)

    #_____________________________________________________________________________
    def add_particle(self, part):

        part.idx = len(self.tracks)+1
        self.tracks.append(part)

        return part

    #_____________________________________________________________________________
    def print_vec(self, vec):
            print "theta vec:", TMath.Pi()-vec.Theta()
            print
            return
            print "pxyz:", vec.Px(), vec.Py(), vec.Pz()
            print "en, phi:", vec.E(), vec.Phi()
            print
            v3 = vec.Vect()
            print "vxyz:", v3.x(), v3.y(), v3.z()
            print "theta v3: ", TMath.Pi()-v3.Theta()
            print
            theta_add = 1e-5
            v3.SetTheta( v3.Theta() - theta_add )
            print "vxyz:", v3.x(), v3.y(), v3.z()
            print "theta v3: ", TMath.Pi()-v3.Theta()
            print

            vec2 = TLorentzVector(vec)
            vec3 = TLorentzVector(vec)

            vec.SetVect(v3)

            print "theta vec:", TMath.Pi()-vec.Theta()
            print "pxyz:", vec.Px(), vec.Py(), vec.Pz()
            print "en, phi:", vec.E(), vec.Phi()
            print

            vec2.SetTheta( vec2.Theta() - theta_add )

            print "theta vec:", TMath.Pi()-vec2.Theta()
            print "pxyz:", vec2.Px(), vec2.Py(), vec2.Pz()
            print "en, phi:", vec2.E(), vec2.Phi()
            print

            print "Delta theta, en, phi", vec3.Theta()-vec.Theta(), vec3.E()-vec.E(), vec3.Phi()-vec.Phi()
            print "Delta theta, en, phi", vec3.Theta()-vec2.Theta(), vec3.E()-vec2.E(), vec3.Phi()-vec2.Phi()




















