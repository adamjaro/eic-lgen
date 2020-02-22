
import atexit

import ROOT as rt
from ROOT import TFile, TTree, gROOT, AddressOf

#_____________________________________________________________________________
class file_io:
    #output from lgen
    #_____________________________________________________________________________
    def __init__(self, parse):

        #name for the output file
        nam = parse.get("lgen", "nam").strip("\"'")
        print "Output name:", nam

        #lgen ascii output
        self.out = open(nam+"_evt.dat", "w")
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

        self.tx_out = open(nam+".tx", "w")
        self.tx_ievt = 1

        #ROOT output
        self.out_root = TFile(nam+".root", "RECREATE")
        #tree variables, all Double_t
        tlist = ["phot_en", "phot_eta", "phot_phi", "phot_theta", "phot_m"]
        tlist += ["phot_px", "phot_py", "phot_pz"]
        tlist += ["phot_vx", "phot_vy", "phot_vz"]
        tlist += ["el_en", "el_eta", "el_phi"]
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

        atexit.register(self.close)

    #_____________________________________________________________________________
    def write_dat(self, tracks):
        #ascii output for the event, pythia6 format

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
        #vtxlin = "VERTEX: "+str(vx)+" "+str(vy)+" "+str(vz)+" 0 1 0 0 "+ntrk
        vtxlin = "VERTEX:"
        vtx_prec = 9
        if vx<1e-9 and vy<1e-9 and vz<1e-9:
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
        #ROOT output for generated photon (phot) and electron (el)

        t = self.tree_out

        for i in tracks:
            #select the final photon and electron
            if i.stat != 1: continue

            #final photon
            if i.pdg == 22:

                t.phot_en    = i.vec.Energy()
                t.phot_eta   = i.vec.Eta()
                t.phot_phi   = i.vec.Phi()
                t.phot_theta = i.vec.Theta()
                t.phot_m     = i.vec.M()
                t.phot_px    = i.vec.Px()
                t.phot_py    = i.vec.Py()
                t.phot_pz    = i.vec.Pz()
                t.phot_vx    = i.vx
                t.phot_vy    = i.vy
                t.phot_vz    = i.vz

            #final electron
            if i.pdg == 11:

                t.el_en     = i.vec.Energy()
                t.el_eta    = i.vec.Eta()
                t.el_phi    = i.vec.Phi()

        #fill the tree
        self.ltree.Fill()

    #_____________________________________________________________________________
    def close(self):

        self.out.close()

        self.out_root.Write()
        self.out_root.Close()

        #print "file_io: closed"
















