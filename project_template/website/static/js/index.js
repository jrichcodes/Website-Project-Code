function deleteGearItem(gearItemId){
    fetch('/delete-gearitem', {
        method: "POST",
        body: JSON.stringify({ gearItemId: gearItemId}),
    }).then((_res) => {
        location.reload()
    });
}