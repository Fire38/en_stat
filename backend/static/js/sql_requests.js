$.ajax({
    url: '/en_stat/get_main_count_information',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#count').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_main_top_information',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#top-list').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_main_players_information',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#top-players').html(data)
    }
})


