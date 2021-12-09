# Trigger studies for a BParking data set during Run 3

This code is used to estimate the Level-1 performance of various trigger configurations aimed at an RK analysis in Run 3.


log in to lxplus (You better setup this at lxplus as the input files are sitting at eos so it is easier for you to access ...)
```
ssh your_username@lxplus7.cern.ch
```


Setup CMSSW:
```
cmsrel CMSSW_11_1_0
cd CMSSW_11_1_0/src
```

clone the repository: 
```
git clone git@github.com:gitytakahas/Run3BparkingTriggerStudies.git
cd Run3BparkingTriggerStudies
git checkout forJordan
```



## Produce ntuples for trigger efficiency study

Produce ntuples:
```
python genstudy_l1.py
```


## Produce ntuples for the rate study 

Please first check what is written at: https://twiki.cern.ch/twiki/bin/view/CMS/HowToL1TriggerMenu#2_General_steps_of_L1_menu_studi

Produce ntuples:
```
python rate.py
```


In both efficiency and the rate study, you can add jet object ... (for this you need to investigate how to derive Level-1 jet object).

For consultation, you can always as HLT matter most: 
https://mattermost.web.cern.ch/cms-tsg/channels/hlt-user-support


