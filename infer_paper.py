import subprocess
import os
infer_dict = {
    'A2B':{
        'name':'A2B',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CNMC',
        'sty_data':'/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CHOP/',
        'template_datapoint': '88BT1_t1_n4_rig.nii.gz'
    },
    'B2A':{
        'name':'B2A',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CHOP',
        'sty_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CNMC/',
        'template_datapoint': 'CNMC_0m_9030_t1_n4_rig.nii.gz'
    },


    'A2C':{
        'name':'A2C',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CNMC',
        'sty_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CO/',
        'template_datapoint': 'CO_323_V1_t1_n4_rig.nii.gz'
    },
    'C2A':{
        'name':'C2A',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CO',
        'sty_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CNMC/',
        'template_datapoint': 'CNMC_0m_9030_t1_n4_rig.nii.gz'
    },

    'B2C':{
        'name':'B2C',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CHOP',
        'sty_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CO/',
        'template_datapoint': 'CO_323_V1_t1_n4_rig.nii.gz'
    },
    'C2B':{
        'name':'C2B',
        'cont_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CO',
        'sty_data': '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/tr_CHOP/',
        'template_datapoint': '88BT1_t1_n4_rig.nii.gz'
    },

}
base_path = '/home/abhijeet/Datasets/Multisite_4Seq_Rig/data/'
for key in infer_dict.keys():
    out_path = os.path.join(base_path, f'preds_{key}')
    os.makedirs(out_path, exist_ok= True)
    style_image = os.path.join(infer_dict[key]['sty_data'],infer_dict[key]['template_datapoint'])
    subprocess.check_call(f"bash harmonize_images.sh {style_image} {infer_dict[key]['cont_data']} {out_path} expr_customer/", shell=True)


#subprocess.check_call("./script.ksh %s %s %s" % (arg1, str(arg2), arg3), shell=True)