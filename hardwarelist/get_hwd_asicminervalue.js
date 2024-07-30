//I ran this in the browser console on the page https://www.asicminervalue.com/

$(document).ready(function() {
    var fulltext = "";
    // Select the first tbody element on the page
    var $firstTbody = $('tbody').first();

    // Iterate over each tr element within the tbody
    $firstTbody.find('tr').each(function() {
        // For each tr, find all td elements and map their text content into an array
        var tdTexts = $(this).find('td').map(function() {
            return $(this).text().trim(); // Trim the text to remove any extra whitespace
        }).get(); // Get the array of text contents

        // Join the array elements with semicolons
        var rowText = tdTexts.join(';');

        // Print out the resulting string for the current row
        fulltext += rowText + "\n"
    });
    console.log(fulltext);
});