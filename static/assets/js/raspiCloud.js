$(document).ready(function(){

    // Carga tabla
    $('#refresh').click(function(){
           var cookies = document.cookie;
           var token = cookies.split('=')[1]
          $.ajax({
                url: '/api/v1/rpiJson',

                data: JSON.stringify ({
                    "jsonrpc": "2.0",
                    "method": "generateJson",
                    "params": {
                        "token": token
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
                        row += '<td align="right"> ' + element.diskSize + '</td>';
                        row += '<td align="right"> ' + element.diskAvail + '</td>';
                        row += '<td align="right"> ' + element.diskUse + '</td>';
                        row += '<td align="right"> ' + element.status + '</td>';
                        row += '</tr>';
                    });

                    $("#tableBody").html(row);

                },
                error: function (err){
                    console.log("Error");
                }

            });

    });



     $('#submitLogin').submit(function (event) {
        event.preventDefault(); // stop submit form
        var email = $("#username").val();
        var pass = $("#password").val();

        // Autenticacion Login
        $.ajax({
            url: '/api/v1/login',

            data: JSON.stringify ({
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "email": email,
                    "password": pass
                    },
                "id": "login"
            }),

            type:"POST",
            contentType: "application/json",

            success:  function (data){
                // Redirect to dashboard.html if login == TRUE
                if(data.result){
                    var token = data.result;
                    document.cookie = "token="+encodeURIComponent( token ) + " ; path=/"
                    window.location.href = '/dashboard';
                }else{
                    $('#loginError').show();
                }

            },
            error: function (err){
                console.log("Error");
            }
        });



    });

    // Despliegue
    $("#deploy").click(function(){
          var cookies = document.cookie;
          var token = cookies.split('=')[1]
          $.ajax({
            url: '/api/v1/deploy',

            data: JSON.stringify ({
                "jsonrpc": "2.0",
                "method": "run",
                "params": {
                    "token": token
                    },
                "id": "run"
            }),

            type:"POST",
            contentType: "application/json",

            success:  function (data){
            },
            error: function (err){
                console.log("Error");
            }

        });
    });

    // Cambio de Modo
    $("select#myselected").change(function(){
        var mode = $(this).children(":selected").val()
        var cookies = document.cookie;
        var token = cookies.split('=')[1]
       $.ajax({
            url: '/api/v1/rescute',

            data: JSON.stringify ({
                "jsonrpc": "2.0",
                "method": "rescuteMode",
                "params": {
                    "rescuteMode": mode,
                    "token": token
                    },
                "id": "rescuteMode"
            }),

            type:"POST",
            contentType: "application/json",

            success:  function (data){
            },
            error: function (err){
                console.log("Error");
            }

    });
   });

    // Logout
    $("#signout").click(function(){
          document.cookie = "token=; max-age=0"
          var cookies = document.cookie;
          window.location.href = '/';

          console.log(cookies)
    });

    // Registro
     $('#submitRegister').submit(function (event) {
        event.preventDefault(); // stop submit form
        var firstName = $("#first_name").val();
        var lastName = $("#last_name").val();
        var email = $("#email").val();
        var password = $("#passwordRegister").val();

         $.ajax({
            url: '/api/v1/register',

            data: JSON.stringify ({
                "jsonrpc": "2.0",
                "method": "register",
                "params": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email,
                    "password": password
                    },
                "id": "register"
            }),

            type:"POST",
            contentType: "application/json",

            success:  function (data){
                alert("Registrado correctamente");

            },
            error: function (err){
                console.log("Error");
            }

     });

    });


});