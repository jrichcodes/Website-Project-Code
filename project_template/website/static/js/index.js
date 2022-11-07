function deleteGearItem(gearItemId, tripId){
    fetch('/delete-gearitem', {
        method: "POST",
        body: JSON.stringify({ gearItemId: gearItemId}),
    }).then((_res) => {
        window.location.href = "/trip-summary/" + tripId;
    });
}

function deleteTrip(tripId) {
    fetch('/delete-trip', {
        method: "POST",
        body: JSON.stringify({tripId: tripId}),
    }).then((_res) => {
        window.location.href = "/events";
    });
}