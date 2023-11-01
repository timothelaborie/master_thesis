//I ran this in the browser console on the page https://en.bitcoin.it/wiki/Mining_hardware_comparison

var tables = document.querySelectorAll('.wikitable');
var output = [];
var hashTable = {};

tables.forEach((element, index) => {
    console.log(`Index: ${index}`);
    var rows = element.querySelectorAll('tr');

    for (var i = 1; i < rows.length; i++) {
		if(true){
			var cells = rows[i].querySelectorAll('td');
			var hardwareName = cells[0].textContent.trim();
			var hashrate = cells[1].textContent.trim().replace(/[^0-9.]/g, "");
			var efficiency = cells[2].textContent.trim().replace(/[^0-9.]/g, "");
		} else {
			var cells = rows[i].querySelectorAll('td');
			var hashrate = cells[0].textContent.trim().replace(/[^0-9.]/g, "");
			var efficiency = cells[1].textContent.trim().replace(/[^0-9.]/g, "");
			var th = rows[i].querySelectorAll('th');
			var hardwareName = th[0].textContent.trim();
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
    }
});

for (var hardware in hashTable) {
    var avgHashrate = hashTable[hardware].hashrate.count > 0 ? hashTable[hardware].hashrate.total / hashTable[hardware].hashrate.count : 'N/A';
    var avgEfficiency = hashTable[hardware].efficiency.count > 0 ? hashTable[hardware].efficiency.total / hashTable[hardware].efficiency.count : 'N/A';
    output.push(hardware + '<sep>' + (avgHashrate+"").substr(0,6) + '<sep>' + (avgEfficiency+"").substr(0,6));
}

console.log(output);