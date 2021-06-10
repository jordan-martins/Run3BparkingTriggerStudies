from ROOT import TGraphErrors, TCanvas, Double, TFile
import math, copy

lumis = ['L1p2', 'L1p3', 'L1p4', 'L1p5', 'L1p8']
runs = [322088, 322088, 322088, 322088, 322079]

graphs = []

const=Double(2544.*11200)

for pt in range(3,9):

    req = 'e1_pt > ' + str(pt) + ' && e2_pt > ' + str(pt) + '&& abs(e1_eta) < 1.0 && abs(e2_eta) < 1.0 && dr_1p0 < 1.'

    graph = TGraphErrors()
    graph.SetName('DoubleEG' + str(pt))
    graph.SetTitle('DoubleEG' + str(pt))
    graph.GetXaxis().SetTitle('Luminosity (E34)')
    graph.GetYaxis().SetTitle('Estimated Rate')
    
    
    idx = 0

    for run, lumi in zip(runs, lumis):

        file = TFile('rate_' + str(run) + '_' + lumi + '.root')
        tree = file.Get('tree')
        
        den = Double(tree.GetEntries())
        num = Double(tree.GetEntries(req))

       
        eff = num/den

        print 'num,den', num, den, eff

        efferr = math.sqrt(eff*(1-eff)/den)
        


        graph.SetPoint(idx, Double(lumi.replace('p','.').replace('L','')), eff*const)
        
        graph.SetPointError(idx, 0., efferr*const)

        idx += 1

    graphs.append(copy.deepcopy(graph))
        


output = TFile('rate_summary.root', 'recreate')

for graph in graphs:

    graph.Write()


output.Write()
output.Close()


    
