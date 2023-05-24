const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December'
];
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

function app() {
    return {
        month: '',
        year: '',
        no_of_days: [],
        blankdays: [],
        days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],

        // events: [{
        //         event_date: new Date(2023, 3, 1),
        //         event_title: "April Fool's Day",
        //         event_theme: 'blue'
        //     },

        //     {
        //         event_date: new Date(2023, 9, 2),
        //         event_title: "Birthday",
        //         event_theme: 'red'
        //     },

        //     {
        //         event_date: new Date(2020, 3, 16),
        //         event_title: "Upcoming Event",
        //         event_theme: 'green'
        //     }
        // ],
        events: [],
        
        event_title: '',
        event_date: '',
        event_theme: 'blue',

        themes: [{
                value: "blue",
                label: "Blue Theme"
            },
            {
                value: "red",
                label: "Red Theme"
            },
            {
                value: "yellow",
                label: "Yellow Theme"
            },
            {
                value: "green",
                label: "Green Theme"
            },
            {
                value: "purple",
                label: "Purple Theme"
            }
        ],

        openEventModal: false,

        readjson(){
            fetch('/js/data.json')
            .then(response => response.json())
            .then(data => {
                console.log(data.event_date);
                data.event_date = new Date(data.event_date);
                console.log(data);
                this.events.push({
                    event_date: data.event_date,
                    event_title: data.event_title,
                    event_theme: data.event_theme
                })
            });
        },

        initDate() {
            let today = new Date();
            this.month = today.getMonth();
            this.year = today.getFullYear();
            this.datepickerValue = new Date(this.year, this.month, today.getDate()).toDateString();
        },

        isToday(date) {
            const today = new Date();
            const d = new Date(this.year, this.month, date);

            return today.toDateString() === d.toDateString() ? true : false;
        },

        showEventModal(date) {
            // open the modal
            this.openEventModal = true;
            this.event_date = new Date(this.year, this.month, date).toDateString();
        },

        addEvent() {
            if (this.event_title == '') {
                return;
            }

            this.events.push({
                event_date: this.event_date,
                event_title: this.event_title,
                event_theme: this.event_theme
            });

            console.log(this.events);

            // clear the form data
            this.event_title = '';
            this.event_date = '';
            this.event_theme = 'blue';

            //close the modal
            this.openEventModal = false;
        },

        getNoOfDays() {
            let daysInMonth = new Date(this.year, this.month + 1, 0).getDate();

            // find where to start calendar day of week
            let dayOfWeek = new Date(this.year, this.month).getDay();
            let blankdaysArray = [];
            for (var i = 1; i <= dayOfWeek; i++) {
                blankdaysArray.push(i);
            }

            let daysArray = [];
            for (var i = 1; i <= daysInMonth; i++) {
                daysArray.push(i);
            }
            let last = new Date(this.year, this.month, 0).getDate();

            let lmon = [];
            // console.log(last, blankdaysArray.length);
            for(var i=(last+1)-blankdaysArray.length; i<=last; i++){
                lmon.push(i);
            }       
            let lenl = lmon.concat(daysArray).length;
            let temp = [];
            for(let i=1; i<=42-lenl; i++){
                temp.push(i);
            }
            this.no_of_days = daysArray;
            this.blankdays = lmon;
            this.blankdays2 = temp;
        }
    }
}

function menuc(){
    console.log("menuc");
    document.querySelectorAll('[role="menu"]').forEach((e)=>{

        if(e.classList.contains('hidden')){
            e.classList.remove('hidden');
        }
        else{
            e.classList.add('hidden');
        }
    });
}