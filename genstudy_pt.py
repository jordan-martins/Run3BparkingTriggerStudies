from ROOT import TFile, TTree, Double, TLorentzVector
from DataFormats.FWLite import Events, Handle
from common.deltar import deltaR
from TreeProducerGen import *

#files=['file:./root/MINIAOD.root']
files=['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18MiniAOD/BuToKee_MufilterPt6_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/MINIAODSIM/PUPoissonAve20_BParking_102X_upgrade2018_realistic_v15-v1/00000/01501E26-9276-7149-A74D-5E4B2E028DC8.root']

events = Events(files)
nevent = int(events.size())
print 'Number of files analyzed: ',len(files),' Total number of events: ',nevent

handle = Handle('std::vector<reco::GenParticle>')
label = ("prunedGenParticles")
out = TreeProducerGen('root/genstudy_pt.root')

nanalyzed = 0
ndropped = 0
for ievent,ev in enumerate(events):
    #if ievent > 10 : continue
    if ievent%1000==0: print('{0:.2f}% processed'.format(Double(ievent)/Double(nevent)*100.))
    ev.getByLabel(label, handle)
    gps = handle.product()
    gen_bs = [p for p in gps if abs(p.pdgId())==521] 
    genmuons = [p for p in gps if abs(p.pdgId()) == 13 and p.status()==1]

    if False : 
        print '-'*80
        for gen in gen_bs:
            print gen.pdgId(), 'ndaughters=', gen.numberOfDaughters()
            for ii in range(gen.numberOfDaughters()):
                print '\t d:', gen.daughter(ii).pdgId()
            print gen.pdgId(), 'nmothers=', gen.numberOfMothers()
            for ii in range(gen.numberOfMothers()):
                print '\t m:', gen.mother(ii).pdgId()

    bs = []
    genelectrons = None
    for p in gen_bs:
        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
        genelectrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
        bs.append(p)
    if len(bs)!=1: 
        ndropped += 1
        continue

    genelectrons = sorted(genelectrons, key = lambda e : e.pt(), reverse = True )
    genmuons = sorted(genmuons, key = lambda mu : mu.pt(), reverse = True )

    #print len(genelectrons)

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

    out.tree.Fill()
    nanalyzed += 1

print 'Number of events analyzed: ',nanalyzed,' Number of events dropped: ',ndropped
out.endJob()
