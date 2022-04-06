var currWindow = false;
let markers = [];


function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 53.349804,
            lng: -6.260310
        },
        zoom: 13.5,
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
        color = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
    } else if (bikes_availablity > 0 & bikes_availablity <= 0.25) {
        color = "http://maps.google.com/mapfiles/ms/icons/orange-dot.png";
    } else if (bikes_availablity > 0.25 & bikes_availablity <= 0.5) {
        color = "http://maps.google.com/mapfiles/ms/icons/purple-dot.png";
    } else if (bikes_availablity > 0.5 & bikes_availablity <= 0.75) {
        color = "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";
    } else if (bikes_availablity > 0.75 & bikes_availablity <= 1) {
        color = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
    }
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
                    "       Weather: " + data[0]["description"]+
                    " Temperature: " + parseInt(data[0]["temp"] -  273.15 ) + "°C"+
                    " Feels like: " + parseInt(data[0]["feels_like"] -  273.15 ) + "°C"
                    // +
                    // " Humidity: " + data[0]["humidity"] + "%"+
                    // " Wind speed: " + data[0]["wind_speed"] + "m/s";
            })
}
// Function to graph the average availability by hour for a clicked station
function forecast_weather(station_number) {
    fetch("/forecast_weather/"+station_number).then(response => {
            return response.json();
        }).then(data => {

        // Load the chart object from the api
        chart_data = new google.visualization.DataTable();

        // Info for the graph such as title
        options = {
            title: 'Forecast Temperature Per Hour',
            width: '700', height: '400',
            hAxis: {title: 'Hour of the Day (00:00)',},
            vAxis: {title: 'celcius',},
        };

        // Make columns for the chart and specify their type and title
        chart_data.addColumn('timeofday', "Time of Day");
        chart_data.addColumn('Temperature', "temp");
        // Add data.
        for (i = 0; i < data.length; i++) {
            chart_data.addRow([[data[i]['Hourly'], 0, 0], data[i]['temp']]);
        }
        chart = new google.visualization.LineChart(document.getElementById('forecast_chart'));
        chart.draw(chart_data, options);
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
            width: '700', height: '400',
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
             width: '700', height: '400',
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
