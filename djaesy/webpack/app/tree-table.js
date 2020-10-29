
// Import CSS
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
import 'toastr/build/toastr.css'

// Import JS
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
import 'toastr/toastr.js'

// Lib CSS
import './assets/css/tree-table.scss'


;(function() {
    $(document).ready(function() {

        // --
        // Main code
        // --

        // Return table with id generated from row's name field
        function format(row_id_prefix, row_id, classes='display') {
            let childTable = '<table id="'+ row_id_prefix + row_id + '" class="data-child-table ' + classes + '" width="100%">' +
                '<thead style="display:none"></thead >' +
                '</table>';
            return $(childTable).toArray();
        }

        // function format2(rowData) {
        //     let childTable = '<table id="mt' + rowData.id + '" class="display compact nowrap w-100" width="100%">' +
        //         '<thead style="display:none"></thead >' +
        //         '</table>';
        //     return $(childTable).toArray();
        // }

        // function format3(rowData) {
        //     let childTable = '<table id="in' + rowData.id + '" class="display wrap w-100 cell-border" width="100%">' +
        //         '<thead style="display:none"></thead >' +
        //         '</table>';
        //     return $(childTable).toArray();
        // }

        function child_table_load(table, subtable, row_id_prefix, level) {

            return function () {

                let tr = $(this).closest('tr');
                let datatable = $(this).closest('table').DataTable();
                let row = datatable.row(tr);
                let rowData = row.data();
                let id = rowData.id;
                let sub_datatable = null;

                if (row.child.isShown()) {
                    row.child.hide();
                    tr.removeClass('shown');
                    $('#' + row_id_prefix + id).DataTable().destroy();
                } else {

                    row.child(format(row_id_prefix, id), 'child-data p-0').show();

                    sub_datatable = $('#' + row_id_prefix + id).DataTable({
                        dom: "t",
                        columns: COLUMNS[subtable].columns,
                        columnDefs: COLUMNS[subtable].columnDefs,
                        select: false,
                        paging: false,
                        ordering: false
                    });

                    tr.addClass('shown');

                    $.get(`${LEVELS_URL[0]}?${level}=${id}`)
                    .done(function load_main_table(result) {
                        let data = result.data;
                        sub_datatable.clear().draw();
                        sub_datatable.rows.add(data).draw();
                    })
                    .fail(function (result) {
                        console.log('fail');
                        toastr['error']('error', 'real error');
                    });
                }
            }
        }

        if(typeof REPORT_TABLES !== "undefined") {

            // Main table
            REPORT_TABLES[0] = $('#ReportTable').DataTable({
                dom: 't',
                formatNumber: function(toFormat) {
                    return toFormat.toString().replace(
                      /\B(?=(\d{3})+(?!\d))/g, "'"
                    );
                },
                pageLength: COLUMNS[0].pageLength,
                columns: COLUMNS[0].columns,
                columnDefs: COLUMNS[0].columnDefs,
                order: false,
                ordering: false
            });

            $('#ReportTable tbody').on('click', 'td.controls.h_1',
                child_table_load(0, 1, 'cl', 'h_1')
            );

            $('tbody').on('click', 'td.controls.h_2',
                child_table_load(1, 2, 'ml', 'h_2')
            );

            $('tbody').on('click', 'td.controls.h_3',
                child_table_load(2, 3, 'xl', 'h_3')
            );

            $('tbody').on('click', 'td.controls.h_4',
                child_table_load(3, 4, 'zl', 'h_4')
            );
        }

    });
}.call(this));
