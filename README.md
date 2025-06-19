# prostatemri_AI

Welcome! 

Here we provide the scripts that were used for a publication in European Radiology. In the publication a nnU-Net were trained to detect clinically significant prostate cancer in biparametric MRI data from a screening population. All steps are explained below. Most of the scripts are python except the statistical analysis, which were done in R. 


Step 1 - Conversion to nifti and naming):

Before using the script, data has to be converted to the nifti format. The authors used DicomSort (https://github.com/dicomsort/dicomsort) and dcm2niix (https://github.com/rordenlab/dcm2niix) to perform this. Since the converstion to nifti has to adapted to the format of the original data, our script is not provided. We recommend reading the documentation for the applications instead. 
We used the naming convention listed in nnU-Net (https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_format.md). Our files are named as {codenr}_{modalitynumber}.nii.gz. Modality number for T2 is 0001, for DWI 0002 and for ADC 0003. Example: '0001_0001.nii.gz' for code number 0001 and modality T2 (0001).


Step 2 - Transformation:

With the input data in nifti format we then performed a transformation of the DWI and ADC images to match the resolution and number of slices of the T2-weighted images. The script uses TorchIO (https://torchio.readthedocs.io). Please see the script "Transform.py". 


Step 3 - Registration:

With the transformed data we then performed a rigid registration of the DWI b=0 image and the T2-weighted image with the b0 image as moving using Elastix (https://elastix.dev). The registration was then applied to the other b-values and the ADC map using Transformix (which is a part of Elastix). Please see the script "Registration.py".

Step 4 - Annotation:

The reference masks to be used for training were created manually using ITK-snap (https://www.itksnap.org/pmwiki/pmwiki.php). The masks were named as "{codenr}.nii.gz".


Step 5 - Training of nnU-Net:
For complete documentation of the usage of nnU-Net please see their (nnUNetv2_plan_and_preprocess -d 113 -c 2d 3d_fullres -pl --verify_dataset_integrity).

We used the following commands: 

For plan and preprocessing (Dataset113_prostate is the dataset name):
nnUNetv2_plan_and_preprocess -d 113 -c 2d 3d_fullres -pl --verify_dataset_integrity

For training (simultaneously on 5 GPUs, one fold per GPU):
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr nnUNetTrainer 113 2d 0 --npz & # train on GPU 0
sleep 200
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr nnUNetTrainer 113 2d 1 --npz & # train on GPU 1
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr nnUNetTrainer 113 2d 2 --npz & # train on GPU 2
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr nnUNetTrainer 113 2d 3 --npz # train on GPU 3
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr nnUNetTrainer 113 2d 4 --npz # train on GPU 4
wait
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train -tr nnUNetTrainer 113 3d_fullres 0 --npz & # train on GPU 0
sleep 200
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train -tr nnUNetTrainer 113 3d_fullres 1 --npz & # train on GPU 1
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train -tr nnUNetTrainer 113 3d_fullres 2 --npz & # train on GPU 2
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train -tr nnUNetTrainer 113 3d_fullres 3 --npz & # train on GPU 3
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train -tr nnUNetTrainer 113 3d_fullres 4 --npz & # train on GPU 4

For finding best configuration:
nnUNetv2_find_best_configuration 113 -tr nnUNetTrainer

For inference (prediction) on test set:
nnUNetv2_predict -d Dataset113_prostate -i ./Dataset113_prostate/imagesTs -o ./inference_testset_dataset113_3d_fullres -f  0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans --save_probabilities

For postprocessing:
nnUNetv2_apply_postprocessing -i ./inference_testset_dataset113_3d_fullres -o ./inference_testset_dataset113_3d_fullres_PP -pp_pkl_file ./nnUNet_results/Dataset113_prostate/nnUNetTrainer__nnUNetPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json ./nnUNet_results/Dataset113_prostate/nnUNetTrainer__nnUNetPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/plans.json

Step 6 - Statistical analysis:
Softmax values were used to create ROC-curves. The statistical program R were used for calculation of AUC and confidence intervals. The code for R i 




