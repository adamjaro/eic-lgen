
import ConfigParser

from ROOT import TF1

#_____________________________________________________________________________
class beam_effects_v2:
    #angular divergence and emittance
    #_____________________________________________________________________________
    def __init__(self, parse):

        # flag to use or not use the beam effects
        self.use_beam_effects = False
        if parse.has_section("beff2") == True:
            self.use_beam_effects = parse.getboolean("beff2", "use_beam_effects")

        print "Beam effects V2 configuration:"
        print "use_beam_effects =", self.use_beam_effects

        if self.use_beam_effects == False: return

        #beam size at IP in x, sigma_x in mm
        sig_x = parse.getfloat("beff2", "sig_x")
        print "sig_x =", sig_x
        self.vtx_x = self.make_gaus("vtx_x", sig_x)

        #beam size at IP in y, sigma_y in mm
        sig_y = parse.getfloat("beff2", "sig_y")
        print "sig_y =", sig_y
        self.vtx_y = self.make_gaus("vtx_y", sig_y)

        #bunch length along z
        sig_z = parse.getfloat("beff2", "sig_z")
        print "sig_z =", sig_z
        self.vtx_z = self.make_gaus("vtx_z", sig_z)

        #angular divergence in x, horizontal, rad
        theta_x = parse.getfloat("beff2", "theta_x")
        print "theta_x =", theta_x
        self.div_x = self.make_gaus("div_x", theta_x)

        #angular divergence in y, vertical, rad
        theta_y = parse.getfloat("beff2", "theta_y")
        print "theta_y =", theta_y
        self.div_y = self.make_gaus("div_y", theta_y)

    #_____________________________________________________________________________
    def apply(self, tracks):
        #apply beam effects

        if not self.use_beam_effects: return

        #beam size in x, y and z
        xpos = self.vtx_x.GetRandom()
        ypos = self.vtx_y.GetRandom()
        zpos = self.vtx_z.GetRandom()

        #angular divergence in x and y
        tx = self.div_x.GetRandom()
        ty = self.div_y.GetRandom()

        #apply to the final particles
        for i in tracks:
            #select only final particles
            if i.stat != 1: continue

            #vertex position
            i.vx = xpos
            i.vy = ypos
            i.vz = zpos

            #divergence in x by rotation along y
            i.vec.RotateY(tx)

            #divergence in y by rotation along x
            i.vec.RotateX(ty)



    #_____________________________________________________________________________
    def make_gaus(self, name, sig):

        gx = TF1(name, "gaus", -12*sig, 12*sig)
        gx.SetParameters(1, 0, sig)

        return gx
















