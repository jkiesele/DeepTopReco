
export DEEPTOPRECO=`pwd`/../
cd ../../DeepJet/environment
source lxplus_env.sh
export PATH=$DEEPTOPRECO/scripts:$PATH
export PYTHONPATH=$DEEPTOPRECO/modules:$PYTHONPATH
export LD_LIBRARY_PATH=$DEEPTOPRECO/modules:$LD_LIBRARY_PATH
cd -

echo "DeepTopReco environment set up"