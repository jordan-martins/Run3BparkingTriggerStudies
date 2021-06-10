import ROOT
import math 
import numpy as num 
from TreeProducerCommon import *

class TreeProducer_l1electron(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducer_l1electron is called for', name)
        super(TreeProducer_l1electron, self).__init__(name,**kwargs)


        self.addBranch('gen_ept',                  'f')
        self.addBranch('gen_eeta',                  'f')
        self.addBranch('l1e_pt',                  'f')
        self.addBranch('l1e_eta',                  'f')
        self.addBranch('l1e_dr',                  'f')
