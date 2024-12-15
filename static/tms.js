const currentDate = new Date();

function getTimestamps(year, month) {
    return new Promise((resolve, reject) => {
        const data = { year, month };

        $.ajax({
            url: `/getMonthlyTimestamps`,
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: (data) => {
                const timestamps = data.timestamps;
                const events = [];

                timestamps.forEach((timestamp) => {
                    const startDate = timestamp.startDate;
                    const endDate = timestamp.endDate;
                    const startTime = timestamp.startTime;
                    const endTime = timestamp.endTime;

                    events.push(timestampToEvent(startDate, startTime, "Clocked In"));

                    if (endDate) {
                        events.push(timestampToEvent(endDate, endTime, "Clocked out"));
                    }
                });

                // Resolve the Promise with the events array
                resolve(events);
            },
            error: (error) => {
                // Reject the Promise if there’s an error
                reject(error);
            }
        });
    });
}


function timestampToEvent(date, time, title){
    const month = String(date.month).padStart(2, '0'); // Ensure month is 2 digits
    const day = String(date.day).padStart(2, '0'); // Ensure day is 2 digits
    const hour = String(time.hour).padStart(2, '0');
    const minute = String(time.minute).padStart(2, '0');
    return {title: title, start: `${date.year}-${month}-${day}T${hour}:${minute}`}
}

document.addEventListener('DOMContentLoaded', async function() {

    const greetingElement = document.getElementById('greeting');
    const now = new Date();


document.getElementById('check-in-btn').addEventListener("click", ()=>{
    addEventsToCalendar();
});

document.getElementById('check-out-btn').addEventListener("click", ()=>{
    addEventsToCalendar();
});


    // Kalender-Initialisierung
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',  // Display events in a list format for the month
        selectable: true,           // Allow users to select time slots
        editable: true,             // Allow users to edit events
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: ""
        },
        events: [
        ],

        datesSet: async function(info) {
            const year = info.view.currentStart.getFullYear();
            const month = info.view.currentStart.getMonth() + 1;

            try{
                 // Get all events from the calendar
                const currentEvents = calendar.getEvents();

                // Loop through each event and remove it
                currentEvents.forEach(event => event.remove());

                const events = await getTimestamps(year, month);

                // Add each event to the calendar
                events.forEach(eventData => {
                    calendar.addEvent(eventData); // Add each event to the calendar
                });

                // Render the calendar after adding the events
                calendar.render();

            }catch(error){
                 console.error("Error fetching timestamps:", error);
            }

        }
    });

    async function addEventsToCalendar(){
            try {
         // Get all events from the calendar
        const currentEvents = calendar.getEvents();

        // Loop through each event and remove it
        currentEvents.forEach(event => event.remove());

        // Wait for getTimestamps to complete before rendering the calendar
        const events = await getTimestamps(currentDate.getFullYear(), currentDate.getMonth() + 1);

        // Add each event to the calendar
        events.pop();
        events.forEach(eventData => {
            calendar.addEvent(eventData); // Add each event to the calendar
        });

        // Render the calendar after adding the events
        calendar.render();

    } catch (error) {
        console.error("Error fetching timestamps:", error);
    }
    }

    addEventsToCalendar();

});


