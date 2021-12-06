import copy from 'rollup-plugin-copy'
import { babel } from '@rollup/plugin-babel';

module.exports = [
    {
        input: 'src/resources/js/week.js',
        plugins: [
            copy({
                targets: [
                    { src: 'node_modules/fullcalendar/*.js', dest: 'src/static/js/fullcalendar' },
                    { src: ['node_modules/fullcalendar/*.css'], dest: 'src/static/css/fullcalendar' },
                    { src: ['node_modules/fullcalendar/locales/*.js'], dest: 'src/static/js/fullcalendar/locales' },
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
        plugins: [
            babel({ babelHelpers: 'bundled' }),
        ],
        output: {
            file: 'src/static/js/main.js',
            format: 'iife'
        }
    }
]