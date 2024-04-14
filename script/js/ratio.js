var ratioChart = echarts.init(document.getElementById('ratio-container'));

const albums = [
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


$.ajax({
	url: '/assets/lyric_stats.csv',
	dataType: 'text',
	success: function(mydata) {

		var ratio_option;
		var singleAxis = [];
		var series = [];
		var title = [];

		albums.forEach(function (album, idx) {
		  title.push({
			textBaseline: 'middle',
			top: ((idx + 0.25) * 100) / 10 + '%',
			text: album[0]
		  });
		  singleAxis.push({
			left: 275,
			bottom: 0,
			type: 'value',
			boundaryGap: false,
			top: (idx * 100) / 10 + '%',
			height: 100 / 10 + '%',
			axisLine: {
				show: false
			},
			axisTick: {
				show: false
			},
			axisLabel: {
				show: false,
			 	//interval: 0.05
			 	interval: 50
			},
			min: 25,
			//max: 0.35
			max: 350
		  });
		  series.push({
			title: album[0],
			name: album[0],
			color: album[1],
			singleAxisIndex: idx,
			coordinateSystem: 'singleAxis',
			type: 'scatter',
			data: [],
			symbolSize: function (dataItem) {
			  //return dataItem[2]/10;
			  return dataItem[2]*100;
			}
		  });
		});

		singleAxis[8].axisLabel.show = true;
		singleAxis[8].axisTick.show = true;
		singleAxis[8].axisLine.show = true;
		singleAxis[8].name = 'Word Count';
		singleAxis[8].nameLocation = 'start';
		singleAxis[8].nameGap = 10;

		// Split the lines  
		var lines = mydata.split('\n');  

		lines.forEach(function(line, lineNo) {  
			var items = line.split(',');  
			if(lineNo !== 0) {
				songtitle = items[3];
				album = items[1];
				
				if (parseFloat(items[6]) === 0.0) {
					ratio = 0.0;
				} else {
					ratio = parseFloat(items[12])/parseFloat(items[6]);
				}

				series.forEach(function(series) {
					if(series.title === album) {
						//series.data.push([ratio.toFixed(3),songtitle,parseFloat(items[6])]);
						series.data.push([parseFloat(items[6]),songtitle,ratio.toFixed(3)]);
					}
				});
			}
		});

		ratio_option = {
			grid: {
				left: '5%',
				right: '5%'
				//bottom: '10%'
			},
			tooltip: {
				position: 'top',
				// trigger: 'axis',
				showDelay: 0,
				formatter: function (params) {
					return (
						'<b>'+params.value[1]+'</b>'+'<br/>' +
						params.seriesName + '<br/>' +
						'Ratio: '+ params.value[2]
					);
				}
			},
			title: title,
			singleAxis: singleAxis,
			series: series
		};

		console.log(ratio_option);

		ratio_option && ratioChart.setOption(ratio_option);
	},
	error: function (e, t) {  
        console.error(e, t);  
    }
});

//ratio_option && ratioChart.setOption(ratio_option);


/*
ratio_option = {
  title: {
    text: 'Pronoun Ratio',
    subtext: 'Data from Genius.com with LyricGenius API, 2022'
  },
  grid: {
    left: '5%',
    right: '20%',
    //bottom: '7%',
    top: '20%',
    //containLabel: true
  },
  tooltip: {
    // trigger: 'axis',
    showDelay: 0,
    formatter: function (params) {
    	return (
          	'<b>'+params.seriesName+'</b>'+'<br/>' +
          	params.value[1] + '<br/>' +
			'Ratio: '+ params.value[0]
        );
    },
    axisPointer: {
      show: true,
      type: 'cross',
      lineStyle: {
        type: 'dashed',
        width: 1
      }
    }
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
    right: 0,
    top: 'center',
	borderWidth: 2
  },
  xAxis: [
    {
	  name: 'Pronoun Ratio',
	  nameLocation: 'middle',
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
	  name: 'Album',
	  nameLocation: 'middle',
	  nameGap: 20,
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

var ratioChart = echarts.init(document.getElementById('agg-container'));
$.ajax({
	url: window.location.origin + '/data/lyric_stats.csv',
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
				['Will Of The People', '#8B572A']
		  
		];

		albums.forEach(function(album) {
			ratio_option.series.push({
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
				ratio = parseFloat(items[12])/parseFloat(items[6]);

				ratio_option.series.forEach(function(series) {
					if(series.name === album) {
						//series.data.push({'x':WordTotal,'y':PTotal,'title':title});
						series.data.push([ratio,title]);
					}
				});
			}
		});
		 
		console.log(ratio_option.series);

		ratio_option && ratioChart.setOption(ratio_option);
	},
	error: function (e, t) {  
        console.error(e, t);  
    }
});

*/
