import copy from 'rollup-plugin-copy';

module.exports = [
    {
        input: 'src/resources/js/week.js',
        plugins: [
            copy({
                targets: [
                    { src: 'node_modules/fullcalendar/*.js', dest: 'src/static/js/fullcalendar' },
                    { src: ['node_modules/fullcalendar/*.css'], dest: 'src/static/css/fullcalendar' },
                    { src: ['node_modules/fullcalendar/locales/*.js'], dest: 'src/static/js/fullcalendar/locales' },

                    { src: 'node_modules/jquery-datetimepicker/build/*.js', dest: 'src/static/js/datetimepicker' },
                    { src: ['node_modules/jquery-datetimepicker/build/*.css'], dest: 'src/static/css/datetimepicker' },
                ]
            })
        ],
        output: {
            file: 'src/static/js/week.js',
            format: 'iife'
        }
    },
    {
        input: 'src/resources/js/main.js',
        output: {
            file: 'src/static/js/main.js',
            format: 'iife'
        }
    }
]