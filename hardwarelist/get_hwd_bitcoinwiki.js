//I ran this in the browser console on the pages:
//https://en.bitcoin.it/wiki/Mining_hardware_comparison
//https://en.bitcoin.it/wiki/Non-specialized_hardware_comparison

var tables = document.querySelectorAll('.wikitable');
var output = [];
var hashTable = {};

tables.forEach((element, index) => {
    console.log(`Index: ${index}`);
    var rows = element.querySelectorAll('tr');

    for (var i = 1; i < rows.length; i++) {

        // delete any <sup> tags
        var sups = rows[i].querySelectorAll('sup');
        for (var j = 0; j < sups.length; j++) {
            sups[j].remove();
        }

        var cells = rows[i].querySelectorAll('td');


        var hardwareName = cells[0].textContent.trim();
        var hashrate = cells[1].textContent.trim().replace(/[^0-9.]/g, "");
        var efficiency = cells[2].textContent.trim().replace(/[^0-9.]/g, "");
        var Watts = cells[4].textContent.trim().replace(/[^0-9.]/g, "");



        //check if page url contains "Non" and index is 1
        if (window.location.href.includes("Non") && index === 1) {
            Watts = cells[3].textContent.trim().replace(/[^0-9.]/g, "");
        }


        if (!hashTable[hardwareName]) {
            hashTable[hardwareName] = {
                hashrate: {
                    total: 0,
                    count: 0
                },
                efficiency: {
                    total: 0,
                    count: 0
                },
                Watts: {
                    total: 0,
                    count: 0
                }
                
            };
        }

        if (/\d/.test(hashrate)) { // check if there are any digits present in hashrate
            hashrate = parseFloat(hashrate);
            hashTable[hardwareName].hashrate.total += hashrate;
            hashTable[hardwareName].hashrate.count++;
        }

        if (/\d/.test(efficiency)) { // check if there are any digits present in efficiency
            efficiency = parseFloat(efficiency);
            hashTable[hardwareName].efficiency.total += efficiency;
            hashTable[hardwareName].efficiency.count++;
        }

        if (/\d/.test(Watts)) { // check if there are any digits present in Watts
            Watts = parseFloat(Watts);
            hashTable[hardwareName].Watts.total += Watts;
            hashTable[hardwareName].Watts.count++;
        }
    }
});

for (var hardware in hashTable) {
    var avgHashrate = hashTable[hardware].hashrate.count > 0 ? hashTable[hardware].hashrate.total / hashTable[hardware].hashrate.count : 'unknown';
    var avgEfficiency = hashTable[hardware].efficiency.count > 0 ? hashTable[hardware].efficiency.total / hashTable[hardware].efficiency.count : 'unknown';
    var avgWatts = hashTable[hardware].Watts.count > 0 ? hashTable[hardware].Watts.total / hashTable[hardware].Watts.count : 'unknown';

    //if avgEfficiency is unknown but the other two are not, then calculate it
    // if (avgEfficiency === 'unknown' && avgHashrate !== 'unknown' && avgWatts !== 'unknown') {
    //     avgEfficiency = avgHashrate / avgWatts;
    // }

    output.push(hardware + ';' + (avgHashrate+"") + ';' + (avgEfficiency+"")); // + ';' + (avgWatts+"")
}

console.log(output);