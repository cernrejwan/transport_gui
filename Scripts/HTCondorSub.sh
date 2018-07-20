#!/bin/bash

# Author: Michael.Bacak@cern.ch
# Date:   2 October 2017

fileName=$1.CondorSub.sh
rm -rf $fileName

HTsubfileName=$1
HToutputfileName=$1.outHT
HTerrputfileName=$1.errHT
HTlogputfileName=$1.logHT

echo 'executable            = ' $HTsubfileName >> $fileName
echo 'arguments             = ' >> $fileName
echo 'output                = ' $HToutputfileName >> $fileName
echo 'error                 = ' $HTerrputfileName >> $fileName
echo 'log                   = ' $HTlogputfileName >> $fileName
echo '+JobFlavour           = "tomorrow" ' >> $fileName
echo 'queue' >> $fileName

chmod +x $1
chmod +x $fileName
