import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import toastr from 'toastr'


;(function() {

    Vue.directive('init', {
      bind: function(el, binding, vnode) {
        vnode.context[binding.arg] = binding.value;
      }
    });

    Vue.use(VueAxios, axios);
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

    var event_notification = new Vue({
        el: '#event_notification',
        delimiters: ["{[","]}"],
        data: {
            message: 'Hello Vue!',
            severity_description: {
                'C': '🔺 Crítico',
                'H': '🟠 Alto',
                'M': '🟡 Médio',
                'L': '🟢 Baixo',
                'I': '🔘 Informativo'
            },
            csrf_token: '',
            owner_id: '',
            notifications: [],
            severity_class: '',
            silence_form_id: '',
            silence_form_notification: {},
            silence_form_sending: false,
            silence_form_multiple: false,
            silence_form_comment: '',
            alerts_modal: null,
            silence_modal: null,
            backdrop: false,
            filter: '',
            all_selected: false
        },
        computed: {
            notificationsToShow: function() {
                if(this.filter !== '') {
                    let self = this;
                    return this.notifications.filter(function (n) {
                        return n.severity === self.filter;
                    })
                } else {
                    return this.notifications;
                }
            },
            severitiesAvailable: function() {
                let severeties = {};
                this.notifications.forEach(function(n) {
                    //let desc = severity_description[n.severity];
                    let desc = n.severity;
                    if(!severeties[desc]) severeties[desc] = 1; else severeties[desc] += 1;
                });
                return severeties;
            },
            totalNotifications: function() {
                return this.notifications.length;
            },
            totalSelected: function() {
                let count = 0;
                this.notificationsToShow.forEach(function(n) {
                    if(n.selected) {
                        count += 1;
                    }
                });
                return count;
            },
            notificationsSelected: function() {
                if(this.silence_form_multiple) {
                    return this.notificationsToShow.filter(function (n) {
                        return n.selected;
                    });
                } else {
                    return [this.silence_form_notification];
                }
            },
            notificationsSelectedIds: function() {
                if(this.silence_form_multiple) {
                    return this.notificationsSelected.map(function (n) {
                        return n.id;
                    });
                }
            },
            showClearFilter: function() {
                return Boolean(this.filter !== '' && Object.keys(this.severitiesAvailable).length > 1);
            }
        },
        methods: {
            closeAll: function() {
                this.alerts_modal.modal('hide');
                this.silence_modal.modal('hide');
                this.backdrop = false;
            },
            severityClass: function() {
                let severity = this.notifications.map(function(n) { return severity_level[n.severity] });
                let max_level = Math.max.apply(Math, severity);
                return level_class[max_level];
            },
            getNotificationById: function(nid) {
                let found = false;
                let notification_obj = null;
                this.notifications.forEach(function(notification) {
                    if(!found && notification.id === nid) {
                        found = true;
                        notification_obj = notification;
                    }
                });
                return notification_obj;
            },
            removeNotification: function(nid) {
                let notification = this.getNotificationById(nid);
                const index = this.notifications.indexOf(notification);
                if (index > -1) {
                    this.notifications.splice(index, 1);
                }
            },
            selectNotification: function(nid) {
                let notification = this.getNotificationById(nid);
                const index = this.notifications.indexOf(notification);
                if (index > -1) {
                    this.$set(this.notifications[index], 'selected', !this.notifications[index].selected);
                }
            },
            toggleSelectAll: function() {
                if(this.all_selected) {
                    this.unselectAll();
                } else {
                    this.selectAll();
                }
            },
            selectAll: function() {
                let self = this;
                this.notifications.forEach(function(notification, idx) {
                    self.$set(self.notifications[idx], 'selected', true);
                });
                this.all_selected = true;
            },
            unselectAll: function() {
                let self = this;
                this.notifications.forEach(function(notification, idx) {
                    self.$set(self.notifications[idx], 'selected', false);
                });
                this.all_selected = false;
            },
            setFilter: function(filter='') {
                this.filter = filter;
            },
            silenceAlert: function(nid) {
                let self = this;
                this.silence_form_id = nid;
                this.backdrop = true;
                this.silence_form_multiple = false;
                this.silence_form_notification = this.getNotificationById(nid);
                this.alerts_modal.on('hidden.bs.modal', function() {
                    self.silence_modal.modal('show');
                    self.alerts_modal.off('hidden.bs.modal');
                });
                this.alerts_modal.modal('hide');
                event.preventDefault();
            },
            silenceSelectedAlert: function() {
                let selected_ids = []
                this.notificationsToShow.forEach(function(n) {
                    if(n.selected) {
                        selected_ids.push(n.id);
                    }
                });
                if(selected_ids.length === 1) {
                    this.silenceAlert(selected_ids[0]);
                } else {
                    this.silence_form_id = selected_ids.join(',');
                    this.silence_form_multiple = true;
                    let self = this;
                    this.alerts_modal.on('hidden.bs.modal', function() {
                        self.silence_modal.modal('show');
                        self.alerts_modal.off('hidden.bs.modal');
                    });
                    this.alerts_modal.modal('hide');
                }
                event.preventDefault();
            },
            cancelSilence: function() {
                let self = this;
                this.silence_modal.on('hidden.bs.modal', function() {
                    self.alerts_modal.modal('show');
                    self.silence_modal.off('hidden.bs.modal');
                });
                this.silence_modal.modal('hide');
            },
            silenceRequest: function(event) {

                if(this.silence_form_sending) return;

                let self = this;

                this.silence_form_sending = true;
                event.preventDefault();

                let data = {};
                const url = '/api/v1/events/silence/';
                const config = {headers: {"X-CSRFToken": this.csrf_token}};

                if(this.silence_form_multiple) {
                    data = {
                        event_id: this.notificationsSelectedIds.join(','),
                        silence_comment: this.silence_form_comment,
                    }
                } else {
                    data = {
                        event_id: this.silence_form_id,
                        silence_comment: this.silence_form_comment,
                    }
                }

                data.event_id_type = 'event_report';

                this.axios.post(url, data, config)
                .then(function (response) {
                    if(self.silence_form_multiple) {
                        self.notificationsSelected.forEach(function(n) {
                            self.removeNotification(n.id);
                        });
                    } else {
                        self.removeNotification(self.silence_form_id);
                    }
                    // -- Switch modal
                    if(self.totalNotifications > 0) {
                        self.silence_modal.on('hidden.bs.modal', function () {
                            self.alerts_modal.modal('show');
                            self.silence_modal.off('hidden.bs.modal');
                        });
                    }
                    self.silence_modal.modal('hide');
                    // -- Notify and finish
                    toastr['success']('Operação de silenciar alertas concluída com sucesso!', 'Sucesso');
                    self.silence_form_sending = false;
                })
                .catch(function (error) {
                    // -- Notify and finish
                    toastr['error']('Houve um erro ao silenciar a alertas! Contate o suporte.', 'Erro');
                    self.silence_form_sending = false;
                });
            }
        },
        mounted: function () {

            let self = this;
            this.owner_id = $('#ownerId').data('owner');
            this.csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            this.silence_modal = $('#alertsSilenceModal');
            this.alerts_modal = $('#alertsModal');
            this.event_icon = $('#eventsIcon');

            $.ajax({
                url: '/api/v1/events/',
                method: 'GET',
                success: function (data) {
                    self.notifications = data.notifications;
                    self.severity_class = self.severityClass();
                },
                error: function (error) {
                    console.log(error);
                }
            });

            const eventReportSocket = new WebSocket('ws://' + window.location.host + '/ws/v1/events/report/' + this.owner_id + '/');

            eventReportSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                self.notifications.unshift(data);
                self.severity_class = self.severityClass();
                self.event_icon.addClass('ring');
                setTimeout(function() {
                    self.event_icon.removeClass('ring');
                }, 1000);

            };

            eventReportSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };

        }
    });

}.call(this));