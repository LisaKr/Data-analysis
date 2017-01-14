# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#%matplotlib inline
#from nilearn.image import resample_img
#import nibabel
import os                                    # system functions\n",
import nipype.interfaces.freesurfer as fs    # freesurfer\n",
import nipype.interfaces.io as nio           # i/o routines\n",
import nipype.interfaces.utility as util     # utility\n",
import nipype.pipeline.engine as pe          # pypeline engine\n",
import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni


rois = []  

#rois.append((30,-21,-18))
#rois.append((-30,-21,-18)),
#rois.append((30,9,-30)),
#rois.append((-30,9,-30)),

#subjects = os.listdir("/scr/kalifornien1/data/nki_enhanced/preprocessed_fmri/structural/asymmetric/")


sublist = '/scr/ilm1/lisa/scripts/subjects.txt'
with open(sublist, 'r') as f:
    subjects = [line.strip() for line in f] #all 312

workingdir = "/scr/ilm1/lisa/attention/working_dir/"
resultsdir = "/scr/ilm1/lisa/attention/results/"

wf = pe.Workflow(name="main")
wf.base_dir = workingdir
wf.config['execution']['crashdump_dir'] = wf.base_dir + "crash_files"



roi_infosource = pe.Node(util.IdentityInterface(fields=['roi']), name="roi_infosource")
roi_infosource.iterables = ('roi', rois) 

subjects_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']), name="subjects_infosource")
subjects_infosource.iterables = ("subject_id", subjects)



ds = pe.Node(nio.DataSink(), name="datasink")
#ds.run_without_submitting = True",
ds.inputs.base_directory = resultsdir

datasource = pe.Node(nio.DataGrabber(infields=['subject_id'], outfields = ['EPI_bandpassed']), name="datasource") #grabs data
datasource.inputs.base_directory = "/scr/kalifornien1/data/nki_enhanced/preprocessed_fmri/structural/asymmetric/"  
datasource.inputs.template = '%s/smri/warped_image/_tr_2500/%s_r00_afni_bandpassed_wtsimt.nii.gz'
datasource.inputs.template_args['EPI_bandpassed'] = [['subject_id', "subject_id"]] 
#datasource.inputs.template = '%s_r00_afni_bandpassed_wtsimt.nii.gz' datasource.inputs.template_args['EPI_bandpassed'] = [['subject_id']] 
#datasource.inputs.template_args['EPI_full_spectrum'] = [['subject_id', "fullspectrum"]] 
datasource.inputs.sort_filelist = True
wf.connect(subjects_infosource, "subject_id", datasource, "subject_id")




sphere = pe.Node(afni.Calc(), name="sphere")
sphere.inputs.in_file_a = fsl.Info.standard_image("/SCR/lisa/attention/group_analysis/MNI152_T1_3mm.nii.gz")
sphere.inputs.outputtype='NIFTI_GZ'
#sphere.inputs.out_file = "roi_sphere.nii"   
def roi2exp(coord): 
    radius = 4
    return "step((%d*%d)-(x+%d)*(x+%d)-(y+%d)*(y+%d)-(z+%d)*(z+%d))" %(radius, radius, coord[0], coord[0], coord[1], coord[1], -coord[2], -coord[2])

def roi2name(coord):
    return 'roi_sphere_%s_%s_%s.nii.gz'%(str(coord[0]), str(coord[1]), str(coord[2])) 

    
    
    
wf.connect(roi_infosource, ("roi", roi2exp), sphere, "expr")   
wf.connect(roi_infosource, ("roi", roi2name), sphere,"out_file") 
wf.connect(sphere, "out_file", ds, "@sphere")




extract_timeseries = pe.Node(afni.Maskave(), name="extract_timeseries") 
wf.connect(sphere, "out_file", extract_timeseries, "mask") 
wf.connect(datasource, "EPI_bandpassed", extract_timeseries, "in_file") 


correlation_map = pe.Node(afni.Fim(), name="correlation_map")
correlation_map.inputs.out = "Correlation"
correlation_map.inputs.outputtype = "NIFTI_GZ"
correlation_map.inputs.out_file = "corr_map.nii.gz"
wf.connect(extract_timeseries, "out_file", correlation_map, "ideal_file")
wf.connect(datasource, "EPI_bandpassed", correlation_map, "in_file")

z_trans = pe.Node(interface=afni.Calc(), name='z_trans')
z_trans.inputs.expr = 'log((1+a)/(1-a))/2'
z_trans.inputs.outputtype = 'NIFTI_GZ'
wf.connect(correlation_map, "out_file", z_trans, "in_file_a")
wf.connect(z_trans, 'out_file', ds, "@seed_based_z")


wf.run()
#export AFNI_1D_ZERO_TEXT=YES #you need to write it in the command line before running, otherwise AFNI will misbehave

