var currWindow = false;
let markers = [];
var prediction_time;
var prediction_station;


function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 53.349804,
            lng: -6.260310
        },
        zoom: 15,
        mapId: 'c977067f443727f6',
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false,
    });

    fetch("/stations")
        .then(
            response => {
                return response.json();
            }
        ).then(data =>{
            console.log("data: ", data);

            map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 53.349804, lng: -6.260310},
            zoom: 13.5,
            mapId: 'c977067f443727f6',
            mapTypeControl: false,
            fullscreenControl: false,
            streetViewControl: false,});

            data.forEach(station => {
                console.log("station: ", station);

                const marker = new google.maps.Marker({
                    position: {lat: station.position_lat, lng: station.position_long},
                    title: station.name,

                    available_bikes: station.available_bikes,
                    available_stands: station.available_bike_stands,
                    icon: marker_color(station.available_bikes, station.available_bike_stands),
                    map: map,
                    animation: google.maps.Animation.DROP
                    // infowindow: station_info_window,
                });
                markers.push(marker);
                var last_update_time = new Date(station.last_update_time).toLocaleString('en-ie');
                marker.addListener("click", () => {
                if (currWindow) {
                    currWindow.close();
                }
                const station_info_window = new google.maps.InfoWindow({
                content: "<h3>" + station.name + "</h3>"
                + "<p><b>Available Bikes: </b>" + station.available_bikes + "</p>"
                + "<p><b>Available Stands: </b>" + station.available_bike_stands + "</p>"
                + "<p><b>Last Updated: </b>" + last_update_time + "</p>"
                });

                currWindow = station_info_window;
                station_info_window.open(map, marker);
                hourlyChart(station.number);
                dailyChart(station.number);
                forecast_weather();
                });
            });
        }).catch(err => {
            console.log("Oops!", err);
        });
}

