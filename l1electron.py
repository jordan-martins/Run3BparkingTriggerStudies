from DataFormats.FWLite import Events, Handle
from deltar             import deltaR, bestMatch
from ROOT import TFile, TTree, Double, TLorentzVector
from array import array
import math
from os import listdir
from os.path import isfile, join
from TreeProducer_l1electron import *


mypath='/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/'

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles = onlyfiles[0:3]

events = Events(onlyfiles)
#events = Events('/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/AOD_BparkingTriggerStudy_nomufilter_5753.root')

Nevt = int(events.size())
print len(onlyfiles), 'files are analyzed. Total # of events = ', Nevt


##################################################
handle  = Handle ('std::vector<reco::GenParticle>')
label = ("genParticles")

handle_e  = Handle ('BXVector<l1t::EGamma>')
label_e = ("gtStage2Digis", "EGamma")

#handle_mu  = Handle ('BXVector<l1t::Muon>')
#label_mu = ("gtStage2Digis", "Muon")
##################################################

nevents = 0
ndrop = 0

out = TreeProducer_l1electron('l1electron_' + str(len(onlyfiles)) + 'files_'  + str(Nevt) + 'events.root')


for ev in events:

    ev.getByLabel(label, handle)

    if nevents%1000==0: print('{0:.2f}'.format(Double(nevents)/Double(Nevt)*100.), '% processed')

    gps = handle.product()

#    gps_muons = sorted([p for p in gps if abs(p.pdgId())==13 and p.status()==1 and abs(p.eta()) < 2.4 ], key = lambda mu : mu.pt(), reverse = True )
    gps_electrons = sorted([p for p in gps if abs(p.pdgId())==11 and p.status()==1 and abs(p.eta()) < 2.7], key = lambda e : e.pt(), reverse = True )


#    gps = [p for p in gps if abs(p.pdgId())==521] 
# 
#    gen_electrons = None
#    gen_bs = []
#
#    for p in gps:
#
#        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
#        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
#        
#        gen_electrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
#        gen_bs.append(p)
#        
#
#    if len(gen_bs)!=1: 
#        ndrop += 1
#        continue



#    ev.getByLabel(label_mu, handle_mu)
#    muons = handle_mu.product()

#    L1_muons = []
#
#    for jj in range(muons.size(0)):
#        L1_muons.append(muons.at(0,jj))


    ev.getByLabel(label_e, handle_e)
    electrons = handle_e.product()

    L1_electrons = []


    for jj in range(electrons.size(0)):
        L1_electrons.append(electrons.at(0,jj))


 #   L1_muons = sorted([mu for mu in L1_muons], key = lambda mu : mu.pt(), reverse = True)
    L1_electrons = sorted([e for e in L1_electrons], key = lambda e : e.pt(), reverse = True)

#    for ii in L1_electrons:
#        print ii.pt()



#    for gen_mu in gps_muons:
#        bm, maxdR = bestMatch(gen_mu, L1_muons)
#
#        gen_mupt[0] =  gen_mu.pt()
#        gen_mueta[0] = gen_mu.eta()
#        gen_muphi[0] = gen_mu.phi()
#
#        if bm!=None:
#            l1mu_dr[0] = maxdR
#            l1mu_pt[0] = bm.pt()
#            l1mu_eta[0] = bm.eta()
#            l1mu_phi[0] = bm.phi()
#        else:
#            l1mu_dr[0] = -1
#            l1mu_pt[0] = -1 
#            l1mu_eta[0] = -1
#            l1mu_phi[0] = -1


#    for gen_e in gen_electrons:
    for gen_e in gps_electrons:
        bm, maxdR = bestMatch(gen_e, L1_electrons)

        out.gen_ept[0] =  gen_e.pt()
        out.gen_eeta[0] = gen_e.eta()

        if bm!=None:
            out.l1e_dr[0] = maxdR
            out.l1e_pt[0] = bm.pt()
            out.l1e_eta[0] = bm.eta()
        else:
            out.l1e_dr[0] = -1
            out.l1e_pt[0] = -1
            out.l1e_eta[0] = -1

        

        out.tree.Fill()
    
#    L1_matched_electrons = []
#
#    for ielectron, gen_electron in enumerate(gen_electrons):
#
#        bm, maxdR = bestMatch(gen_electron, L1_electrons)
#        
#        ie[0] = ielectron
#        
#        if bm!=None:
#            l1_mindr[0] = maxdR
#            l1_pt[0] = bm.pt()
#            l1_eta[0] = bm.eta()
#            l1_phi[0] = bm.phi()
#            l1_hwPt[0] = bm.hwPt()
#            l1_hwEta[0] = bm.hwEta()
#            l1_hwPhi[0] = bm.hwPhi()
#            l1_iso[0] = bm.hwIso()
#            l1_toweriphi[0] = bm.towerIPhi()
#            l1_towerieta[0] = bm.towerIEta()
#            l1_rawEt[0] = bm.rawEt()
#            l1_isoEt[0] = bm.isoEt()
#            l1_footprintEt[0] = bm.footprintEt()
#            l1_ntt[0] = bm.nTT()
#            l1_shape[0] = bm.shape()
#            l1_towerHoE[0] = bm.towerHoE()
#            l1_HwQual[0] = bm.hwQual()
#
#            L1_overlap.append(bm)
##            print 'removing', bm, 'from', L1_electrons
##            import pdb; pdb.set_trace()
##            L1_electrons.remove(bm)
##            print 'after removing', L1_electrons
#
#            
#        else:
#            l1_mindr[0] = 99
#            l1_pt[0] = 99
#            l1_eta[0] = 99
#            l1_phi[0] = 99
#        
#            l1_hwPt[0] = -1
#            l1_hwEta[0] = -1
#            l1_hwPhi[0] = -1
#            l1_iso[0] = -1
#            l1_toweriphi[0] = -1
#            l1_towerieta[0] = -1
#            l1_rawEt[0] = -1
#            l1_isoEt[0] = -1
#            l1_footprintEt[0] = -1
#            l1_ntt[0] = -1
#            l1_shape[0] = -1
#            l1_towerHoE[0] = -1
#            l1_HwQual[0] = -1
#
#
#
#        if maxdR < 0.4 and not (bm in L1_overlap):
#            L1_matched_electrons.append(bm)
#
#        tree.Fill()
#
#
#
#    gen_bpt[0] = gen_bs[0].pt()
#
#    if len(L1_matched_electrons)==2:
#        l1e_dr[0] = deltaR(L1_matched_electrons[0].eta(), L1_matched_electrons[0].phi(),
#                           L1_matched_electrons[1].eta(), L1_matched_electrons[1].phi())
#
#
##        e1 = TLorentzVector()
##        e2 = TLorentzVector()
##        e1.SetPtEtaPhiM()
##        import pdb; pdb.set_trace()
#        mee[0] = (L1_matched_electrons[0].p4() + L1_matched_electrons[1].p4()).M()
#
#
#    else:
#        l1e_dr[0] = 9
#        mee[0] = -9
#
#    pairtree.Fill()

    nevents += 1

print nevents, 'has been analyzed, while dropping', ndrop, 'events'

#output.Write()
#output.Close()

out.endJob()
