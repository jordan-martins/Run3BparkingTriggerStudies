from DataFormats.FWLite import Events, Handle
from common.deltar             import deltaR, bestMatch
from ROOT import TFile, TTree, Double, TLorentzVector, TChain
from array import array
import math
from os import listdir
from os.path import isfile, join
from TreeProducer import *
import numpy as np 

from optparse import OptionParser, OptionValueError 
usage = "usage: python runTauDisplay_BsTauTau.py" 
parser = OptionParser(usage)  

#parser.add_option("-r", "--runnum", default='322079', type="string", help="runnum", dest="runnum") 
parser.add_option("-i", "--input", default="/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/EZB_12_108p1/EphemeralZeroBias1/zbD1/211125_191622/0000/L1Ntuple_9.root", type="string", help="input", dest="input") 
parser.add_option("-o", "--output", default="test.root", type="string", help="output", dest="output")

(options, args) = parser.parse_args()  

print options


chain = TChain('l1UpgradeEmuTree/L1UpgradeTree', 'L1Upgrade')

chain.Add(options.input)

Nevt = chain.GetEntries()

print Nevt, 'events detected'



nevents = 0

out = TreeProducer(options.output)

drdict = {
    3.0:1.0,
    3.5:1.0,
    4.0:1.0,
    4.5:0.9,
    5.0:0.9,
    5.5:0.8,
    6.0:0.8,
    6.5:0.8,
    7.0:0.8,
    7.5:0.7,
    8.0:0.7,
    8.5:0.7,
    9.0:0.7,
    9.5:0.6,
    10.0:0.6,
    10.5:0.6,
    11.0:0.6,
    11.5:0.5,
    12.0:0.5,
    12.5:0.5,
    13.0:0.5,
    13.5:0.4,
    14.0:0.4,
}   




for evt in xrange(Nevt):
    chain.GetEntry(evt)

    if evt%10000==0: print('{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed')

    L1_muons_eta1p5 = [(chain.muonEt[i], chain.muonEta[i], chain.muonPhi[i]) for i in range(len(chain.muonEt)) if chain.muonQual[i] >= 12 and abs(chain.muonEta[i]) < 1.5]

    L1_muons_eta2p4 = [(chain.muonEt[i], chain.muonEta[i], chain.muonPhi[i]) for i in range(len(chain.muonEt)) if chain.muonQual[i] >= 12 and abs(chain.muonEta[i]) < 2.4]

    L1_electrons_eta1p0 = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 1.]

    L1_electrons_eta1p2 = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 1.218]

    L1_electrons_eta1p4 = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 1.4]

    L1_electrons_eta1p5 = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 1.5]

    L1_electrons_eta2p5 = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 2.5]


    L1_muons_eta1p5 = sorted(L1_muons_eta1p5, key = lambda mu : mu[0], reverse = True)
    L1_muons_eat2p4 = sorted(L1_muons_eta2p4, key = lambda mu : mu[0], reverse = True)
    L1_electrons_eta1p0 = sorted(L1_electrons_eta1p0, key = lambda e : e[0], reverse = True)
    L1_electrons_eta1p2 = sorted(L1_electrons_eta1p2, key = lambda e : e[0], reverse = True)
    L1_electrons_eta1p4 = sorted(L1_electrons_eta1p4, key = lambda e : e[0], reverse = True)
    L1_electrons_eta1p5 = sorted(L1_electrons_eta1p5, key = lambda e : e[0], reverse = True)
    L1_electrons_eta2p5 = sorted(L1_electrons_eta2p5, key = lambda e : e[0], reverse = True)



    out.nmuons_eta1p5[0] = len(L1_muons_eta1p5)
    out.nmuons_eta2p4[0] = len(L1_muons_eta2p4)

    out.nelectrons_eta1p0[0] = len(L1_electrons_eta1p0)
    out.nelectrons_eta1p5[0] = len(L1_electrons_eta1p5)
    out.nelectrons_eta2p5[0] = len(L1_electrons_eta2p5)