// Function to return a marker colour depending on the amount of available bikes remaining
function marker_color(available_bikes, available_stands) {

    let bikes_availablity = (available_bikes / (available_bikes + available_stands));

    let color;

    if (bikes_availablity == 0) {
        color = "data:image/png;base64,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";
    } else if (bikes_availablity > 0 & bikes_availablity <= 0.25) {
        color = "data:image/png;base64,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";
    } else if (bikes_availablity > 0.25 & bikes_availablity <= 0.5) {
        color = "data:image/png;base64,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";
    } else if (bikes_availablity > 0.5 & bikes_availablity <= 0.75) {
        color = "data:image/png;base64,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";
    } else if (bikes_availablity > 0.75 & bikes_availablity <= 1) {
        color = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAxCAMAAACf+RsMAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAADAFBMVEUAAAAANQUAMgUAWwkAWwgAdwkAXAkAWgoAWwoAWAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAEANAcAOwgAOwgANgcAJQQAIwMAJAQAHgMAAgAAAAAAAwAAAAAAAgAAdRAAjxQAYgsAWwkAXAkAQQYAAAAAAAAAAAAAAAAAMAcAQQkAQQkARQoAhBMAkhQAfRAAeQ8Aeg8AYgwAKQQAJwQAKAQAGgMAAAAAAAAAXA0AmBUAlhUAhxIAXQkAXQkALwUAAAAALwcATAsAexEAkBQAfxAAcg4AXAkASAcALgUAGgMAAAAAAAAAAAAATgsAlRUAlBUAlhUAhBEAXAkAKQQAAAAAAAAAAAAAMAcAWQwAexEAkxUATQsANQcAgRIAehEAMwcASwoAgREAcQ4AWwkASAcANgUAGgMAAAAAAAAAQwkAmRYAkRQAIwUAAAAAdBAAaQ8AAAAALAYAlRUAfxEAWwkAXQkAJAQAAAAAAAAAQgkAJQUAAwAAdBAAag8AAQAALQYAlBUAfxAAIwQAAAAAAAAAAAAAAAAAAgAAAAAARQoAgBEAXgoAXAkAJQQAAAAAAQAAAAAAAAAAMQcAbQ8AgBIAAgAAkxUAkRQAiRMAcQ4ATQgAQQYAFgIAAAAAAAAAkhUAKwYACQEAdxEAbRAABgEAMwcAkxUAeQ8AWgkAWgkAGgIAAAAAAAAAOggAlBUAfRIAdhEAjhQAjBQAdBAAgBIAeA8AWQkAGQIAAAAAOggAAAAAAAAAOggAlRUAeA8AGgIAAAAAAAAAAAAARwkAcA4Acw4AjxQAixMAcQ4AcQ4AZQsANAUAAAAAAAAAXAkAWgkAWgkAXgoAiRMAlRUAgxEAWwkAWwkAWwkAWwkAXgkAWwkAWwgAWwgAagwAbA0Aaw0AaQwAXAgAWwgAWwgAWwgAWgkAWgkAWgkAWgkAXAkAWwoAWwoAWwoAWAoAAAAAmBUAlhUAlRUAlxUAXAkAWwkAOgj///8d2Jt5AAAA93RSTlMAAAAAAAAAAAAABUZaWUACC8X7/LUBQ2lnbdj8+vX1+vzPazoBpPj48vD+/fb+jkR8vO7t6/j26e3t5+zt7rF6j+v+/vb7/umNtunw9ujo/u3osos3e+r+/fzq+/JmP5297fH+7uv49u3f6+n98uy9mTTz/v73+Pj3/ev76fz9/lRl8vj4+ff+7Pzq/flTAwZp9+/o9vz48lg+uNL19/n89vXx+fDGszH+8e/39fPn/fH9+fP1Qvz+8/D7+vDy8fnxQf1R9Pj68O7tHFKR6+j37err8olQFmD49/H2/ej1+PfxThtGRc729LJHRBYLvvbymwMqNiIBSiTnRQAAAAFiS0dE/6UH8sUAAAAHdElNRQfmBA0VIBCZ/Xl/AAAB+UlEQVQ4y2NgGM6Ai5uHFwh4+PgJKBQQ/C4kLCz0XQSfQlExcQlJKWkZWTl5BUUlCXFlXApVVL9/V1P/8VNDU0tbR/f7dz0c6vQNDI2MTUx//jIzt7C0sraxtbPHbqbDd0cn55+/gOCns7OLq7ab+3d7LMrEPDy9vMHKwMDH188/IDAoOARDYej3MKefv8IjoArDI6Oi/d1ivseiKYuLT0hM+vkrOSU1DWJ5ekZmVnZObl5+QSGKwtjvRcVAFSWlZeW/QQp/V1RWVdfU/qmrF25AUdj4vQmkoKS5pRWisK29o7Or9q9Wd08vkrK+/gkTJ2EqnDxlqta06TP6++AKZ86aPWfuL7DCeTCFuh3zFyxclLN4ydJly+EKG4T/OYH9sGLlqtUQhWvWrlv/6+eGjX82bd6yFa6wt2dbODhQtu/YuQsSPLv37A3/9XPfxr/7D0w/iKnw18/fv2AMoBV4FKKCUYWjCqmq8JAzVoUbwAoRKfzwkaPHqqEAbnQ4kHMcqPDEST64wlOnz5yFgnPnYaZduHj20uW/fzdduXoNkV8Zr9+4CQY3bt2OgIA7d+/dvHn/wf2Hj5iQMjbz4ydPIeDRs+cvwOD5y1dggddvWJAVwsHbd+8/gMH7j6wQERZkhXDA9unzFyj4+o2dATdgY+OAA058Coc0AAAwih26GbZCFAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wNC0xM1QyMTozMTozMSswMDowMAfqwWEAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDQtMTNUMjE6MzE6MzErMDA6MDB2t3ndAAAAAElFTkSuQmCC";    }
    return color;
}


// Function to filter markers based on selected colour in radio buttons
function filterMarkers(color) {

    // First we can check if all colours was selected and just make all markers visible
    if (color == "all") {
        for (let i = 0; i < markers.length; i++) {
             markers[i].setVisible(true)
        }
    } else {
        // make an array to store all the markers of this colour
        let colouredMarkers = [];
        for (let i = 0; i < markers.length; i++) {
            if (color == markers[i].icon) {
                colouredMarkers.push(markers[i]);
            }
            // First make all markers invisible as we're looping through
            markers[i].setVisible(false);
        }
        // Then make all the markers of the selected colour visible
        for (let i = 0; i < colouredMarkers.length; i++) {
            colouredMarkers[i].setVisible(true);

        }
    }
}


// Function will be called on page load to display current weather type
function currentWeather() {
    fetch("/current_weather").then(
        response => {
            return response.json();
        }).then(
            data => {
                console.log("currentWeather: ", data[0]["main"])
                document.getElementById("displayWeatherType").textContent =
                    "  Currently the weather is: " + data[0]["description"]+
                    " Temperature: " + parseInt(data[0]["temp"] -  273.15 ) + "°C"+
                    " Feels like: " + parseInt(data[0]["feels_like"] -  273.15 ) + "°C";
            })
}

// Function to graph the average availability by hour for a clicked station
function forecast_weather() {
    fetch("/weather_forecast").then(response => {
            return response.json();
        }).then(data => {

        // Load the chart object from the api
        table_data = new google.visualization.DataTable();

        options = {
               showRowNumber: false,
               allowHtml: true,
               width: '50%',
               height: '100%',
            };

        // Make columns for the chart and specify their type and title
        table_data.addColumn('string',"Date");
        table_data.addColumn('string', "Weather");
        table_data.addColumn('number', "Average temperature(°C)");
        table_data.addColumn('number', "Average wind speed");
        // Add data.
        for (i = 3; i >= 0; i--) {
            var date = new Date(data[i]['Daily']).toLocaleDateString('en-ie');
            table_data.addRows([
               [date, data[i]['main'], data[i]['Avg_temp'] - 273.15, data[i]['Avg_wind_speed']]
            ]);
        }
        table = new google.visualization.Table(document.getElementById('forecast_table'));
        table.draw(table_data, options);
    });
}


// Function to graph the average availability by hour for a clicked station
function hourlyChart(station_number) {
    fetch("/hourly/"+station_number).then(response => {
            return response.json();
        }).then(data => {

        // Load the chart object from the api
        chart_data = new google.visualization.DataTable();

        // Info for the graph such as title
        options = {
            title: 'Average Availability Per Hour',
            width: '300', height: '200',
            hAxis: {title: 'Hour of the Day (00:00)',},
            vAxis: {title: 'Number of Available Bikes'}
        };

        // Make columns for the chart and specify their type and title
        chart_data.addColumn('timeofday', "Time of Day");
        chart_data.addColumn('number', "Average Available Bikes ");
        // Add data.
        for (i = 0; i < data.length; i++) {
            chart_data.addRow([[data[i]['Hourly'], 0, 0], data[i]['Avg_bikes_avail']]);
        }
        chart = new google.visualization.LineChart(document.getElementById('hour_chart'));
        chart.draw(chart_data, options);
    });
}


// Function to graph the average availability by day in week for a clicked station
function dailyChart(station_number) {
    fetch("/daily/"+station_number).then(response => {
            return response.json();
        }).then(data => {

        var chosen_station;
        var analysis_title_output = "";

        bike_stands = 0;
        bikes_free = 0;
        count = 0;
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        day_name_abbreviation = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"];
        average = [];
        for (i = 0; i < day_name.length; i++) {
            data.forEach(obj => {
                chosen_station = obj.name;

                if (obj.DayName == day_name[i]) {
                    bike_stands = obj.Avg_bike_stands;
                    bikes_free = bikes_free + obj.Avg_bikes_free;
                    count = count + 1;
                }
            })
            average.push(bikes_free/count);
            bikes_free = 0;
            count = 0;
        }

         chart_data = new google.visualization.DataTable();
         options = {
             title: 'Average Availability Per Day',
             width: '300', height: '200',
             vAxis: {
                title: 'Number of Bikes'
             }
        };
        chart_data.addColumn('string', "Week_Day_No");
        chart_data.addColumn('number', "Average Bikes Available");

        for (i = 0; i < day_name.length; i++) {
            chart_data.addRow([day_name_abbreviation[i], average[i]]);
        }

        analysis_title_output = "<h2>" + chosen_station + "</h2>";
        document.getElementById("analysis_title").innerHTML = analysis_title_output;

        chart = new google.visualization.ColumnChart(document.getElementById("daily_chart"));
        chart.draw(chart_data, options);
    });
}

// Prediction Function
function prediction(station_number,time) {
    console.log("In prediction function" + station_number + time)

    fetch("/prediction/"+station_number+"/"+time).then(response => {
        return response.json();
    }).then(data => {

        console.log(data)
        console.log("availabilityPrediction: ", data.bikes)

        document.getElementById("displayPrediction").textContent =
                    "Available Bikes: " + + data.bikes
    })
}

// Function to populate the select dropdown menu for prediction station
function predictionStationDropDown() {
    fetch("/stations").then(response => {
        return response.json();
    }).then(data => {

        var station_output = "<form><label for='station_option'>Choose a station: </label>"
            + "<select name='station_option' id='station_option' onchange='setPredictionStation(this)'>"
            + "<option value='' disabled selected> ------------------------------------------- </option><br>";

        data.forEach(station => {
            station_output += "<option value=" + station.number + ">" + station.name + "</option><br>";
        })

        station_output += "</select></form><button type=\"button\" onclick='setPredictionValue()'>predict</button> ";
        document.getElementById("prediction_station").innerHTML = station_output;

    }).catch(err => {
        console.log("Error:", err);
    })
}

// Function to populate the select dropdown menu for prediction time
function predictionDateDropDown() {
    fetch("/weather_forecast_time").then(response => {
            return response.json();
        }).then(data => {

            console.log("predictionDateDropDown:", data);

            var date_output = "<form><label for='future_date'>choose an hour in the next 4 days:</label>"
            + "<select name='date_option' id='date_option' onchange='setPredictionTime(this)'>"
            + "<option value='' disabled selected> ------------------------------------------- </option><br>";

            for (i = 95; i >= 0; i--) {
                var date = new Date(data[i]['Daily']);
                date_output += "<option value="+data[i]['Daily']/1000+">" + date + "</option><br>";}

            date_output += "</select></form>";

            document.getElementById("prediction_date").innerHTML = date_output;

        }).catch(err => {
        console.log("Error:", err);
    })
}

// Function to set user choice prediction time
function setPredictionTime(control) {
    prediction_time = control.value;
    console.log("setPredictionTime: " + prediction_time)
}

// Function to set user choice station
function setPredictionStation(control) {
    prediction_station = control.value;
    console.log("setPredictionTime: " + prediction_station)
}

// Function to trigger prediction function
function setPredictionValue() {
    console.log("setPredictionValue: " + prediction_station + prediction_time)
    prediction(prediction_station,prediction_time);
}