import ROOT
import sys

filename = sys.argv[1]
print(filename)
f = ROOT.TFile(filename)
f.histfluka.Draw()

while True:
    pass
