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


;(function() {
    $(document).ready(function() {
        // --
        // Main code
        // --

        function update_table_selection() {
            let selected = $('.dataTables_wrapper tr.selected td:first-child').map(function(){
                return $.trim($(this).text());
            }).get();
            $(document).trigger('vehicle-details:track-selection', [selected, true]);
        }

        let list_datatable = $('#vehicle_segments').DataTable({
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

        list_datatable.on('select', update_table_selection);
        list_datatable.on('deselect', update_table_selection);

        $(document).on('vehicle-details:go-to-last-pos', function() {
            list_datatable.rows().deselect();
        });

    });
}.call(this));
