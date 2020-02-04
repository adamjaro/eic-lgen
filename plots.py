#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

from gen_zeus import gen_zeus
from gen_h1 import gen_h1

import plot_utils as ut

#_____________________________________________________________________________
def plot_vxy():

    #vertex position of generated photon along x and y

    xbin = 0.01
    ybin = 0.001

    xmin = -1.5
    xmax = 1.5

    ymin = -0.2
    ymax = 0.2

    can = ut.box_canvas()

    hV = ut.prepare_TH2D("hV", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("phot_vy:phot_vx >> hV")

    hV.SetXTitle("#it{x} of primary vertex (mm)")
    hV.SetYTitle("#it{y} of primary vertex (mm)")

    hV.SetTitleOffset(1.6, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.13)

    #gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vxy

#_____________________________________________________________________________
def plot_theta_SigTheta():

    #distribution in theta and parametrization

    tbin = 1e-5
    tmax = 1.5e-3

    can = ut.box_canvas()

    ht = ut.prepare_TH1D("ht", tbin, 0, tmax)

    tree.Draw("(TMath::Pi()-phot_theta) >> ht") # *1000

    #theta parametrization
    from gen_zeus import gen_zeus
    gen = gen_zeus(18, 275, 1)
    tpar = gen.dSigDtheta
    tpar.SetNpx(600)
    tpar.SetLineWidth(3)

    #scale the parametrization to the plot
    norm = tbin * ht.Integral() / tpar.Integral(0, tmax)
    print "norm:", norm
    gen.theta_const = norm * gen.theta_const

    ht.SetYTitle("Events / ({0:.3f}".format(tbin*1e3)+" mrad)")
    ht.SetXTitle("#vartheta (rad)")

    ht.SetTitleOffset(1.5, "Y")
    ht.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.08)

    ht.Draw()

    ht.SetMaximum(1e6)

    tpar.Draw("same")

    leg = ut.prepare_leg(0.37, 0.84, 0.2, 0.08, 0.035)
    leg.AddEntry(tpar, "Bethe-Heitler parametrization", "l")
    leg.AddEntry(ht, "Angular divergence #sigma_{#vartheta} = 0.2 mrad", "lp")
    leg.Draw("same")

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_vz():

    #vertex position of generated photon along x or y

    vbin = 0.8
    vmin = -80
    vmax = 80

    can = ut.box_canvas()

    hV = ut.prepare_TH1D("hV", vbin, vmin, vmax)

    tree.Draw("phot_vz >> hV")

    hV.SetYTitle("Events / ({0:.3f}".format(vbin)+" mm)")
    hV.SetXTitle("z vertex (mm)")

    hV.SetTitleOffset(1.6, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.05, 0.02)

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vz

#_____________________________________________________________________________
def plot_vx():

    #vertex position of generated photon along x or y

    vbin = 0.1
    vmin = -10
    vmax = 10

    can = ut.box_canvas()

    hV = ut.prepare_TH1D("hV", vbin, vmin, vmax)

    tree.Draw("phot_vx >> hV")
    #tree.Draw("phot_vy >> hV")

    hV.SetYTitle("Events / ({0:.3f}".format(vbin)+" mm)")
    hV.SetXTitle("x vertex (mm)")
    #hV.SetXTitle("y vertex (mm)")

    hV.SetTitleOffset(1.9, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.02)

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vx

