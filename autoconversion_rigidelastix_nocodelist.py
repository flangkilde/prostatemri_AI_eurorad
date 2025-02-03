import os
import shutil
import nibabel as nb
import numpy as np
import torchio as tio
import sys


# Input images in nifti (.nii.gz) format. Naming with {codenr}_{modalitynumber}.nii.gz. Modality number for T2 is 0001,
# for high b-value 0002 and for ADC 0003. Example: '0001_0001.nii.gz' for code number 0001 and modality T2 (0001).
# Input segmentation masks in nifti (.nii.gz) format. Naming {codenr}.nii.gz. Example '0001.nii.gz' for code number 0001.
# Output will be in the same format.
#
# Parameters for Elastix are provided in "parameterFileRigid.txt".


input_path='./input/images/'                   #Folder with original images
work_path='./work_path/'                       #Folder for saving working files
output_path='./output/imagesTr/'               #Folder for saving output images 
input_mask_path='./input/masks/'               #Folder with original segmentation masks
output_mask_path='./output/labelsTr/'          #Folder for saving output masks

os.makedirs(output_path, exist_ok=True)
os.makedirs(work_path, exist_ok=True)
os.makedirs(output_mask_path, exist_ok=True)

for dir_entry in os.scandir(input_mask_path):
    filename=dir_entry.name
    codenr=filename.split('.')[0]
    if codenr=='':
        continue
    if os.path.exists(os.path.join(output_path,'{:04d}_0001.nii.gz'.format(int(codenr)))):
        print("Already registered... skipping...")
        continue

    else:
        if os.path.exists(os.path.join(input_path,'{:04d}_0001.nii.gz'.format(int(codenr)))):
            datacomplete=True
        else:
            datacomplete=False
            print('Data appears to be incomplete. Make sure that images and masks match in the input folder.')
            sys.exit()

        #Extract b0 and b1500
        os.makedirs(work_path+'/registeredelastix/res{:04d}'.format(int(codenr)), exist_ok=True)
        os.makedirs(work_path+'/extractedb/images/res{:04d}'.format(int(codenr)), exist_ok=True)
        if datacomplete:
            file_obj=nb.load(input_path+'/{:04d}_0002.nii.gz'.format(int(codenr)))
            arr=file_obj.get_fdata()
            nif_ex=nb.Nifti1Image(arr[...,0],file_obj.affine,file_obj.header)
            nb.save(nif_ex,work_path+'/extractedb/images/{:04d}_0002_b0.nii.gz'.format(int(codenr)))
            file_obj=nb.load(input_path+'/{:04d}_0002.nii.gz'.format(int(codenr)))
            arr=file_obj.get_fdata()
            nif_ex=nb.Nifti1Image(arr[...,3],file_obj.affine,file_obj.header)
            nb.save(nif_ex,work_path+'/extractedb/images/{:04d}_0002_b1500.nii.gz'.format(int(codenr)))
            
            
        

        os.makedirs(work_path+'/registeredelastix/res{:04d}'.format(int(codenr)), exist_ok=True)
        os.makedirs(work_path+'/registeredelastix/transformix/res{:04d}'.format(int(codenr)), exist_ok=True)

        #run elastic on T2 and b0 with b0 as moving image
        if 1==1:
            os.system('elastix -f {0:}/{1:04d}_0001.nii.gz -m {2:}/extractedb/images/{1:04d}_0002_b0.nii.gz '
                      '-out "{2:}/registeredelastix/res{1:04d}" -p parameterFileRigid.txt'.format(input_path, int(codenr), work_path))

        #apply the registration from above to b1500
        if 1==1:
            os.system('transformix -in {0:}/extractedb/images/{1:04d}_0002_b1500.nii.gz -out {2:}/registeredelastix/transformix/res{1:04d} -tp {2:}/registeredelastix/res{1:04d}/TransformParameters.0.txt'.format(work_path, int(codenr), work_path))
            file_obj=nb.load(work_path+'/registeredelastix/transformix/res{:04d}/result.nii'.format(int(codenr)))
            nb.save(file_obj, output_path+'/{:04d}_0002.nii.gz'.format(int(codenr)))

        #apply the registration from above to ADC
        if 1==1:
            os.system('transformix -in {0:}/{1:04d}_0003.nii.gz -out {2:}/registeredelastix/transformix/res{1:04d} -tp {2:}/registeredelastix/res{1:04d}/TransformParameters.0.txt'.format(input_path, int(codenr), work_path))
            file_obj2=nb.load(work_path+'/registeredelastix/transformix/res{:04d}/result.nii'.format(int(codenr)))
            nb.save(file_obj2, output_path+'/{:04d}_0003.nii.gz'.format(int(codenr)))

        #apply the registration from above to mask
        if 1==1:
            os.system('cp {0:}/registeredelastix/res{1:04d}/TransformParameters.0.txt {0:}/registeredelastix/res{1:04d}/TransformParametersMask.0.txt'.format(work_path, int(codenr)))
            os.system("sed -i '' 's/FinalBSplineInterpolationOrder 3/FinalBSplineInterpolationOrder 0/'  {0:}/registeredelastix/res{1:04d}/TransformParametersMask.0.txt".format(work_path, int(codenr)))
            os.system('transformix -in {0:}/{2:04d}.nii.gz -out {1:}/registeredelastix/transformix/res{2:04d} -tp {1:}/registeredelastix/res{2:04d}/TransformParametersMask.0.txt'.format(input_mask_path, work_path, int(codenr)))
            file_obj2=nb.load(work_path+'/registeredelastix/transformix/res{:04d}/result.nii'.format(int(codenr)))
            nb.save(file_obj2, output_mask_path+'/{:04d}.nii.gz'.format(int(codenr)))

        #copy T2 to outputpath
        if 1==1:
            shutil.copyfile('{0:}/{1:04d}_0001.nii.gz'.format(input_path, int(codenr), output_path),'{2:}/{1:04d}_0001.nii.gz'.format(input_path, int(codenr), output_path))

 
