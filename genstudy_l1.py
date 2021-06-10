from DataFormats.FWLite import Events, Handle
from common.deltar             import deltaR, bestMatch
from ROOT import TFile, TTree, Double, TLorentzVector
from array import array
import math, copy
from os import listdir
from os.path import isfile, join
from TreeProducerGen import *


mypath='/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/'

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles = onlyfiles[0:1000]

#onlyfiles = '/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/AOD_BparkingTriggerStudy_nomufilter_5753.root'

events = Events(onlyfiles)
#events = Events()

Nevt = int(events.size())
print len(onlyfiles), 'files are analyzed. Total # of events = ', Nevt


##################################################
handle  = Handle ('std::vector<reco::GenParticle>')
label = ("genParticles")

handle_e  = Handle ('BXVector<l1t::EGamma>')
label_e = ("gtStage2Digis", "EGamma")

handle_mu  = Handle ('BXVector<l1t::Muon>')
label_mu = ("gtStage2Digis", "Muon")

##################################################

nevents = 0
ndrop = 0

out = TreeProducerGen('genstudy_l1_signal_' + str(len(onlyfiles)) + 'files_'  + str(Nevt) + 'events.root')

ptrange = np.arange(3, 11, 1).tolist() 

for ev in events:

    

    if nevents%1000==0: print('{0:.2f}'.format(Double(nevents)/Double(Nevt)*100.), '% processed')

#    gps = handle.product()

#    gps_muons = sorted([p for p in gps if abs(p.pdgId())==13 and p.status()==1 and abs(p.eta()) < 2.4 ], key = lambda mu : mu.pt(), reverse = True )
#    gps_muons_1p5 = sorted([p for p in gps if abs(p.pdgId())==13 and p.status()==1 and abs(p.eta()) < 1.5], key = lambda mu : mu.pt(), reverse = True )
#    gps_electrons = sorted([p for p in gps if abs(p.pdgId())==11 and p.status()==1 and abs(p.eta()) < 2.7], key = lambda e : e.pt(), reverse = True )
#    gps_electrons_1p0 = sorted([p for p in gps if abs(p.pdgId())==11 and p.status()==1 and abs(p.eta()) < 1.], key = lambda e : e.pt(), reverse = True )


    ####################################
    # gen
    ####################################

    ev.getByLabel(label, handle)
    gps = handle.product()


    gen_bs = [p for p in gps if abs(p.pdgId())==521] 

    genmuons = [p for p in gps if abs(p.pdgId()) == 13 and p.status()==1]

#    print '-'*80
#
#    for gen in gen_bs:
#        print gen.pdgId(), 'ndaughters=', gen.numberOfDaughters()
#        for ii in range(gen.numberOfDaughters()):
#            print '\t d:', gen.daughter(ii).pdgId()
#
#        print gen.pdgId(), 'nmothers=', gen.numberOfMothers()
#        
#        for ii in range(gen.numberOfMothers()):
#            print '\t m:', gen.mother(ii).pdgId()


    
    
 
    bs = []
    genelectrons = None

    for p in gen_bs:

        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
        
        genelectrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
        bs.append(p)
        



    if len(bs)!=1: 
        ndrop += 1
        continue
        

    genelectrons = sorted(genelectrons, key = lambda e : e.pt(), reverse = True )
    genmuons = sorted(genmuons, key = lambda mu : mu.pt(), reverse = True )

#    print len(genelectrons)

    out.gen_e1_pt[0] = genelectrons[0].pt()
    out.gen_e1_eta[0] = genelectrons[0].eta()
    out.gen_e2_pt[0] = genelectrons[1].pt()
    out.gen_e2_eta[0] = genelectrons[1].eta()
    out.gen_dr[0] = deltaR(genelectrons[0].eta(), genelectrons[0].phi(), genelectrons[1].eta(), genelectrons[1].phi())
    out.gen_mass[0] = (genelectrons[0].p4() + genelectrons[1].p4()).M()
    out.gen_b_pt[0] = bs[0].pt()
    out.gen_b_eta[0] = bs[0].eta()
    out.gen_b_phi[0] = bs[0].phi()

    out.ngenmuons[0] = len(genmuons)
    out.ngenelectrons[0] = len(genelectrons)


    #########################



    ev.getByLabel(label_mu, handle_mu)
    muons = handle_mu.product()

    L1_muons = []

    for jj in range(muons.size(0)):
        L1_muons.append(muons.at(0,jj))


    ev.getByLabel(label_e, handle_e)
    electrons = handle_e.product()

    L1_electrons = []


    for jj in range(electrons.size(0)):
        L1_electrons.append(electrons.at(0,jj))


