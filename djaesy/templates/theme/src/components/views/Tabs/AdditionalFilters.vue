<template>
    <div
        class="
            px-4
            py-8
            border-b border-gray-200
            sm:px-6
            rounded-lg
            grid grid-cols-1
            gap-y-6 gap-x-4
        "
    >
        <overtime
            :initial="overtime"
            :onUpdate="handleOvertimeChange"
        ></overtime>
        <task-description-filter
            v-model="description"
        ></task-description-filter>
    </div>
</template>

<script>
import Overtime from '../../forms/Overtime.vue'
import TaskDescriptionFilter from '../../forms/TaskDescription.vue'
import { mapActions, mapState } from 'vuex'
export default {
    components: {
        Overtime,
        TaskDescriptionFilter,
    },
    data() {
        return {
            description: '',
        }
    },
    watch: {
        description(value) {
            if (!value || !(typeof value === 'object')) {
                this.setTaskDescriptionFilter(null)
                return
            }
            const [_, description] = value
            this.setTaskDescriptionFilter(description)
        },
    },
    computed: {
        ...mapState({
            overtime: (state) => state.filters.overtime,
            taskDescritpion: (state) => state.filters.taskDescritpion,
        }),
    },
    methods: {
        ...mapActions([
            'setFocalPointFilter',
            'setOvertimeFilter',
            'setTaskDescriptionFilter',
        ]),
        handleOvertimeChange(option) {
            this.setOvertimeFilter(option.value)
        },
    },
}
</script>

<style></style>
