$(document).ready(function(){
    $('#title').keyup(function () {
    if (this.value.length === 0) {
        $('#limit').show();
        $('#remaining').hide();
    } else {
        $('#limit').hide();
                             $('#remaining').show();
    }

    if (this.value.length > 18) {
        return false;
    }

    $("#remaining").html("Chars Left : " + (18 - this.value.length))});

    $('#caption').keyup(function () {
    if (this.value.length === 0) {
        $('#limit2').show();
        $('#remaining2').hide();
    } else {
        $('#limit2').hide();
        $('#remaining2').show();
    }

    if (this.value.length > 140) {
        return false;
    }

    $("#remaining2").html("Chars Left : " + (140 - this.value.length));
    });

    $('#info').keyup(function () {
    if (this.value.length === 0) {
        $('#limit3').show();
        $('#remaining3').hide();
    } else {
        $('#limit3').hide();
        $('#remaining3').show();
    }

    if (this.value.length > 50) {
        return false;
    }

    $("#remaining3").html("Chars Left : " + (50 - this.value.length));
    });

  });


$(document).ready(function () {
    $('select').selectize({
        sortField: 'text'
    });
});

$(document).ready(function(){
$('#upload').on('submit', function(event){

    event.preventDefault();
    $('#ssub').prop('disabled', true);
    var formData = new FormData($('#upload')[0]);
    
    $.ajax({

        xhr: function(){
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', function(e){
                if (e.lengthComputable){
                    var percent = Math.round((e.loaded / (e.total + 307200)) * 100);
                    $("#progress").attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%')
                }
            });
            return xhr
        },
        type : 'POST',
        url : '/post',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        
        success: function (data) {
            $('#alert').show();
            $('#alert-text').html("");
            $('#alert-text').html(data.error);
            $('#ssub').prop('disabled', false);
            if(data.error=="Success"){
                $("#upload")[0].reset();
                window.location.href = "/my_ads";
            }
            else{
                $(document).scrollTop(0);
            }
        }
    });
    return false;
    });
});