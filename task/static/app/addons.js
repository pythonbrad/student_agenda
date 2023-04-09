// This script contains all addons who can will be used in the application
Addons = {
    // This function permit to communicate with the server
    request: function (_url, _json, _func, _async=true) {
        $.ajax({
            url: _url,
            type: _json ? 'post' : 'get',
            dataType: 'json',
            ContentType: 'application/json',
            success: _func,
            data: _json,
            async: _async
        });
    },
}