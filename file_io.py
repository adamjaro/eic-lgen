
import atexit

import ROOT as rt
from ROOT import TFile, TTree, gROOT, AddressOf, TClonesArray

#_____________________________________________________________________________
class file_io:
    #output from lgen
    #_____________________________________________________________________________
    def __init__(self, parse):

        #create the individual outputs
        self.set_write_dat = False
        if parse.has_option("lgen", "write_dat"):
            self.set_write_dat = parse.getboolean("lgen", "write_dat")

        self.set_write_tx = False
        if parse.has_option("lgen", "write_tx"):
            self.set_write_tx = parse.getboolean("lgen", "write_tx")

        self.set_write_root = True
        if parse.has_option("lgen", "write_root"):
            self.set_write_root = parse.getboolean("lgen", "write_root")

        if self.set_write_dat: self.make_dat(parse)
        if self.set_write_tx: self.make_tx(parse)

        self.ltree = None
        if self.set_write_root: self.make_root(parse)

    #_____________________________________________________________________________
    def make_dat(self, parse):

        #dat output, Pythia6 format

        #name for the output file
        nam = parse.get("lgen", "nam").strip("\"'") + "_evt.dat"
        print "Dat output name:", nam

        #lgen ascii output
        self.out = open(nam, "w")
        #event counter
        self.ievt = 1
        #header for the ascii output
        header = []
        header.append("  LGEN EVENT FILE ") # LGEN
        header.append(" ============================================")
        header.append("I, ievent, IChannel, process, subprocess, nucleon, struckparton, partontrck, Y, Q2, X, W2, NU, trueY, trueQ2, trueX, trueW2,trueNu, SIGtot, errSIGtot, D, F1NC, F3NC, G1NC,G3NC, A1NC, F1CC, F3CC, G1CC, G5CC, nrTracks")
        header.append(" ============================================")
        header.append("  I  K(I,1)  K(I,2)  K(I,3)  K(I,4)  K(I,5) P(I,1)  P(I,2)  P(I,3)  P(I,4)  P(I,5)  V(I,1)  V(I,2)  V(I,3)")
        header.append(" ============================================")
        for i in header: self.out.write(i+"\n")

    #_____________________________________________________________________________
    def make_tx(self, parse):

        #TX output

        nam = parse.get("lgen", "nam").strip("\"'") + ".tx"
        print "TX output name:", nam

        self.tx_out = open(nam, "w")
        self.tx_ievt = 1

    #_____________________________________________________________________________
    def make_root(self, parse):

        #ROOT output

        nam = parse.get("lgen", "nam").strip("\"'") + ".root"
        print "ROOT output name:", nam

        self.out_root = TFile(nam, "recreate")
        #tree variables, all Double_t
        tlist = ["phot_en", "phot_theta", "phot_phi"]
        tlist += ["el_en", "el_theta", "el_phi"]
        #C structure holding the variables
        struct = "struct tree_out { Double_t "
        for i in tlist: struct += i + ", "
        struct = struct[:-2] + ";};"
        gROOT.ProcessLine( struct )
        #create the output tree
        self.tree_out = rt.tree_out() # instance of the C structure
        self.ltree = TTree("ltree", "ltree")
        for i in tlist:
            exec("self.tree_out."+i+"=0")
            self.ltree.Branch(i, AddressOf(self.tree_out, i), i+"/D")

        #particles array
        self.particles_out = TClonesArray("TParticle")
        self.particles_out.SetOwner(True)
        self.ltree.Branch("particles", self.particles_out)

        atexit.register(self.close_root)

    #_____________________________________________________________________________
    def write_dat(self, tracks):
        #ascii output for the event, pythia6 format

        if not self.set_write_dat: return

        #write event header to the output
        self.out.write("   0")
        #event number
        self.out.write("{0:11d}".format(self.ievt))
        #placeholder for integer variables
        self.out.write("     15      4      2      1      0      0")
        #placeholder for event kinematics and cross section, 22 parameters, 10 decimal digits, 19 characters
        for ii in xrange(22): 
            self.out.write("{0:19.10E}".format(0.))
        #number of tracks in the event
        self.out.write( "{0:13d}".format(len(tracks)) )
        self.out.write("\n")
        self.out.write(" ============================================\n")

        #put tracks in the event
        for i in tracks:
            i.write(self.out)

        #place event footer to the output
        self.out.write(" =============== Event finished ===============\n")
        #increment event count after writing the event
        self.ievt += 1

    #_____________________________________________________________________________
    def write_tx(self, tracks):

        #TX Starlight format

        if not self.set_write_tx: return

        #tracks and vertex position in cm
        tracks_tx = []
        vx = 0.
        vy = 0.
        vz = 0.
        #tracks loop
        for t in tracks:
            #only final particles
            if t.stat != 1: continue

            vx = t.vx/10.
            vy = t.vy/10.
            vz = t.vz/10.

            t.write_tx(tracks_tx)

        #number of tracks for event and vertex lines
        ntrk = str(len(tracks_tx))

        #event line
        evtlin = "EVENT: "+str(self.tx_ievt)+" "+ntrk+" 1"
        self.tx_out.write(evtlin+"\n")

        #vertex line
        vtxlin = "VERTEX:"
        vtx_prec = 9
        if abs(vx)<1e-9 and abs(vy)<1e-9 and abs(vz)<1e-9:
            vtx_prec = 0
        vtx_form = " {0:."+str(vtx_prec)+"f}"
        vtxlin += vtx_form.format(vx)
        vtxlin += vtx_form.format(vy)
        vtxlin += vtx_form.format(vz)
        vtxlin += " 0 1 0 0 "+ntrk
        self.tx_out.write(vtxlin+"\n")

        #track lines
        for tlin in tracks_tx:
            self.tx_out.write(tlin+"\n")

        self.tx_ievt += 1

    #_____________________________________________________________________________
    def write_root(self, tracks):

        #ROOT output

        if not self.set_write_root: return

        #initialize the particles array
        ipos = 0
        self.particles_out.Clear("C")

        t = self.tree_out

        for i in tracks:
            #select the final photon and electron
            if i.stat != 1: continue

            #put the particles to TParticles clones array
            i.write_tparticle(self.particles_out, ipos)
            ipos += 1

            #final photon
            if i.pdg == 22:

                t.phot_en    = i.vec.Energy()
                t.phot_theta = i.vec.Theta()
                t.phot_phi   = i.vec.Phi()

            #final electron
            if i.pdg == 11:

                t.el_en     = i.vec.Energy()
                t.el_theta  = i.vec.Theta()
                t.el_phi    = i.vec.Phi()

        #fill the tree
        self.ltree.Fill()

    #_____________________________________________________________________________
    def close_root(self):

        self.out_root.Write()
        self.out_root.Close()

















