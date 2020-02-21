#one assumes that request is already the object, which contains the sequences

def build_driver(request):

    driver = 'cmsDriver RECO '

    driver+= ' --conditions '+str(request['sequences'][0]['conditions'])
    driver+= ' --step '+str(request['sequences'][0]['step'])
    driver+= ' --era '+str(request['sequences'][0]['era'])
    driver+= ' --customize '+str(request['sequences'][0]['customize'])
    driver+= ' --datatier '+str(request['sequences'][0]['datatier'])
    driver+= ' --nThreads '+str(request['sequences'][0]['nThreads'])
    driver+= ' '+str(request['sequences'][0]['extra'])
    driver+= ' --eventcontent '+str(request['sequences'][0]['eventcontent'])
    
    if('DQM' in request['sequences']['datatier']):
        driver+= ' --python_filename harvest_'+request['dataset_name']+'_cfg.py'
    else:
        driver+= ' --python_filename reco_'+request['dataset_name']+'_cfg.py'

    return driver

def build_driver_Harvest(request):
    
    driver = 'cmsDriver HARVEST '

    if not('DQM' in request['sequences'][0]['datatier']):
        return '\n'

    else:
        {

            driver+= ' --conditions '+str(request['sequences'][1]['conditions'])
            driver+= ' --step '+str(request['sequences'][1]['step'])
            driver+= ' --era '+str(request['sequences'][1]['era'])
            driver+= ' --customize '+str(request['sequences'][1]['customize'])
            driver+= ' --datatier '+str(request['sequences'][1]['datatier'])
            driver+= ' --nThreads '+str(request['sequences'][1]['nThreads'])
            driver+= ' '+str(request['sequences'][1]['extra'])
            driver+= ' --eventcontent '+str(request['sequences'][1]['eventcontent'])
            
        }

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
    file_dict.write('global_tag='+str(request['sequences'][0]['conditions']))
    file_dict.write('campaign='+str(request['member_of_campaign']))
    file_dict.write('acquisition_era='+str(request['acquisition_era']))

    file_dict.write('processing_string='+str(request['process_string']))
    file_dict.write('priority='+str(request['priority']))
    file_dict.write('time_event='+str(request['time_event']))
    file_dict.write('size_event='+str(request['size_event']))
    file_dict.write('size_memory='+str(request['memory']))
    file_dict.write('multicore='+str(request['sequences'][0]['nThreads']))

    file_dict.write('['+str(request['acquisition_era'])+'-v1-'+str(request['input_dataset']).split('/')[0]+'-'+str(request['process_string'])+']') #version needs to change according to the input dataset

    file_dict.write('dset_run_dict={"'+str(request['input_dataset'])+'" : '+str(request['runs'])+' }')

    file_dict.write('cfg_path='+str(request['config_file_name']))
    file_dict.write('request_id='+str(request['request_id']))
    file_dict.write('harvest_cfg='+str(request['harvest_file_name']))

    file_dict.close()

    return file_dict
    #it returns a file

