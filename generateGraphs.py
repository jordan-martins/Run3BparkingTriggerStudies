import copy, math, os
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TGraphErrors, Double
from DisplayManager import DisplayManager, add_Preliminary, add_CMS, add_label
from officialStyle import officialStyle
from array import array
import numpy as np

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)


from optparse import OptionParser, OptionValueError
usage = "usage: python runTauDisplay_BsTauTau.py"
parser = OptionParser(usage)

parser.add_option("-t", "--type", default='ult', type="string", help="type [rate, eff, anal, ult]", dest="type")
parser.add_option('-w', '--weight', action="store_true", default=False, dest='weight')
parser.add_option("-q", "--q2", default='low', type="string", help="q2 [low, high]", dest="q2")


(options, args) = parser.parse_args()

print options

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]

gencut = 'gen_e1_pt > 5. && gen_e2_pt > 5. && abs(gen_e1_eta) < 2.4 && abs(gen_e2_eta) < 2.4'   # github default
#gencut = 'gen_e1_pt > 5. && gen_e2_pt > 5. && abs(gen_e1_eta) < 1.5 && abs(gen_e2_eta) < 1.5'   # yuta's talk
#gencut = 'gen_e1_pt > 0.5 && gen_e2_pt > 0.5 && abs(gen_e1_eta) < 1.5 && abs(gen_e2_eta) < 1.5' # 2018
#gencut = '1'

q2cut = '1.1 < gen_mass*gen_mass && gen_mass*gen_mass < 6.25'
#q2cut = '1'

if options.q2 =='high':
    q2cut = 'gen_mass*gen_mass > 14.82'

gencut = '&&'.join([gencut, q2cut])

print 'gencut = ', gencut

pdf = None

if options.weight:
#    pdffile = TFile('root/pdf.root')
    pdffile = TFile('root/pdf_subleading.root')
    pdf = pdffile.Get('pdf')
    pdf.Scale(1./pdf.GetSumOfWeights())

    print pdf, 'detected'

def calc(name, num, den):
    eff = num/den

    efferr = 0.


    if num!=0:
        efferr = math.sqrt(eff*(1-eff)/den)

    print name, num, den, eff, efferr

    return eff, efferr


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def createGraph(name):

    graph = TGraphErrors()            
    graph.SetName(name)
    graph.SetTitle(name)

    return copy.deepcopy(graph)


def fillGraph(tree, type, sel, gencut, graph, ipt, pt):

    sf = Double(1.)

    den = Double(tree.GetEntries())
    num = Double(tree.GetEntries(sel))

    if type=='anal': 
        den = Double(tree.GetEntries(sel))
        num = Double(tree.GetEntries(sel + ' && ' + gencut))

    if type=='ult': 

        if not options.weight:
            num = Double(tree.GetEntries(sel + ' && ' + gencut))            

        if options.weight:

            num = 0

            for ibin in range(1,pdf.GetXaxis().GetNbins()+1):
                frac = pdf.GetBinContent(ibin)
                threshold_down = pdf.GetBinLowEdge(ibin)
                threshold_up = pdf.GetBinLowEdge(ibin) + pdf.GetBinWidth(ibin)


#                print threshold

                newgencut = copy.deepcopy(gencut)
#                newgencut = newgencut.replace('gen_e1_pt > 2 && gen_e2_pt > 2', 'gen_e1_pt > ' + str(threshold) + ' && gen_e2_pt > ' + str(threshold))
                newgencut = newgencut.replace('gen_e1_pt > 2 && gen_e2_pt > 2', 'gen_e2_pt > ' + str(threshold_down))
                

                num_i = Double(tree.GetEntries(sel + ' && ' + newgencut))

                print sel + ' && ' + newgencut, 'count =', num_i, 'frac = ', frac, 'effective=', frac*num_i
#                print 
#                print '(down, up) =', threshold_down, threshold_up,frac, num_i, frac*num_i


                num += frac*num_i

                
                


    print '-'*80
    eff, efferr = calc(graph.GetName(), num, den)

    if type == 'rate':
        sf = Double(2544*11200/1.8)


    graph.SetPoint(ipt, pt, eff*sf)
    graph.SetPointError(ipt, 0, efferr*sf)




ensureDir('plots/')


#file2read = 'root/genstudy_l1_signal_1500files_354036events.root'
file2read = 'root/genstudy_l1.root'


if options.type == 'rate':
    file2read = 'root/rate_322079_L1p8.root'

sfile = TFile(file2read)

tree = sfile.Get('tree')

hists = []
titles = []

#ptrange = np.arange(3, 11, 0.5).tolist()
ptrange = np.arange(3, 11, 1).tolist()





graph_singleMu = createGraph('singleMu')

#gencut = 'gen_e1_pt > 2. && gen_e2_pt > 2 && abs(gen_e1_eta) < 2.4 && abs(gen_e2_eta) < 2.4'
for ipt, pt in enumerate(ptrange):
    
    sel = 'singleMu' + str(pt) + '==1'
    
    if options.type=='rate':
        sel = 'mu1_pt >= ' + str(pt)

    fillGraph(tree, options.type, sel, gencut, graph_singleMu, ipt, pt)


graphs_MuE = []

for ipt_mu, pt_mu in enumerate(ptrange):

    graph_MuE = createGraph('Mu' + str(pt_mu))

    for ipt_e, pt_e in enumerate(ptrange):
        
        sel = 'singleMu' + str(pt_mu) + '==1 && (e1_pt >= ' + str(pt_e) + ' || e2_pt >= ' + str(pt_e) + ') '

        if options.type=='rate':
            sel = 'mu1_pt >= ' + str(pt_mu) + '&& e1_pt >=' + str(pt_e)


        fillGraph(tree, options.type, sel, gencut, graph_MuE, ipt_e, pt_e)

        
    graphs_MuE.append(graph_MuE)




graph_DoubleE_dR = createGraph('DoubleE_dR')

for ipt_e, pt_e in enumerate(ptrange):

    sel = 'doubleE' + str(pt_e) + '==1'

    fillGraph(tree, options.type, sel, gencut, graph_DoubleE_dR, ipt_e, pt_e)



out = TFile('plot_' + options.type + '.root', 'recreate')

graph_singleMu.Write()
graph_DoubleE_dR.Write()

for graph in graphs_MuE:
    graph.Write()

out.Write()
out.Close()





