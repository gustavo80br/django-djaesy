<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-3 lg:gap-8">
            <!-- Left column -->
            <div class="grid grid-cols-1 gap-4 lg:col-span-2">
                <task-list-summary
                    v-if="!actAsPM && selectedProject"
                ></task-list-summary>
                <task-list :onEditClick="edit"></task-list>
            </div>

            <!-- Right column -->
            <div class="grid grid-cols-1 gap-4 sticky top-0">
                <select-project-menu v-if="!actAsPM"></select-project-menu>
                <right-column-tabs
                    v-if="!actAsPM && selectedProject"
                    @record:saved="handleRecordSaved"
                ></right-column-tabs>
                <hour-stats v-if="!actAsPM && !selectedProject"></hour-stats>
                <approve-report v-if="actAsPM"></approve-report>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, useStore } from 'vuex'

import HourStats from '../stats/HourStats.vue'
import RightColumnTabs from './Tabs/RightColumnTabs.vue'
import ApproveReport from './Tabs/ApproveReport.vue'
import TaskList from '../tables/TaskList.vue'
import TaskListSummary from '../tables/TaskListSummary.vue'
import SelectProjectMenu from '../forms/SelectProjectMenu.vue'

export default {
    components: {
        HourStats,
        RightColumnTabs,
        TaskList,
        TaskListSummary,
        SelectProjectMenu,
        RightColumnTabs,
        ApproveReport,
    },
    computed: {
        ...mapState({
            selectedProject: (state) => state.filters.project,
            period: (state) => state.filters.period,
            actAsPM: (state) => state.actAsPM,
            editing: (state) => state.editing,
        }),
    },
    setup() {
        const { dispatch } = useStore()
        const edit = (record) => {
            dispatch('setEditing', record)
        }

        const handleRecordSaved = () => {
            dispatch('setEditing', null)
        }

        return {
            edit,
            handleRecordSaved,
        }
    },
}
</script>
