import {getCookie, showLoader, hideLoader} from './main';

document.addEventListener('DOMContentLoaded', function () {
    //custom styling for week view
    document.getElementById('week_day_text').classList.add('calendar');

    // used for time where the calendar is initially scrolled at
    var date = new Date();
    date.setHours(date.getHours() - 1);

    // calendar definition
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: perms.calendar_extended ? 'predakTimeGrid' : 'timeGridWeek',
        views: {
            predakTimeGrid: {
                type: 'timeGridWeek',
                duration: { days: 8},
                dateAlignment: "week"
            }
        },
        headerToolbar: { // custom header
            start: null,
            center: null,
            end: null
        },
        validRange: function (nowDate) {
            if (perms.calendar_history) return {};
            var d = new Date(nowDate.getTime());
            d.setHours(0);
            d.setMinutes(0);

            return {
                start: d
            };
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
        events: transports_list_url, // url to fetch transports from,
        loading: function (isLoading) {
            if (isLoading) {
                calendarEl.classList.add('calendar-loading');
                showLoader();
            } else {
                hideLoader();
                calendarEl.classList.remove('calendar-loading');
            }
        },
        eventSourceSuccess: function (content, xhr) {
            hideLoader();
            calendarEl.classList.remove('calendar-loading');

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
            return {html: htmlWrapper}
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

            showLoader();
            calendarEl.classList.add('loading-calendar');

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
                    hideLoader();
                    calendarEl.style.opacity = 'initial';
                    setTimeout(function () {
                        calendarEl.classList.remove('loading-calendar');
                        calendarEl.style.opacity = null;
                    }, 100);
                })
        },
        eventClick: function (eventClickInfo) { // when user clicks on event, show modal with transport detail
            document.querySelector('#transport-detail').innerHTML = '';
            var transportId = eventClickInfo.event.extendedProps.transport_id;

            modal.show();
            htmx.ajax('GET', base_host + '/form/' + transportId, {
                target: '#transport-detail',
                source: '.loading-svg-wrapper'
            });
        },
        scrollTime: date.toTimeString(), // scroll to current time
        editable: perms.calendar_editable,
        eventDurationEditable: perms.calendar_editable,
        eventResizableFromStart: perms.calendar_editable,
        datesSet: (dateInfo) => { // when date is set on the calendar, change text in the menu
            document.getElementById('week_day_text').innerHTML = dateInfo.start.toLocaleDateString("sk-SK") + ' - ' + dateInfo.end.toLocaleDateString("sk-SK");
        }
    });

    // event sent from transport detail template (transports/elements/form.html) when transport is saved
    document.addEventListener('transportSaved', function () {
        calendar.refetchEvents();
    });

    // go to previous week
    try {
        document.getElementById('calendar_prev').addEventListener('click', () => {
            var originalActiveStart = calendar.view.activeStart.getTime();
            var originalActiveEnd = calendar.view.activeEnd.getTime();

            calendar.prev();

            var currentActiveStart = calendar.view.currentStart.getTime();
            var currentActiveEnd = calendar.view.currentEnd.getTime();

            if (currentActiveStart === originalActiveStart && currentActiveEnd === originalActiveEnd) {
                $.notify("Časový rozsah nemôžete posunúť do minulosti.", "error");
            }
        });

        // go to next week
        document.getElementById('calendar_next').addEventListener('click', () => {
            calendar.next();
        });

        // go to this day
        document.getElementById('calendar_today').addEventListener('click', () => {
            calendar.today();
        });
    } catch (error) {
    }

    calendar.render();
});

// get event description from transport data
function getEventDescription(transport) {
    var carry = '<strong>' + transport.registration_number + '</strong><br>';
    carry += '<span class="event-ribbon" style="background-color: ' + transport.transport_priority.color + '; color: ' + transport.transport_priority.font_color + ';">' + transport.transport_priority.name + '</span><br>';
    carry += '<span class="event-ribbon" style="background-color: ' + transport.transport_status.color + '; color: ' + transport.transport_status.font_color + ';">' + transport.transport_status.name + '</span><br>';
    carry += 'Dodávateľ: <strong>' + transport.supplier + '</strong><br>';
    carry += 'Dopravca: <strong>' + transport.carrier + '</strong><br>';

    return carry;
}