import nibabel as nb
import numpy as np
import torchio as tio
#import scitool.dataview_devel.pyqtgraph_gui as plt2D
#import pylab as plt
import os
import shutil

# Script uses TorchIO to resample the DWI and ADC map to the same resolution and number of slices as the T2-weighted images.
# # Input images in nifti (.nii.gz) format. Naming with {codenr}_{modalitynumber}.nii.gz. Modality number for T2 is 0001,
# for DWI 0002 and for ADC 0003. Example: '0001_0001.nii.gz' for code number 0001 and modality T2 (0001).
# Output will be in the same format.

os.makedirs("./output/", exist_ok=True)

datadir = './data/'
for dir_entry in os.scandir(datadir):
  filename=dir_entry.name
  if '_0002' in dir_entry.name:
    code_nr=filename.split('_')[0]
    print('Converting Case {}'.format(code_nr))
    
    #Loads T2, DWI and ADC
    imageT2 = tio.ScalarImage(datadir+"/{}_0001.nii.gz".format(code_nr))
    imagediff = tio.ScalarImage(datadir+"/{}_0002.nii.gz".format(code_nr))
    imageADC = tio.ScalarImage(datadir+"/{}_0003.nii.gz".format(code_nr))

    #Resamples DWI and ADC with T2 as target
    transforms=[
      tio.Resample(target=imageT2),
    ]
    transform = tio.Compose(transforms)
    resampledDWI = transform(imagediff)
    resampledADC = transform(imageADC)
    
    resampledDWI.save('./output/{}_0002.nii.gz'.format(code_nr))
    resampledADC.save('./output/{}_0003.nii.gz'.format(code_nr))

    #Copy the T2-weighted file to the output folder
    shutil.copyfile(datadir+"/{}_0001.nii.gz".format(code_nr), './output/{}_0001.nii.gz'.format(code_nr))


