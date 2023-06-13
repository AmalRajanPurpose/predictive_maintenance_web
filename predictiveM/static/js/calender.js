//$(document).ready(function() {
//    var date = new Date();
//    var d = date.getDate();
//    var m = date.getMonth();
//    var y = date.getFullYear();
//
//    var eventsFromSource = []; // create an empty variable to hold the events from eventSources
//
//    /* initialize the external events
//    -----------------------------------------------------------------*/
//
//    // ...
//
//    /* initialize the calendar
//    -----------------------------------------------------------------*/
//
//    var calendar =  $('#calendar').fullCalendar({
//        header: {
//            left: 'title',
//            center: 'agendaDay,agendaWeek,month',
//            right: 'prev,next today'
//        },
//
//        height:400,
//        width:300,
//        editable: true,
//        firstDay: 1,
//        selectable: true,
//        defaultView: 'month',
//        axisFormat: 'h:mm',
//        columnFormat: {
//            month: 'ddd',
//            week: 'ddd d',
//            day: 'dddd M/d',
//            agendaDay: 'dddd d'
//        },
//        titleFormat: {
//            month: 'MMMM yyyy',
//            week: "MMMM yyyy",
//            day: 'MMMM yyyy'
//        },
//        allDaySlot: false,
//        selectHelper: true,
//        // select: function(start, end, jsEvent, view) {
//        //     var eventData;
//        //     var selectedEvent = eventsFromSource.find(function(event) {
//        //         return moment(event.start).format("YYYY-MM-DD") === moment(start).format("YYYY-MM-DD");
//        //     });
//        //     if (selectedEvent) {
//        //         eventData = {
//        //             title: selectedEvent.title,
//        //             start: start,
//        //             end: end,
//        //             allDay: false
//        //         };
//        //         $('#calendar').fullCalendar('renderEvent', eventData, true);
//        //         $('#calendar').fullCalendar('unselect');
//
//        //         // showreading(selectedEvent.title);
//        //         console.log(eventData)
//        //     } else {
//        //         console.log('pppppppppppppp')
//        //         // var title = prompt('Event Title:');
//        //         // if (title) {
//        //         //     eventData = {
//        //         //         title: title,
//        //         //         start: start,
//        //         //         end: end,
//        //         //         allDay: false
//        //         //     };
//        //         //     $('#calendar').fullCalendar('renderEvent', eventData, true);
//        //         //     $('#calendar').fullCalendar('unselect');
//        //         // }
//        //     }
//        // },
//        eventSources: [
//            {
//                url: '{% url "production_graph" %}',
//                type: 'POST',
//                data: {
//                    csrfmiddlewaretoken: '{{ csrf_token }}'
//                },
//                success: function(response) {
//                    $.each(response, function(index, event) {
//                        eventsFromSource.push({
//                            title: event.title,
//                            start: event.start,
//                            end: event.end,
//                            allDay: event.allDay,
//                            className: event.className
//                        });
//                    });
//                }
//            }
//        ]
//
//    });
//});
