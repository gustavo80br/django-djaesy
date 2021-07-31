<template>
  <TransitionRoot
    appear
    :show="isOpen"
    as="template"
  >
    <Dialog
      as="div"
      @close="closeModal"
    >
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
            <DialogOverlay class="fixed inset-0 bg-black opacity-30" />
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
            <div class="
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
                            ">
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
                Duplicate: select a date to duplicate the task
              </DialogTitle>
              <div class="mt-4">
                <label
                  for="duplicateTo"
                  class="
                                        block
                                        text-sm
                                        font-medium
                                        mt-2
                                        text-gray-700
                                    "
                >
                  Date to duplicate this task to
                </label>
                <div class="mt-1">
                  <el-date-picker
                    name="duplicateTo"
                    class="
                                shadow-sm
                                focus:ring-sky-500 focus:border-sky-500
                                block
                                w-full
                                sm:text-sm
                                border-gray-300
                                rounded-md
                            "
                    v-model="selectedDuplicateTo"
                    type="date"
                    placeholder="Pick a day"
                  >
                  </el-date-picker>
                </div>
              </div>

              <div class="mt-4 flex justify-end">
                <cancel-button @click="closeModal">Cancel</cancel-button>
                <submit-button @click="onConfirm">Confirm Duplicate</submit-button>
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
        SubmitButton,
        CancelButton,
    },
    props: ['isOpen', 'duplicateTo', 'onConfirm'],
    emits: ['update:isOpen', 'update:duplicateTo'],
    setup(props, { emit }) {
        const selectedDuplicateTo = ref(props.duplicateTo)

        watch(selectedDuplicateTo, (value) => {
            emit('update:duplicateTo', value)
        })

        return {
            selectedDuplicateTo,
            closeModal() {
                emit('update:isOpen', false)
            },
        }
    },
}
</script>
