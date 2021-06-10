import ROOT
import math 
import numpy as num 
from TreeProducerCommon import *

class TreeProducer_l1muon(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducer_l1muon is called for', name)
        super(TreeProducer_l1muon, self).__init__(name,**kwargs)


        self.addBranch('gen_mupt',                  'f')
        self.addBranch('gen_mueta',                  'f')
        self.addBranch('l1mu_pt',                  'f')
        self.addBranch('l1mu_eta',                  'f')
        self.addBranch('l1mu_dr',                  'f')
