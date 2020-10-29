import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import toastr from 'toastr'


;(function() {

    Vue.directive('iframe', {
        inserted: function(el) {
            // el.src = el.dataset.src;
            // el.contentWindow.location.replace(el.dataset.src);
            // el.contentWindow.location.reload();
            // console.log(el.contentWindow.location.href);

            let djaesyframe = el;

            let ifrm = document.createElement("iframe");
            ifrm.setAttribute("src", el.dataset.src);
            ifrm.setAttribute("id", el.id);
            ifrm.setAttribute('class', el.className);

            ifrm.addEventListener('load', function(event) {
                ifrm.contentWindow.postMessage({
                    message: 'send-me-your-tab-title-please',
                    tab_id: this.id,
                    tab_pathname: ifrm.contentWindow.location.pathname,
                    tab_origin: ifrm.contentWindow.location.origin
                });
            });

            el.appendChild(ifrm);
        },
    });

    Vue.use(VueAxios, axios);
    Vue.config.productionTip = false;

    let app = new Vue({
        el: '#djaesy-main',
        delimiters: ["{[","]}"],
        data: {
            pathname: '/',
            body: null,
            document: null,
            sidebar: null,
            tabs: []
        },
        computed: {
            tabIsClosable: function() {
                return (this.tabs.length > 1);
            }
        },
        methods: {
            // -- Sidebar
            openSidebar: function() {
                this.body.removeClass('sidebar-collapse');
                this.body.removeClass('sidebar-toggle');
                this.sidebar.removeClass('toggled');
                this.sidebar_wrapper.addClass('sidebar-scroll');
            },
            closeSidebar: function() {
                this.body.addClass('sidebar-collapse');
                this.body.addClass('sidebar-toggle');
                this.sidebar.addClass('toggled');
                this.sidebar_wrapper.removeClass('sidebar-scroll');
                $('.sidebar .collapse').collapse('hide');
            },
            toggleSidebar: function() {
                if(this.body.hasClass('sidebar-collapse')) {
                    this.openSidebar();
                } else {
                    this.closeSidebar();
                }
            },
            // -- Control Sidebar
            openControlSidebar: function() {
                this.body.addClass('control-sidebar-open');
            },
            closeControlSidebar: function() {
                this.body.removeClass('control-sidebar-open');
            },
            toggleControlSidebar: function() {
                if(this.body.hasClass('control-sidebar-open')) {
                    this.closeControlSidebar();
                } else {
                    this.openControlSidebar();
                }
            },
            // -- Full Screen
            enterFullScreen: function() {
                this.body.addClass('fullscreen');
                this.closeSidebar();
            },
            exitFullScreen: function() {
                this.body.removeClass('fullscreen');
            },
            toggleFullScreen: function() {
                if(this.body.hasClass('fullscreen')) {
                    this.exitFullScreen();
                } else {
                    this.enterFullScreen();
                }
            },
            // -- Menu Tabs
            openTab: function(event, url, icon, title) {
                let id = this.uuid();
                let iframe_id = `iframe-${id}`;
                url = `${window.location.origin}${url}`;
                this.tabs.forEach(function(item) {
                    item.active = false;
                });
                this.tabs.push(
                    {id: id, url: url, display_url:url, icon: icon, title: title, iframe_id: iframe_id, active: true}
                );
            },
            closeTab: function(event, id) {
                if(this.tabIsClosable) {
                    this.tabs = this.tabs.filter(function(item){
                        return item.id !== id;
                    });
                }
                this.setLastTabActive();
            },
            setLastTabActive: function() {
                let active = 0;
                this.tabs.forEach(function(item) {
                    if(item.active) {
                        active++;
                    }
                });
                if(active === 0 && this.tabs.length > 0) {
                    let tab = this.tabs[this.tabs.length - 1];
                    tab.active = true;
                    document.title = tab.title;
                }
            },
            selectTab: function(event, id) {
                this.tabs.forEach(function(item) {
                    item.active = item.id === id;
                    if(item.active) {
                        document.title = item.title;
                        window.history.replaceState( null, null, item.display_url);
                    }
                });
            },
            updateTabTitle: function(id, title, icon, url) {
                this.tabs.forEach(function(tab) {
                    if(tab.iframe_id === id) {
                        tab.title = title;
                        tab.icon = icon;
                        tab.display_url = url;
                        if(tab.active) {
                            document.title = tab.title;
                        }
                        window.history.replaceState( null, null, url);
                    }
                });
            },
            // -- Utils
            closeAll: function() {
                this.closeSidebar();
                this.closeControlSidebar();
            },
            // -- Create UUID
            uuid: function() {
              return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                let r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
              });
            }
        },
        mounted: function () {

            this.body = $('body');
            this.document = $(document);
            this.sidebar = $('.sidebar');
            this.sidebar_wrapper = $('#sidebar-menu');

            let url = window.djaesy_tab_url;

            if(!djaesy_no_tab) {
                this.pathname = window.djaesy_app_pathname;
                this.openTab(null, url, '', 'title' );
            }

            this.setLastTabActive();
            let self = this;

            window.addEventListener('message', function(e) {
                switch(e.data.message) {
                    case 'send-me-your-tab-title-please':
                        window.parent.postMessage({
                            message: 'here-is-my-tab-title',
                            tab_id: e.data.tab_id,
                            tab_title: window.djaesy_page_tile,
                            tab_icon: window.djaesy_page_icon,
                            tab_pathname: e.data.tab_pathname,
                            tab_origin: e.data.tab_origin
                        });
                        break;
                    case 'here-is-my-tab-title':
                        let pathname = e.data.tab_pathname;
                        let origin = e.data.tab_origin;
                        let display_url;
                        if(self.pathname) display_url = `${origin}${self.pathname}${pathname}`;
                        else display_url = `${origin}${pathname}`;
                        self.updateTabTitle(
                            e.data.tab_id,
                            e.data.tab_title,
                            e.data.tab_icon,
                            display_url
                        );
                        break;
                    default:
                        break;
                }
            });

            // Get arbitrary element with id "my-element"
            let myElementToCheckIfClicksAreInsideOf = document.querySelector('.sidebar');
            // Listen for click events on body
            window.addEventListener('click', function (event) {
                if (!myElementToCheckIfClicksAreInsideOf.contains(event.target)) {
                    $('.sidebar-toggle .sidebar .collapse').collapse('hide');
                }
            });
            window.addEventListener('blur', function() {
                $('.sidebar-toggle .sidebar .collapse').collapse('hide');
            });
            self.sidebar.on('mouseover', function() {
                window.focus();
            });

        }
    });

    // var event_notification = new Vue({
    //     el: '#event_notification',
    //     delimiters: ["{[","]}"],
    //     data: {
    //         message: 'Hello Vue!',
    //         severity_description: {
    //             'C': '🔺 Crítico',
    //             'H': '🟠 Alto',
    //             'M': '🟡 Médio',
    //             'L': '🟢 Baixo',
    //             'I': '🔘 Informativo'
    //         },
    //         csrf_token: '',
    //         owner_id: '',
    //         notifications: [],
    //         severity_class: '',
    //         silence_form_id: '',
    //         silence_form_notification: {},
    //         silence_form_sending: false,
    //         silence_form_multiple: false,
    //         silence_form_comment: '',
    //         alerts_modal: null,
    //         silence_modal: null,
    //         backdrop: false,
    //         filter: '',
    //         all_selected: false
    //     },
    //     computed: {
    //         notificationsToShow: function() {
    //             if(this.filter !== '') {
    //                 let self = this;
    //                 return this.notifications.filter(function (n) {
    //                     return n.severity === self.filter;
    //                 })
    //             } else {
    //                 return this.notifications;
    //             }
    //         },
    //         severitiesAvailable: function() {
    //             let severeties = {};
    //             this.notifications.forEach(function(n) {
    //                 //let desc = severity_description[n.severity];
    //                 let desc = n.severity;
    //                 if(!severeties[desc]) severeties[desc] = 1; else severeties[desc] += 1;
    //             });
    //             return severeties;
    //         },
    //         totalNotifications: function() {
    //             return this.notifications.length;
    //         },
    //         totalSelected: function() {
    //             let count = 0;
    //             this.notificationsToShow.forEach(function(n) {
    //                 if(n.selected) {
    //                     count += 1;
    //                 }
    //             });
    //             return count;
    //         },
    //         notificationsSelected: function() {
    //             if(this.silence_form_multiple) {
    //                 return this.notificationsToShow.filter(function (n) {
    //                     return n.selected;
    //                 });
    //             } else {
    //                 return [this.silence_form_notification];
    //             }
    //         },
    //         notificationsSelectedIds: function() {
    //             if(this.silence_form_multiple) {
    //                 return this.notificationsSelected.map(function (n) {
    //                     return n.id;
    //                 });
    //             }
    //         },
    //         showClearFilter: function() {
    //             return Boolean(this.filter !== '' && Object.keys(this.severitiesAvailable).length > 1);
    //         }
    //     },
    //     methods: {
    //         closeAll: function() {
    //             this.alerts_modal.modal('hide');
    //             this.silence_modal.modal('hide');
    //             this.backdrop = false;
    //         },
    //         severityClass: function() {
    //             let severity = this.notifications.map(function(n) { return severity_level[n.severity] });
    //             let max_level = Math.max.apply(Math, severity);
    //             return level_class[max_level];
    //         },
    //         getNotificationById: function(nid) {
    //             let found = false;
    //             let notification_obj = null;
    //             this.notifications.forEach(function(notification) {
    //                 if(!found && notification.id === nid) {
    //                     found = true;
    //                     notification_obj = notification;
    //                 }
    //             });
    //             return notification_obj;
    //         },
    //         removeNotification: function(nid) {
    //             let notification = this.getNotificationById(nid);
    //             const index = this.notifications.indexOf(notification);
    //             if (index > -1) {
    //                 this.notifications.splice(index, 1);
    //             }
    //         },
    //         selectNotification: function(nid) {
    //             let notification = this.getNotificationById(nid);
    //             const index = this.notifications.indexOf(notification);
    //             if (index > -1) {
    //                 this.$set(this.notifications[index], 'selected', !this.notifications[index].selected);
    //             }
    //         },
    //         toggleSelectAll: function() {
    //             if(this.all_selected) {
    //                 this.unselectAll();
    //             } else {
    //                 this.selectAll();
    //             }
    //         },
    //         selectAll: function() {
    //             let self = this;
    //             this.notifications.forEach(function(notification, idx) {
    //                 self.$set(self.notifications[idx], 'selected', true);
    //             });
    //             this.all_selected = true;
    //         },
    //         unselectAll: function() {
    //             let self = this;
    //             this.notifications.forEach(function(notification, idx) {
    //                 self.$set(self.notifications[idx], 'selected', false);
    //             });
    //             this.all_selected = false;
    //         },
    //         setFilter: function(filter='') {
    //             this.filter = filter;
    //         },
    //         silenceAlert: function(nid) {
    //             let self = this;
    //             this.silence_form_id = nid;
    //             this.backdrop = true;
    //             this.silence_form_multiple = false;
    //             this.silence_form_notification = this.getNotificationById(nid);
    //             this.alerts_modal.on('hidden.bs.modal', function() {
    //                 self.silence_modal.modal('show');
    //                 self.alerts_modal.off('hidden.bs.modal');
    //             });
    //             this.alerts_modal.modal('hide');
    //             event.preventDefault();
    //         },
    //         silenceSelectedAlert: function() {
    //             let selected_ids = []
    //             this.notificationsToShow.forEach(function(n) {
    //                 if(n.selected) {
    //                     selected_ids.push(n.id);
    //                 }
    //             });
    //             if(selected_ids.length === 1) {
    //                 this.silenceAlert(selected_ids[0]);
    //             } else {
    //                 this.silence_form_id = selected_ids.join(',');
    //                 this.silence_form_multiple = true;
    //                 let self = this;
    //                 this.alerts_modal.on('hidden.bs.modal', function() {
    //                     self.silence_modal.modal('show');
    //                     self.alerts_modal.off('hidden.bs.modal');
    //                 });
    //                 this.alerts_modal.modal('hide');
    //             }
    //             event.preventDefault();
    //         },
    //         cancelSilence: function() {
    //             let self = this;
    //             this.silence_modal.on('hidden.bs.modal', function() {
    //                 self.alerts_modal.modal('show');
    //                 self.silence_modal.off('hidden.bs.modal');
    //             });
    //             this.silence_modal.modal('hide');
    //         },
    //         silenceRequest: function(event) {
    //
    //             if(this.silence_form_sending) return;
    //
    //             let self = this;
    //
    //             this.silence_form_sending = true;
    //             event.preventDefault();
    //
    //             let data = {};
    //             const url = '/api/v1/events/silence/';
    //             const config = {headers: {"X-CSRFToken": this.csrf_token}};
    //
    //             if(this.silence_form_multiple) {
    //                 data = {
    //                     event_id: this.notificationsSelectedIds.join(','),
    //                     silence_comment: this.silence_form_comment,
    //                 }
    //             } else {
    //                 data = {
    //                     event_id: this.silence_form_id,
    //                     silence_comment: this.silence_form_comment,
    //                 }
    //             }
    //
    //             data.event_id_type = 'event_report';
    //
    //             this.axios.post(url, data, config)
    //             .then(function (response) {
    //                 if(self.silence_form_multiple) {
    //                     self.notificationsSelected.forEach(function(n) {
    //                         self.removeNotification(n.id);
    //                     });
    //                 } else {
    //                     self.removeNotification(self.silence_form_id);
    //                 }
    //                 // -- Switch modal
    //                 if(self.totalNotifications > 0) {
    //                     self.silence_modal.on('hidden.bs.modal', function () {
    //                         self.alerts_modal.modal('show');
    //                         self.silence_modal.off('hidden.bs.modal');
    //                     });
    //                 }
    //                 self.silence_modal.modal('hide');
    //                 // -- Notify and finish
    //                 toastr['success']('Operação de silenciar alertas concluída com sucesso!', 'Sucesso');
    //                 self.silence_form_sending = false;
    //             })
    //             .catch(function (error) {
    //                 // -- Notify and finish
    //                 toastr['error']('Houve um erro ao silenciar a alertas! Contate o suporte.', 'Erro');
    //                 self.silence_form_sending = false;
    //             });
    //         }
    //     },
    //     mounted: function () {
    //
    //         let self = this;
    //         this.owner_id = $('#ownerId').data('owner');
    //         this.csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    //         this.silence_modal = $('#alertsSilenceModal');
    //         this.alerts_modal = $('#alertsModal');
    //         this.event_icon = $('#eventsIcon');
    //
    //         $.ajax({
    //             url: '/api/v1/events/',
    //             method: 'GET',
    //             success: function (data) {
    //                 self.notifications = data.notifications;
    //                 self.severity_class = self.severityClass();
    //             },
    //             error: function (error) {
    //                 console.log(error);
    //             }
    //         });
    //
    //         const eventReportSocket = new WebSocket('ws://' + window.location.host + '/ws/v1/events/report/' + this.owner_id + '/');
    //
    //         eventReportSocket.onmessage = function(e) {
    //             const data = JSON.parse(e.data);
    //             self.notifications.unshift(data);
    //             self.severity_class = self.severityClass();
    //             self.event_icon.addClass('ring');
    //             setTimeout(function() {
    //                 self.event_icon.removeClass('ring');
    //             }, 1000);
    //
    //         };
    //
    //         eventReportSocket.onclose = function(e) {
    //             console.error('Chat socket closed unexpectedly');
    //         };
    //
    //     }
    // });

}.call(this));