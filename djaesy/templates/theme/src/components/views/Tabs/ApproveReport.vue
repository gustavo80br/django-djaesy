<template>
  <div class="rounded-lg shadow">
    <div class="bg-white rounded-lg grid grid-cols-1 gap-4">
      <div class="px-4 py-5 ">
        Select a User
        <select-user-menu></select-user-menu>
      </div>
      <div class="border-t px-4 py-5">
        <div class="text-sm text-gray-700 mb-4">Here are the available reports for the selected user. <br> Select one to view the details.</div>

        <RadioGroup v-model="selected">
          <div class="space-y-4">
            <RadioGroupOption
              as="template"
              v-for="report in reports"
              :key="report.project"
              :value="report"
              v-slot="{ active, checked }"
            >
              <div :class="[active ? 'ring-1 ring-offset-2 ring-teal-500' : '', 'relative block rounded-lg border border-gray-300 bg-white shadow-sm px-6 py-4 cursor-pointer hover:border-gray-400 sm:flex sm:justify-between focus:outline-none']">
                <div class="flex items-center">
                  <div class="text-sm">
                    <RadioGroupLabel
                      as="p"
                      class="font-medium text-gray-900"
                    >
                      {{ projects.filter((item)=>report.project == item.id)[0].name }}
                    </RadioGroupLabel>
                    <RadioGroupDescription
                      as="div"
                      class="text-gray-500"
                    >
                      <span v-if="report.status=='approved'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Approved
                      </span>
                      <span v-if="report.status=='rejected'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        Rejected
                      </span>
                      <span v-if="report.status=='submitted'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        Submitted
                      </span>
                      <span v-if="report.status=='working'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-sky-100 text-sky-800">
                        Working on
                      </span>
                      {{ ' ' }}
                      <p class="sm:inline">{{ report.month }}</p>
                    </RadioGroupDescription>
                  </div>
                </div>
                <RadioGroupDescription
                  as="div"
                  class="mt-2 flex text-sm sm:mt-0 sm:block sm:ml-4 sm:text-right"
                >
                  <div class="font-medium text-gray-900">{{ report.hours }}h</div>
                  <div class="ml-1 text-gray-500 sm:ml-0" v-if="report.overtime">{{ report.overtime }} <span class="text-red-800">OT</span> </div>
                </RadioGroupDescription>
                <div
                  :class="[checked ? 'border-teal-500' : 'border-transparent', 'absolute -inset-px rounded-lg border-2 pointer-events-none']"
                  aria-hidden="true"
                />
              </div>
            </RadioGroupOption>
          </div>
        </RadioGroup>
      </div>
    </div>
  </div>
</template>


<script>
import SelectUserMenu from '../../forms/SelectUserMenu.vue'
import {
    RadioGroup,
    RadioGroupDescription,
    RadioGroupLabel,
    RadioGroupOption,
} from '@headlessui/vue'

import { mapState } from 'vuex'

export default {
    emits: ['change'],
    components: {
        SelectUserMenu,
        RadioGroup,
        RadioGroupDescription,
        RadioGroupLabel,
        RadioGroupOption,
    },
    data() {
        return {
            selected: null,
        }
    },
    computed: {
        ...mapState({
            projects: (state) => state.projects,
            reports: (state) => state.reports,
        }),
    },
    watch: {
        selected(value) {
            this.$emit('change', value)
        },
    }
}
</script>
