// Dependencies of Theme and AdminLTE

import '../mdbootstrap/css/bootstrap.css'
import '../sb-admin-2/scss/sb-admin-2.scss'

import 'node-waves/src/scss/waves.scss'
import 'morris.js/morris.css'
import 'select2/src/scss/core.scss'

import 'toastr/build/toastr.css'
import './assets/css/icons.css'

import './assets/css/theme.scss'



// import 'datatables.net-bs4/css/dataTables.bootstrap4.css'
// import 'datatables.net-autofill-bs4/css/autoFill.bootstrap4.css'
// import 'datatables.net-buttons-bs4/css/buttons.bootstrap4.css'
// import 'datatables.net-colreorder-bs4/css/colReorder.bootstrap4.css'
// import 'datatables.net-fixedcolumns-bs4/css/fixedColumns.bootstrap4.css'
// import 'datatables.net-fixedheader-bs4/css/fixedHeader.bootstrap4.css'
// import 'datatables.net-keytable-bs4/css/keyTable.bootstrap4.css'
// import 'datatables.net-responsive-bs4/css/responsive.bootstrap4.css'
// import 'datatables.net-rowgroup-bs4/css/rowGroup.bootstrap4.css'
// import "datatables.net-select-bs4/css/select.bootstrap4.css"
//

import 'jquery'
import './autoselect.js'

import './js/djaesy-admin.js'

import 'mdbootstrap/js/popper.js'
import 'mdbootstrap/js/bootstrap.min.js'

import 'toastr/toastr.js'

import 'node-waves/src/js/waves.js'
import 'mousetrap'
import '../select2/select2.full.js'

import 'datatables.net-bs4/css/dataTables.bootstrap4.css'
import 'datatables.net-autofill-bs4/css/autoFill.bootstrap4.css'
import 'datatables.net-buttons-bs4/css/buttons.bootstrap4.css'
import 'datatables.net-colreorder-bs4/css/colReorder.bootstrap4.css'
import 'datatables.net-fixedcolumns-bs4/css/fixedColumns.bootstrap4.css'
import 'datatables.net-fixedheader-bs4/css/fixedHeader.bootstrap4.css'
import 'datatables.net-keytable-bs4/css/keyTable.bootstrap4.css'
import 'datatables.net-responsive-bs4/css/responsive.bootstrap4.css'
import 'datatables.net-rowgroup-bs4/css/rowGroup.bootstrap4.css'
import "datatables.net-select-bs4/css/select.bootstrap4.css"

import 'datatables.net-bs4'
import 'datatables.net-autofill-bs4'
import 'datatables.net-buttons-bs4'
import 'datatables.net-buttons/js/buttons.colVis.js'
import 'datatables.net-buttons/js/buttons.html5.js'
import 'datatables.net-buttons/js/buttons.print.js'
import 'datatables.net-colreorder-bs4'
import 'datatables.net-fixedcolumns-bs4'
import 'datatables.net-fixedheader-bs4'
import 'datatables.net-keytable-bs4'
import 'datatables.net-responsive-bs4'
import 'datatables.net-rowgroup-bs4'
import 'datatables.net-select-bs4'

import './datetime.js'
import './multiselectbox.js'
import './select2_init.js'
import './form_helpers.js'
import './translation.js'


import { VehicleMap } from './vehicle_map.js';
window.VehicleMap = VehicleMap;

import 'simplebar'

function toast_alert(title, content, type='primary', delay=2000) {
    let g_alert = $('#generic-alert');
    let g_alert_title = g_alert.find('#generic-alert-title');
    let g_alert_content = g_alert.find('#generic-alert-content');
    g_alert_title.text(title);
    g_alert_content.text(content);
    g_alert.removeClass('alert-primary alert-secondary alert-success alert-danger alert-warning alert-info alert-light alert-dark');
    g_alert.addClass(`alert-${type}`);
    g_alert.attr('style', 'display: block');
    g_alert.toast({'delay': delay}).toast('show');
}

function update_table_selection() {
    let selected = $('.dataTables_wrapper tr.selected td:first-child').map(function(){
        return $.trim($(this).text());
    }).get();
    $(".selected-items-field").val(selected);
}

