var lang = "en";

$( document ).ready(function() {
	$('#Loader1').hide();
	$('#Loader2').hide();
});

document.addEventListener("keydown", function(event) {
	if(event.keyCode == 13) {
		getResult();
	}
});



function getResult() {
	var enteredFormula = $('#formula').val();
	$('#Loader1').show();
	$('.formulaText').hide();
	$('.InputErrorDiv').hide();
	$('.userinputPanel').hide();
	$('.resultPanel').hide();
	var statementQueFlag = false;
	if(enteredFormula == "") {
		alert("Please enter valid value");
		$('.userinputPanel').hide();
		$('#Loader1').hide();
	} else {

			var data={'formula':enteredFormula};
			var url = "";

			if (enteredFormula.indexOf("=") >= 0) {
				url = "getresponse";
			} else if (lang == "hn" || lang == "en") {
				statementQueFlag = true;
				if(lang == "en") {
					url = "getengformula";
				} else if(lang == "hn") {
					url = "gethindiformula";
				}
			}


			$.post(url, data)
		    .done(function (response, statusText,xhr) {
		        // IN response
		    	$('.userInputDiv').empty();
		    	var status=xhr.status;


		    	if(status == 206) {
		    		var formulaText = response.replace(/\\\\/g,'\\');
        			$('.formula').html(response);
        			setTimeout(function(){
        				$(".latex").latex();
        				$('.formulaText').show();
        				$('.submitBtn').hide();
    		        	$('.userinputPanel').show();
    		        	$('.userInputDiv').empty();
    		        	$('.userInputDiv').hide();
    		        	$('#Loader1').hide();
    				}, 200);
		    	} else {
		    		if(status == 200) {
		    		    // OUT response
		    		    // todo: resultList
		    		    var qid = response[response.length-1]['qid'];
		    		    // cut off qid from response
		    		    response.length -= 1;
				        var valueList = response[response.length-1]['values'];
				        var resultList = response;
				        resultList.length -= 1;
				        $('.userinputPanel').hide();
				        $('.resultValue').text("");
		          	  	$('.resultPanel').hide();
				        $('.userInputDiv').empty();
				        $('.userInputDiv').show();
				        $('.InputErrorDiv').hide();
			        	$('.submitBtn').show();
			        	var source_text = 'Source: www.wikidata.org'
			        	if (qid.length > 0) {
			        	    source_text += '/wiki/' + qid;}
			        	$('.sourceDiv').text(source_text);
                        $('.sourceDiv').show();
				        if(resultList.length == 1) {
				        	var result = resultList;

				        	if(result != '') {

				        		var constantArray = ['pi','golden','golden_ratio','c','speed_of_light','mu_0','epsilon_0','Planck','hbar','G',
				        		                     'gravitational_constant','g','e','elementary_charge','gas_constant',
				        		                     'alpha','fine_structure','N_A','Avogadro','k',
				        		                     'Boltzmann','sigma','Stefan_Boltzmann','Wien','Rydberg',
				        		                     'm_e','electron_mass','m_p','proton_mass','m_n','neutron_mass','S','mu_{0}'];
				        		var constantVal = ['3.141592653589793','1.618033988749895','1.618033988749895','299792458.0','299792458.0','1.2566370614359173e-06',
				        		                   '8.854187817620389e-12','6.62607004e-34','1.0545718001391127e-34','6.67408e-11',
				        		                   '6.67408e-11','9.80665','1.6021766208e-19','1.6021766208e-19','8.3144598',
				        		                   '0.0072973525664','0.0072973525664','6.022140857e+23','6.022140857e+23','1.38064852e-23',
				        		                   '1.38064852e-23','5.670367e-08','5.670367e-08','0.0028977729','10973731.568508',
				        		                   '9.10938356e-31','9.10938356e-31','1.672621898e-27','1.672621898e-27','1.672621898e-27','1.672621898e-27','5.24411510858423962092','1.2566370614359173e-06'];
				        		var string = '';
				        		if(jQuery.inArray($.trim(result), constantArray) !== -1) {
				        			var index = jQuery.inArray($.trim(result), constantArray);
				        			string = '<div class="form-group col-sm-6">'+
											    '<label for="exampleInputEmail1"><span style="font-weight:500;font-size: 25px;">'+$.trim(result)+'</span></label>'+
											    '<input type="text" class="form-control" placeholder="Enter Value" name="'+$.trim(result)+'" value="'+valueList[i]+'">'+
											'</div>';
									// string = '<div class="form-group col-sm-6">'+
											    //'<label for="exampleInputEmail1"><span style="font-weight:500;font-size: 25px;">'+$.trim(result)+'</span></label>'+
											    //'<input type="text" class="form-control" placeholder="Enter Value" name="'+$.trim(result)+'" value="'+constantVal[index]+'">'+
											//'</div>';
				        			// string = '<input type="hidden" class="form-control" name="'+$.trim(result)+'" value="'+constantVal[index]+'">';
				        		} else {
				        			string = '<div class="form-group col-sm-6">'+
									    '<label for="exampleInputEmail1"><span style="font-weight:500;font-size: 25px;">'+$.trim(result)+'</span></label>'+
									    '<input type="text" class="form-control" placeholder="Enter Value" name="'+$.trim(result)+'">'+
									'</div>';
				        		}



					        	$('.userInputDiv').append(string);
					        	$('.userinputPanel').show();


				        	} else {
				        		$('.resultValue').text(enteredFormula);
				          	  	$('.resultPanel').show();
				        	}
				        } else {
				        	$.each(resultList, function(i, data) {

					            var result = data;

					        		if (i == (resultList.length - 1)) {

					        			$('.formula').html(data.formula);
					        			setTimeout(function(){
					        				$(".latex").latex();
					        				$('.formulaText').show();
				        				}, 200);

					        		} else {
					        			var constantArray = ['pi','golden','golden_ratio','c','speed_of_light','mu_0','epsilon_0','Planck','hbar','G',
						        		                     'gravitational_constant','g','e','elementary_charge','gas_constant',
						        		                     'alpha','fine_structure','N_A','Avogadro','k',
						        		                     'Boltzmann','sigma','Stefan_Boltzmann','Wien','Rydberg',
						        		                     'm_e','electron_mass','m_p','proton_mass','m_n','neutron_mass','S','mu_{0}'];
						        		var constantVal = ['3.141592653589793','1.618033988749895','1.618033988749895','299792458.0','299792458.0','1.2566370614359173e-06',
						        		                   '8.854187817620389e-12','6.62607004e-34','1.0545718001391127e-34','6.67408e-11',
						        		                   '6.67408e-11','9.80665','1.6021766208e-19','1.6021766208e-19','8.3144598',
						        		                   '0.0072973525664','0.0072973525664','6.022140857e+23','6.022140857e+23','1.38064852e-23',
						        		                   '1.38064852e-23','5.670367e-08','5.670367e-08','0.0028977729','10973731.568508',
						        		                   '9.10938356e-31','9.10938356e-31','1.672621898e-27','1.672621898e-27','1.672621898e-27','1.672621898e-27','5.24411510858423962092','1.2566370614359173e-06'];
						        		var string = '';
						        		// Search constants and get index
						        		var index = jQuery.inArray($.trim(result), constantArray);
						        		// if constant was found take value or else ask for value input later on
						        		var displayValue = (index !== -1) ? constantVal[index] : "Enter Value";

						        		var displayText = $.trim(result) // TODO identifier + "(" + name + ")";
						        		// build display for a single identifier
                                        string = '<div class="form-group col-sm-6">'+
                                                    '<label for="exampleInputEmail1"><span style="font-weight:500;font-size: 25px;">'+displayText+'</span></label>'+
                                                    '<input type="text" class="form-control" placeholder="Enter Value" name="'+$.trim(result)+'" value="'+valueList[i]+'">'+
                                                '</div>';
                                        // string = '<div class="form-group col-sm-6">'+
                                                    //'<label for="exampleInputEmail1"><span style="font-weight:500;font-size: 25px;">'+displayText+'</span></label>'+
                                                    //'<input type="text" class="form-control" placeholder="Enter Value" name="'+$.trim(result)+'" value="'+displayValue+'">'+
                                                //'</div>';
                                        // string = '<input type="hidden" class="form-control" name="'+$.trim(result)+'" value="'+constantVal[index]+'">';

							        	$('.userInputDiv').append(string);
					        		}



					        });
				        	$('.userinputPanel').show();

				        }
				        //$('.userInputDiv').append('<input type="hidden" class="form-control" name="formula" value="'+$('#formula').val()+'">');
			        } else {
			        	$('.InputErrorDiv').html(response);
			        	$('.InputErrorDiv').show();
			        	$('.submitBtn').hide();
                        $('.sourceDiv').hide();
			        	$('.userinputPanel').show();
			        	$('.userInputDiv').hide();
			        }
			        $('#Loader1').hide();
		    	}


		    })
		    .fail(function () {
		    	$('#Loader1').hide();
		    });

		// }

	}
}


