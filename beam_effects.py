
import ConfigParser

from ROOT import TF1

#_____________________________________________________________________________
class beam_effects:
    #angular divergence and emittance
    #_____________________________________________________________________________
    def __init__(self, parse):

        # flag to use or not use the beam effects
        self.use_beam_effects = False
        if parse.has_section("beff") == True:
            self.use_beam_effects = parse.getboolean("beff", "use_beam_effects")

        print "Beam effects configuration:"
        print "use_beam_effects =", self.use_beam_effects

        if self.use_beam_effects == False: return

        #angular divergence along theta, sigma_theta in rad
        sig_theta = parse.getfloat("beff", "sig_theta")
        print "sig_theta =", sig_theta
        self.angular_divergence = TF1("angular_divergence", "gaus", -6.*sig_theta, 6.*sig_theta)
        self.angular_divergence.SetParameters(1, 0, sig_theta) # const, mean, sigma

        #beam size at IP in x, sigma_x in mm
        sig_x = parse.getfloat("beff", "sig_x")
        print "sig_x =", sig_x
        self.emit_x = TF1("emit_x", "gaus", -6.*sig_x, 6.*sig_x)
        self.emit_x.SetParameters(1, 0, sig_x)

        #beam size at IP in y, sigma_y in mm
        sig_y = parse.getfloat("beff", "sig_y")
        print "sig_y =", sig_y
        self.emit_y = TF1("emit_y", "gaus", -6.*sig_y, 6.*sig_y)
        self.emit_y.SetParameters(1, 0, sig_y)

        #bunch length along z
        #parse.set("beff", "sig_z", 1.)
        sig_z = parse.getfloat("beff", "sig_z")
        print "sig_z =", sig_z
        self.vtx_z = TF1("vtx_z", "gaus", -6.*sig_z, 6.*sig_z)
        self.vtx_z.SetParameters(1, 0, sig_z)

    #_____________________________________________________________________________
    def apply(self, tracks):
        #apply beam effects to outgoing photon phot and electron el

        if not self.use_beam_effects: return

        #angular divergence
        theta_add = self.angular_divergence.GetRandom()

        #beam size in x and y
        xpos = self.emit_x.GetRandom()
        ypos = self.emit_y.GetRandom()

        #bunch length along z
        zpos = self.vtx_z.GetRandom()

        #apply to the final particles
        for i in tracks:
            #select only final particles
            if i.stat != 1: continue

            i.vec.SetTheta( i.vec.Theta() - theta_add )
            i.vx = xpos
            i.vy = ypos
            i.vz = zpos

























