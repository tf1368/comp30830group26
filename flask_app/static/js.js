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

                new google.maps.Marker({
                    // Add the co-ordinates and name to each marker and specify which map it belongs to
                    position: {lat: station.position_lat, lng: station.position_long},
                    // Add the station name and number as attributes to the marker, this can be used as an identifier
                    title: station.name,
                    number: station.number,
                    // // Also add the available bikes and stands
                    available_bikes: station.available_bikes,
                    available_stands: station.available_bike_stands,
                    // icon: determineAvailabilityPercent(station.available_bikes, station.available_bike_stands),
                    map: map
                    // infowindow: station_info_window,
                })

            });

        }).catch(err => {
            console.log("Oops!", err);
        });
}
