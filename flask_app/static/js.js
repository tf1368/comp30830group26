var currWindow = false;
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
                    // Add the co-ordinates and name to each marker and specify which map it belongs to
                    position: {lat: station.position_lat, lng: station.position_long},
                    // Add the station name and number as attributes to the marker, this can be used as an identifier
                    title: station.name,
                    number: station.number,
                    icon:{
                       url: "pointer.svg",
                        scaledSize: new google.maps.Size(38,31)
                    },
                    animation: google.maps.Animation.DROP,
                    // // Also add the available bikes and stands
                    available_bikes: station.available_bikes,
                    available_stands: station.available_bike_stands,
                    // icon: determineAvailabilityPercent(station.available_bikes, station.available_bike_stands),
                    map: map
                    // infowindow: station_info_window,
                });
                var last_update_time = new Date(station.last_update_time).toLocaleString('en-ie');
                marker.addListener("click", () => {
                if (currWindow) {
                    currWindow.close();
                }
                const infowindow = new google.maps.InfoWindow({
                content: "<h3>" + station.name + "</h3>"
                + "<p><b>Available Bikes: </b>" + station.available_bikes + "</p>"
                + "<p><b>Available Stands: </b>" + station.available_bike_stands + "</p>"
                + "<p><b>Last Updated: </b>" + last_update_time + "</p>"
                });
                currWindow = infowindow;
                infowindow.open(map, marker);
                hourlyChart(station.number);
                });
            });
        }).catch(err => {
            console.log("Oops!", err);
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
            width: '700', height: '450',
            hAxis: {title: 'Hour of the Day (00:00)',},
            vAxis: {title: 'Number of Available Bikes'}
        };
        // Make columns for the chart and specify their type and title
        chart_data.addColumn('timeofday', "Time of Day");
        chart_data.addColumn('number', "Average Available Bikes ");

        for (i = 0; i < data.length; i++) {
            chart_data.addRow([[data[i]['Hourly'], 0, 0], data[i]['Avg_bikes_avail']]);
        }
        chart = new google.visualization.LineChart(document.getElementById('hour_chart'));
        chart.draw(chart_data, options);
    });
}