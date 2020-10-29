import 'daterangepicker/daterangepicker.css'
import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css'

import 'moment/moment.js'
import 'daterangepicker/daterangepicker.js'
import 'eonasdan-bootstrap-datetimepicker/src/js/bootstrap-datetimepicker.js'

;(function() {

    $(document).ready(function() {

        let moment = require('moment');

        moment.locale('pt-br', {
            week : {
                dow : 2 // Monday is the first day of the week
            }
        });

        // YEAR PICKER
        $('.widget-yearpicker').each(function(idx, el) {
            el = $(el);
            let data = el.data();
            let options = {}
            for(const key in data) {
                options[key] = data[key];
            }
            el.datetimepicker(options);
            el.parent().find('.input-group-prepend').on('click', function(event) {
                el.trigger('focus');
            });
        });

        // DATE PICKER
        $('.widget-datepicker').each(function(idx, el) {
            el = $(el);
            let date_format = el.data('format');
            let view_mode = el.data('view-mode');
            let options = {
                viewMode: view_mode,
                format: date_format
            };
            if(el.data('max-date')) { options.maxDate = el.data('max-date'); }
            if(el.data('min-date')) { options.minDate = el.data('min-date'); }
            el.datetimepicker(options);
            el.parent().find('.input-group-prepend').on('click', function() {
                el.trigger('focus');
            });
        });

        // DATE RANGE
        $('.widget-daterangepicker').each(function() {
            let el = $(this);
            el.daterangepicker({
                singleDatePicker: false,
                alwaysShowCalendars: true,
                timePicker: true,
                timePicker24Hour: true,
                drops: el.data('drops') ? el.data('drops') : 'up',
                autoUpdateInput:  true,
                locale: {
                    "format": 'DD/MM/YY HH:mm',
                    "applyLabel": "Selecionar",
                    "cancelLabel": "Cancelar",
                    "fromLabel": "De",
                    "toLabel": "Para",
                    "customRangeLabel": "Especificar",
                    "daysOfWeek": [
                        "Dom",
                        "Seg",
                        "Ter",
                        "Qua",
                        "Qui",
                        "Sex",
                        "Sáb"
                    ],
                    "monthNames": [
                        "Janeiro",
                        "Fevereiro",
                        "Março",
                        "Abril",
                        "Maio",
                        "Junho",
                        "Julho",
                        "Agosts",
                        "Setembro",
                        "Outubro",
                        "Novembro",
                        "Dezembro"
                    ],
                    "firstDay": 1
                },
                ranges: {
                    //'Qualquer Data': [null, null],
                    'Hoje': [moment().startOf('day'), moment().endOf('day')],
                    'Ontem': [moment().startOf('day').subtract(1, 'days'), moment().endOf('day').subtract(1, 'days')],
                    'Esta semana': [moment().startOf('week'), moment().endOf('week')],
                    'Semana passada': [moment().startOf('week').subtract(1, 'weeks'), moment().endOf('week').subtract(1, 'weeks')],
                    'Este Mês': [moment().startOf('month'), moment().endOf('month')],
                    'Mês Passado': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            });
            el.data('daterangepicker').setStartDate(el.data('start-date'));
            el.data('daterangepicker').setEndDate(el.data('end-date'));
            $(document).on('app-panel:slider-drag-end', function() {
                let top = $(el).offset().top - $(window).scrollTop();
                let bottom = $(window).height();
                let position = top/bottom;
                if(position >= 0.5)  {
                    el.data('daterangepicker').drops='up';
                } else {
                    el.data('daterangepicker').drops='down';
                }
            });
        });

    });

}.call(this));
