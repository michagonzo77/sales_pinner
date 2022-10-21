let map, infoWindow, options, marker;
var all_markers = [];

var curday = function(sp){
    today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //As January is 0.
    var yyyy = today.getFullYear();
    
    if(dd<10) dd='0'+dd;
    if(mm<10) mm='0'+mm;
    return (mm+sp+dd+sp+yyyy);
    };
    console.log(curday('/'));




function initMap() {
    // Map options
    options = {
        zoom: 16,
        center: { lat: 25.7617, lng: -80.1918 }
    }

    // New map
    map = new google.maps.Map(document.getElementById("map"), options);

    // Add Marker Function
    function addMarker(props) {
        // all_markers.push(`${props.coords}`)
        if (marker) {
            marker.setPosition(props.coords);
        } else {
            marker = new google.maps.Marker({
                position: props.coords,
                map: map,
                animation: google.maps.Animation.DROP
            });
        }
        if (props.content) {
            infoWindow = new google.maps.InfoWindow({
                content: props.content
            });
            marker.addListener('click', function () {
                infoWindow.open(map, marker);
            });
        }
        // console.log(all_markers)
    }

    function addSavedMarkers(props){
        console.log(props.coords)
        marker = new google.maps.Marker({
            position: props.coords,
            map: map,
            animation: google.maps.Animation.DROP,
        })
    }

    // Listen for click on map
    google.maps.event.addListener(map, 'click',
        function (event) {
            var myLatLng = event.latLng;
            var lat = myLatLng.lat();
            console.log(lat)
            var lng = myLatLng.lng();
            console.log(lng)
            console.log(event.latLng)
            addMarker({
                coords: event.latLng, 
                content: 
                `
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
                <option value="1" id="prospected">Prospected</option>
                <option value="2" id="set_meeting">Set Meeting</option>
                </select>
                <input type="hidden" name="lat" value=${lat}>
                <input type="hidden" name="lng" value=${lng}>
                <button class="btn btn-primary mt-1">Submit</button>
                </form>`});
                map.data.toGeoJson(function (json) {
                    localStorage.setItem('geoData', JSON.stringify(json));
                });
        });

    // Listen for click on marker
    google.maps.event.addListener(map, 'click',
        function () {
            infoWindow.open(map, marker);
        });

        // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
            // console.log(`Lat: ${position.coords.latitude} Lng: ${position.coords.longitude}`);
            
            // Center map to user's position.
            map.panTo({
                lat: position.coords.latitude,
                lng: position.coords.longitude
            });
        },
        err => alert(`Error (${err.code}): ${getPositionErrorMessage(err.code)}`)
        );
    } else {
        alert('Geolocation is not supported by your browser.');
    }

    function getBusinesses(){
        fetch('/get_businesses')
            .then(res =>  res.json())
            .then(data => {
                console.log(data)
                for( let i = 0; i < data.length; i++){
                    lat = data[i].lat
                    lng = data[i].lng
                    coordobj = {lat: parseFloat(lat), lng: parseFloat(lng)}
                    // console.log(lat + ',' + lng)
                    // console.log(lat)
                    // console.log(lng)
                    addSavedMarkers({
                        coords: coordobj
                    })
                }
            })
    }               
    getBusinesses();

}


// function saveMarker() {
//     map.data.toGeoJson(function (json) {
//         localStorage.setItem('geoData', JSON.stringify(json));
//     });
// }

// function loadMarkers(map) {
//     var data = JSON.parse(localStorage.getItem('geoData'));
//     map.data.addGeoJson(data);
// }


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
    
    
    
    // const locationButton = document.createElement("button");
    
    // locationButton.textContent = "Pan to Current Location";
    // locationButton.classList.add("custom-map-control-button");
    // map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(locationButton);
    // locationButton.addEventListener("onload", () => {
    //     // Try HTML5 geolocation.
    //     if (navigator.geolocation) {
    //         navigator.geolocation.getCurrentPosition(
    //             (position) => {
    //                 const pos = {
    //                     lat: position.coords.latitude,
    //                     lng: position.coords.longitude,
    //                 };
    
    //                 infoWindow.setPosition(pos);
    //                 infoWindow.setContent("Location found.");
    //                 infoWindow.open(map);
    //                 map.setCenter(pos);
    //             },
    //             () => {
    //                 handleLocationError(true, infoWindow, map.getCenter());
    //             }
    //         );
    //     } else {
    //         // Browser doesn't support Geolocation
    //         handleLocationError(false, infoWindow, map.getCenter());
    //     }
    // });