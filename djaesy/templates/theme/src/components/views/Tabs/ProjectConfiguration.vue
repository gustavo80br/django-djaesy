<template>
    <div>
        <div class="px-4 py-5">
            <form class="space-y-6" action="#" method="POST">
                <div class="grid grid-cols-1 gap-6">
                    <focal-point v-model.sync="focalPoint"></focal-point>
                    <task-description v-model="description"></task-description>
                    <time-period v-model="timePeriod"></time-period>
                    <sort-results v-model="sortResults"></sort-results>
                </div>
            </form>
        </div>
    </div>
    <div class="px-4 py-3 bg-gray-50 text-right sm:px-6 rounded-b-lg">
        <submit-button @click="save">Save</submit-button>
    </div>
</template>

<script>
import FocalPoint from '../../forms/FocalPoint.vue'
import TaskDescription from '../../forms/TaskDescription.vue'
import TimePeriod from '../../forms/TimePeriod.vue'
import SortResults from '../../forms/SortResults.vue'
import SubmitButton from '../../forms/SubmitButton.vue'
import { mapState, mapActions } from 'vuex'
import people from '../../../store/people'

export default {
    components: {
        FocalPoint,
        TaskDescription,
        TimePeriod,
        SortResults,
        SubmitButton,
    },
    data() {
        return {
            focalPoint: people[0],
            description: '',
            timePeriod: null,
            sortResults: null,
        }
    },
    watch: {
        selectedProject() {
            this.initProjectDefault()
        },
    },
    computed: {
        ...mapState({
            selectedProject: (state) => state.filters.project,
            projectDefaults: (state) => state.projectDefaults,
            descriptions: (state) => state.descriptions,
        }),
    },
    methods: {
        ...mapActions(['search', 'setProjectDefault']),
        save() {
            const project = {
                id: this.selectedProject.id,
                focalPoint: this.focalPoint,
                description: this.description,
                sortResults: this.sortResults,
                timePeriod: this.timePeriod,
            }
            this.setProjectDefault(project)
            this.$notify({
                title: 'Succesfully saved!',
                message: 'Project preferences has been updated',
                type: 'success'
              });
        },
        initProjectDefault() {
            const projectDefault = this.projectDefaults.get(
                this.selectedProject.id
            )
            if (projectDefault) {
                this.focalPoint = projectDefault.focalPoint
                this.sortResults = projectDefault.sortResults
                this.timePeriod = projectDefault.timePeriod
                this.description = projectDefault.description
            }
        },
    },
    mounted() {
        this.initProjectDefault()
    },
}
</script>