#    L1_muons = sorted([mu for mu in L1_muons if mu.hwQual() >= 12], key = lambda mu : mu.pt(), reverse = True)
#    L1_electrons = sorted([e for e in L1_electrons if abs(e.eta()) < 2.4], key = lambda e : e.pt(), reverse = True)

    L1_muons = sorted([mu for mu in L1_muons if mu.hwQual() >= 12 and abs(mu.eta()) < 1.5], key = lambda mu : mu.pt(), reverse = True)
    L1_electrons = sorted([e for e in L1_electrons if abs(e.eta()) < 1.], key = lambda e : e.pt(), reverse = True)


    out.nmuons[0] = len(L1_muons)

    out.nelectrons[0] = len(L1_electrons)

#    flag_singleE = [False for i in range(ptrange)]

#    for ii, pt in enumerate(ptrange):
#
#        flag = False
#
#        for ge in genelectrons:
#            bm, maxdR = bestMatch(ge, L1_electrons)
#
#            if bm!=None and maxdR < 0.4 and bm.pt() >= pt:
#                flag = True
                
            
    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons)
    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons)
#    bm_mu, maxdR_mu = bestMatch(genelectrons[1], L1_electrons)

    if bm_e1!=None and maxdR_e1 < 0.4:
        out.e1_pt[0] = bm_e1.pt()
        out.e1_eta[0] = bm_e1.eta()
    else:
        out.e1_pt[0] = -1
        out.e1_eta[0] = -1
        
    if bm_e2!=None and maxdR_e2 < 0.4:
        out.e2_pt[0] = bm_e2.pt()
        out.e2_eta[0] = bm_e2.eta()
    else:
        out.e2_pt[0] = -1
        out.e2_eta[0] = -1



    for ii, pt in enumerate(ptrange):

        flag = False

        for gm in genmuons:

            bm_mu, maxdR_mu = bestMatch(gm, L1_muons)

            if bm_mu!=None and maxdR_mu < 0.4 and bm_mu.pt() >= pt:
        
                flag = True


        if pt==3:
            out.singleMu3[0] = flag
        elif pt==4:
            out.singleMu4[0] = flag
        elif pt==5:
            out.singleMu5[0] = flag
        elif pt==6:
            out.singleMu6[0] = flag
        elif pt==7:
            out.singleMu7[0] = flag
        elif pt==8:
            out.singleMu8[0] = flag
        elif pt==9:
            out.singleMu9[0] = flag
        elif pt==10:
            out.singleMu10[0] = flag
        else:
            print 'Not expected !!!'




    # di-electron seed 

    L1_electrons_dynamic = copy.deepcopy(L1_electrons)
    

    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons_dynamic)

    
    if bm_e1!=None and maxdR_e1 < 0.4:
#        print 'before', len(L1_electrons_dynamic)
        L1_electrons_dynamic.remove(bm_e1)
#        print 'after', len(L1_electrons_dynamic)

    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons_dynamic)     

    for ii, pt in enumerate(ptrange):

        flag = False

        if bm_e1!=None and bm_e2!=None and maxdR_e1 < 0.4 and maxdR_e2 < 0.4 and bm_e1.pt() >= pt and bm_e2.pt() >= pt and deltaR(bm_e1.eta(), bm_e1.phi(), bm_e2.eta(), bm_e2.phi()) < 1.:
            flag = True

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



        
        
        


#    if bm_mu!=None and maxdR_mu < 0.4:
#        out.mu1_pt[0] = bm_mu.pt()
#        out.mu1_eta[0] = bm_mu.eta()
#    else:
#        out.mu1_pt[0] = -1
#        out.mu1_eta[0] = -1





#    if out.nelectrons[0]>1:
#        out.e2_pt[0] = L1_electrons[1].pt()
#        out.e2_eta[0] = L1_electrons[1].eta()
##        out.e2_phi[0] = L1_electrons[1].phi()
#        out.dr[0] = deltaR(L1_electrons[0].eta(), L1_electrons[0].phi(), L1_electrons[1].eta(), L1_electrons[1].phi())
#
#
#        # check gen. matching
#        dR_11 = deltaR(L1_electrons[0].eta(),L1_electrons[0].phi(), genelectrons[0].eta(), genelectrons[0].phi())
#        dR_12 = deltaR(L1_electrons[0].eta(),L1_electrons[0].phi(), genelectrons[1].eta(), genelectrons[1].phi())
#        dR_21 = deltaR(L1_electrons[1].eta(),L1_electrons[1].phi(), genelectrons[0].eta(), genelectrons[0].phi())
#        dR_22 = deltaR(L1_electrons[1].eta(),L1_electrons[1].phi(), genelectrons[1].eta(), genelectrons[1].phi())
#
#        if (dR_11 < 0.4 and dR_22 < 0.4) or (dR_12 < 0.4 and dR_21 < 0.4):
#            out.ismatch[0] = 1
#        else:
#            out.ismatch[0] = 0
#        
#
#    else:
#        out.e2_pt[0] = -1
#        out.e2_eta[0] = -1
##        out.e2_phi[0] = -1
#        out.dr[0] = -1
#        out.ismatch[0] = -1



    out.tree.Fill()


    nevents += 1

print nevents, 'has been analyzed, while dropping', ndrop, 'events'

out.endJob()
