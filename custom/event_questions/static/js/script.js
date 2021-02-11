var confirm_attendee_record = function (e) {
    var form = document.forms["attendee_registration"];
    var jform = $(form);
    var url = form.getAttribute('action');
    
    // console.log(url, '************************************************************', jform.find("#tick_qunt").html());
    // var tick = document.getElementById("tick_qunt").value;
    var tick = 1;
    // console.log(tick);
    var flag = 1;
    for(var i = 1; tick >= i; i++) { 
        var nm = document.forms["attendee_registration"][i+"-name"].value;
        if (nm == null || nm == "") {
            document.getElementById("error_nm").innerHTML = "Enter name"
            return false;
        }
        else {
            document.getElementById('error_nm').style.display='none';
       }
            var email = document.forms["attendee_registration"][i+"-email"].value;
            // var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
            var reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if (email == null || email == "") {
                document.getElementById("error_email").innerHTML = "Enter email"
                return false;
            }
            if (reg.test(email) == false) 
            {
                document.getElementById("error_email").innerHTML = "Invalid Email Address"
                return false;
            }
            else {
                document.getElementById('error_email').style.display='none';
            }
            var ph = document.forms["attendee_registration"][i+"-phone"].value;
            var filter=/^[0-9]+$/;
            if (ph == null || ph == "") {
                document.getElementById("error_phone").innerHTML = "Enter Phone no"
                return false;
            }
            else if(!filter.test(ph) )
            {
                document.getElementById("error_phone").innerHTML = "Enter numeric value for Phone no"
                return false;
            }
            else
            {
                document.getElementById('error_phone').style.display='none';
            }
            for (var j=1;10>=j;j++)
            {
                // console.log(document.getElementsByName(i+"-answer_id-"+j))
                var ans_id = document.forms["attendee_registration"][i+"-answer_id-"+j];
                // console.log(ans_id, document.forms["attendee_registration"])
                if(ans_id)
                {
                    var ans = document.forms["attendee_registration"][i+"-answer_id-"+j].value;
                    // console.log(ans);
                    var reg = document.forms["attendee_registration"][i+"-reg_express-"+j].value;
                    // console.log(reg);
                    if (reg)
                    {
                        // console.log('ans'+ans);
                        // console.log('reg'+reg);
                        // console.log(ans.match(reg));
                        if (ans.match(reg) == null) 
                        {
                            document.forms["attendee_registration"][i+'-error_msg-'+j].style.display='block';
                            break;

                        }
                        else
                        {
                            document.forms["attendee_registration"][i+'-error_msg-'+j].style.display='none';
                            flag=0;
                        }
                    }
                }
            else
            {
                // console.log('else777');
                continue;
            }
        }
    }
    //     console.log(flag);
        if (flag == 1)
        // {console.log($('#attendee_registration').serialize());
        $.ajax({
            // 'url': '/event/registration/confirm',
            'url': url,
            'type': 'POST',
            'data': $('#attendee_registration').serialize(),
            'dataType': 'json',
            'async': true,
            'success': function(data) {
                console.log('success'+data.success);
                if (data.success == 'Successfully created')
                {
                    // console.log('if');
                   location.replace('/page/feedback');
               }
           }
       });
   }
// }

