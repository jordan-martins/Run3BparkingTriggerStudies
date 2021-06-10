from DataFormats.FWLite import Events, Handle
from deltar             import deltaR, bestMatch
from ROOT import TFile, TTree, Double, TLorentzVector
from array import array
import math
from os import listdir
from os.path import isfile, join
from TreeProducer import *


mypath='/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/'

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles = onlyfiles[0:100]

events = Events(onlyfiles)
#events = Events('/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/AOD_BparkingTriggerStudy_nomufilter_5753.root')

Nevt = int(events.size())
print len(onlyfiles), 'files are analyzed. Total # of events = ', Nevt


##################################################
handle  = Handle ('std::vector<reco::GenParticle>')
label = ("genParticles")

##################################################

nevents = 0
ndrop = 0

out = TreeProducer('genstudy_signal_' + str(len(onlyfiles)) + 'files_'  + str(Nevt) + 'events.root')


for ev in events:

    ev.getByLabel(label, handle)

    if nevents%1000==0: print('{0:.2f}'.format(Double(nevents)/Double(Nevt)*100.), '% processed')

    gps = handle.product()

    gps_muons = sorted([p for p in gps if abs(p.pdgId())==13 and p.status()==1 and abs(p.eta()) < 2.4 ], key = lambda mu : mu.pt(), reverse = True )
    gps_muons_1p5 = sorted([p for p in gps if abs(p.pdgId())==13 and p.status()==1 and abs(p.eta()) < 1.5], key = lambda mu : mu.pt(), reverse = True )
    gps_electrons = sorted([p for p in gps if abs(p.pdgId())==11 and p.status()==1 and abs(p.eta()) < 2.7], key = lambda e : e.pt(), reverse = True )
    gps_electrons_1p0 = sorted([p for p in gps if abs(p.pdgId())==11 and p.status()==1 and abs(p.eta()) < 1.], key = lambda e : e.pt(), reverse = True )


#    print '-'*80
#    for ii, imuon in enumerate(gps_muons):
#        print '\t muon', ii, imuon.pt()
#
#    for ii, ielectron in enumerate(gps_electrons):
#        print '\t electron:', ii, ielectron.pt()

    out.nmuons[0] = len(gps_muons)
    out.nmuons_1p5[0] = len(gps_muons_1p5)

    out.nelectrons[0] = len(gps_electrons)
    out.nelectrons_1p0[0] = len(gps_electrons_1p0)

    if out.nmuons[0]!=0:
        out.mu1_pt[0] = gps_muons[0].pt()
        out.mu1_eta[0] = gps_muons[0].eta()
    else:
        out.mu1_pt[0] = -1
        out.mu1_eta[0] = -1

    if out.nmuons_1p5[0]!=0:
        out.mu1_pt_1p5[0] = gps_muons_1p5[0].pt()
        out.mu1_eta_1p5[0] = gps_muons_1p5[0].eta()
    else:
        out.mu1_pt_1p5[0] = -1
        out.mu1_eta_1p5[0] = -1

        
    if out.nelectrons[0]!=0:
        out.e1_pt[0] = gps_electrons[0].pt()
        out.e1_eta[0] = gps_electrons[0].eta()
    else:
        out.e1_pt[0] = -1
        out.e1_eta[0] = -1

    if out.nelectrons_1p0[0]!=0:
        out.e1_pt_1p0[0] = gps_electrons_1p0[0].pt()
        out.e1_eta_1p0[0] = gps_electrons_1p0[0].pt()
    else:
        out.e1_pt_1p0[0] = -1
        out.e1_eta_1p0[0] = -1



    if out.nelectrons[0]>1:
        out.e2_pt[0] = gps_electrons[1].pt()
        out.e2_eta[0] = gps_electrons[1].eta()
#        import pdb; pdb.set_trace()
        out.dr[0] = deltaR(gps_electrons[0].eta(), gps_electrons[0].phi(), gps_electrons[1].eta(), gps_electrons[1].phi())
    else:
        out.e2_pt[0] = -1
        out.e2_eta[0] = -1
        out.dr[0] = -1

    if out.nelectrons_1p0[0]>1:
        out.e2_pt_1p0[0] = gps_electrons_1p0[1].pt()
        out.e2_eta_1p0[0] = gps_electrons_1p0[1].eta()
        out.dr_1p0[0] = deltaR(gps_electrons_1p0[0].eta(), gps_electrons_1p0[0].phi(), gps_electrons_1p0[1].eta(), gps_electrons_1p0[1].phi())
    else:
        out.e2_pt_1p0[0] = -1
        out.e2_eta_1p0[0] = -1
        out.dr_1p0[0] = -1



    gps_bs = [p for p in gps if abs(p.pdgId())==521] 
 
    bs = []
    electrons = None

    for p in gps_bs:

        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
        
        electrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
        bs.append(p)
        



    if len(bs)!=1: 
        ndrop += 1
        continue
        

    electrons = sorted(electrons, key = lambda e : e.pt(), reverse = True )

    out.kee_e1_pt[0] = electrons[0].pt()
    out.kee_e1_eta[0] = electrons[0].eta()
    out.kee_e2_pt[0] = electrons[1].pt()
    out.kee_e2_eta[0] = electrons[1].eta()

    out.kee_dr[0] = deltaR(electrons[0].eta(), electrons[0].phi(), electrons[1].eta(), electrons[1].phi())
    out.kee_mass[0] = (electrons[0].p4() + electrons[1].p4()).M()

    out.b_pt[0] = bs[0].pt()
    out.b_eta[0] = bs[0].eta()

    out.tree.Fill()

#    ev.getByLabel(label_e, handle_e)
#    electrons = handle_e.product()
#
#    L1_electrons = []
#
#    for jj in range(electrons.size(0)):
#        L1_electrons.append(electrons.at(0,jj))
#
#
#    L1_electrons = sorted([e for e in L1_electrons], key = lambda e : e.pt(), reverse = True)
#    L1_overlap = []
#
#    L1_matched_electrons = []
#
#    for ielectron, gen_electron in enumerate(gen_electrons):
#
#        bm, maxdR = bestMatch(gen_electron, L1_electrons)
#        
#        gen_ept[0] = gen_electron.pt()
#        gen_eeta[0] = gen_electron.eta()
#        gen_ephi[0] = gen_electron.phi()
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
