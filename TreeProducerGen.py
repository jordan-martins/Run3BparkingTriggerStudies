import ROOT
import math 
import numpy as np
from TreeProducerCommon import *

ptrange = np.arange(3, 11, 1).tolist() 

class TreeProducerGen(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducerGen is called for', name)
        super(TreeProducerGen, self).__init__(name,**kwargs)


        self.addBranch('nmuons',                  'i')
        self.addBranch('nelectrons',                  'i')

#        self.addBranch('mu1_pt',                  'f')
#        self.addBranch('mu1_eta',                  'f')

        self.addBranch('e1_pt',                  'f')
        self.addBranch('e1_eta',                  'f')
        self.addBranch('e2_pt',                  'f')
        self.addBranch('e2_eta',                  'f')

        for pt in ptrange:
            self.addBranch('doubleE' + str(pt),                  '?')
            self.addBranch('singleMu' + str(pt),                  '?')
            

#        self.addBranch('dr',                  'f')
#        self.addBranch('ismatch',                  'i')



        self.addBranch('gen_e1_pt',                  'f')
        self.addBranch('gen_e1_eta',                  'f')
        self.addBranch('gen_e2_pt',                  'f')
        self.addBranch('gen_e2_eta',                  'f')
        self.addBranch('gen_dr',                  'f')
        self.addBranch('gen_mass',                  'f')

        self.addBranch('gen_b_pt',                  'f')
        self.addBranch('gen_b_eta',                  'f')
        self.addBranch('gen_b_phi',                  'f')

        self.addBranch('ngenmuons',                  'i')
        self.addBranch('ngenelectrons',                  'i')


        def finalDaughters(particle, daughters):
            '''Fills daughters with all the daughters of particle.
            Recursive function.'''

            if particle.numberOfDaughters() == 0:
                daughters.append(particle)
            else:
                foundDaughter = False
                for i in range( particle.numberOfDaughters() ):
                    dau = particle.daughter(i)

                    if dau.status() >= 1:
                        daughters = finalDaughters( dau, daughters )
                        foundDaughter = True

                if not foundDaughter:
                    daughters.append(particle)

            return daughters
