"use strict";

var codegen = {
    // Helpers
    pressAndHold: function(id, handler) {
        var timeoutId = 0;
        $('#' + id).off('mousedown').mousedown(function() {
            timeoutId = setTimeout(handler, 1000);
        }).on('mouseup mouseleave', function() {
            clearTimeout(timeoutId);
        });
    }
}
