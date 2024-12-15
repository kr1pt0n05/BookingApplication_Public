document.addEventListener('DOMContentLoaded', function() {

const vacationModal = document.getElementById('vacationModal');
    const vacationRequestList = document.getElementById('vacationRequestList');
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const submitVacationRequestButton = document.getElementById('submitVacationRequest');
    const vacationDaysLeftDisplay = document.getElementById('vacationDaysLeft');
    const errorMsg = document.getElementById('errorMsg');
    let vacationDaysLeft = 30;

    // Öffnet das Modal für Urlaubsantrag
    vacationRequestBtn.addEventListener('click', function() {
        vacationModal.style.display = 'block';
    });

    // Schließt das Modal
    document.querySelector('.close').addEventListener('click', function() {
        vacationModal.style.display = 'none';
    });

    function calculateVacationDays(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const millisecondsPerDay = 1000 * 60 * 60 * 24;
        return Math.ceil((end - start) / millisecondsPerDay) + 1;
    }

    function isValidVacationDate(date) {
        const day = date.getDay();
        return day !== 0 && day !== 6; // Kein Wochenende
    }

    submitVacationRequestButton.addEventListener('click', function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        if (!startDate || !endDate) {
            errorMsg.textContent = "Bitte Start- und Enddatum eingeben.";
            return;
        }

        const vacationDays = calculateVacationDays(startDate, endDate);

        if (vacationDays > vacationDaysLeft) {
            errorMsg.textContent = "Sie haben nicht genug verbleibende Urlaubstage.";
            return;
        }

        const start = new Date(startDate);
        const end = new Date(endDate);

        if (!isValidVacationDate(start) || !isValidVacationDate(end)) {
            errorMsg.textContent = "Urlaub kann nur an Wochentagen beantragt werden.";
            return;
        }

        errorMsg.textContent = ""; // Fehlernachricht zurücksetzen

        vacationDaysLeft -= vacationDays;
        vacationDaysLeftDisplay.textContent = `Verbleibende Tage: ${vacationDaysLeft}`;

        // Füge den Urlaubsantrag zur Liste hinzu
        const listItem = document.createElement('li');
        listItem.classList.add('vacation-request-item');
        listItem.innerHTML = `
            <span>${startDate} to ${endDate}</span>
            <span class="status">status: open</span>
        `;
        vacationRequestList.appendChild(listItem);

        // Schließen des Modals nach dem Senden
        vacationModal.style.display = 'none';

        startDateInput.value = '';
        endDateInput.value = '';
    });
});
