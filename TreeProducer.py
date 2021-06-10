import ROOT
import math 
import numpy as np
from TreeProducerCommon import *

ptrange = np.arange(3, 11, 1).tolist() 

class TreeProducer(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducer is called for', name)
        super(TreeProducer, self).__init__(name,**kwargs)


        self.addBranch('nmuons',                  'i')
        self.addBranch('nelectrons',                  'i')

        self.addBranch('mu1_pt',                  'f')
        self.addBranch('mu1_eta',                  'f')

        self.addBranch('e1_pt',                  'f')
        self.addBranch('e1_eta',                  'f')

        for pt in ptrange:
            self.addBranch('doubleE' + str(pt),                  '?')

