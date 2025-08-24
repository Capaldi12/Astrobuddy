"use strict";

// Loads data when document is loaded
$(document).ready(function() {
    $.ajax({
        url: 'data/data.json',
        method: 'GET',
        dataType: 'json',

        success: function(data) {
            /* I put the data on the document, then tell context provider
             * where to take it. There's probably a better way to do it,
             * but given that's the only time data changes, I figured it
             * is fine for now...
             */

            document.gameData = data;
            $('data-context').attr('data-attr', 'gameData');
        },

        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data: ', textStatus, errorThrown);
            alert('Error fetching data. See console for details.');
        }
    });

});
