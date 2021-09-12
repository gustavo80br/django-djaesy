<template>
    <Listbox as="div" v-model="selectedOption">
        <ListboxLabel class="block text-sm font-medium text-gray-700">
            Time record type
        </ListboxLabel>
        <div class="relative mt-1">
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
                <span class="block truncate">{{ selectedOption.name }}</span>
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
                        class="w-5 h-5 text-gray-400"
                        aria-hidden="true"
                    />
                </span>
            </ListboxButton>

            <transition
                leave-active-class="transition duration-100 ease-in"
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
                        v-slot="{ active, selected }"
                        v-for="option in options"
                        :key="option.name"
                        :value="option"
                        as="template"
                    >
                        <li
                            :class="[
                                active
                                    ? 'text-white bg-teal-600'
                                    : 'text-gray-900',
                                'cursor-default select-none relative py-2 pl-3 pr-9',
                            ]"
                        >
                            <span
                                :class="[
                                    selected ? 'font-medium' : 'font-normal',
                                    'ml-6 block truncate',
                                ]"
                                >{{ option.name }}</span
                            >
                            <span
                                v-if="selected"
                                class="
                                    absolute
                                    inset-y-0
                                    left-0
                                    flex
                                    items-center
                                    pl-3
                                    text-amber-600
                                "
                            >
                                <CheckIcon class="w-5 h-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </div>
    </Listbox>
</template>

<script>
import { ref, watch } from 'vue'
import {
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOptions,
    ListboxOption,
} from '@headlessui/vue'
import { CheckIcon, SelectorIcon } from '@heroicons/vue/solid'

export default {
    components: {
        Listbox,
        ListboxButton,
        ListboxLabel,
        ListboxOptions,
        ListboxOption,
        CheckIcon,
        SelectorIcon,
    },
    props: ['initial', 'onUpdate'],
    setup(props) {
        const options = [
            { name: 'All', value: null },
            { name: 'Overtime', value: true },
            { name: 'Regular Hour', value: false },
        ]
        const selectedOption = ref(props.initial || options[0])

        watch(selectedOption, (value) => {
            props.onUpdate(value)
        })

        return {
            options,
            selectedOption,
        }
    },
}
</script>
