#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "lgen.root"
    infile = "../lgen/data/lgen_18x275_qr_1p2Mevt.root"

    iplot = 2
    funclist = []
    funclist.append( gen_xy ) # 0
    funclist.append( gen_Q2 ) # 1
    funclist.append( gen_Log10_Q2 ) # 2
    funclist.append( gen_E ) # 3
    funclist.append( gen_theta ) # 4
    funclist.append( gen_Q2_theta ) # 5

    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("ltree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def gen_xy():

    #distribution of x and y

    xbin = 1e-8
    xmin = 6e-8
    xmax = 3e-3

    ybin = 1e-2
    ymin = 0.06
    ymax = 1

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
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











