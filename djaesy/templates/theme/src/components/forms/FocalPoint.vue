<template>
    <Listbox as="div" v-model="selectedFocalPoint">
        <ListboxLabel class="block text-sm font-medium text-gray-700">
            Focal Point
        </ListboxLabel>
        <div class="mt-1 relative">
            <ListboxButton
                class="
                    relative
                    w-full
                    bg-white
                    border border-gray-300
                    rounded-md
                    shadow-sm
                    pl-3
                    pr-10
                    py-2
                    text-left
                    cursor-default
                    focus:outline-none
                    focus:ring-1
                    focus:ring-teal-500
                    focus:border-teal-500
                    sm:text-sm
                "
            >
                <span class="flex items-center" v-if="selectedFocalPoint">
                    <img
                        :src="selectedFocalPoint.avatar"
                        alt=""
                        class="flex-shrink-0 h-6 w-6 rounded-full"
                    />
                    <span class="ml-3 block truncate">{{
                        selectedFocalPoint.name
                    }}</span>
                </span>
                <span
                    class="
                        ml-3
                        absolute
                        inset-y-0
                        right-0
                        flex
                        items-center
                        pr-2
                        pointer-events-none
                    "
                >
                    <SelectorIcon
                        class="h-5 w-5 text-gray-400"
                        aria-hidden="true"
                    />
                </span>
            </ListboxButton>

            <transition
                leave-active-class="transition ease-in duration-100"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
            >
                <ListboxOptions
                    class="
                        absolute
                        z-10
                        mt-1
                        w-full
                        bg-white
                        shadow-lg
                        max-h-56
                        rounded-md
                        py-1
                        text-base
                        ring-1 ring-black ring-opacity-5
                        overflow-auto
                        focus:outline-none
                        sm:text-sm
                    "
                >
                    <ListboxOption
                        as="template"
                        v-for="person in people"
                        :key="person.id"
                        :value="person"
                        v-slot="{ active, selectedFocalPoint }"
                    >
                        <li
                            :class="[
                                active
                                    ? 'text-white bg-teal-600'
                                    : 'text-gray-900',
                                'cursor-default select-none relative py-2 pl-3 pr-9',
                            ]"
                        >
                            <div class="flex items-center">
                                <img
                                    :src="person.avatar"
                                    alt=""
                                    class="flex-shrink-0 h-6 w-6 rounded-full"
                                />
                                <span
                                    :class="[
                                        selectedFocalPoint
                                            ? 'font-semibold'
                                            : 'font-normal',
                                        'ml-3 block truncate',
                                    ]"
                                >
                                    {{ person.name }}
                                </span>
                            </div>

                            <span
                                v-if="selectedFocalPoint"
                                :class="[
                                    active ? 'text-white' : 'text-teal-600',
                                    'absolute inset-y-0 right-0 flex items-center pr-4',
                                ]"
                            >
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </div>
    </Listbox>
</template>

<script>
import people from '../../store/people' //TODO: fetch from API
import {
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
} from '@headlessui/vue'
import { CheckIcon, SelectorIcon } from '@heroicons/vue/solid'

export default {
    props: ['modelValue'],
    emits: ['update:modelValue'],

    components: {
        Listbox,
        ListboxButton,
        ListboxLabel,
        ListboxOption,
        ListboxOptions,
        CheckIcon,
        SelectorIcon,
    },
    data() {
        return {
            people,
            selectedFocalPoint: people[0],
        }
    },
    watch: {
        selectedFocalPoint(value) {
            this.$emit('update:modelValue', value)
        },
        modelValue(value) {
            if (value !== this.selectedFocalPoint)
                this.selectedFocalPoint = value
        },
    },
    mounted() {
        if (this.modelValue) this.selectedFocalPoint = this.modelValue
    },
}
</script>
