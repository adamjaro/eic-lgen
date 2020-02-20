
from ROOT import TDatabasePDG, TMath

from math import sqrt, cos, log, tan, pi

from particle import particle

#electron initialized from its energy and polar and azimuthal angle

#_____________________________________________________________________________
class electron(particle):
    #_____________________________________________________________________________
    def __init__(self, en, theta, phi):
        particle.__init__(self, 11)

        #transverse momentum
        m = TDatabasePDG.Instance().GetParticle(11).Mass()
        pt = sqrt( 0.5*(en**2 - m**2)*(1.-cos(2.*theta)) )

        #pseudorapidity, rotate the theta for pz negative
        theta = pi - theta
        eta = -log( tan(theta/2.) )

        #set the electron Lorentz vector
        self.vec.SetPtEtaPhiE(pt, eta, phi, en)

        #status for the final particle
        self.stat = 1

















