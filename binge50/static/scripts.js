var iframes = [];

$(document).ready(function() {
    
    // generate youtube iframe for each tvshow
    $.getJSON(Flask.url_for('json'), function(tvshows) {
        for (var i = 0; i < tvshows.length; i++) {
            iframes.push(youtube(tvshows[i]));
        }
    }); 
    
    // pause all trailers
    for (var i = 0; i < iframes.length; i++) {
        iframes[i].pauseVideo();  
    };
    
    // generate circular rating bars
    drawCircle('.circle_imdb', '#f6da51');
    drawCircle('.circle_tomato', '#df6c4f');
    drawCircle('.circle_metascore', '#1a99aa');
    
    // animate navbar icons
    spinIcon('#update-spinner');
    
    // provide sound event listener7
    clickUnmute('#sound-spinner', iframes);
    
    // update animation
    $('#update-spinner').click(function(e) {
        e.preventDefault();
        drawCircle('.circle_imdb', '#f6da51');
        drawCircle('.circle_tomato', '#df6c4f');
        drawCircle('.circle_metascore', '#1a99aa');        
    })
});

/**
 * Generate youtube trailer iframe based on the id stored in tvshow.trailer
 */
function youtube(tvshow) {
    var player = new YT.Player(tvshow.trailer, {
        videoId: tvshow.trailer,       // YouTube Video ID
        width: '100%',                 // Player width (in px)
        height: '100%',                // Player height (in px)
        playerVars: {
            autoplay: 1,               // Auto-play the video on load
            controls: 0,               // Show pause/play buttons in player
            showinfo: 0,               // Hide the video title
            modestbranding: 1,         // Hide the Youtube Logo
            loop: 1,                   // Run the video in a loop
            fs: 1,                     // Hide the full screen button
            cc_load_policy: 0,         // Hide closed captions
            iv_load_policy: 3,         // Hide the Video Annotations
            autohide: 1,               // Hide video controls when playing
            rel: 0,                    // Hide related videos
            playlist: tvshow.trailer,  // Run the video in a loop
            start: 32
        },
        events: {
            onReady: function(e) {
                e.target.mute();
                $('#'+tvshow.trailer).parent().hover(
                    function() {
                        e.target.playVideo();
                    },
                    function() {
                        e.target.pauseVideo();
                    }
                 );
                $('#'+tvshow.trailer).parent().addClass('initialized');
            },
            onStateChange: function(e) {
                if ($('#'+tvshow.trailer).parent().hasClass('initialized')) {
                    e.target.pauseVideo();
                    $('#'+tvshow.trailer).parent().removeClass('initialized');
                }
            }
        }
    });
    return player;
}

/**
 * Generate circular progress bar based on target element and color
 */
function drawCircle(element, color) {
    $(element).circleProgress({
        size: 200,
        thickness: 8,
        startAngle: 0.5 * Math.PI,
        fill: color
    });    
}

/**
 * Animate Font Awesome icons on hover
 */
function spinIcon(element) {
    $(element).hover(
        function() {
            $(this).children('.fa').addClass('fa-spin');
        },
        function() {
            $(this).children('.fa').removeClass('fa-spin');
        }
    );    
}

/**
 * Click event listeners for sound-spinner
 */
function clickUnmute(element, array) {    
    $(element).click(function(e) {
        if ($(this).children().hasClass('fa-volume-off')) {
            
            $(this).children()
            .removeClass('fa-volume-off')
            .addClass('fa-volume-up');
            
            for (var i = 0; i < array.length; i++) {
                if (array[i].a != null) {
                    array[i].unMute();
                }
            }
            
            e.preventDefault();
        }
        else {
            
            $(this).children()
            .removeClass('fa-volume-up')
            .addClass('fa-volume-off');
            
            for (var i = 0; i < array.length; i++) {
                if (array[i].a != null) {
                    array[i].mute();  
                }
            }    
            
            e.preventDefault();
        }
    });
}