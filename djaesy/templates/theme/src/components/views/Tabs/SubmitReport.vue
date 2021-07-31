<template>
  <div class="
            px-4
            py-5
            border-b border-gray-200
            sm:px-6
            rounded-lg
            grid grid-cols-1
            gap-y-6 gap-x-4
            overflow-hidden
        ">
    <div v-if="reports.filter((item)=>item.month =='2021-07').length > 0" class="text-center text-md text-gray-500">
        Your monthly report has already been submitted.
    </div>
    <div v-else class="text-center text-md text-gray-500">
      Please preview your monthly report before submitting.
      <div class="px-4 py-3 text-center sm:px-6 rounded-b-lg">
      <submit-button @click="preview">Preview report</submit-button>
      <submit-button
        @click="isModalOpen = true"
        class="bg-primary hover:bg-sky-500 focus:ring-sky-500"
      >Submit report</submit-button>
    </div>
    </div>


  </div>
  <confirm-submit-report
    v-model:isOpen="isModalOpen"
    :onConfirm="submit"
  ></confirm-submit-report>
</template>

<script>
import SubmitButton from '../../forms/SubmitButton.vue'
import ConfirmSubmitReport from '../../forms/modals/ConfirmSubmitReport.vue'
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
    components: {
        SubmitButton,
        ConfirmSubmitReport,
    },
    data() {
        return {
            isModalOpen: false,
        }
    },
    computed: {
        ...mapState({
            tasks: (state) => state.filteredRecords,
            reports: (state) => state.reports,
        }),
    },
    methods: {
        ...mapActions(['setPeriod', 'setPeriodType', 'addReport']),
        preview() {
            this.setPeriodType('monthly')
            const now = moment()
            let month = new Date(now.clone().startOf('month'))
            this.setPeriod([
                month,
                new Date(month.getFullYear(), month.getMonth() + 1, 0),
            ])
        },
        submit() {
            this.isModalOpen = false
            const [total_tasks, overtime_tasks] = this.taskTimesInMinutes()
            let totalMinutes = 0
            let overtimeMinutes = 0
            try {
                totalMinutes = total_tasks.reduce((a, b) => a + b)
            } catch {}
            try {
                overtimeMinutes = overtime_tasks.reduce((a, b) => a + b)
            } catch {}

            this.addReport({
                month: '2021-07',
                project: 1,
                status: 'submitted',
                hours: this.minutesToHours(totalMinutes),
                overtime: this.minutesToHours(overtimeMinutes),
                tasks: this.tasks,
            })
            this.$notify({
                title: 'Report submmited!',
                message: 'Your report is submitted',
                type: 'success',
            })
        },

        taskTimesInMinutes() {
            let total_tasks = []
            let overtime_tasks = []
            Object.entries(this.tasks).forEach((entry) => {
                let data = entry[1]
                if (data.overtime)
                    overtime_tasks.push(this.hoursToMinutes(entry[1].hours))
                total_tasks.push(this.hoursToMinutes(entry[1].hours))
            })
            return [total_tasks, overtime_tasks]
        },
        hoursToMinutes(str_hours) {
            let hour_minute = str_hours.split(':')
            let hour = parseInt(hour_minute[0])
            let min = parseInt(hour_minute[1])
            return hour * 60 + min
        },
        minutesToHours(min) {
            Number.prototype.pad = function (size) {
                let s = String(this)
                while (s.length < (size || 2)) {
                    s = '0' + s
                }
                return s
            }
            let full_hours = Math.floor(min / 60)
            let minutes = min % 60
            return `${full_hours.pad(1)}:${minutes.pad(2)}`
        },
    },
}
</script>

<style></style>
