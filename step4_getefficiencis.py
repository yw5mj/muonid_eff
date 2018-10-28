#! /bin/env python
from ROOT import *
from array import array
import os
gROOT.SetBatch()
gStyle.SetOptStat(0)
plotdir='~/www/tempproject_octo18'
tags=[i[4:-5] for i in os.listdir("./output") if i[:4]=='pass']
tags.sort()
ary=array('d',[float(i) for i in tags]+[3.0])
passhist=TH1F("pass","Muon ID efficiency;#theta;efficiency [%]",len(tags),ary)
failhist=TH1F("fail",";#theta",len(tags),ary)
for n,tag in enumerate(tags):
    fpass=TFile('output/pass{0}.root'.format(tag))
    h=fpass.Get('pass'+tag)
    func=h.GetFunction("fitfunc")
    sigpass=func.GetParameter(6)
    sigpassUnc=func.GetParError(6)
    passhist.SetBinContent(n+1,sigpass)
    passhist.SetBinError(n+1,sigpassUnc)

    ffail=TFile('output/fail{0}.root'.format(tag))
    h=ffail.Get('fail'+tag)
    func=h.GetFunction("fitfunc")
    sigfail=func.GetParameter(6)
    sigfailUnc=func.GetParError(6)
    failhist.SetBinContent(n+1,sigfail)
    failhist.SetBinError(n+1,sigfailUnc)
    print "theta bin: {0}\n\t#pass: {1}, Unc: {2}\n\t#fail: {3}, Unc: {4}\n".format(tag,sigpass,sigpassUnc,sigfail,sigfailUnc)
eff=passhist.Clone("efficiency")
eff.Divide(passhist+failhist)
eff.Scale(100)
eff.SetMinimum(70)
eff.SetMaximum(110)
eff.SetLineWidth(2)
eff.SetMarkerStyle(20)
c=TCanvas()
eff.Draw()
c.Print(plotdir+"/efficiencies.png")
