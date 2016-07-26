$(document).ready(function(){
    $("#profileDiv").fadeIn(2000);
    $("#form").fadeIn(2000);
    $("#change").click(function() {
        $("#changePass").slideDown(2500);
        $("#form").slideUp(1500);
    });
});