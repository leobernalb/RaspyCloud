$(document).ready(function(){

  $.ajax({
        url: '/api/v1/rpiJson',

        data: JSON.stringify ({
            "jsonrpc": "2.0",
            "method": "generateJson",
            "params": {
                "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"
                },
            "id": "generateJson"
        }),

        type:"POST",
        contentType: "application/json",

        success:  function (data){

            var row = '';

            // Body
            $.each(data.result.raspberryPi, (index, element) => {
                row += '<tr align="right">';

                row += '<td align="right"> ' + element.hostname + '</td>';
                row += '<td align="right"> ' + element.ip + '</td>';
                row += '<td align="right"> ' + element.mac + '</td>';
                row += '<td align="right"> <a class="btn-floating waves-effect waves-light red"><i class="material-icons replay">replay</i></a> </td>';
                row += '</tr>';
            });

            $("#tableBody").html(row);


        },
        error: function (err){
            console.log("Error");
        }

    });



     $('#submitLogin').submit(function (event) {
        event.preventDefault(); // stop submit form
        var user = $("#username").val();
        var pass = $("#password").val();

        $.ajax({
            url: '/api/v1/login',

            data: JSON.stringify ({
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": user,
                    "password": pass
                    },
                "id": "login"
            }),

            type:"POST",
            contentType: "application/json",

            success:  function (data){
                // Redirect to dashboard.html if login == TRUE
                console.log(data)
                if(data.result)
                    window.location.href = '/dashboard';
                else
                    alert("Pa tu casa")

            },
            error: function (err){
                console.log("Error");
            }

     });

    });



});