<template>
  <a href="#" class="flex-shrink-0 group block">
    <div class="flex items-center">
      <div>
        <img class="inline-block h-9 w-9 rounded-full" :src="avatar" :alt="name" />
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900">
          {{ name }}
        </p>
        <p class="text-xs font-medium text-gray-500 group-hover:text-gray-700">
          {{ email }}
        </p>
      </div>
    </div>
  </a>
</template>
<script>

export default {
    props: ['name', 'email', 'avatar'],
}
</script>
