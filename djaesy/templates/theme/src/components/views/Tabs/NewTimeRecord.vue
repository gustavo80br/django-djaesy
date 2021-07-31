<template>
    <div>
        <div class="px-4 py-5">
            <div class="grid grid-cols-2 gap-4">
                <div
                    v-if="date.toLocaleDateString() == '7/5/2021'"
                    class="sm:col-span-2 p-2"
                >
                    <div class="rounded-md bg-green-50 p-4">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <i class="fad fa-lights-holiday"></i>
                            </div>
                            <div class="ml-3">
                                <h3 class="text-sm font-medium text-green-800">
                                    Colombia's Holiday
                                </h3>
                                <div class="mt-2 text-sm text-green-700">
                                    <p>Feast of Saints Peter and Paul</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <label
                        for="date"
                        class="block text-sm font-medium text-gray-700"
                    >
                        Date
                    </label>
                    <div class="mt-1">
                        <el-date-picker
                            name="date"
                            class="
                                shadow-sm
                                focus:ring-sky-500 focus:border-sky-500
                                block
                                w-full
                                sm:text-sm
                                border-gray-300
                                rounded-md
                            "
                            v-model="date"
                            type="date"
                            placeholder="Pick a day"
                            :disabled-date="disabledDate"
                            :shortcuts="shortcuts"
                        >
                        </el-date-picker>
                    </div>
                </div>

                <div class="sm:col-span-1">
                    <label
                        for="hours"
                        class="block text-sm font-medium text-gray-700"
                        >Worked Hours</label
                    >
                    <div class="mt-1">
                        <input
                            v-model="hours"
                            @blur="fixHours"
                            v-maska="'#:##'"
                            type="text"
                            name="hours"
                            id="hours"
                            placeholder="0:00"
                            class="text-right pr-4"
                            style="height: 40px"
                        />
                    </div>
                </div>

                <div class="sm:col-span-2">
                    <task-description
                        v-model.sync="description"
                    ></task-description>
                </div>

                <div class="sm:col-span-2">
                    <label
                        for="comments"
                        class="block text-sm font-medium text-gray-700"
                    >
                        Comments
                    </label>
                    <div class="mt-1">
                        <el-input
                            name="comments"
                            id="comments"
                            placeholder="Tickets IDs, links..."
                            v-model="comments"
                            clearable
                        >
                        </el-input>
                    </div>
                </div>

                <div class="sm:col-span-1">
                    <focal-point v-model="focalPoint"></focal-point>
                </div>

                <div v-if="!editing" class="sm:col-span-1">
                    <label
                        for="price"
                        class="block text-sm font-medium text-gray-700"
                        >Repeat this record</label
                    >
                    <div class="mt-1 relative rounded-md shadow-sm">
                        <input
                            v-model="repeat"
                            type="number"
                            name="repeat"
                            id="repeat"
                            class="
                                focus:ring-teal-500 focus:border-teal-500
                                block
                                w-full
                                pl-7
                                pr-12
                                sm:text-sm
                                border-gray-300
                                rounded-md
                            "
                            placeholder="1"
                        />
                        <div
                            class="
                                absolute
                                inset-y-0
                                right-0
                                pr-3
                                flex
                                items-center
                                pointer-events-none
                            "
                        >
                            <span
                                class="text-gray-500 sm:text-sm"
                                id="price-currency"
                            >
                                times
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div
        class="
            px-4
            py-3
            bg-gray-50
            text-right
            sm:px-6
            rounded-b-lg
            overflow-hidden
        "
    >
        <cancel-button v-if="editing" @click="cancelEditing"
            >Cancel</cancel-button
        >
        <submit-button
            @click="save"
            :disabled="!date || !taskDescription || !hours || !comments"
            >Save</submit-button
        >
    </div>
    <overtime-modal
        v-model:isOpen="isOTModalOpen"
        v-model:overtimeType="overtimeType"
        v-model:overtimeReason="overtimeReason"
        :onConfirm="save"
    ></overtime-modal>
</template>

<script>
import OvertimeModal from '../../forms/modals/OvertimeModal.vue'
import FocalPoint from '../../forms/FocalPoint.vue'
import TaskDescription from '../../forms/TaskDescription.vue'
import people from '../../../store/people'
import SubmitButton from '../../forms/SubmitButton.vue'
import CancelButton from '../../forms/CancelButton.vue'
import { maska } from 'maska'
import { mapState, mapActions } from 'vuex'
import { hourStringToMinutes } from '../../../helpers/hours'

