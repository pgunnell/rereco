from core.model.model_base import ModelBase

#These are the only features which are needed for a request
#No need for not keeping output -> output will always be kept

class Request(ModelBase):

    _ModelBase__schema = {
        # Database id
        '_id': '',
        # PrepID
        'prepid': '',
        # Energy in TeV
        'energy': 0.0,
        # Step type: MiniAOD, NanoAOD, etc.
        'step': '',
        # CMSSW version
        'cmssw_release': '',
        # User notes
        'notes': '',
        # Input dataset name
        'input_dataset_name': '',
        # Output dataset name
        'output_dataset_name': '',
        # List of dictionaries that have cmsDriver options
        'sequences': [],
        # Action history
        'history': [],
        # Status 
        'status': 'new', #it should be either approved, submitted, done (nothing else)
        # Workflow name in computing when submitted 
        'reqmgr_name': '', 
        # process string
        'process_string': '', 
        # Default memory
        'memory': 2300}

    __lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9]{1,50}'),
        'energy': lambda energy: energy >= 0.0,
        'step': lambda step: step in ['DR', 'MiniAOD', 'NanoAOD'],
        'memory': lambda memory: memory >= 0,
        'cmssw_release': lambda cmssw_release: 'CMSSW' in cmssw_release
    }

    def __init__(self, json_input=None):
        ModelBase.__init__(self, json_input)

    def check_attribute(self, attribute_name, attribute_value):
        if attribute_name in self.__lambda_checks:
            return self.__lambda_checks.get(attribute_name)(attribute_value)

        return True
