$.ajax({
    url: '/en_stat/get_total_per_year_graphics',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#totalPlayersPerYear').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_total_per_month_graphics',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#totalPlayersPerMonth').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_total_per_game_graphics',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#totalPlayersPerGame').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_quality_and_forum_resonance_graphics',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#qualityAndResonance').html(data)
    }
})


$.ajax({
    url: '/en_stat/get_often_players_graphics',
    type: 'get',
    data: {
        year: year
    },
    success: function(data){
        $('#oftenPlayers').html(data)
    }
})