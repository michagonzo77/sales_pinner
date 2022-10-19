let map, infoWindow, options, marker;
var markersArray = [];


function initMap() {
    // Map options
    options = {
        zoom: 15,
        center: { lat: 25.7617, lng: -80.1918 }
    }

    // New map
    map = new google.maps.Map(document.getElementById("map"), options);

    // Add Marker Function
    function addMarker(props) {
        if (marker) {
            marker.setPosition(props.coords);
        } else {
            marker = new google.maps.Marker({
                position: props.coords,
                map: map
            });
        }

        if(props.content){
        infoWindow = new google.maps.InfoWindow({
            content:props.content
        });

        marker.addListener('click', function(){
            infoWindow.open(map,marker);
        });

        
    }
}

    // Listen for click on map
    google.maps.event.addListener(map, 'click',
        function (event) {
            addMarker({ coords: event.latLng, content:`
            <form class="pe-3 pb-2" action="/businesses/create" method="post">
            <label for="business_name">Business Name:</label>
            <input type="text" class="form-control" name="business_name" id="business_name">
            <label for="first_name">First Name:</label>
            <input type="text" class="form-control" name="first_name" id="first_name">
            <label for="last_name">Last Name:</label>
            <input type="text" class="form-control" name="last_name" id="last_name">
            <label for="email">Email:</label>
            <input type="text" class="form-control" name="email" id="email">
            <label for="phone">Phone:</label>
            <input type="text" class="form-control" name="phone" id="phone">
            <label for="pipeline_status">Status:</label>
            <select class="form-control" name="pipeline_status" id="pipeline_status">
            <option>Prospected</option>
            <option>Set Meeting</option>
            </select>
            <button class="btn btn-primary mt-1">Submit</button>
            </form>`});
        });

    // Listen for click on marker
    google.maps.event.addListener(map, 'click',
        function () {
            infoWindow.open(map, marker);
        });




    // // Add marker 
    // marker = new google.maps.Marker({
    //     position:{ lat: 25.7617, lng: -80.1918 },
    //     map:map
    // })

    // infoWindow = new google.maps.InfoWindow({
    //     content:'<h1>New Business</h1>'
    // });

    // marker.addListener('click', function(){
    //     infoWindow.open(map, marker);
    // });



    const locationButton = document.createElement("button");

    locationButton.textContent = "Pan to Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    infoWindow.setPosition(pos);
                    infoWindow.setContent("Location found.");
                    infoWindow.open(map);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

window.initMap = initMap;