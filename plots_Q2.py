#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH3D

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "lgen.root"
    #infile = "../lgen/data/lgen_18x275_qr_1p2Mevt.root"
    infile = "../lgen/data/lgen_18x275_qr_xB_yA_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_xB_yB_1p2Mevt.root"

    iplot = 7
    funclist = []
    funclist.append( gen_xy ) # 0
    funclist.append( gen_Q2 ) # 1
    funclist.append( gen_Log10_Q2 ) # 2
    funclist.append( gen_E ) # 3
    funclist.append( gen_theta ) # 4
    funclist.append( gen_Q2_theta ) # 5
    funclist.append( gen_Log10x_y ) # 6
    funclist.append( gen_Q2_theta_E ) # 7

    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("ltree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def gen_xy():

    #distribution of x and y

    xbin = 2e-9
    xmin = 8e-9
    xmax = 2e-4

    ybin = 1e-2
    ymin = 0.06
    ymax = 1.1

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("gen_y:gen_x >> hXY")

    can = ut.box_canvas()

    ut.put_yx_tit(hXY, "#it{y}", "#it{x}", 1.4, 1.2)

    hXY.Draw()

    gPad.SetLogx()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_xy

#_____________________________________________________________________________
def gen_Q2():

    #plot the Q^2

    qbin = 1e-3
    qmin = 1e-4
    qmax = 1

    hQ2 = ut.prepare_TH1D("hQ2", qbin, qmin, qmax)

    tree.Draw("gen_Q2 >> hQ2")

    can = ut.box_canvas()

    ut.put_yx_tit(hQ2, "Events", "#it{Q}^{2}", 1.4, 1.2)

    hQ2.Draw()

    gPad.SetLogx()
    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2

#_____________________________________________________________________________
def gen_Log10_Q2():

    #plot the log_10(Q^2)

    lqbin = 0.1
    lqmin = -5
    lqmax = 2

    hLog10Q2 = ut.prepare_TH1D("hLog10Q2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(gen_Q2) >> hLog10Q2")

    can = ut.box_canvas()

    ut.put_yx_tit(hLog10Q2, "Events", "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    hLog10Q2.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10_Q2

#_____________________________________________________________________________
def gen_E():

    #electron energy

    ebin = 0.1
    emin = 0
    emax = 17

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("gen_E >> hE")

    can = ut.box_canvas()

    ut.put_yx_tit(hE, "Events", "#it{E'}", 1.4, 1.2)

    hE.Draw()

    #gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_E

#_____________________________________________________________________________
def gen_theta():

    #electron polar angle theta

    #theta range, rad
    tbin = 1e-3
    tmin = 0
    tmax = 0.2

    hTheta = ut.prepare_TH1D("hTheta", tbin, tmin, tmax)

    tree.Draw("gen_theta >> hTheta")

    can = ut.box_canvas()

    ut.put_yx_tit(hTheta, "Events", "#theta (rad)", 1.4, 1.2)

    hTheta.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_theta

#_____________________________________________________________________________
def gen_Q2_theta():

    #Q^2 relative to theta

    qbin = 1e-3
    #qmin = 1e-5
    qmin = 0
    qmax = 0.45

    tbin = 5e-4
    tmin = 0
    tmax = 0.04

    hQ2theta = ut.prepare_TH2D("hQ2theta", tbin, tmin, tmax, qbin, qmin, qmax)

    tree.Draw("gen_Q2:gen_theta >> hQ2theta")

    can = ut.box_canvas()

    ut.put_yx_tit(hQ2theta, "#it{Q}^{2}", "#theta (rad)", 1.4, 1.2)

    hQ2theta.Draw()

    #gPad.SetLogx()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2_theta

#_____________________________________________________________________________
def gen_Log10x_y():

    #distribution of log_10(x) and y

    xbin = 0.01
    xmin = -8.5
    xmax = -3.5

    ybin = 5e-3
    #ymin = 0.06
    ymin = 1e-2
    ymax = 1.1

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("gen_y:TMath::Log10(gen_x) >> hXY")

    can = ut.box_canvas()

    ytit = "#it{y}"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(x)"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    #gPad.SetLogx()
    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10x_y

#_____________________________________________________________________________
def gen_Q2_theta_E():

    #Q^2 relative to theta and energy

    #qbin = 1e-3
    qmin = 0
    qmax = 0.45
    #qmax = 1e-2

    #tbin = 5e-4
    tmin = 0
    tmax = 0.04

    emin = 0
    emax = 17

    hQtE = TH3D("hQtE", "hQtE", 100, tmin, tmax, 100, qmin, qmax, 100, emin, emax)

    #hQ2theta = ut.prepare_TH2D("hQ2theta", tbin, tmin, tmax, qbin, qmin, qmax)

    can = ut.box_canvas()

    tree.Draw("gen_E:gen_Q2:gen_theta >> hQtE")

    hQtE.SetXTitle("x: theta")
    hQtE.SetYTitle("y: Q2")
    hQtE.SetZTitle("z: energy")

    profile = hQtE.Project3DProfile("yx")

    profile.SetXTitle("Electron polar angle #theta (rad)")
    profile.SetYTitle("#it{Q}^{2} (GeV^{2})")
    profile.SetZTitle("Electron energy E_{e^{-}} (GeV)")
    profile.SetTitle("")

    profile.SetTitleOffset(1.3, "X")
    profile.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.15)

    profile.Draw("colz")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2_theta_E

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











