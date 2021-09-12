<template>
  <div class="bg-white dark:bg-primary border dark:border-sky-600 shadow rounded-lg">
    <dl class="
                            grid grid-cols-1
                            rounded-lg
                            bg-white
                            dark:bg-sky-800
                            overflow-hidden
                            shadow
                            divide-y divide-gray-200 dark:divide-sky-600
                            md:grid-cols-4 md:divide-y-0 md:divide-x
                        ">
      <div
        v-for="item in calculatedStats"
        :key="item.name"
        class="px-4 py-5 sm:p-4"
      >
        <dt class="text-base font-normal text-gray-900 dark:text-gray-50">
          {{ item.name }}
        </dt>
        <dd class="
                                    mt-1
                                    flex
                                    justify-between
                                    items-baseline
                                    md:block
                                    lg:flex
                                ">
          <div :class="[
                                        item[period] === '0:00'
                                            ? 'text-gray-300 dark:text-gray-50'
                                            : item.name === 'Hours Overtime'
                                            ? 'text-teal-600 dark:text-teal-100'
                                            : 'text-teal-600 dark:text-teal-100',
                                        'flex items-baseline text-2xl font-semibold',
                                    ]">
            {{ item.value }}
          </div>
        </dd>
      </div>
    </dl>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment';

export default {
    data() {
        return {
            workExpected: {
                daily: 8,
                weekly: 40,
                monthly: 160,
                range: null,
            },
            stats: [
                {
                    name: 'Hours Expected',
                    value: '8:00',
                },
                {
                    name: 'Hours Worked',
                    value: '8:00',
                },
                {
                    name: 'Hours Missing',
                    value: '0:30',
                },
                {
                    name: 'Hours Overtime',
                    value: '0:30'
                },
            ],
        }
    },
    computed: {
        ...mapState({
            tasks: (state) => state.filteredRecords,
            selectedProject: (state) => state.filters.project,
            period: (state) => state.filters.period,
            actAsPM: (state) => state.actAsPM,
        }),
        calculatedStats () {
          const statistics = this.calculateStatistics();
          let self = this;
          statistics.forEach(function(item, i) {
            self.stats[i].value = self.minutesToHours(item);
          });
          return this.stats;
        }
    },
    methods: {
      hoursToMinutes (str_hours) {
        let hour_minute = str_hours.split(':');
        let hour = parseInt(hour_minute[0]);
        let min = parseInt(hour_minute[1]);
        return (hour * 60) + min;
      },
      minutesToHours (min) {
        Number.prototype.pad = function(size) {
          let s = String(this);
          while (s.length < (size || 2)) {s = "0" + s;}
          return s;
        }
        let full_hours = Math.floor(min/60);
        let minutes = min % 60;
        return `${full_hours.pad(1)}:${minutes.pad(2)}`;
      },
      taskTimesInMinutes () {
        let total_tasks = [];
        let overtime_tasks = [];
        Object.entries(this.tasks).forEach(entry => {
          let data = entry[1];
          if(data.overtime) overtime_tasks.push(this.hoursToMinutes(entry[1].hours));
          total_tasks.push(this.hoursToMinutes(entry[1].hours));
        });
        return [total_tasks, overtime_tasks];
      },
      calculateStatistics () {
        const [total_tasks, overtime_tasks] = this.taskTimesInMinutes();
        let expectedMinutes = this.getDaysInFilteredRange() * 4 * 60;
        let overtimeMinutes = 0;
        let totalMinutes = 0;
        try {
          totalMinutes = total_tasks.reduce((a, b) => a + b);
        } catch {}
        try {
          overtimeMinutes = overtime_tasks.reduce((a, b) => a + b);
        } catch {}
        let missingMinutes = expectedMinutes - totalMinutes;
        if(missingMinutes < 0) missingMinutes = 0;
        return [expectedMinutes, totalMinutes, missingMinutes, overtimeMinutes];
      },
      getDaysInFilteredRange () {
        const [startDate, endDate] = this.period;
        var day = moment(startDate);
        var businessDays = 0;
        while (day.isSameOrBefore(endDate,'day')) {
          if (day.day()!=0 && day.day()!=6) businessDays++;
          day.add(1,'d');
        }
        return businessDays;
      }
    }
}
</script>
