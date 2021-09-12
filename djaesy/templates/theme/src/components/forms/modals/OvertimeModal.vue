<template>
    <TransitionRoot appear :show="isOpen" as="template">
        <Dialog as="div" @close="closeModal">
            <div class="fixed inset-0 z-10 overflow-y-auto">
                <div class="min-h-screen px-4 text-center">
                    <TransitionChild
                        as="template"
                        enter="duration-300 ease-out"
                        enter-from="opacity-0"
                        enter-to="opacity-100"
                        leave="duration-200 ease-in"
                        leave-from="opacity-100"
                        leave-to="opacity-0"
                    >
                        <DialogOverlay
                            class="fixed inset-0 bg-black opacity-30"
                        />
                    </TransitionChild>

                    <span
                        class="inline-block h-screen align-middle"
                        aria-hidden="true"
                    >
                        &#8203;
                    </span>

                    <TransitionChild
                        as="template"
                        enter="duration-300 ease-out"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="duration-200 ease-in"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <div
                            class="
                                inline-block
                                w-full
                                max-w-md
                                p-6
                                my-8
                                overflow-hidden
                                text-left
                                align-middle
                                transition-all
                                transform
                                bg-white
                                shadow-xl
                                rounded-2xl
                            "
                        >
                            <DialogTitle
                                as="h3"
                                class="
                                    text-lg
                                    font-medium
                                    leading-6
                                    mb-5
                                    text-gray-900
                                "
                            >
                                Overtime: your hours exceed the assigned amount
                            </DialogTitle>
                            <div class="mt-4">
                                <overtime-type
                                    v-model:overtimeType="selectedOvertimeType"
                                ></overtime-type>
                                <label
                                    for="overtimeReason"
                                    class="
                                        block
                                        text-sm
                                        font-medium
                                        mt-2
                                        text-gray-700
                                    "
                                >
                                    Overtime Reason
                                </label>
                                <div class="mt-1">
                                    <el-input
                                        name="overtimeReason"
                                        id="overtimeReason"
                                        placeholder="Type the overtime reason"
                                        v-model="selectedOvertimeReason"
                                        clearable
                                    >
                                    </el-input>
                                </div>
                            </div>

                            <div class="mt-4 flex justify-end">
                                <cancel-button @click="closeModal"
                                    >Cancel</cancel-button
                                >
                                <submit-button @click="onConfirm"
                                    >Confirm Overtime</submit-button
                                >
                            </div>
                        </div>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script>
import { ref, watch } from 'vue'
import OvertimeType from '../OvertimeType.vue'
import SubmitButton from '../SubmitButton.vue'
import CancelButton from '../CancelButton.vue'
import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogOverlay,
    DialogTitle,
} from '@headlessui/vue'

export default {
    components: {
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogOverlay,
        DialogTitle,
        OvertimeType,
        SubmitButton,
        CancelButton,
    },
    props: ['isOpen', 'overtimeType', 'overtimeReason', 'onConfirm'],
    emits: ['update:isOpen', 'update:overtimeType', 'update:overtimeReason'],
    setup(props, { emit }) {
        const selectedOvertimeType = ref(props.overtimeType)
        const selectedOvertimeReason = ref(props.overtimeReason)

        watch(selectedOvertimeType, (value) => {
            emit('update:overtimeType', value)
        })
        watch(selectedOvertimeReason, (value) => {
            emit('update:overtimeReason', value)
        })

        return {
            selectedOvertimeType,
            selectedOvertimeReason,
            closeModal() {
                emit('update:isOpen', false)
            },
        }
    },
}
</script>
