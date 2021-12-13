$(document).ready(function(){
    $('div#intro-text button.loads').click(function() {
        var ajax_url = $(this).attr('data-ajax-url');

        $.ajax({
            url: ajax_url,
            data: {
                format: 'json'
            },
            type: 'GET',
            // The type of data we expect back
            dataType : "jsonp",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
        .done(function( json ) {
            // alert("request received successfully")
            if(json.success == 'success') {
                var loadDiv = $(this).siblings('div.info');
                var $loadTxt = $('<h3>').text("A non-religious, non-political student organization aiming to promote Persian culture among Virginia Tech Community");

                // $(loadDiv).text(loadTxt);
                $('.info').append($loadTxt);


            }
            else {
                alert("Error: " + json.error)
            }

        })
        // // Code to run if the request fails; the raw request and
        // // status codes are passed to the function
        // .fail(function( xhr, status, errorThrown ) {
        //     alert( "Sorry, there was a problem!" );
        //     console.log( "Error: " + errorThrown );
        //     // console.log( "Status: " + status );
        //     // console.dir( xhr );
        // })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });


    $('div.event-story button.register').click(function() {
        var story_id = $(this).attr('data-story-id');
        var ajax_url = $(this).attr('data-ajax-url');

        // Using the core $.ajax() method
        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                story_id: story_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
            // alert("request received successfully")
            if(json.success == 'success') {
                var registerDiv = $(this).siblings('div.registered');
                var newRegister = json.registered + " Registered";
                $(registerDiv).text(newRegister);

                var successMsg = $('<p class="register-success">Register Successful!</p>');
                $(successMsg).appendTo( $(this).parent() ).fadeOut('slow', function(){
                    $(this).remove();

        });
            }
            else {
                alert("Error: " + json.error)
            }

        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            // console.log( "Status: " + status );
            // console.dir( xhr );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });


    $('div.event-like button.like').click(function() {
        var story_id = $(this).attr('data-story-id');
        var ajax_url = $(this).attr('data-ajax-url');

        // Using the core $.ajax() method
        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                story_id: story_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
            // alert("request received successfully")
            if(json.success == 'success') {
                var scoreDiv = $(this).siblings('div.score');
                var newScore = json.score;
                $(scoreDiv).text(newScore);

                var successMsg = $('<p class="like-success">Like Successful!</p>');
                $(this).parent().append(successMsg);
                $(successMsg).appendTo( $(this).parent() ).fadeOut('slow', function(){
                    $(this).remove();

        });
            }
            else {
                alert("Error: " + json.error)
            }

        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            // console.log( "Status: " + status );
            // console.dir( xhr );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });

    $('div.event-like button.dislike').click(function() {
        var story_id = $(this).attr('data-story-id');
        var ajax_url = $(this).attr('data-ajax-url');

        // Using the core $.ajax() method
        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                story_id: story_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
            // alert("request received successfully")
            if(json.success == 'success') {
                var scoreDiv = $(this).siblings('div.score');
                var newScore = json.score;
                $(scoreDiv).text(newScore);

                var successMsg = $('<p class="like-success">Dislike Successful!</p>');
                $(this).parent().append(successMsg);
                $(successMsg).appendTo( $(this).parent() ).fadeOut('slow', function(){
                    $(this).remove();

        });
            }
            else {
                alert("Error: " + json.error)
            }

        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            // console.log( "Status: " + status );
            // console.dir( xhr );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        // alert( "The request is complete!" );
        });
    });



    // event handler for date
    $('div#intro-text button.load').click(function(){
        var loadDiv = $(this).siblings('div.info');
        var loadTxt = $('<h3>').text("A non-religious, non-political student organization aiming to promote Persian culture among Virginia Tech Community");

        $(loadDiv).append(loadTxt)

    });

    // checks the querystring for main search box
    checkQueryStringMain();
    // checks the querystring for event search box
    checkQueryString();

    // event handler for navigation sub bar
    // it adds sub menu to the 'about' tab of the navigation bar
    // and it changes the 'about' background color
    $('.about-parent').click(function() {
        var menu = $('<div class="dd-menu">\n' +
            '                    <ul>\n' +
            '                        <li>\n' +
            '                            <a href="/events/isvt" class="dd_menu_a">\n' +
            '                                <div class="fold">\n' +
            '                                    <span class="text">What is ISVT?</span>\n' +
            '                                </div>\n' +
            '                            </a>\n' +
            '                        </li>\n' +
            '                        <li>\n' +
            '                            <a href="/events/directory" class="dd_menu_a">\n' +
            '                                <div class="fold">\n' +
            '                                    <span class="text">Executive Board</span>\n' +
            '                                </div>\n' +
            '                            </a>\n' +
            '                        </li>\n' +
            '                        <li>\n' +
            '                            <a href="/events/join" class="dd_menu_a">\n' +
            '                                <div class="fold">\n' +
            '                                    <span class="text">Become a Member</span>\n' +
            '                                </div>\n' +
            '                            </a>\n' +
            '                        </li>\n' +
            '                    </ul>\n' +
            '                </div>');
        document.getElementById("text").style.backgroundColor="#000000";

        $(menu).appendTo( $(this).parent() ).mouseleave(function(){
            $(this).remove();
            document.getElementById("text").style.backgroundColor="#808080";
        });
        console.log(menu);
    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// checkQueryString function that simulates search feature,
// on search box in the header of all pages.
// When the user types in a search phrase and clicks the enter on keyboard,
// they will be redirected to a search results page.
function checkQueryStringMain(){
    var querystring = window.location.search;

    var urlParams = new URLSearchParams(querystring);
    if(urlParams.has("search")) {
        var keyword = urlParams.get("search");
        if(keyword == 'event') {
            window.location.href="/events/stories";
        }
        else {
            window.alert("No results were found. Please try your search again.");
        }
    }
}

// checkQueryString function that simulates search feature
// on event search box in the event page.
// When the user types in a search phrase and clicks the enter on keyboard,
// they will be redirected to a search results page.
function checkQueryString(){
    var querystring = window.location.search;

    var urlParams = new URLSearchParams(querystring);
    if(urlParams.has("search-event")) {
        var keyword = urlParams.get("search-event");
        if(keyword == 'celebration') {
            window.location.href="/events/stories/results";
        }
        else {
            window.alert("No results were found. Please try your search again.");
        }
    }
}


//Event handler for click on a delete button
function deleteClick () {
    deleteComment($(this).data('id'));
}

function addComment(comment) {
    //Create a new div with id "comment-[id]" containing the comment
    var $commentDiv = $('<div />', {
        id: 'comment-' + comment.id,
        'class': 'comment',
        html: comment.text
    })

    //Create the delete button with the attribute data-id,
    //which will be used for deleting
    var $deleteLink = $('<a href="#" data-id="' + comment.id + '"/>', {
        'class': 'delete_comment',
        html: '<p><img src="images/icon_del.gif" alt="delete"></p>',
        click: deleteClick //Reference to the event handler we created above
    });

    //Add the delete button to the comment div
    $commentDiv.append($deleteLink);
    //Add the comment div to your comment area
    $('#show-comments').append($commentDiv);
}

function deleteComment(id) {
    $.ajax('delete_comment.php', {
        type: 'POST',
        data: {
            id: id
        },
        success: function() {
            //Ajax successful: remove the comment div from your comment area
            $('#comment-' + id).remove();
        },
        error: function() {
            //Ajax not successful: show an error
            alert('An error occured while deleting the comment!');
        }
    });
}