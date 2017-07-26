

from TrainData_topreco_base import TrainData_topreco_base,fileTimeOut
import numpy

class TrainData_topreco(TrainData_topreco_base):
    
    def __init__(self):
        TrainData_topreco_base.__init__(self)
        
        ##
        ## register any branch you use later here.
        ## exceptions are branches that are added with addBranch (see below)
        ## it does not harm to add branches twice.
        ##
        self.registerBranches(['gen_mttbar','met_phi'])
        
        self.weightbranchX='gen_mttbar'
        
        self.referenceclass='flatten'
        self.weight_binX = numpy.array([
                350,360,370,380,400,425,450,500,
                600,700],dtype=float)
        
        
        self.weightbranchY='met_phi' #just a dummy branch for now. needs to be different from x branch. 
        # this input is needed for 2D reco
        
        #make just one bin - no reweighting in second variable
        self.weight_binY = numpy.array(
            [-5,5],
            dtype=float
            )
        
        
        ###########################################################################################
        ########################## #define the branches to be read ################################
        ###########################################################################################
        #global variables
        #self.addBranches(['nj','nl','nb']) 
        #one lepton
        self.addBranches(['l_pt','l_eta','l_phi','l_m'],1) 
        #one met - the explicit 1 can be omitted
        self.addBranches(['met_pt','met_phi']) 
        #six  jets
        self.addBranches(['j_pt','j_eta','j_phi','j_m'],6) 
        #and the chi2 mttbar
        self.addBranches(['mttbar_chi']) 
        
        
        self.regressiontargetclasses=['reg_mttbar']
        
        
    def readFromRootFile(self,filename,TupleMeanStd, weighter):
        
        from preprocessing import MeanNormZeroPad, MeanNormZeroPadParticles
        import numpy
        from stopwatch import stopwatch
        
        sw=stopwatch()
        swall=stopwatch()
        
        import ROOT
        
        fileTimeOut(filename,120) #give eos two minute to recover
        rfile = ROOT.TFile(filename)
        tree = rfile.Get(self.treename)
        self.nsamples=tree.GetEntries()
        Tuple = self.readTreeFromRootToTuple(filename)
        
        ###########################################################################################
        ############ this is where you define how to read in the branches and what to do with them
        ###########################################################################################
        
        
        
        
        ############ MeanNormZeroPad means that all branches are just put into a serial list
        ############ such as: jet1_pt, jet1_eta, jet2_pt, jet2_eta, ...
        ############ if there are not suffiecient jets, the rest of the list is filled
        ############ with zero (zero padding)
        ############ In addition, the variables are transformed such that they are centred around
        ############ zero and the width of the distribution is about 1.
        ############ This is only a technica trick that makes it easier for the DNN to converge
        reco_global = MeanNormZeroPad(filename,TupleMeanStd,
                                   self.branches,
                                   self.branchcutoffs,self.nsamples)
        
        ############ Another choice for the preprocessing that will be important for you is
        ############ MeanNormZeroPadParticles. It does the same rescaling as MeanNormZeroPad, 
        ############ but organises the array as a 2D array per event. Such that e.g. each 
        ############ jet has its own list. This can be important when e.g. using more
        ############ evolved neural networks than just dense layers. We will come to this later,
        ############ however, I put an example already here (but commented)
        #reco_jetslist = MeanNormZeroPadParticles(filename,TupleMeanStd,
        #                           self.branches[3],      # the jet branches (see function above)
        #                           self.branchcutoffs[3], # the jet branch cut-offs (maximum six) as defined above
        #                           self.nsamples)
        
        
        ############ Here we read the branch that contains the truth information
        truth = Tuple['gen_mttbar']
        
        
        
        oldlength=self.nsamples
        if self.remove:
            notremoves=weighter.createNotRemoveIndices(Tuple)
            # this has do be done for each array produced before
            # don't forget!
            # it selects only the entries from the array that should not be removed,
            # (where the notremoves array as an entry above 0)
            reco_global=reco_global[notremoves > 0]
            truth=truth[notremoves > 0]
            
            
            print("kept "+str(int(float(self.nsamples)/float(oldlength))*100)+"%" )
            
        # we don't use weights for now, so we fill the weight array with 1
        weights=numpy.empty(self.nsamples)
        weights.fill(1.)
        self.nsamples=truth.shape[0]
        
        
        # any array that shoul dbe used by the DNN needs to be added here
        # w: these are the weights (you don't have to change this)
        # x: this is the reconstructed information to fill
        # y: the true information
        self.w=[weights]
        self.x=[reco_global]
        self.y=[truth]
        
        
        
        
        
        
        
        
        
        
        
        