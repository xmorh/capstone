document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',
        headerToolbar: {
        left: 'prev,next today',
        center: 'title',
      },
      initialDate: '2024-11-01',
      navLinks: true, 
      businessHours: true, 
      editable: true,
      selectable: true,
      events: [

        // areas where "Meeting" must be dropped
        {
          groupId: 'availableForMeeting',
          start: '2024-11-11T10:00:00',
          end: '2024-11-11T16:00:00',
          display: 'background'
        },
        {
          groupId: 'availableForMeeting',
          start: '2024-11-13T10:00:00',
          end: '2024-11-13T16:00:00',
          display: 'background'
        },

        // red areas where no events can be dropped
        {
          start: '2024-11-04',
          end: '2024-11-04',
          overlap: false,
          display: 'background',
          color: '#ff9f89'
        },
        {
          start: '2024-11-06',
          end: '2024-11-08',
          overlap: false,
          display: 'background',
          color: '#ff9f89'
        }
      ],

    dateClick: function(info) {
        window.location.href = '';
    }

    });

    calendar.render();
  });