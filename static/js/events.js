
var inst = mobiscroll.eventcalendar('#demo-event-popover', {
    theme: 'windows',
    themeVariant: 'light',
    clickToCreate: false,
    dragToCreate: false,
    dragToMove: false,
    dragToResize: false,
    eventDelete: false,
    view: {
      calendar: {
        popover: true,
        count: true,
      },
    },
    onEventClick: function (args) {
      mobiscroll.toast({
        message: args.event.title,
      });
    },
  });
  
  mobiscroll.getJson(
    'https://trial.mobiscroll.com/events/?vers=5',
    function (events) {
      inst.setEvents(events);
    },
    'jsonp',
  );
    