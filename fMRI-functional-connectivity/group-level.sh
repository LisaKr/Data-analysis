!/bin/bash

fslmerge -t /scr/ilm1/lisa/attention/group_analysis/merged_file_roi_${1}.${2}.${3}.nii.gz /scr/ilm1/lisa/attention/results/_roi_${1}.${2}.${3}/_subject_id_*/corr_map_calc.nii.gz #how to iterate

randomise -i merged_file_roi_${1}.${2}.${3}.nii.gz -o /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3} \
  -d /scr/ilm1/lisa/attention/group_analysis/GLM/glm.mat -t /scr/ilm1/lisa/attention/group_analysis/GLM/glm.con -T

fslmaths   /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3.nii.gz -thr 0.95 -bin -mul  /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tstat3.nii.gz /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3_threshed.nii.gz     #positive contrast

fslmaths   /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4.nii.gz -thr 0.95 -bin -mul  /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tstat4.nii.gz /scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4_threshed.nii.gz    #negative contrast

cluster --in=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3_threshed.nii.gz --thresh=0.0001 --oindex=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_positive/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3_threshed_clusterIndex --olmax=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_positive/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3_threshed_clusterIndexLmax.txt --osize=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_positive/results_roi_${1}.${2}.${3}_tfce_corrp_tstat3_threshed_size -mm > /SCR/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_positive/cluster_info_tstat3.txt

cluster --in=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4_threshed.nii.gz --thresh=0.0001 --oindex=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_negative/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4_threshed_clusterIndex --olmax=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_negative/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4_threshed_clusterIndexLmax.txt --osize=/scr/ilm1/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_negative/results_roi_${1}.${2}.${3}_tfce_corrp_tstat4_threshed_size -mm > /SCR/lisa/attention/group_analysis/results_roi_${1}.${2}.${3}/cluster_negative/cluster_info_tstat4.txt

