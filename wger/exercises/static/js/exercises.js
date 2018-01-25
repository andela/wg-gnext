/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */

/*
 wger exercise functions
 */

'use strict';

/*
 Highlight a muscle in the overview
 */

function wgerHighlightMuscle(element) {
  var $muscle;
  var muscleId;
  var isFront;
  var divId;
  divId = $(element).data('target');
  isFront = ($(element).data('isFront') === 'True') ? 'front' : 'back';
  muscleId = divId.match(/\d+/);

  // Reset all other highlighted muscles
  $muscle = $('.muscle');
  $muscle.removeClass('muscle-active');
  $muscle.addClass('muscle-inactive');

  // Highlight the current one
  $(element).removeClass('muscle-inactive');
  $(element).addClass('muscle-active');

  // Set the corresponding background
  $('#muscle-system').css('background-image',
    'url(/static/images/muscles/main/muscle-' + muscleId + '.svg),' +
    'url(/static/images/muscles/muscular_system_' + isFront + '.svg)');

  // Show the corresponding exercises
  $('.exercise-list').hide();
  $('#' + divId).show();
}

/*
 D3js functions
 */

function wgerDrawWeightLogChart(data, otherData, divId, otherUser) {
  let ctx = document.getElementById('svg-' + divId);

  // process my data into appropriate fields for the graph
  let listOfChartData = [];
  let chartData = {
    dates: [],
    weight: [],
    reps: []
  };
  data.forEach((element) => {
    element.forEach((item)  => {
      chartData.dates.push(item.date);
      chartData.weight.push(item.weight);
      chartData.reps.push(item.reps);
    });
  });
  listOfChartData.push(chartData);

  // process other user's data into required fields for the graph
  if (otherData) {
    let listOfOtherData =[];
    let otherChartData = {
      dates: [],
      weight: [],
      reps: []
    };
    otherData.forEach((element) => {
      element.forEach((item)  => {
        otherChartData.dates.push(item.date);
        otherChartData.weight.push(item.weight);
        otherChartData.reps.push(item.reps);
      });
    });
    listOfOtherData.push(otherChartData);

    var myChart = new Chart(ctx, {
      type: 'bar',
        data: {
          labels: listOfChartData[0].dates, // dates for x axis
          datasets: [{
            label: "My weights",
            backgroundColor: '#3465a4',
            borderColor: '#3465a4',
            data: listOfChartData[0].weight // to be plotted against the y-axis
          },
          {
            label: "My reps",
              backgroundColor: '#7093bf',
              borderColor: '#7093bf',
              data: listOfChartData[0].reps  // to be plotted against the x-axis
          },
          {
            label: otherUser + "'s weights",
            backgroundColor: '#900C3F',
            borderColor: '#900C3F',
            data: listOfOtherData[0].weight // to be plotted against the y-axis
          },
          {
            label: otherUser + "'s reps",
              backgroundColor: '#F5B9B9',
              borderColor: '#7873bf',
              data: listOfOtherData[0].reps  // to be plotted against the x-axis
          }]
        },
        options: {
        }
    });


  } else {
    var myChart = new Chart(ctx, {
      type: 'bar',
        data: {
          labels: listOfChartData[0].dates, // dates for x axis
          datasets: [{
            label: "My weights",
            backgroundColor: '#3465a4',
            borderColor: '#3465a4',
            data: listOfChartData[0].weight // to be plotted against the y-axis
          },
          {
            label: "My reps",
              backgroundColor: '#7093bf',
              borderColor: '#7093bf',
              data: listOfChartData[0].reps  // to be plotted against the x-axis
          }]
        },
        options: {
        }
    });
  }
}
