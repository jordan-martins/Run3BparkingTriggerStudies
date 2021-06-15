import copy, math, os
from numpy import array
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

gen_pt  = 'gen_e1_pt > 0.5 && gen_e2_pt > 0.5'
gen_eta = 'abs(gen_e1_eta) < 2.4 && abs(gen_e2_eta) < 2.4'
#gen_q2  = '(gen_mass*gen_mass) > 1.1 && (gen_mass*gen_mass) < 6.25'

#if options.q2 =='high': gen_q2 = 'gen_mass*gen_mass > 14.82'

gencut = ' && '.join([gen_pt, gen_eta]) #, gen_q2]) # don't apply gen_ q2 req.
print 'gencut = ', gencut

eff_histo = None
if options.weight:
    eff_file = TFile('root/eff.root')
    eff_histo = eff_file.Get('eff')
    print eff_histo, 'detected'

def calc(name, num, den):
    eff = num/den
    efferr = 0.
    if num!=0:
        efferr = math.sqrt(eff*(1-eff)/den)
    print "name:", name, " numer: ",num, " denom: ", den, " eff: ", eff, " err: ", efferr
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

    if type=='eff': 
        num = Double(tree.GetEntries(sel))

    if type=='ult': 
        if not options.weight:
            num = Double(tree.GetEntries(sel + ' && ' + gencut))
        else:
            num = 0
            ybins = eff_histo.GetYaxis().GetNbins()
            xbins = eff_histo.GetXaxis().GetNbins()
            for ybin in range(1,ybins+1):
                for xbin in range(1,xbins+1):
                    if xbin > ybin : continue
                    eff = eff_histo.GetBinContent(xbin,ybin)
                    y_down = eff_histo.GetYaxis().GetBinLowEdge(ybin)
                    y_up = eff_histo.GetYaxis().GetBinLowEdge(ybin) + eff_histo.GetYaxis().GetBinWidth(ybin)
                    x_down = eff_histo.GetXaxis().GetBinLowEdge(xbin)
                    x_up = eff_histo.GetXaxis().GetBinLowEdge(xbin) + eff_histo.GetXaxis().GetBinWidth(xbin)
                    gen_e1_pt = 'gen_e1_pt > ' + str(y_down)
                    if ybin < ybins : gen_e1_pt += ' && ' + 'gen_e1_pt < ' + str(y_up)
                    gen_e2_pt = 'gen_e2_pt > ' + str(x_down)
                    if xbin < xbins : gen_e2_pt += ' && ' + 'gen_e2_pt < ' + str(x_up)
                    newgencut = ' && '.join([gen_e1_pt, gen_e2_pt, gen_eta])
                    entry = Double(tree.GetEntries(sel + ' && ' + newgencut))
                    num += entry*eff
                
    print '-'*80
    eff, efferr = calc(graph.GetName(), num, den)

    if type == 'rate':
        sf = Double(2544*11200/1.8)

    graph.SetPoint(ipt, pt, eff*sf)
    graph.SetPointError(ipt, 0, efferr*sf)

ensureDir('plots/')
file2read = 'root/genstudy_l1.root'


if options.type == 'rate':
    file2read = 'root/rate_322079_L1p8.root'

sfile = TFile(file2read)

tree = sfile.Get('tree')

hists = []
titles = []

ptrange = np.arange(3, 11, 1).tolist()

graph_singleMu = createGraph('singleMu')

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
