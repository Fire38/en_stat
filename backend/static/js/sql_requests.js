$.ajax({
    url: '/en_stat/sql_requests',
    type: 'get',
    success: function(data){
        console.log(data)
        $('#test').text(data)
    }


})