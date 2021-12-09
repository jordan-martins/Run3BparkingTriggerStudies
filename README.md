# Trigger studies for a BParking data set during Run 3

This code is used to estimate the Level-1 performance of various trigger configurations aimed at an RK analysis in Run 3.

Setup CMSSW:
```
cmsrel CMSSW_11_1_0
cd CMSSW_11_1_0/src
```

clone the repository: 
```
git clone git@github.com:gitytakahas/Run3BparkingTriggerStudies.git
git checkout forJordan
```



## Produce ntuples for trigger efficiency and rate estimation

Produce ntuples:
```
python genstudy_l1.py
```

You can then add whatever you want ... 

