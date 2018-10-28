#! /bin/env python
import os,sys,time
from ROOT import *
gROOT.SetBatch()
tag=[i[:-5] for i in os.listdir("./output") if '.root' in i] if len(sys.argv)<2 else [sys.argv[1]]
tag.sort()
plotdir='~/www/tempproject_octo18'
c=TCanvas()

def fits(tag):
    dataset = TFile('output/{0}.root'.format(tag))
    h=dataset.Get(tag)
    fitfunc=TF1("fitfunc",'expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])+[6]*TMath::Voigt(x-[7],[8],[9])',50,140)
    fitfunc.SetParameters(10,-0.05,2*h.GetBinContent(1),80,1,50,h.GetBinContent(40),91.1,2,2)
##    fitfunc=TF1("fitfunc",'expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])+gaus(6)',50,140)
    fitfunc.SetParLimits(2,0,15*h.GetBinContent(1))
    fitfunc.SetParLimits(3,0,150)
    fitfunc.SetParLimits(4,0,100)
    fitfunc.SetParLimits(5,40,100)
    fitfunc.SetParLimits(6,0,20*h.GetBinContent(40))
    fitfunc.SetParLimits(7,87,93)
    fitfunc.SetParLimits(8,0,10)
    fitfunc.SetParLimits(9,0,10)

    h.Fit("fitfunc")
    h.SetMarkerStyle(20)
    fitf=h.GetFunction('fitfunc')

    bkg1=TF1('bkg1','expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])',50,140)
    bkg1.SetParameters(fitf.GetParameter(0),fitf.GetParameter(1),fitf.GetParameter(2),fitf.GetParameter(3),fitf.GetParameter(4),fitf.GetParameter(5))
    bkg1.SetLineColor(4)
    h.Draw('e1p')
    bkg1.Draw('same')
    c.Print(plotdir+'/fittest.png')
    print "Fitting pars for:",tag
    print "Chi_square:",fitfunc.GetChisquare()

for i in tag:
    fits(i)
#    if raw_input("continue?(y/n): ")=='n': break
    time.sleep(1)

