function callAlert() {
    alert("You're part of clan " + randomFunc(names));
}

function randomFunc(names) {
    return names[Math.floor(Math.random() * names.length)];
    }

const names = [
    "Banu Haqim", "Brujah", "Gangrel", "Hecata", "Lasombra", "Malkavian", "Ministry",
    "Nosferatu", "Ravnos", "Toreador", "Tremere", "Tzimisce", "Ventrue"
]

console.log(randomFunc(names));