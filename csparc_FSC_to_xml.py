#!/usr/bin/env python

#### reads a FSC text file from cryoSPARC and converts to FSC xml for emdb deposition
#### uses (box*px)/wavenumber for resolution in angstrom
#### reports the masked-corrected FSC

import sys
errmsg = '\nUSAGE: csparc_FSC_to_xml.py <csparc textfile> <boxsize in px> <pixel size in Angstrom>'

try:
    fscfile = open(sys.argv[1],'r').readlines()
except:
    sys.exit('ERROR: Error reading FSC text file{0}'.format(errmsg))

try:
    box = float(sys.argv[2])
except:
    sys.exit('ERROR: Invalid box size {0}'.format(errmsg))

try:
    px = float(sys.argv[3])
except:
    sys.exit('ERROR: Invalid pixel size {0}'.format(errmsg))


filename = sys.argv[1].split('/')[-1].split('.')[0]
outfscfile = open('FSC_{0}.xml'.format(filename),'w')
outfscfile.write('<fsc title="cryoSPARC masked-corrected FSC" xaxis="Resolution (A-1)" yaxis="Correlation Coefficient">')
print('RES\t1/RES\tCC')
pastcutoff = False
for i in fscfile[1:]:
    line = i.split()
    wavenumber = float(line[0])
    cc = float(line[4])
    resolution = (box*px)/wavenumber
    outfscfile.write('''
  <coordinate>
    <x>{0}</x>
    <y>{1}</y>
  </coordinate>'''.format(1/resolution,cc))
    if cc< 0.143 and pastcutoff == False:
        print('------------------------')
        pastcutoff = True
    print('{0}\t{1}\t{2}'.format(round(resolution,2),round(1/resolution,3),round(cc,3)))

outfscfile.write('\n</fsc>')