function submit_action_form(action_id, has_form, max_selected=0) {

    let selected = $(".selected-items-field").val();

    if(max_selected >= 0) {
        if(selected) {
            selected = selected.split(',').length;
            if(max_selected && selected > max_selected) {
                if(max_selected === 1) {
                    toastr["warning"](TRANS_SELECT_ONLY_ONE, TRANS_MULTIPLE_SELECTED);
                    return;
                } else {
                    toastr["warning"](TRANS_SELECT_LIMIT_EXCEEDED, TRANS_MULTIPLE_SELECTED);
                    return;
                }
            }
        } else {
            toastr["warning"](TRANS_SELECT_AT_LEAST_ONE, TRANS_NO_ITEM_SELECTED);
            return;
        }
    }

    if(has_form) {
        $(`#action_modal_${action_id}`).modal().show();
    } else {
        $(`#action_form_${action_id}`).submit();
    }

}

function previous_selected_rows(previous_selected, dt) {
    let prev = previous_selected.split(',');
    dt.rows().every( function () {
        let idx = this.data()[0];
        if(prev.includes(idx)){
            this.select();
        }
    });
}

function clean_form_validation(form) {
    form = $(form);
    form.find('.alert').hide();
    form.find('.is-invalid').removeClass('is-invalid');
    form.find('.invalid-feedback').removeClass('invalid-feedback');
}

