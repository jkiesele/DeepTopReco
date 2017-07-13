


from TrainData import TrainData,fileTimeOut
import numpy

class TrainData_topreco_base(TrainData):
    
    def __init__(self):
        TrainData.__init__(self)
        
        import c_meanNormZeroPad
        c_meanNormZeroPad.setTreeName("data")
        
        self.treename="data"
        self.allbranchestoberead=[]
        self.undefTruth=[]
        self.truthclasses=['']