function getResultFromInputs() {
	$('#Loader2').show();
	var formDataArray = $('.userInputForm').serializeArray();

	var formJSON = {};
    $.each(formDataArray, function () {
        if (formJSON[this.name]) {
            if (!formJSON[this.name].push) {
            	formJSON[this.name] = [formJSON[this.name]];
            }
            formJSON[this.name].push(parseFloat(this.value, 10) || '');
        } else {
        	formJSON[this.name] = parseFloat(this.value, 10) || '';
        }
    });

    var saveData = $.ajax({
        type: 'POST',
        url: "getfinalresult",
        data: JSON.stringify(formJSON),
        dataType: "json",
        contentType: "",
        success: function(resultData) {
        	$('#Loader2').hide();
        	console.log(resultData);
        	$('.resultValue').text(resultData);
        	$('.resultPanel').show();}
	});

	saveData.error(function(response) {
			$('#Loader2').hide();
	  	    $('.resultValue').text(response.responseText);
	  	    $('.resultPanel').show();
	});

}

function languagechange() {
	var newlang = $("#langSelect option:selected").val();
	lang = newlang;
	console.log(lang);
	$('.userinputPanel').hide();
    $('.resultValue').text("");
	$('.resultPanel').hide();

	if(lang == "en") {
		$('.titleText').html("Mathematical Question Answering System (MathQA)");
		$('.langText').html("Language");
		$('.searchBtnText').html("Search");
		$('.submitBtnText').html("Submit");

	} else if(lang =="hn"){
		$('.titleText').html("Mathematical Question Answering System (MathQA)");
		$('.langText').html("भाषा");
		$('.searchBtnText').html("खोज");
		$('.submitBtnText').html("जमा करें");

	}
}