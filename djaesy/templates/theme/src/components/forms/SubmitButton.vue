<template>
  <button
    type="submit"
    :disabled="disabled"
    @click="$emit('click')"
    :class="[type == 'danger'?'bg-red-600 hover:bg-red-700 focus:ring-red-500':'bg-teal-600 hover:bg-teal-700 focus:ring-teal-500',
      'mr-2 inline-flex items-center justify-center py-2 px-4 border border-transparent shadow-sm text-md',
      'font-medium rounded-md text-white focus:outline-none focus:ring-2',
      'focus:ring-offset-2  disabled:opacity-50 disabled:cursor-not-allowed']"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
    props: {
        disabled: {
            default: false,
        },
        type: {
            default: 'success',
        },
    },
    emits: ['click'],
}
</script>
