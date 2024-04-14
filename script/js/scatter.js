var scatter_option;
scatter_option = {
  // title: {
  //   text: 'Word Count vs Pronoun Count',
  //   subtext: 'Data from Genius.com with LyricGenius API, 2022'
  // },
  grid: {
    left: '10%',
    right: '10%',
    //bottom: '7%',
    top: '5%',
    //containLabel: true
  },
  tooltip: {
    // trigger: 'axis',
    showDelay: 0,
    formatter: function (params) {
    	return (
          	'<b>'+params.value[2]+'</b>'+'<br/>' +
          	//params.seriesName + '<br/>' +
			'Words: '+ params.value[0] + '<br/>' +
			'Pronouns: '+ params.value[1] + '<br/>'
        );
    },
  },
  toolbox: {
    feature: {
      dataZoom: {},
      brush: {
        type: ['rect', 'polygon', 'clear']
      }
    }
  },
  brush: {},
  legend: {
	orient: 'vertical',
    right: 25,
    top: 35,
	float: true,
	borderWidth: 2,
	itemGap: 2,
  },
  xAxis: [
    {
	  name: 'Word Count',
	  nameLocation: 'middle',
	  nameGap: 30,
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        show: false
      }
    }
  ],
  yAxis: [
    {
	  name: 'Pronoun Count',
	  nameLocation: 'middle',
	  nameGap: 30,
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        show: false
      }
    }
  ],

  // filled in with jquery/ajax from csv 
  series: []
};

var scatterChart = echarts.init(document.getElementById('scatter-container'));
$.ajax({
	url: '/assets/lyric_stats.csv',
	dataType: 'text',
	success: function(mydata) {

		var albums = [
				['Showbiz', '#10DBEB'],
				['Origin of Symmetry', '#F1C41C'],
				['Absolution', '#6A768D'],
				['Black Holes and Revelations', '#F56E23'],
				['The Resistance', '#500790'],
				['The 2nd Law', '#47C017'],
				['Drones', '#000000'],
				['Simulation Theory', '#FF37DB'],
				['Will of the People', '#8B572A']
		  
		];

		albums.forEach(function(album) {
			scatter_option.series.push({
				name: album[0], 
				color: album[1],
				data: [],
				type: 'scatter',
				emphasis: {
					focus:'series'
				}
			});
		});


        // Split the lines  
        var lines = mydata.split('\n');  

		lines.forEach(function(line, lineNo) {  
			var items = line.split(',');  
			if(lineNo !== 0) {
				title = items[3];
				album = items[1];
				WordTotal = parseFloat(items[6]);
				UniqueWords = parseFloat(items[5]);
				PTotal = parseFloat(items[12]);

				scatter_option.series.forEach(function(series) {
					if(series.name === album) {
						series.data.push([WordTotal,PTotal,title]);
					}
				});
			}
		});
		 
		scatter_option && scatterChart.setOption(scatter_option);
	},
	error: function (e, t) {  
		console.log(e);
		console.log(t);
        console.error(e, t);  
    }
});