export default {
    components: {
        FocalPoint,
        TaskDescription,
        SubmitButton,
        CancelButton,
        OvertimeModal,
    },
    directives: { maska },
    emits: ['record:saved'],
    data() {
        return {
            disabledDate(time) {
                return time.getTime() > Date.now()
            },
            shortcuts: [
                {
                    text: 'Today',
                    value: new Date(),
                },
                {
                    text: 'Yesterday',
                    value: (() => {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24)
                        return date
                    })(),
                },
                {
                    text: 'A week ago',
                    value: (() => {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
                        return date
                    })(),
                },
            ],
            id: null,
            date: new Date(),
            hours: '',
            focalPoint: people[0],
            comments: '',
            description: '',
            taskDescription: '',
            overtime: false,
            overtimeReason: '',
            overtimeType: '',
            repeat: 1,
            isOTModalOpen: false,
        }
    },
    computed: {
        ...mapState({
            projectDefaults: (state) => state.projectDefaults,
            project: (state) => state.filters.project,
            editing: (state) => state.editing,
        }),
    },
    watch: {
        editing(value) {
            if (!value) return
            else this.edit(value)
        },
        description(value) {
            if (!value || !(typeof value === 'object')) return
            const [_, description] = value
            this.taskDescription = description
        },
        project() {
            this.initProjectDefault()
        },
    },
    methods: {
        ...mapActions(['saveRecord', 'getHoursByDate']),
        async exceededHours(date, amount, repeat = 1) {
            const dailyMinutes = this.project.expectedDailyMinutes

            const registeredHours = await this.getHoursByDate(date)

            const addingMinutes = hourStringToMinutes(amount) * repeat

            let registeredMinutes = 0
            for (const hour of registeredHours) {
                registeredMinutes += hourStringToMinutes(hour)
            }
            if (registeredMinutes + addingMinutes > dailyMinutes) {
                return {
                    exceeded: true,
                    amount: registeredMinutes + addingMinutes - dailyMinutes,
                }
            }

            return {
                exceeded: false,
                amount: 0,
            }
        },
        async save() {
            const validateOvertime =
                this.isOTModalOpen &&
                this.overtime &&
                (!this.overtimeType || !this.overtimeReason)
            if (validateOvertime) {
                this.$notify({
                    title: 'Required fields!',
                    message: 'Overtime Type and Reason are required.',
                    type: 'error',
                })
                return
            }
            const validation = await this.exceededHours(
                this.date,
                this.hours,
                this.repeat
            )

            if (!this.overtime && validation.exceeded) {
                this.isOTModalOpen = true
                this.overtime = true
                return
            }
            this.isOTModalOpen = false
            let holiday = false
            // if(this.date.toLocaleDateString() == '7/5/2021') holiday = true
            if (this.overtime) {
                const hours = parseInt(validation.amount / 60)
                const minutes = validation.amount % 60
                this.saveRecord({
                    id: this.id,
                    date: this.date,
                    hours: `${hours}:${minutes.toString().padStart(2, '0')}`,
                    focalPoint: this.focalPoint,
                    comments: this.comments,
                    taskDescription: this.taskDescription,
                    overtime: this.overtime,
                    overtimeType: this.overtimeType,
                    overtimeReason: this.overtimeReason,
                    repeat: 1,
                    holiday: holiday,
                })
                const regular =
                    hourStringToMinutes(this.hours) * this.repeat -
                    validation.amount / this.repeat
                const regularHours = parseInt(regular / 60)
                const regularMinutes = regular % 60
                this.saveRecord({
                    id: this.id,
                    date: this.date,
                    hours: `${regularHours}:${regularMinutes
                        .toString()
                        .padStart(2, '0')}`,
                    focalPoint: this.focalPoint,
                    comments: this.comments,
                    taskDescription: this.taskDescription,
                    repeat: this.repeat,
                    holiday: holiday,
                })
            } else {
                this.saveRecord({
                    id: this.id,
                    date: this.date,
                    hours: this.hours,
                    focalPoint: this.focalPoint,
                    comments: this.comments,
                    taskDescription: this.taskDescription,
                    repeat: this.repeat,
                    holiday: holiday,
                })
            }
            this.initProjectDefault()
            this.$emit('record:saved')
            this.$notify({
                title: 'Succesfully saved!',
                message: 'The record has been added/updated in time tracker',
                type: 'success',
            })
        },
        cancelEditing() {
            this.initProjectDefault()
            this.$emit('record:saved')
        },
        fixHours() {
            let tokens = this.hours.split(':')
            if (tokens[1].length == 0) tokens[1] = '00'
            else if (tokens[1].length == 1) tokens[1] = '0' + tokens[1]
            this.hours = tokens.join(':')
        },
        edit(record) {
            this.id = record.id
            this.date = record.date
            this.hours = record.hours
            this.comments = record.comments
            this.focalPoint = record.focalPoint
            this.taskDescription = record.taskDescription
            this.description = record.taskDescription
            this.overtime = record.overtime
            this.overtimeReason = record.overtimeReason
            this.overtimeType = record.overtimeType
            this.repeat = 1
        },
        initProjectDefault() {
            if (this.editing) {
                return this.edit(this.editing)
            }
            this.id = null
            this.date = new Date()
            this.hours = ''
            this.comments = ''
            this.overtime = false
            this.overtimeReason = ''
            this.overtimeType = ''
            if (!this.project) {
                this.focalPoint = people[0]
                this.description = ''
                return
            }
            const projectDefault = this.projectDefaults.get(this.project.id)
            if (projectDefault) {
                this.focalPoint = projectDefault.focalPoint
                this.description = projectDefault.description
            }
        },
    },
    mounted() {
        this.initProjectDefault()
    },
}
</script>
