const checkInBtn = document.getElementById('check-in-btn');
const checkOutBtn = document.getElementById('check-out-btn');

    // Funktion zum Aktivieren und Deaktivieren der Buttons
    function toggleButtons() {
        if (checkInBtn.disabled) {
            checkInBtn.disabled = false; // Aktivieren des Check-In Buttons
            checkOutBtn.disabled = true; // Deaktivieren des Check-Out Buttons
        } else {
            checkInBtn.disabled = true; // Deaktivieren des Check-In Buttons
            checkOutBtn.disabled = false; // Aktivieren des Check-Out Buttons
        }
    }


    function isUserClockedIn(){
        $.ajax({
        url: `/getCurrentWorktimeStatistics`,
        type: "GET",
        success: function(data) {

            const isClockedIn = data.statistics.clocked_in;
            if(isClockedIn){
                checkInBtn.disabled = true;
                checkOutBtn.disabled = false;
            }else{
                checkInBtn.disabled = false;
                checkOutBtn.disabled = true;
            }
        },
        error: function(error) {
            alert("Couldn't check out!");
        }
        });
    }

    // Event Listener für den Check-In Button
    checkInBtn.addEventListener('click', function() {
        toggleButtons(); // Buttons tauschen
    });

    // Event Listener für den Check-Out Button
    checkOutBtn.addEventListener('click', function() {
        toggleButtons(); // Buttons tauschen
    });

    // Initialzustand: Check-In Button ist aktiv, Check-Out Button ist deaktiviert
    checkInBtn.disabled = false;
    checkOutBtn.disabled = true;

isUserClockedIn();
