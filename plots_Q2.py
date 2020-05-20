#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH3D

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "lgen.root"
    infile = "lgen_test1.root"
    #infile = "../lgen/data/lgen_18x275_qr_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_xB_yA_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_xB_yB_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_xC_yA_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_xD_yC_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_Qa_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_Qb_1p2Mevt.root"
    #infile = "../lgen/data/lgen_18x275_qr_Qc_10p2Mevt.root"

    iplot = 13
    funclist = []
    funclist.append( gen_xy ) # 0
    funclist.append( gen_Q2 ) # 1
    funclist.append( gen_Log10_Q2 ) # 2
    funclist.append( gen_E ) # 3
    funclist.append( gen_theta ) # 4
    funclist.append( gen_Q2_theta ) # 5
    funclist.append( gen_Log10x_y ) # 6
    funclist.append( gen_Q2_theta_E ) # 7
    funclist.append( gen_run_qr ) # 8
    funclist.append( gen_Log10x_Log10y ) # 9
    funclist.append( gen_lx_ly_lQ2 ) # 10
    funclist.append( rel_gen_Q2_el_Q2 ) # 11
    funclist.append( gen_phi ) # 12
    funclist.append( rel_gen_Q2_beff_el_Q2 ) # 13

    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("ltree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def gen_xy():

    #distribution of x and y

    xbin = 2e-9
    xmin = 8e-14
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
    lqmin = -11
    lqmax = 5

    hLog10Q2 = ut.prepare_TH1D("hLog10Q2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(gen_Q2) >> hLog10Q2")
    #tree.Draw("TMath::Log10(gen_el_Q2) >> hLog10Q2")

    can = ut.box_canvas()

    gPad.SetGrid()

    ut.put_yx_tit(hLog10Q2, "Events", "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    gPad.SetLogy()

    hLog10Q2.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10_Q2

#_____________________________________________________________________________
def gen_E():

    #electron energy

    ebin = 0.01
    emin = 0
    emax = 20

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("gen_E >> hE")

    can = ut.box_canvas()

    ut.put_yx_tit(hE, "Events", "#it{E'}", 1.4, 1.2)

    hE.Draw()

    gPad.SetLogy()

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

    tree.Draw("TMath::Pi()-gen_theta >> hTheta")

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
    xmin = -13.5
    xmax = -3.5

    ybin = 5e-5
    #ymin = 0.06
    ymin = 0
    ymax = 1.1

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    tree.Draw("gen_y:TMath::Log10(gen_x) >> hXY")
    #tree.Draw("gen_y:gen_u >> hXY")

    ytit = "#it{y}"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(x)"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10x_y

#_____________________________________________________________________________
def gen_Q2_theta_E():

    #Q^2 relative to theta and energy

    qbin = 1e-3
    qmin = 0
    qmax = 0.45
    #qmax = 1e-2

    tbin = 2e-4
    tmin = 0
    tmax = 0.04

    ebin = 0.1
    emin = 0
    emax = 20

    hQtE = ut.prepare_TH3D("hQtE", tbin, tmin, tmax, qbin, qmin, qmax, ebin, emin, emax)

    can = ut.box_canvas()

    tree.Draw("gen_E:gen_Q2:gen_theta >> hQtE")

    profile = hQtE.Project3DProfile("yx")

    profile.SetXTitle("Electron polar angle #theta (rad)")
    profile.SetYTitle("#it{Q}^{2} (GeV^{2})")
    profile.SetZTitle("Electron energy E_{e^{-}} (GeV)")
    profile.SetTitle("")

    profile.SetTitleOffset(1.3, "X")
    profile.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.15)

    profile.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2_theta_E

#_____________________________________________________________________________
def gen_run_qr():

    #run a testing sample with the quasi-real generator

    from gen_quasi_real import gen_quasi_real
    from gen_quasi_real_v2 import gen_quasi_real_v2
    import ConfigParser

    parse = ConfigParser.RawConfigParser()
    parse.read("lgen_quasireal_18x275.ini")

    #gen = gen_quasi_real(parse, None)
    gen = gen_quasi_real_v2(parse, None)

    for i in xrange(12):

        u = rt.Double(0)
        y = rt.Double(0)
        gen.eq.GetRandom2(u, y)

        print u, y

#gen_run_qr

#_____________________________________________________________________________
def gen_Log10x_Log10y():

    #distribution of log_10(x) and log_10(y)

    xbin = 0.1
    xmin = -12
    xmax = 0

    ybin = 0.1
    ymin = -4.5
    ymax = 0

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    #tree.Draw("TMath::Log10(gen_y):TMath::Log10(gen_x) >> hXY")
    tree.Draw("gen_v:gen_u >> hXY")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10x_Log10y

#_____________________________________________________________________________
def gen_lx_ly_lQ2():

    #distribution of log_10(x), log_10(y) and log_10(Q^2)

    xbin = 0.1
    xmin = -12
    xmax = 0

    ybin = 0.1
    ymin = -4.5
    ymax = 0

    lqbin = 0.1
    lqmin = -9
    lqmax = 3

    hXYQ2 = ut.prepare_TH3D("hXYQ2", xbin, xmin, xmax, ybin, ymin, ymax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw("TMath::Log10(gen_Q2):gen_v:gen_u >> hXYQ2")

    pXYQ2 = hXYQ2.Project3DProfile("yx")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    pXYQ2.SetXTitle(xtit)
    pXYQ2.SetYTitle(ytit)
    pXYQ2.SetZTitle("log_{10}(#it{Q}^{2} (GeV^{2}))")
    pXYQ2.SetTitle("")

    pXYQ2.SetTitleOffset(1.3, "X")
    pXYQ2.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.16)

    gPad.SetGrid()

    pXYQ2.SetContour(300)
    pXYQ2.SetMinimum(lqmin)
    pXYQ2.SetMaximum(lqmax)

    pXYQ2.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_lx_ly_lQ2

#_____________________________________________________________________________
def rel_gen_Q2_el_Q2():

    #relative difference in true Q^2 and generated electron Q^2

    dbin = 1e-5
    dmin = -1e-2
    dmax = 1e-2

    lqbin = 0.1
    lqmin = -12
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    tree.Draw("(gen_Q2-gen_el_Q2)/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")

    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_el_Q2

#_____________________________________________________________________________
def rel_gen_Q2_beff_el_Q2():

    #relative difference in Q^2 between plain generator and electron after beam effects

    dbin = 0.1
    dmin = -1
    dmax = 1

    lqbin = 0.1
    lqmin = -12
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    tree.Draw("(gen_Q2-gen_el_Q2)/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")

    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_beff_el_Q2

#_____________________________________________________________________________
def gen_phi():

    #electron azimuthal angle phi

    #phi range, rad
    pbin = 0.1
    pmin = -7
    pmax = 7

    hPhi = ut.prepare_TH1D("hPhi", pbin, pmin, pmax)

    tree.Draw("gen_phi >> hPhi")

    can = ut.box_canvas()

    ut.put_yx_tit(hPhi, "Events", "#phi (rad)", 1.4, 1.2)

    hPhi.Draw()

    #gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_phi

#_____________________________________________________________________________
def rel_gen_Q2_beff_el_Q2():

    #relative difference in Q^2 between plain generator and electron after beam effects

    dbin = 0.05
    dmin = -10
    dmax = 2

    lqbin = 0.05
    lqmin = -11
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    Q2form = "(2*18*el_en*(1-TMath::Cos(TMath::Pi()-el_theta)))"

    #tree.Draw("(gen_el_Q2-"+Q2form+")/gen_el_Q2:TMath::Log10(gen_el_Q2) >> hRQ2")

    tree.Draw("(gen_Q2-"+Q2form+")/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")


    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_beff_el_Q2

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











