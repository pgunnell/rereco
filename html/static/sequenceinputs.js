function save_sequence(){
    var conditions = document.getElementById("conditions").value;
    var datatier = document.getElementById("datatier").value;
    var era = document.getElementById("era").value;
    var extra = document.getElementById("extra").value;
    var customize = document.getElementById("customize").value;
    var nThreads = document.getElementById("nThreads").value;
    var eventcontent = document.getElementById("eventcontent").value;

    if(conditions=='' || datatier=='' || step=='' || eventcontent=='' || era==''){
	alert("Not saved: some variables are empty");
    }
    else {
	
	//need to update the request after the sequence
	var driver = "cmsDriver --conditions "+conditions+" --datatier "+datatier+" --era "+era+" --step "+step+" --eventcontent "+eventcontent+" --customize "+customize+" --nThreads "+nThreads+" "+extra;

	let data = {"sequences": driver};

	//need to add an API for updating the request

	alert("Sequence saved correctly");
    }
}


