let submit = document.getElementById("submit");
console.log(submit);
console.log("dsf");
let soil_types = {
    "Black":0,
    "Clayey":1,
    "Loamy":2,
    "Red":3,
    "Sandy":4
}
let crop_type={
    "Barley":0,
    "Cotton":1,
    "Ground_Nuts":2,
    "Maize":3,
    "Millets":4,
    "Oil_seeds":5,
    "Paddy":6,
    "Pulses":7,
    "Sugarcane":8,
    "Tobacco":9,
    "Wheat":10
}


let soiltype = document.getElementById("soiltype");
soiltype.addEventListener("change",(event)=>{
    document.getElementById("soiltypes").value=soiltype.value;
})


let croptype = document.getElementById("croptype");
croptype.addEventListener("change", (event) => {
    document.getElementById("croptypes").value = croptypes.value;
})




submit.addEventListener("click", (event)=>{
    console.log(document.getElementById("soiltypes").value);
    console.log(document.getElementById("croptypes").value);
    event.preventDefault();

})