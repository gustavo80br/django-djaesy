<template>
    <Listbox as="div" v-model="selected">
        <ListboxLabel class="block text-sm font-medium text-gray-700">
            Results order
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
                <span class="block truncate">{{ selected.name }}</span>
                <span
                    class="
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
                        max-h-60
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
                        v-for="option in sortingOptions"
                        :key="option.id"
                        :value="option"
                        v-slot="{ active, selected }"
                    >
                        <li
                            :class="[
                                active
                                    ? 'text-white bg-teal-600'
                                    : 'text-gray-900',
                                'cursor-default select-none relative py-2 pl-8 pr-4',
                            ]"
                        >
                            <span
                                :class="[
                                    selected ? 'font-semibold' : 'font-normal',
                                    'block truncate',
                                ]"
                            >
                                {{ option.name }}
                            </span>

                            <span
                                v-if="selected"
                                :class="[
                                    active ? 'text-white' : 'text-teal-600',
                                    'absolute inset-y-0 left-0 flex items-center pl-1.5',
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
import {
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
} from '@headlessui/vue'
import { CheckIcon, SelectorIcon } from '@heroicons/vue/solid'
import { sortingOptions } from '../../constants/sorting'

export default {
    components: {
        Listbox,
        ListboxButton,
        ListboxLabel,
        ListboxOption,
        ListboxOptions,
        CheckIcon,
        SelectorIcon,
    },
    props: ['modelValue'],
    emit: ['update:modelValue'],
    data() {
        return {
            selected: sortingOptions[0],
            sortingOptions,
        }
    },
    watch: {
        selected(value) {
            this.$emit('update:modelValue', value)
        },
        modelValue(value) {
            if (value !== this.selected) this.selected = value
        },
    },
    mounted() {
        if (this.modelValue) {
            this.selected = this.modelValue
        } else {
            this.$emit('update:modelValue', this.selected)
        }
    },
}
</script>