#    out.instL[0] = chain.instL
#    out.npu[0] = chain.npu
#    out.run[0] = chain.runnr
#    out.evt[0] = chain.lumiSec
#    out.lumi[0] = chain.eventnr

    if out.nmuons_eta1p5[0]!=0:
        out.mu1_eta1p5_pt[0] = L1_muons_eta1p5[0][0]
        out.mu1_eta1p5_eta[0] = L1_muons_eta1p5[0][1]
        out.mu1_eta1p5_phi[0] = L1_muons_eta1p5[0][2]
    else:
        out.mu1_eta1p5_pt[0] = -1
        out.mu1_eta1p5_eta[0] = -1
        out.mu1_eta1p5_phi[0] = -1

    if out.nmuons_eta2p4[0]!=0:
        out.mu1_eta2p4_pt[0] = L1_muons_eta2p4[0][0]
        out.mu1_eta2p4_eta[0] = L1_muons_eta2p4[0][1]
        out.mu1_eta2p4_phi[0] = L1_muons_eta2p4[0][2]
    else:
        out.mu1_eta2p4_pt[0] = -1
        out.mu1_eta2p4_eta[0] = -1
        out.mu1_eta2p4_phi[0] = -1


        
    if out.nelectrons_eta1p0[0]!=0:
        out.e1_eta1p0_pt[0] = L1_electrons_eta1p0[0][0]
        out.e1_eta1p0_eta[0] = L1_electrons_eta1p0[0][1]
        out.e1_eta1p0_phi[0] = L1_electrons_eta1p0[0][2]
    else:
        out.e1_eta1p0_pt[0] = -1
        out.e1_eta1p0_eta[0] = -1
        out.e1_eta1p0_phi[0] = -1

    if out.nelectrons_eta1p0[0]>1:
        out.e2_eta1p0_pt[0] = L1_electrons_eta1p0[1][0]
        out.e2_eta1p0_eta[0] = L1_electrons_eta1p0[1][1]
        out.e2_eta1p0_phi[0] = L1_electrons_eta1p0[1][2]
    else:
        out.e2_eta1p0_pt[0] = -1
        out.e2_eta1p0_eta[0] = -1
        out.e2_eta1p0_phi[0] = -1



    if out.nelectrons_eta1p5[0]!=0:
        out.e1_eta1p5_pt[0] = L1_electrons_eta1p5[0][0]
        out.e1_eta1p5_eta[0] = L1_electrons_eta1p5[0][1]
        out.e1_eta1p5_phi[0] = L1_electrons_eta1p5[0][2]
    else:
        out.e1_eta1p5_pt[0] = -1
        out.e1_eta1p5_eta[0] = -1
        out.e1_eta1p5_phi[0] = -1

    if out.nelectrons_eta1p5[0]>1:
        out.e2_eta1p5_pt[0] = L1_electrons_eta1p5[1][0]
        out.e2_eta1p5_eta[0] = L1_electrons_eta1p5[1][1]
        out.e2_eta1p5_phi[0] = L1_electrons_eta1p5[1][2]
    else:
        out.e2_eta1p5_pt[0] = -1
        out.e2_eta1p5_eta[0] = -1
        out.e2_eta1p5_phi[0] = -1



    if out.nelectrons_eta2p5[0]!=0:
        out.e1_eta2p5_pt[0] = L1_electrons_eta2p5[0][0]
        out.e1_eta2p5_eta[0] = L1_electrons_eta2p5[0][1]
        out.e1_eta2p5_phi[0] = L1_electrons_eta2p5[0][2]
    else:
        out.e1_eta2p5_pt[0] = -1
        out.e1_eta2p5_eta[0] = -1
        out.e1_eta2p5_phi[0] = -1

    if out.nelectrons_eta2p5[0]>1:
        out.e2_eta2p5_pt[0] = L1_electrons_eta2p5[1][0]
        out.e2_eta2p5_eta[0] = L1_electrons_eta2p5[1][1]
        out.e2_eta2p5_phi[0] = L1_electrons_eta2p5[1][2]
    else:
        out.e2_eta2p5_pt[0] = -1
        out.e2_eta2p5_eta[0] = -1
        out.e2_eta2p5_phi[0] = -1





    for pt in ptrange:

        flag = False

        for ii, e1 in enumerate(L1_electrons_eta1p2):
            
            if flag: break

            for jj, e2 in enumerate(L1_electrons_eta1p2):


                if jj <= ii: continue


                if e1[0] >= pt and e2[0] >= pt and deltaR(e1[1], e1[2], e2[1], e2[2]) < Double(drdict[pt]):
                        
                    flag = True
                    break
                        

        getattr(out, 'dyn_doubleE' + str(pt) + '_eta1p2')[0] = flag



    out.tree.Fill()


    nevents += 1

print nevents, 'has been analyzed'

out.endJob()
