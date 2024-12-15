document.addEventListener('DOMContentLoaded', async function() {

document.getElementById('calendar_').addEventListener('click', function() {
    window.location.href = "tms";
});

document.getElementById('statistics_').addEventListener('click', function() {
    window.location.href = "statistics";
});

document.getElementById('vaq_request_').addEventListener('click', function() {
    window.location.href = "vaq_request";
});

document.getElementById('logoutButton').addEventListener("click", ()=>{
    console.log("clicked");
    $.ajax({
    url: `/logout`,
    type: "POST",
    success: function(data) {

        window.location.replace("/");
    },
    error: function(error) {
        alert("Couldn't check out!");
    }
    });
}
)


document.getElementById('check-in-btn').addEventListener("click", function(){
    $.ajax({
    url: `/check-in`,
    type: "GET",
    success: function(data) {
        console.log("Checked in!");

    },
    error: function(error) {
        alert("Couldnt check in!");
    }
    });
})

document.getElementById('check-out-btn').addEventListener("click", function(){
    $.ajax({
    url: `/check-out`,
    type: "GET",
    success: function(data) {
        console.log("Checked out!");
    },
    error: function(error) {
        alert("Couldn't check out!");
    }
    });
})

});
