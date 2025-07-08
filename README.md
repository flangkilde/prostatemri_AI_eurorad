# prostatemri_AI

Welcome! 

Here we provide the scripts that were used for the article "Evaluation of AI for Prostate Cancer Detection in Biparametric-MRI Screening Population Data" in European Radiology. In the publication a nnU-Net were trained to detect clinically significant prostate cancer in biparametric MRI data from a screening population. All steps are explained below. Most of the scripts are python except the statistical analysis, which were done in R. 


Step 1 - Conversion to nifti and naming):

Before using the script, data has to be converted to the nifti format. The authors used DicomSort (https://github.com/dicomsort/dicomsort) and dcm2niix (https://github.com/rordenlab/dcm2niix) to perform this. Since the converstion to nifti has to adapted to the format of the original data, our script is not provided. We recommend reading the documentation for the applications instead. 
We used the naming convention listed in nnU-Net (https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_format.md). Our files are named as {codenr}_{modalitynumber}.nii.gz. Modality number for T2 is 0001, for DWI 0002 and for ADC 0003. Example: '0001_0001.nii.gz' for code number 0001 and modality T2 (0001).


Step 2 - Transformation:

With the input data in nifti format we then performed a transformation of the DWI and ADC images to match the resolution and number of slices of the T2-weighted images. The script uses TorchIO (https://torchio.readthedocs.io). Please see the script "Transform.py". 


Step 3 - Registration:

With the transformed data we then performed a rigid registration of the DWI b=0 image and the T2-weighted image with the b0 image as moving using Elastix (https://elastix.dev). The registration was then applied to the other b-values and the ADC map using Transformix (which is a part of Elastix). Please see the script "Registration.py". The parameter file use by the script is also available and should be located in the same folder. 

Step 4 - Annotation:

The reference masks to be used for training were created manually using ITK-snap (https://www.itksnap.org/pmwiki/pmwiki.php). The masks were named as "{codenr}.nii.gz".


Step 5 - Training of nnU-Net:
For complete documentation of the usage of nnU-Net please see their Github (https://github.com/MIC-DKFZ/nnUNet).

The commands that we used are listed in "nnUNet_execution.txt".


Step 6 - Statistical analysis:
For statistical analysis the reference (0 or 1), the maximum softmax value for that case and the PI-RADS from the primary evaluation was saved in an Excel file. The data were then analyzed with R to draw an ROC and calculate AUROC and CIs. 




