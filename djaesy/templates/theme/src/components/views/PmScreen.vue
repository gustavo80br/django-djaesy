<template>
  <div class="container mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-3 lg:gap-8">
      <!-- Left column -->
      <div class="grid grid-cols-1 gap-4 lg:col-span-2">
        <div class="rounded-lg shadow bg-white px-4 py-5 grid grid-cols-1 gap-4 min-h-screen">
            <report-task-list v-if="report" :report="report"></report-task-list>
            <span v-else class="text-gray-500"> Please select a user report from the available options to see the details.</span>
        </div>
      </div>

      <!-- Right column -->
      <div class="grid grid-cols-1 gap-4 sticky top-0">
        <approve-report @change='selectReport'></approve-report>
      </div>
    </div>
  </div>
</template>

<script>
import ApproveReport from './Tabs/ApproveReport.vue'
import ReportTaskList from '../tables/ReportTaskList.vue'

export default {
    components: {
        ApproveReport,
        ReportTaskList,
    },
    data(){
        return {
            report: null,
        }
    },
    methods:{
        selectReport(item){
            this.report = item
        }
    }
}
</script>
