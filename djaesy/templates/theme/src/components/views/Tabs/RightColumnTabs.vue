<template>
    <div class="rounded-lg shadow">
        <div class="bg-white rounded-lg">
            <div>
                <div class="sm:hidden">
                    <label for="tabs" class="sr-only">Select a tab</label>
                    <select
                        id="tabs"
                        name="tabs"
                        class="
                            block
                            w-full
                            focus:ring-indigo-500 focus:border-indigo-500
                            border-gray-300
                            rounded-md
                        "
                    >
                        <option
                            v-for="tab in tabs"
                            :key="tab.name"
                            :selected="tab.current"
                        >
                            {{ tab.name }}
                        </option>
                    </select>
                </div>
                <div class="hidden sm:block">
                    <div class="border-b border-gray-200">
                        <nav class="-mb-px flex">
                            <a
                                v-for="tab in tabs"
                                @click.prevent="selectTab(tab)"
                                :key="tab.name"
                                :href="tab.href"
                                :class="[
                                    tab.current
                                        ? 'border-teal-500 text-teal-600'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                                    'w-1/3 py-4 px-1 text-center border-b-2 font-medium text-lg',
                                ]"
                            >
                                {{ tab.name }}
                            </a>
                        </nav>
                    </div>
                </div>
            </div>
            <new-time-record
                v-if="selectedTab == 'new'"
                @record:saved="handleRecordSaved"
            ></new-time-record>
            <project-configuration
                v-else-if="selectedTab == 'project'"
            ></project-configuration>
            <additional-filters
                v-else-if="selectedTab == 'search'"
            ></additional-filters>
            <submit-report v-else-if="selectedTab == 'report'"></submit-report>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import AdditionalFilters from './AdditionalFilters.vue'
import ProjectConfiguration from './ProjectConfiguration.vue'
import NewTimeRecord from './NewTimeRecord.vue'
import SubmitReport from './SubmitReport.vue'

export default {
    components: {
        NewTimeRecord,
        AdditionalFilters,
        ProjectConfiguration,
        SubmitReport,
    },
    emits: ['record:saved'],
    data() {
        return {
            tabs: [
                { name: 'Track', href: 'new', current: true },
                { name: 'Search', href: 'search', current: false },
                { name: 'Report', href: 'report', current: false },
                { name: 'Setup', href: 'project', current: false },
            ],
            selectedTab: 'new',
        }
    },
    computed: {
        ...mapState({
            editing: (state) => state.editing,
        }),
    },
    watch: {
        editing(value) {
            if (value) {
                this.selectTab(this.tabs[0])
                this.tabs[0].name = 'Edit'
            } else this.tabs[0].name = 'Track'
        },
    },
    methods: {
        handleRecordSaved() {
            this.$emit('record:saved')
        },
        selectTab(selected) {
            this.selectedTab = selected.href
            this.tabs.forEach(function (tab) {
                if (tab.href == selected.href) tab.current = true
                else tab.current = false
            })
        },
    },
}
</script>
