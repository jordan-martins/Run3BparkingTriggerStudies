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

parser.add_option("-r", "--runnum", default='322079', type="string", help="runnum", dest="runnum") 
parser.add_option("-l", "--lumi", default='L1p8', type="string", help="lumi", dest="lumi") 

(options, args) = parser.parse_args()  

print options


chain = TChain('l1UpgradeEmuTree/L1UpgradeTree', 'tree')
#chain = TChain('l1UpgradeTree/L1UpgradeTree', 'tree')

#for line in open('../ntuple/Run3_NuGun_MC_ntuples.list', 'r'):
#runnum = 322088

for line in open('fileList/' + options.runnum + '_' + options.lumi + '.txt', 'r'):
    line = line.rstrip()

    if line.find('.root')==-1: continue

    print line
    chain.AddFile(line)


#chain.AddFile('/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/condor/reHcalTP_PFA1p_Nu_110X_105p12_mufix_1620043913/9.root')

chain.SetBranchStatus('*', 0)
chain.SetBranchStatus('muon*', 1)
chain.SetBranchStatus('eg*', 1)

Nevt = chain.GetEntries()

print Nevt, 'events detected'




##################################################
#handle  = Handle ('std::vector<reco::GenParticle>')
#label = ("genParticles")

#handle_e  = Handle ('BXVector<l1t::EGamma>')
#label_e = ("gtStage2Digis", "EGamma")

#handle_mu  = Handle ('BXVector<l1t::Muon>')
#label_mu = ("gtStage2Digis", "Muon")

##################################################

nevents = 0

out = TreeProducer('rate_' + options.runnum + '_' + options.lumi + '.root')

ptrange = np.arange(3, 11, 1).tolist() 


for evt in xrange(Nevt):
    chain.GetEntry(evt)

    if evt%1000==0: print('{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed')


#    L1_muons = [(chain.muonEt[i], chain.muonEta[i], chain.muonPhi[i], chain.muonQual[i]) for i in range(len(chain.muonEt)) if chain.muonQual[i] >= 12]
    L1_muons = [(chain.muonEt[i], chain.muonEta[i], chain.muonPhi[i]) for i in range(len(chain.muonEt)) if chain.muonQual[i] >= 12 and abs(chain.muonEta[i]) < 1.5]

#    L1_electrons = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt))]

    L1_electrons = [(chain.egEt[i], chain.egEta[i], chain.egPhi[i]) for i in range(len(chain.egEt)) if abs(chain.egEta[i]) < 1.]


#    print 'mu', L1_muons
#    print 'e', L1_electrons
#    print 'e1p5', L1_electrons_1p0

#    break

    L1_muons = sorted(L1_muons, key = lambda mu : mu[0], reverse = True)
    L1_electrons = sorted(L1_electrons, key = lambda e : e[0], reverse = True)

#    L1_muons_1p5 = sorted([mu for mu in L1_muons if abs(mu.eta()) < 1.5], key = lambda mu : mu.pt(), reverse = True)
#    L1_electrons_1p0 = sorted([e for e in L1_electrons if abs(e.eta()) < 1.0], key = lambda e : e.pt(), reverse = True)

#    import pdb; pdb.set_trace()

    out.nmuons[0] = len(L1_muons)
#    out.nmuons_1p5[0] = len(L1_muons_1p5)

    out.nelectrons[0] = len(L1_electrons)
#    out.nelectrons_1p0[0] = len(L1_electrons_1p0)

    if out.nmuons[0]!=0:
        out.mu1_pt[0] = L1_muons[0][0]
        out.mu1_eta[0] = L1_muons[0][1]
    else:
        out.mu1_pt[0] = -1
        out.mu1_eta[0] = -1

        
    if out.nelectrons[0]!=0:
        out.e1_pt[0] = L1_electrons[0][0]
        out.e1_eta[0] = L1_electrons[0][1]
    else:
        out.e1_pt[0] = -1
        out.e1_eta[0] = -1



    if out.nelectrons[0]>1:


        for pt in ptrange:

            flag = False

            for ii, e1 in enumerate(L1_electrons):

#                print pt, e1[0], e1[1], e1[2]

                if flag: break

                for jj, e2 in enumerate(L1_electrons):


                    if jj >= ii: continue

#                    print ii,jj

                    if e1[0] >= pt and e2[0] >= pt and deltaR(e1[1], e1[2], e2[1], e2[2]) < 1.:
                        
                        flag = True

                        break


            
            if pt==3:
                out.doubleE3[0] = flag
            elif pt==4:
                out.doubleE4[0] = flag
            elif pt==5:
                out.doubleE5[0] = flag
            elif pt==6:
                out.doubleE6[0] = flag
            elif pt==7:
                out.doubleE7[0] = flag
            elif pt==8:
                out.doubleE8[0] = flag
            elif pt==9:
                out.doubleE9[0] = flag
            elif pt==10:
                out.doubleE10[0] = flag
            else:
                print 'Not expected !!!'


#        out.e2_pt[0] = L1_electrons[1][0]
#        out.e2_eta[0] = L1_electrons[1][1]
#        out.dr[0] = deltaR(L1_electrons[0][1], L1_electrons[0][2], L1_electrons[1][1], L1_electrons[1][2])
#    else:
#        out.e2_pt[0] = -1
#        out.e2_eta[0] = -1
#        out.dr[0] = -1


    out.tree.Fill()


    nevents += 1

print nevents, 'has been analyzed'

out.endJob()
