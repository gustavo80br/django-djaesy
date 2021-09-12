<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 w-full">
    <div class="flex">
      <div class="flex-shrink-0">
        <InformationCircleIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
      </div>
      <div class="ml-3 flex-1 md:flex md:justify-between">
        <p class="text-sm text-yellow-700">
            {{ message }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { InformationCircleIcon } from '@heroicons/vue/solid'

export default {
  components: {
    InformationCircleIcon,
  },
  props:{
    message:{
      default: 'Displaying consolidated information. To add a new time record, you need to select a project from the dropdown.',
    }
  },
}
</script>