def get_test_command(request):

    filename = 'get_test_'+str(request['prepid'])+'.sh'

    file_get_test = open(filename,"w")

    file_get_test+=make_release(request)

    file_get_test+='scram b \n'
    file_get_test+=build_driver(request)+'\n'

    file_get_test += 'cmsRun -e -j %s %s || exit $? ; \n' % (runtest_xml_file, configuration_names[-1])+'\n'

    file_get_test += 'grep "TotalEvents" %s \n' % runtest_xml_file
    file_get_test += 'if [ $? -eq 0 ]; then\n'
    file_get_test += '    grep "Timing-tstoragefile-write-totalMegabytes" %s \n' % runtest_xml_file
    file_get_test += '    if [ $? -eq 0 ]; then\n'
    file_get_test += '        events=$(grep "TotalEvents" %s | tail -1 | sed "s/.*>\(.*\)<.*/\\1/")\n' % runtest_xml_file
    file_get_test += '        size=$(grep "Timing-tstoragefile-write-totalMegabytes" %s | sed "s/.* Value=\\"\(.*\)\\".*/\\1/")\n' % runtest_xml_file
    file_get_test += '        if [ $events -gt 0 ]; then\n'
    file_get_test += '            echo "McM Size/event: $(bc -l <<< "scale=4; $size*1024 / $events")"\n'
    file_get_test += '        fi\n'
    file_get_test += '    fi\n'
    file_get_test += 'fi\n'
    file_get_test += 'grep "EventThroughput" %s \n' % runtest_xml_file
    file_get_test += 'if [ $? -eq 0 ]; then\n'
    file_get_test += '  var1=$(grep "EventThroughput" %s | sed "s/.* Value=\\"\(.*\)\\".*/\\1/")\n' % (runtest_xml_file)
    file_get_test += '  echo "McM time_event value: $(bc -l <<< "scale=4; 1/$var1")"\n'
    file_get_test += 'fi\n'
    file_get_test += 'echo CPU efficiency info:\n'
    file_get_test += 'grep "TotalJobCPU" %s \n' % runtest_xml_file
    file_get_test += 'grep "TotalJobTime" %s \n' % runtest_xml_file

    return file_get_test


#copied from McM
def make_release(request):
    #makeRel = 'export SCRAM_ARCH=%s\n' % (self.get_scram_arch())
    makeRel += 'source /cvmfs/cms.cern.ch/cmsset_default.sh\n'
    makeRel += 'if [ -r %s/src ] ; then \n' % (request['cmssw_release'])
    makeRel += ' echo release %s already exists\n' % (request['cmssw_release'])
    makeRel += 'else\n'
    makeRel += 'scram p CMSSW ' + request['cmssw_release'] + '\n'
    makeRel += 'fi\n'
    makeRel += 'cd ' + request['cmssw_release'] + '/src\n'
    makeRel += 'eval `scram runtime -sh`\n'  # setup the cmssw
    
    return makeRel

def create_link_pmp(request):

    link_to_pmp = 'https://cms-pdmv.cern.ch/pmp/historical?r='+request['prepid']

    return link_to_pmp

def create_link_dyma(request):

    dyma_link = 'https://dmytro.web.cern.ch/dmytro/cmsprodmon/workflows.php?prep_id='+request['prepid']

    return dyma_link

def injection_steps(request):

    ssh_command = make_release(request)+'\n'
    ssh_command += 'source subSetupAuto.sh'+'\n'
    ssh_command += build_driver(request)+'\n'
    ssh_command += build_driver_Harvest(request)+'\n'

    master_file = build_dictionary(request)

    ssh_command += 'wmcontrol.py --req_file='+str(master_file)

    return ssh_command
    #this is the bash file which needs to be executed for injection to computing
    
def create_twiki(campaign_ticket):

    campaign = campaign_ticket['subcampaign'].split('-')[0]
    acquisition_era = campaign_ticket['acquisition_era'] #this is just RunB or RunC..                                                                                                                       
    theruns = campaign_ticket['runs']

    twiki=file('twiki_%s.twiki' % campaign, 'w')
    twiki.write('---+++ !%s \n\n' % acquisition_era)
    twiki.write('| *DataSet* | *prepID monitoring* | *run* |\n')

    for pd_name in campaign_ticket['input_datasets']:

        pd_name = pd_name.split('/')[0]
        #example ReReco-Run2016F-JetHT-ForValUL2016_HIPM-0001                                                                                                                                               
        prepid = 'ReReco-%s-%s-%s-0001' % (campaign_ticket['acquisition_era'],campaign_ticket['pd_name'],campaign_ticket['process_string'])
        twiki.write("| %s | [[https://cms-pdmv.cern.ch/pmp/historical?r=%s][%s]] | %s |\n"  %(pd_name, prep_id, prep_id, str(theruns)))

    twiki.close()
    return twiki

