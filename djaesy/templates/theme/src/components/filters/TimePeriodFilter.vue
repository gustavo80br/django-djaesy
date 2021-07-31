<template>
    <div class="flex items-center justify-between">
        <div>
            <span class="relative inline-flex shadow-sm rounded-md">
                <button
                    @click="setType('daily')"
                    type="button"
                    :class="[
                        periodType == 'daily'
                            ? 'bg-secondary text-white hover:bg-teal-400'
                            : 'bg-white text-gray-700 hover:bg-gray-50',
                        'relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500',
                    ]"
                >
                    Daily
                </button>
                <button
                    @click="setType('weekly')"
                    type="button"
                    :class="[
                        periodType == 'weekly'
                            ? 'bg-secondary text-white hover:bg-teal-400'
                            : 'bg-white text-gray-700 hover:bg-gray-50',
                        '-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500',
                    ]"
                >
                    Weekly
                </button>
                <button
                    @click="setType('monthly')"
                    type="button"
                    :class="[
                        periodType == 'monthly'
                            ? 'bg-secondary text-white hover:bg-teal-400'
                            : 'bg-white text-gray-700 hover:bg-gray-50',
                        '-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500',
                    ]"
                >
                    Monthly
                </button>

                <button
                    @click="setType('range')"
                    type="button"
                    :class="[
                        periodType == 'range'
                            ? 'bg-secondary text-white hover:bg-teal-400'
                            : 'bg-white text-gray-700 hover:bg-gray-50',
                        '-ml-px relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500',
                    ]"
                >
                    Range
                </button>
            </span>
        </div>
        <div>
            <el-date-picker
                v-if="periodType == 'daily'"
                v-model="day"
                :disabled-date="disabledDate"
                type="date"
                placeholder="Pick a day"
            >
            </el-date-picker>
            <el-date-picker
                v-if="periodType == 'weekly'"
                v-model="week"
                :disabled-date="disabledDate"
                type="week"
                format="[Week] ww"
                placeholder="Pick a week"
            >
            </el-date-picker>
            <el-date-picker
                v-if="periodType == 'monthly'"
                v-model="month"
                :disabled-date="disabledDate"
                type="month"
                placeholder="Pick a month"
            >
            </el-date-picker>
            <el-date-picker
                v-if="periodType == 'range'"
                v-model="range"
                :disabled-date="disabledDate"
                type="daterange"
                unlink-panels
                range-separator="To"
                start-placeholder="Start date"
                end-placeholder="End date"
                :shortcuts="shortcuts"
            >
            </el-date-picker>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment';

export default {
    data() {
        return {
            disabledDate(time) {
                return time.getTime() > Date.now()
            },
            week: '',
            month: new Date(),
            day: '',
            range: '',
            shortcuts: [
                {
                    text: 'Last week',
                    value: (() => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                        return [start, end]
                    })(),
                },
                {
                    text: 'Last month',
                    value: (() => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                        return [start, end]
                    })(),
                },
                {
                    text: 'Last 3 months',
                    value: (() => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                        return [start, end]
                    })(),
                },
            ],
        }
    },
    watch: {
        day(value) {
            this.setPeriod([new Date(value), new Date(value)])
        },
        week(value) {
            const dt = new Date(value)
            let ndt = new Date(value)
            this.setPeriod([dt, new Date(ndt.setDate(ndt.getDate() + 6))])
        },
        month(value) {
            const dt = new Date(value)
            this.setPeriod([
                dt,
                new Date(dt.getFullYear(), dt.getMonth() + 1, 0),
            ])
        },
        range(value) {
            const [start, end] = value
            this.setPeriod([new Date(start), new Date(end)])
        },
    },
    computed: {
        ...mapState({
            period: (state) => state.period,
            periodType: (state) => state.filters.periodType,
        }),
    },
    methods: {
        ...mapActions(['setPeriod', 'setPeriodType']),
        setType(type) {
            this.setPeriodType(type)
            const now = moment()
            switch (this.periodType) {
              case 'daily':
                this.day = new Date()
                break
              case 'monthly':
                this.month = new Date(now.clone().startOf("month"))
                break
              case 'weekly':
                this.week = new Date(now.clone().startOf("week"))
                break
              case 'range':
                this.range = [new Date(now.clone().startOf("month")), new Date(now)]
            }
        },
    },
}
</script>
