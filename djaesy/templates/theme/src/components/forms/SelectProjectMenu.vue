<template>
    <div class="flex items-center w-full">
        <div class="flex-1">
            <Listbox
                as="div"
                :modelValue="selectedProject"
                @update:modelValue="setProject($event)"
            >
                <ListboxLabel class="sr-only">
                    Change selected project
                </ListboxLabel>
                <div class="relative">
                    <div
                        class="
                            inline-flex
                            w-full
                            shadow-sm
                            rounded-md
                            divide-x divide-sky-600
                        "
                    >
                        <div
                            class="
                                relative
                                w-full
                                z-0
                                inline-flex
                                shadow-sm
                                rounded-md
                                divide-x divide-sky-600
                            "
                        >
                            <div
                                class="
                                    relative
                                    w-full
                                    inline-flex
                                    items-center
                                    bg-sky-500
                                    py-2
                                    pl-3
                                    pr-4
                                    border border-transparent
                                    rounded-l-md
                                    shadow-sm
                                    text-white
                                "
                            >
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                <p class="ml-2.5 text-md font-medium">
                                    {{ selectedProject.name }}
                                </p>
                            </div>
                            <ListboxButton
                                class="
                                    relative
                                    inline-flex
                                    items-center
                                    bg-sky-500
                                    p-2
                                    rounded-l-none rounded-r-md
                                    text-sm
                                    font-medium
                                    text-white
                                    hover:bg-sky-600
                                    focus:outline-none
                                    focus:z-10
                                    focus:ring-2
                                    focus:ring-offset-2
                                    focus:ring-offset-gray-50
                                    focus:ring-sky-500
                                "
                            >
                                <span class="sr-only"
                                    >Change selected project</span
                                >
                                <ChevronDownIcon
                                    class="h-5 w-5 text-white"
                                    aria-hidden="true"
                                />
                            </ListboxButton>
                        </div>
                    </div>

                    <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                    >
                        <ListboxOptions
                            class="
                                origin-top-right
                                absolute
                                z-10
                                right-0
                                mt-2
                                w-full
                                rounded-md
                                shadow-lg
                                overflow-hidden
                                bg-white
                                divide-y divide-gray-200
                                ring-1 ring-black ring-opacity-5
                                focus:outline-none
                            "
                        >
                            <ListboxOption
                                as="template"
                                v-for="project in projects"
                                :key="project.id"
                                :value="project"
                                v-slot="{ active, selected }"
                            >
                                <li
                                    :class="[
                                        active
                                            ? 'text-white bg-sky-500'
                                            : 'text-gray-900',
                                        'cursor-pointer select-none relative p-4 text-sm',
                                    ]"
                                >
                                    <div class="flex flex-col">
                                        <div class="flex justify-between">
                                            <p
                                                :class="
                                                    selected
                                                        ? 'font-semibold'
                                                        : 'font-normal'
                                                "
                                            >
                                                {{ project.name }}
                                            </p>
                                            <span
                                                v-if="selected"
                                                :class="
                                                    active
                                                        ? 'text-white'
                                                        : 'text-sky-500'
                                                "
                                            >
                                                <CheckIcon
                                                    class="h-5 w-5"
                                                    aria-hidden="true"
                                                />
                                            </span>
                                        </div>

                                    </div>
                                </li>
                            </ListboxOption>
                        </ListboxOptions>
                    </transition>
                </div>
            </Listbox>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

import {
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
} from '@headlessui/vue'
import { CheckIcon, ChevronDownIcon } from '@heroicons/vue/solid'

const all = {
    id: 0,
    name: 'All Projects',
    description:
        'This option allows you to work and visualize all your assigned projects.',
}
export default {
    components: {
        Listbox,
        ListboxButton,
        ListboxLabel,
        ListboxOption,
        ListboxOptions,
        CheckIcon,
        ChevronDownIcon,
    },
    computed: {
        ...mapState({
            selectedProject: (state) => state.filters.project || all,
            projects: (state) => {
                if(!state.actAsPM) return [all, ...state.projects]
                else return state.projects
                },
        }),
    },
    methods: {
        ...mapActions(['setProject']),
    },
}
</script>
