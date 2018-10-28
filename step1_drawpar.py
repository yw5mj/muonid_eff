#! /bin/env python
import sys,os
from ROOT import *

gROOT.SetBatch()
gStyle.SetOptStat(0)
f  = TFile('input/data.root')
outdir='~/www/tempproject_octo18/quicklook'
c=TCanvas()
tree=f.Get('tree')

# draw theta spectrum
theta=TH1F('theta',';#theta',50,0,3.14)
tree.Draw('theta_1>>+theta')
tree.Draw('theta_2>>+theta')
theta.Draw()
c.Print(outdir+'/theta.png')

# draw momentum spectrum
p=TH1F("p",";p [GeV]",50,0,300)
tree.Draw("p_1>>+p")
tree.Draw("p_2>>+p")
p.Draw()
c.Print(outdir+'/p.png')

# draw momentum vs theta
thtp=TH2F('thtp',";#theta;p [GeV]",15,0,3.14,15,0,150)
tree.Draw("p_1:theta_1>>+thtp")
tree.Draw("p_2:theta_2>>+thtp")
thtp.Draw("colz")
c.Print(outdir+'/thtp.png')

# inv mass
thtp=TH1F('invmass',";M_{inv} [GeV]",90,50,140)
tree.Draw("((p_1+p_2)**2-(px_1+px_2)**2-(py_1+py_2)**2-(pz_1+pz_2)**2)**.5>>invmass")
thtp.Draw()
c.Print(outdir+'/invMass.png')

# inv mass when muon1 fails ID
thtp=TH1F('invmassf',";M_{inv} [GeV]",90,50,140)
tree.Draw("((p_1+p_2)**2-(px_1+px_2)**2-(py_1+py_2)**2-(pz_1+pz_2)**2)**.5>>invmassf","(!id_1)")
thtp.Draw()
c.Print(outdir+'/invMass_failingID_1.png')
