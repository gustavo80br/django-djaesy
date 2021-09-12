<template>
  <button
    type="submit"
    :disabled="disabled"
    @click="$emit('click')"
    class="
        inline-flex
                justify-center
                py-2
                px-4
                border border-transparent
                shadow-sm
                text-sm
                font-medium
                rounded-md
                text-white
                bg-gray-600
                hover:bg-gray-700
                focus:outline-none
                focus:ring-2
                focus:ring-offset-2
                focus:ring-gray-500
                disabled:opacity-50 disabled:cursor-not-allowed
                mr-2
    "
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
    },
    emits: ['click'],
}
</script>
