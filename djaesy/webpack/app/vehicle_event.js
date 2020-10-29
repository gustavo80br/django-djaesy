import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import toastr from 'toastr'
import {Portal} from '@linusborg/vue-simple-portal'
import 'jquery'


;(function() {

    Vue.directive('init', {
      bind: function(el, binding, vnode) {
        vnode.context[binding.arg] = binding.value;
      }
    });

    Vue.use(VueAxios, axios);

    let truncate = Vue.filter('Truncate', function (text, stop, clamp) {
        return text.slice(0, stop) + (stop < text.length ? clamp || '...' : '')
    });

    Vue.config.productionTip = false;

    let severity_level = {
        'C': 5,
        'H': 4,
        'M': 3,
        'L': 2,
        'I': 1
    };

    let level_class = {
        5: 'badge-danger',
        4: 'orange',
        3: 'badge-warning',
        2: 'badge-success',
        1: 'badge-info'
    };

    let app_element = $('#vehicle_event').length;

    if(app_element) {
        new Vue({
            el: '#vehicle_event',
            delimiters: ["{[", "]}"],
            components: {
                'portal': Portal,
            },
            filters: {
                'truncate': function(value, size) {
                    value = String(value);
                    return value.slice(0, size) + (size < value.length ? '...' : '')
                }
            },
            data: {
                severity_description: {
                    'C': '🔺 Crítico',
                    'H': '🟠 Alto',
                    'M': '🟡 Médio',
                    'L': '🟢 Baixo',
                    'I': '🔘 Informativo'
                },
                level_class: {
                    5: 'badge-danger',
                    4: 'orange',
                    3: 'badge-warning',
                    2: 'badge-success',
                    1: 'badge-info'
                },
                csrf_token: '',
                vehicle_id: '',
                events: [],
                severity_class: '',
                silence_form_id: '',
                silence_form_event: {},
                silence_form_sending: false,
                silence_form_multiple: false,
                silence_form_comment: '',
                silence_modal: null,
                backdrop: false,
                filter: '',
                all_selected: false
            },
            computed: {
                eventsToShow: function () {
                    if (this.filter !== '') {
                        let self = this;
                        return this.events.filter(function (n) {
                            return n.alert__severity === self.filter;
                        })
                    } else {
                        return this.events;
                    }
                },
                severitiesAvailable: function () {
                    let severeties = {};
                    this.events.forEach(function (n) {
                        //let desc = severity_description[n.severity];
                        let desc = n.alert__severity;
                        if (!severeties[desc]) severeties[desc] = 1; else severeties[desc] += 1;
                    });
                    return severeties;
                },
                totalEvents: function () {
                    return this.events.length;
                },
                totalSelected: function () {
                    let count = 0;
                    this.eventsToShow.forEach(function (n) {
                        if (n.selected) {
                            count += 1;
                        }
                    });
                    return count;
                },
                totalSelectedToSilence: function () {
                    return this.eventsSelectedToSilence.length;
                },
                eventsSelected: function () {
                    if (this.silence_form_multiple) {
                        return this.eventsToShow.filter(function (n) {
                            return n.selected;
                        });
                    } else {
                        return [this.silence_form_event];
                    }
                },
                eventsSelectedToSilence: function () {
                    return this.eventsToShow.filter(function (n) {
                        return n.selected & n.report > 0 & !n.report__acknowledged;
                    });
                },
                eventsSelectedIds: function () {
                    if (this.silence_form_multiple) {
                        return this.eventsSelected.map(function (n) {
                            return n.id;
                        });
                    }
                },
                eventsSelectedToSilenceIds: function () {
                    return this.eventsSelectedToSilence.map(function (n) {
                        return n.id;
                    });
                },
                showClearFilter: function () {
                    return Boolean(this.filter !== '' && Object.keys(this.severitiesAvailable).length > 1);
                }
            },
            methods: {
                closeAll: function () {
                    $(this.silence_modal).modal('hide');
                    this.backdrop = false;
                },
                severityClass: function () {
                    let severity = this.events.map(function (n) {
                        return severity_level[n.alert__severity]
                    });
                    let max_level = Math.max.apply(Math, severity);
                    return this.level_class[max_level];
                },
                getEventById: function (nid) {
                    let found = false;
                    let event_obj = null;
                    this.events.forEach(function (event) {
                        if (!found && event.id === nid) {
                            found = true;
                            event_obj = event;
                        }
                    });
                    return event_obj;
                },
                acknowledgeEvent: function (nid, response) {
                    let event = this.getEventById(nid);
                    if(response.data.acknowledged) {
                        event.report__acknowledged = response.data.acknowledged;
                        event.report__acknowledged_by__email = response.data.acknowledged_by__email;
                        event.report__acknowledged_by = response.data.acknowledged_by;
                        event.report__acknowledge_date = response.data.acknowledge_date;
                        event.report__acknowledge_comment = response.data.acknowledge_comment;
                    }
                },
                selectEvent: function (nid) {
                    let event = this.getEventById(nid);
                    const index = this.events.indexOf(event);
                    if (index > -1) {
                        this.$set(this.events[index], 'selected', !this.events[index].selected);
                    }
                },
                toggleSelectAll: function () {
                    if (this.all_selected) {
                        this.unselectAll();
                    } else {
                        this.selectAll();
                    }
                },
                selectAll: function () {
                    let self = this;
                    this.events.forEach(function (event, idx) {
                        self.$set(self.events[idx], 'selected', true);
                    });
                    this.all_selected = true;
                },
                unselectAll: function () {
                    let self = this;
                    this.events.forEach(function (event, idx) {
                        self.$set(self.events[idx], 'selected', false);
                    });
                    this.all_selected = false;
                },
                showOnMap: function(nid) {
                    let n = this.getEventById(nid);
                    if(n) {
                        if (n.segment_id) {
                            $(document).trigger('i3track:select_track', [n.segment_id, n.location]);
                        }
                    }
                },
                setFilter: function (filter = '') {
                    this.filter = filter;
                },
                silenceAlert: function (nid) {
                    this.silence_form_id = nid;
                    this.backdrop = true;
                    this.silence_form_multiple = false;
                    this.silence_form_event = this.getEventById(nid);
                    $(this.silence_modal).modal('show');
                    event.preventDefault();
                },
                silenceSelectedAlert: function () {
                    let selected_ids = this.eventsSelectedToSilenceIds;
                    if (selected_ids.length === 1) {
                        this.silenceAlert(selected_ids[0]);
                    } else {
                        this.silence_form_id = selected_ids.join(',');
                        this.silence_form_multiple = true;
                        $(this.silence_modal).modal('show');
                    }
                    event.preventDefault();
                },
                cancelSilence: function () {
                    $(this.silence_modal).modal('hide');
                },
                silenceRequest: function (event) {

                    if (this.silence_form_sending) return;

                    let self = this;

                    this.silence_form_sending = true;
                    event.preventDefault();

                    let data = {};
                    const url = '/api/v1/events/silence/';
                    const config = {headers: {"X-CSRFToken": this.csrf_token}};

                    if (this.silence_form_multiple) {
                        data = {
                            event_id: this.eventsSelectedToSilenceIds.join(','),
                            silence_comment: this.silence_form_comment,
                        }
                    } else {
                        data = {
                            event_id: this.silence_form_id,
                            silence_comment: this.silence_form_comment,
                        }
                    }

                    data.event_id_type = 'event';

                    this.axios.post(url, data, config)
                        .then(function (response) {
                            if (self.silence_form_multiple) {
                                self.eventsSelectedToSilenceIds.forEach(function (n) {
                                    self.acknowledgeEvent(n, response);
                                });
                            } else {
                                self.acknowledgeEvent(self.silence_form_id, response);
                            }
                            // -- Switch modal
                            $(self.silence_modal).modal('hide');
                            // -- Notify and finish
                            toastr['success']('Operação de silenciar alertas concluída com sucesso!', 'Sucesso');
                            self.silence_form_sending = false;
                        })
                        .catch(function (error) {
                            // -- Notify and finish
                            toastr['error']('Houve um erro ao silenciar a alertas! Contate o suporte.', 'Erro');
                            self.silence_form_sending = false;
                        });
                },
                loadEvents: function(geojson) {

                    let self = this;

                    geojson.features.forEach(function(feature) {
                        let alert = feature.properties;
                        feature.properties.severity_desc = self.severity_description[feature.properties.alert__severity]
                        alert.location = (feature.geometry.coordinates.reverse());
                        self.events.push(feature.properties);
                    });

                    this.severity_class = self.severityClass();

                    $(document).on('i3track:show_event', function() {
                        let urlParams = new URLSearchParams(window.location.search);
                        let event = parseInt(urlParams.get('event'));
                        self.showOnMap(event);
                    });

                    // let self = this;
                    // $.ajax({
                    //     url: `/api/v1/events/${self.vehicle_id}`,
                    //     method: 'GET',
                    //     success: function (data) {
                    //         self.ions = data.events;
                    //         self.severity_class = self.severityClass();
                    //     },
                    //     error: function (error) {
                    //         console.log(error);
                    //     }
                    // });
                }
            },
            mounted: function () {

                this.owner_id = $('#ownerId').data('owner');
                this.vehicle_id = $('#vehicleId').data('vehicle');
                this.csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
                this.silence_modal = '#vehicleSilenceModal';

                let self = this;

                $(document).on('i3track:load_events', function(e, events_geojson){
                    self.loadEvents(events_geojson);
                });

                // const eventReportSocket = new WebSocket('ws://' + window.location.host + '/ws/v1/events/report/' + this.owner_id + '/');
                //
                // eventReportSocket.onmessage = function (e) {
                //     const data = JSON.parse(e.data);
                //     if (data.tracked_object === self.vehicle_id) {
                //         self.loadEvents();
                //     }
                //     // self.events.unshift(data);
                //     // self.severity_class = self.severityClass();
                //     // self.event_icon.addClass('ring');
                //     // setTimeout(function() {
                //     //     self.event_icon.removeClass('ring');
                //     // }, 1000);
                // };
                //
                // eventReportSocket.onclose = function (e) {
                //     console.error('Chat socket closed unexpectedly');
                // };

            }
        });
    }

}.call(this));