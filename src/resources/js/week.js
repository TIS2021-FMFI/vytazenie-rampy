import getCookie from './main';

document.addEventListener('DOMContentLoaded', function () {
    var modalEl = document.querySelector('#modal');
    var modal = new bootstrap.Modal(modalEl);
    modal.hide();

    // used for time where the calendar is initially scrolled at
    var date = new Date();
    date.setHours(date.getHours() - 1);

    // calendar definition
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: { // custom header
            start: null,
            center: null,
            end: null
        },
        locale: 'sk',
        firstDay: 1, // first day is monday
        allDaySlot: false, // don't support full-day events
        slotLabelFormat: {
            hour: 'numeric',
            minute: '2-digit',
            omitZeroMinute: false,
            meridiem: 'long'
        },
        themeSystem: 'bootstrap',
        events: transports_list_url, // url to fetch transports from
        eventSourceSuccess: function (content, xhr) {
            // gets called on successful fetch from api
            var eventArray = [];

            for (var i in content) {
                var transport = content[i];

                // event definition
                eventArray.push({
                    start: transport.process_start,
                    end: transport.process_finish,
                    color: transport.color,
                    customHtml: getEventDescription(transport),
                    transport_id: transport.id
                })
            }

            return eventArray;
        },
        displayEventTime: true,
        eventContent: function (eventInfo) {
            // normally the event title gets escaped,
            // so this way we can display html in the event's body
            var htmlWrapper = '<div class="p-1">' + eventInfo.timeText + '<br>' + eventInfo.event.extendedProps.customHtml + '</div>';
            return { html: htmlWrapper }
        },
        eventChange: function (changeInfo) {
            // gets called when any event is changed (moved, shortened, ...)

            // event object (transport)
            var event = changeInfo.event;

            // data to update
            var eventData = {
                process_start: event.start.toISOString(),
                process_finish: event.end.toISOString(),
            }

            // update transport on api
            fetch(base_host + '/api/transports/' + event.extendedProps.transport_id + '/', {
                method: 'POST',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    // csrf token is defined in the main.js file
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(eventData)
            }).then((res) => res.json())
                .then((data) => {
                    $.notify(data.msg, data.status ? 'success' : 'error');
                })
        },
        eventClick: function (eventClickInfo) {
            var transportId = eventClickInfo.event.extendedProps.transport_id;

            htmx.ajax('GET', base_host + '/form/' + transportId, '#transport-detail');
            document.addEventListener('htmx:afterSettle', () => {
                modal.show()
            }, { once: true });
        },
        scrollTime: date.toTimeString(),
        editable: true,
        eventDurationEditable: true,
        eventResizableFromStart: true
    });

    document.addEventListener('transportSaved', function () {
        modal.hide();

        setTimeout(() => {
            calendar.refetchEvents();
        }, 300);
    });

    calendar.render();
});

// get event description from transport data
function getEventDescription(transport) {
    var carry = '<strong>' + transport.registration_number + '</strong><br>';
    carry += '<span class="event-ribbon" style="background-color: ' + transport.transport_priority.color + '; color: ' + transport.transport_priority.font_color + ';">' + transport.transport_priority.name + '</span><br>';
    carry += '<span class="event-ribbon" style="background-color: ' + transport.transport_status.color + '; color: ' + transport.transport_status.font_color + ';">' + transport.transport_status.name + '</span><br>';
    carry += 'Dodávateľ: ' + transport.supplier + '<br>';
    carry += 'Dopravca: ' + transport.carrier + '<br>';

    return carry;
}