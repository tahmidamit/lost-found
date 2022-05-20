function disable_stuff(page_num){

    if (window.location.href.indexOf('?') == -1) {
        $('#bp').click(function(event){
            event.preventDefault();
            $('#preb').prop('disabled', true);
            return false;
       });

       $("#nextb").click(function(event){
           if(page_num>1){
               window.location.href = window.location.href.concat("?page=2")
               return false;
           }
           else{
            event.preventDefault();
            $(this).prop('disabled', true);
            return false
           }
       });
       
    }
    return false;
}

function stopbutton(page_num){
    if (!(window.location.href.indexOf('?') == -1)) {
      
      var querystring = window.location.search;
      querystring = querystring.slice(1, );
      const myArray = querystring.split("=");
      var num = parseInt(myArray[1]);
      
      if (myArray[0]=="page"){
          
        $('#np').click(function(event){
            if(num>=page_num){
                event.preventDefault();
                $('#nextb').prop('disabled', true);
                
            }

            else{
                
                if(num != NaN && num > 0){
                    num = num + 1;
                    var ans = ("?page=").concat(num.toString());
                    
                    window.location.search = ans

                }
            }
            return false;
        });


        $('#bp').click(function(event){
                    
            if(num==1 || num < 0){
                event.preventDefault();
                $('#preb').prop('disabled', true);
            }

            else{
                
                if(num != NaN && num > 0){
                    num = num - 1;
                    var ans = ("?page=").concat(num.toString());
                    
                    window.location.search = ans

                }
            }
            return false;
        });

      }
    }
    return false;
  }