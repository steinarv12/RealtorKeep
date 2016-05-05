$( document ).ready(function() {
    $("#update").click(function( event ) {
        event.preventDefault();
        $.get(this.href,function(data,status) {
            console.log(status);
            console.log(data);
        });
    });
    console.log( "ready!" );

});