#_____________________________________________________________________________
def plot_dSigDtheta():

    # dSigma / dTheta according to ZEUS parametrization

    Ee = 18

    gen = gen_zeus(Ee, 275) # Ee, Ep, GeV
    sig = gen.dSigDtheta

    can = ut.box_canvas()

    sig.SetLineWidth(3)
    sig.SetNpx(1000)
    sig.SetTitle("")
    sig.Draw()

    sig.GetXaxis().SetTitle("#theta_{#gamma} (rad)")
    sig.GetYaxis().SetTitle("a. u.")

    sig.GetYaxis().SetTitleOffset(1.5)
    sig.GetXaxis().SetTitleOffset(1.3)

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.08)

    leg = ut.prepare_leg(0.58, 0.78, 0.24, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(sig, "#frac{d#sigma}{d#theta_{#gamma}}", "l")
    leg.AddEntry(None, "E_{e} = 18 GeV", "")
    leg.Draw("same")

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_theta():

    #polar angle of generated photons

    tbin = 0.01
    tmax = 0.8

    can = ut.box_canvas()

    ht = ut.prepare_TH1D("ht", tbin, 0, tmax)

    tree.Draw("(TMath::Pi()-phot_theta)*1000 >> ht")

    ht.SetYTitle("Events / ({0:.3f}".format(tbin)+" mrad)")
    ht.SetXTitle("#vartheta (mrad)")

    ht.SetTitleOffset(1.5, "Y")
    ht.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.025)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    ht.Draw()

    leg = ut.prepare_leg(0.2, 0.87, 0.18, 0.08, 0.035)
    leg.AddEntry(None, "Angular distribution of Bethe-Heitler photons", "")
    #leg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_en():

    #energy distribution of generated photons

    ebin = 0.1
    emin = 4
    emax = 28

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("phot_en >> hE")

    hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hE.SetXTitle("#it{E}_{#gamma} (GeV)")

    hE.SetTitleOffset(1.9, "Y")
    hE.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.14)

    hE.GetYaxis().SetMoreLogLabels()

    hE.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_dSigDy():

    # dSigma / dy according to H1 parametrization

    gen = gen_h1(27.6, 920) # Ee, Ep, GeV
    sig = gen.dSigDy

    can = ut.box_canvas()

    sig.SetNpx(300)
    sig.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_dSigDe():

    # dSigma / dEgamma according to ZEUS parametrization

    #gen = gen_zeus(27.6, 920) # Ee, Ep, GeV
    gen = gen_zeus(18, 275, 6) # Ee, Ep, Emin, GeV
    sig = gen.dSigDe

    gStyle.SetPadTickY(1)
    can = ut.box_canvas()

    #frame = gPad.DrawFrame(6, 0, 29, 6)
    frame = gPad.DrawFrame(5, 0, 19, 7.2)

    sig.SetLineWidth(3)
    sig.SetNpx(1000)
    sig.SetTitle("")
    sig.Draw("same")

    frame.GetXaxis().SetTitle("#it{E}_{#gamma} (GeV)")
    frame.GetYaxis().SetTitle("d#sigma / d#it{E}_{#gamma} (mb/GeV)")

    frame.GetYaxis().SetTitleOffset(1.1)
    frame.GetXaxis().SetTitleOffset(1.3)

    frame.SetTickLength(0.015, "X")
    frame.SetTickLength(0.015, "Y")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.01)
    gPad.SetLeftMargin(0.09)

    leg = ut.prepare_leg(0.65, 0.73, 0.24, 0.2, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(sig, "#frac{d#sigma}{d#it{E}_{#gamma}}", "l")
    leg.AddEntry(None, "", "")
    #leg.AddEntry(None, "#it{E}_{e} = 27.6 GeV", "")
    #leg.AddEntry(None, "#it{E}_{p} = 920 GeV", "")
    leg.AddEntry(None, "#it{E}_{e} = 18 GeV", "")
    leg.AddEntry(None, "#it{E}_{p} = 275 GeV", "")
    leg.Draw("same")

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    #infile = "lgen.root"
    infile = "/home/jaroslav/sim/lgen/data/lgen_18x275_10p1Mevt.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 4
    funclist = []
    funclist.append( plot_dSigDe ) # 0
    funclist.append( plot_dSigDy ) # 1
    funclist.append( plot_en ) # 2
    funclist.append( plot_theta ) # 3
    funclist.append( plot_dSigDtheta ) # 4
    funclist.append( plot_vx ) # 5
    funclist.append( plot_vz ) # 6
    funclist.append( plot_theta_SigTheta ) # 7
    funclist.append( plot_vxy ) # 8

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("ltree")

    #call the plot function
    funclist[iplot]()




















