
import ConfigParser
from ROOT import TLorentzVector

from photon import photon
from beam import beam
from beam_effects import beam_effects
from file_io import file_io

from gen_h1 import gen_h1
from gen_zeus import gen_zeus
from gen_quasi_real import gen_quasi_real
from gen_quasi_real_v2 import gen_quasi_real_v2

#_____________________________________________________________________________
class event:
    #lgen generated event
    #_____________________________________________________________________________
    def __init__(self, config):

        #input configuration
        print "Generator configuration:", config
        parse = ConfigParser.RawConfigParser()
        parse.read(config)

        #output from lgen
        self.io = file_io(parse)

        #electron and proton beam, GeV
        self.Ee = parse.getfloat("lgen", "Ee")
        self.Ep = parse.getfloat("lgen", "Ep")
        print "Ee =", self.Ee
        print "Ep =", self.Ep

        #physics generator
        par = parse.get("lgen", "par").strip("\"'") # which parametrization to use
        #select the parametrization
        if par == "h1":
            self.gen = gen_h1(self.Ee, self.Ep, parse)
        elif par == "zeus":
            self.gen = gen_zeus(self.Ee, self.Ep, parse)
        elif par == "quasi-real":
            self.gen = gen_quasi_real(parse, self.io.ltree)
        elif par == "quasi-real-v2":
            self.gen = gen_quasi_real_v2(parse, self.io.ltree)
        else:
            print "Invalid generator specified"
            exit()

        #beam effects, also reads config file
        self.beff = beam_effects(parse)

        #tracks in the event
        self.tracks = []

        #run
        nev = parse.getint("lgen", "nev") # number of events to generate
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

        #run the physics generator
        self.gen.generate(self.add_particle)

        #relations between the final electron and photon
        for i in self.tracks:
            if i.stat != 1: continue

            #electron from the beam electron
            if i.pdg == 11: i.parent_id = 1

            #photon from the outgoing electron
            if i.pdg == 22: i.parent_id = 4

        #apply the beam effects
        self.beff.apply(self.tracks)

        #ascii event output
        self.io.write_dat(self.tracks)
        self.io.write_tx(self.tracks)

        #ROOT output for the photon and scattered electron
        self.io.write_root(self.tracks)

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




















