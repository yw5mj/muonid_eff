# /bin/env python
import sys,os,math
from ROOT import *

gROOT.SetBatch()
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
dataset = TFile('input/data.root')
plotdir='~/www/tempproject_octo18/histsandfits'
os.system("mkdir -p {0}".format(plotdir))
c=TCanvas()
tree=dataset.Get('tree')
outdir='output'
def getplot(tag,cut1,cut2,todraw='((p_1+p_2)**2-(px_1+px_2)**2-(py_1+py_2)**2-(pz_1+pz_2)**2)**.5'):
    # Get Histogram
    cut=[cut1,cut2]
    fout=TFile("{0}/{1}.root".format(outdir,tag),'recreate')
    temp=TH1F(tag,tag,90,50,140)
    temp.SetTitle(tag+";M_{inv} [GeV]")
    for i in cut: tree.Draw('{0}>>+{1}'.format(todraw,tag),i)

    # define funciton and fit
    fitfunc=TF1("fitfunc",'expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])+[6]*TMath::Voigt(x-[7],[8],[9])',50,140)
#    fitfunc=TF1("fitfunc",'expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])+gaus(6)',50,140)
    fitfunc.SetParameters(10,-0.05,2*temp.GetBinContent(1),80,1,50,temp.GetBinContent(40),91.1,2,2)
    fitfunc.SetParLimits(2,0,15*temp.GetBinContent(1))
    fitfunc.SetParLimits(3,0,150)
    fitfunc.SetParLimits(4,0,100)
    fitfunc.SetParLimits(5,40,100)
    fitfunc.SetParLimits(6,0,20*temp.GetBinContent(40))
    fitfunc.SetParLimits(7,87,93)
    fitfunc.SetParLimits(8,0,10)
    fitfunc.SetParLimits(9,0,10)

    temp.Fit("fitfunc")

    # legend, bkg and plotting
    bkg=TF1('bkg','expo(0)+[2]*TMath::Voigt(x-[3],[4],[5])',50,140)
    fitf=temp.GetFunction('fitfunc')
    bkg.SetParameters(fitf.GetParameter(0),fitf.GetParameter(1),fitf.GetParameter(2),fitf.GetParameter(3),fitf.GetParameter(4),fitf.GetParameter(5))
    bkg.SetLineColor(38)
    leg=TLegend(.6,.7,.88,.88)
    leg.AddEntry(temp,"Data")
    leg.AddEntry(fitfunc,"global fit")
    leg.AddEntry(bkg,"background fit")
    temp.Write()
    temp.SetMarkerStyle(20)
    temp.Draw('e1p')
    bkg.Draw('same')
    leg.Draw('same')
    c.Print('{0}/{1}.png'.format(plotdir,tag))
    fout.Close()


passid1='charge_1*charge_2<0&&id_1&&id_2&&theta_1>THETA1&&theta_1<THETA2'
passid2='charge_1*charge_2<0&&id_1&&id_2&&theta_2>THETA1&&theta_2<THETA2'
failid1='charge_1*charge_2<0&&(!id_1)&&id_2&&theta_1>THETA1&&theta_1<THETA2'
failid2='charge_1*charge_2<0&&id_1&&(!id_2)&&theta_2>THETA1&&theta_2<THETA2'

n,m=sys.argv[1],sys.argv[2]
getplot("pass{0}".format(n),passid1.replace('THETA1',n).replace('THETA2',m),passid2.replace('THETA1',n).replace('THETA2',m))
getplot("fail{0}".format(n),failid1.replace('THETA1',n).replace('THETA2',m),failid2.replace('THETA1',n).replace('THETA2',m))
