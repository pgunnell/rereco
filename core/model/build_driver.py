#one assumes that request is already the object, which contains the sequences

def build_driver(request):

    driver = 'cmsDriver'

    driver+= ' --conditions '+str(request['sequences']['conditions'])
    driver+= ' --step '+str(request['sequences']['step'])
    driver+= ' --era '+str(request['sequences']['era'])
    driver+= ' --customize '+str(request['sequences']['customize'])
    driver+= ' --datatier '+str(request['sequences']['datatier'])
    driver+= ' --nThreads '+str(request['sequences']['nThreads'])
    driver+= ' '+str(request['sequences']['extra'])
    driver+= ' --eventcontent '+str(request['sequences']['eventcontent'])

    return driver

def build_dictionary(request):

    #create a file similar to master_DataSet.conf
    filename = 'master_'+str(request['prepid'])+'.conf'

    file_dict = open(filename,"w") 
   
    file_dict.write('[DEFAULT]')

    file_dict.write('group=ppd')
    file_dict.write('user=pgunnell')
    file_dict.write('request_type=ReReco')
    file_dict.write('release='+str(request['cmssw_release']))
    file_dict.write('global_tag='+str(request['sequences']['conditions']))
    file_dict.write('campaign='+str(request['member_of_campaign']))
    file_dict.write('acquisition_era='+str(request['acquisition_era']))

    file_dict.write('processing_string='+str(request['process_string']))
    file_dict.write('priority='+str(request['priority']))
    file_dict.write('time_event='+str(request['time_event']))
    file_dict.write('size_event='+str(request['size_event']))
    file_dict.write('size_memory='+str(request['memory']))
    file_dict.write('multicore='+str(request['sequences']['nThreads']))

    file_dict.write('['+str(request['acquisition_era'])+'-v1-'+str(request['input_dataset']).split('/')[0]+'-'+str(request['process_string'])+']') #version needs to change according to the input dataset

    file_dict.write('dset_run_dict={"'+str(request['input_dataset'])+'" : '+str(request['runs'])+' }')

    file_dict.write('cfg_path='+str(request['config_file_name']))
    file_dict.write('request_id='+str(request['request_id']))
    file_dict.write('harvest_cfg='+str(request['harvest_file_name']))

    file_dict.close()

    return file_dict
    #it returns a file