// Main
$(document).ready(function() {

    // // Menu sidebar
    // if (JSON.parse(localStorage.getItem('menu-sidebar')))
    //     $('body').removeClass('sidebar-collapse');
    // $(document).on('expanded.pushMenu', () => { localStorage.setItem('menu-sidebar', true) });
    // $(document).on('collapsed.pushMenu', () => { localStorage.setItem('menu-sidebar', false) });
    //
    // // Control sidebar
    // if (JSON.parse(localStorage.getItem('control-sidebar'))) {
    //     $('body').addClass('control-sidebar-open');
    //     $('#control-sidebar-toggle').addClass('control-sidebar-open')
    // }
    // $(document).on('expanded.controlsidebar', () => { localStorage.setItem('control-sidebar', true) });
    // $(document).on('collapsed.controlsidebar', () => { localStorage.setItem('control-sidebar', false) });
    //
    // // Fullscreen
    // if (JSON.parse(localStorage.getItem('fullscreen'))) {
    //
    // }

    let table_el = $('#list_datatable');
    if(!table_el.length) {
        table_el = $('#dashboard_table');
    }

    let list_datatable = table_el.DataTable({
        paging: false,
        select: true,
        ordering: false,
        info: false,
        searching: false,
        autoWidth: false,
        dom: '<"datatable-toolbar">ftip',
        oLanguage: {
            sSearch: ''
        },
        language : {
            searchPlaceholder: DATATABLES_SEARCH_PLACEHOLDER
        }
    });

    let dt_toolbar_content = $('.datatable-toolbar-source');
    let dt_toolbar = $('.datatable-toolbar');
    dt_toolbar.append(dt_toolbar_content);

    list_datatable.on('select', update_table_selection);
    list_datatable.on('deselect', update_table_selection);

    $('.select-all-action').on('click', function() {
        let selected = $(".selected-items-field").val().split(',').length;
        let total = list_datatable.rows().count();
        if(selected === total) {
            list_datatable.rows().deselect();
        } else {
            list_datatable.rows().select();
        }
    });


    $('.dataframe thead th.sortable').on('click', function(e) {

        e.preventDefault();

        let index = list_datatable.column(this).index();
        if(!index) {

        }

        if(index === 2) return;

        if(index === 1) {
            if(list_datatable.rows({ selected: true }).indexes().length === list_datatable.rows().indexes().length) {
                list_datatable.rows().deselect();
            } else {
                list_datatable.rows().select();
            }
            return;
        } else {
            index = index - 2
        }

        let order = $('#order');
        let order_by = $('#order_by');

        let actual_order_by = Number(order_by.val());
        let actual_order = order.val();

        if(!actual_order_by || (actual_order_by === index && !actual_order) || !(actual_order_by === index)) {
            actual_order = 'asc';
        } else if(actual_order_by === index && actual_order) {
            if(actual_order === 'asc') actual_order = 'desc';
            else actual_order = 'asc'
        }

        order_by.val(index);
        order.val(actual_order);

        $(this).parents('form').submit();

    });

    $('.call_action').on('click', function() {
        let self = $(this);
        let action_id = self.data('action');
        let show_form = self.data('form');
        let max_selected = self.data('maxselected');
        submit_action_form(action_id, show_form, max_selected);
    });

    $('.call-item-action').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        let self = $(this);
        let tr = self.parents('tr');

        list_datatable.rows().deselect();
        list_datatable.row(tr).select();

        let action_id = self.data('action');
        let show_form = self.data('form');
        let max_selected = self.data('maxselected');

        submit_action_form(action_id, show_form, max_selected);
    });

    let prev_selected = $('#list_previous_selected').val();
    if(prev_selected) {
        previous_selected_rows(prev_selected, list_datatable);
    }

    let action_invalid = $('#action_invalid').val();
    if(action_invalid) {
        let modal = $(`#action_modal_${action_invalid}`)
        modal.modal().show();
        modal.on('hidden.bs.modal', function() {
            clean_form_validation($(this).find('form'));
        });
    }

    // $('select').select2({
    //     placeholder: 'Selecione...'
    // });

    // $('[data-toggle="popover-hover"]').popover();
    // $('[data-toggle="popover-click"]').popover();
    // $('[data-toggle="popover"]').popover();


    if(CASCADE_CLEAR_FIELDS) {
        for(const field in CASCADE_CLEAR_FIELDS) {
            if (CASCADE_CLEAR_FIELDS[field]) {
                CASCADE_CLEAR_FIELDS[field].forEach(function(forward) {
                    $(`#id_${forward}`).on('change', function(y) {
                        var to_clear = $(`#id_${field}`);
                        to_clear.val('');
                        to_clear.trigger('change');
                        if(to_clear.select2 !== undefined) {
                            to_clear.trigger('multiselectbox:reset');
                        }
                    });
                });
            }
        }
    }

    if(CASCADE_DISABLE_FIELDS) {
        for(const field in CASCADE_DISABLE_FIELDS) {
            if (CASCADE_DISABLE_FIELDS[field]) {
                for (const disable_value in CASCADE_DISABLE_FIELDS[field]) {
                    CASCADE_DISABLE_FIELDS[field][disable_value].forEach(function (to_disable) {

                        let trigger_field = $(`#id_${field}`);

                        let enable_or_disable = function(trigger, value, field_to_disable) {

                            let disable = false;

                            if(value === 'EMPTY') {
                                let val = trigger.val();
                                if(val) {
                                    if(val.length === 0) disable = true;
                                } else {
                                    disable = true;
                                }
                            }
                            if(disable) {
                                $(`#id_${field_to_disable}`).attr("disabled", "disabled");
                            } else {
                                $(`#id_${field_to_disable}`).removeAttr("disabled");
                            }
                        };

                        trigger_field.on('change', function() {
                            var el = $(this);
                            enable_or_disable(el, disable_value, to_disable);
                        });

                        enable_or_disable(trigger_field, disable_value, to_disable);

                    });
                }
            }
        }
    }

    if(CASCADE_HIDE_FIELDS) {

        for(const field in CASCADE_HIDE_FIELDS) {
            if (CASCADE_HIDE_FIELDS[field]) {

                let trigger_field = $(`#id_${field}`);

                trigger_field.on('change app_panel:hide-start', function() {

                    // if(CASCADE_HIDE_FIELDS[field][hide_value].field_type)

                    let el = $(this);
                    let value = el.val();
                    if(el.is(':checkbox')) {
                        if(el.is(":checked")) {
                            value = 'on';
                        } else {
                            value = 'off';
                        }
                    }

                    for (const hide_value in CASCADE_HIDE_FIELDS[field]) {

                        let field_type = '';
                        if(CASCADE_HIDE_FIELDS[field][hide_value].field_type) {
                            field_type = CASCADE_HIDE_FIELDS[field][hide_value].field_type;
                            value = $(`#${field}-clear_id`);
                            value = value.length;
                        }

                        let match_empty = (hide_value === 'EMPTY' && value.length === 0);
                        let match_not_empty = (hide_value === 'NOT_EMPTY' && value.length > 0);
                        let match_value = (hide_value === value);

                        if(match_empty || match_value || match_not_empty) {
                            CASCADE_HIDE_FIELDS[field][hide_value]['hide'].forEach(function (to_hide) {
                                $(`#id_${to_hide}`).closest('.col').hide();
                            });
                            CASCADE_HIDE_FIELDS[field][hide_value]['show'].forEach(function (to_show) {
                                $(`#id_${to_show}`).closest('.col').show();
                            });
                        }
                    }
                });
                trigger_field.trigger('app_panel:hide-start');
            }
        }
    }

    $('.image-thumb-hover').popover({
      html: true,
      trigger: 'hover',
      title: function() {
        return $(this).data('title');
      },
      content: function () {
        return '<img height="200" width="200" src="'+$(this).data('img') + '" />';
      }
    });

    $('#load-overlay').hide();
    $('.wrapper').removeClass('blur');

    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": true,
        "progressBar": false,
        "positionClass": "toast-bottom-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    MESSAGES.forEach(function(message) {
        toastr[message.type](message.text, message.title);
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    $(function () {
        $('.tooltip-toggle').tooltip();
    });

});