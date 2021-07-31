<template>
  <div class="space-y-4">
    <div
      v-for="(stat, index) in stats"
      :key="index"
      class="bg-white shadow overflow-hidden rounded-lg"
    >
      <div class="pl-5 pt-2 text-primary">{{ stat.category }}</div>
      <div class="py-3 flex border-b items-center">
        <div class="px-3">
          <i class="fad fa-stopwatch fa-3x text-secondary"></i>
        </div>
        <div>
          <p class="text-base font-normal text-gray-900 truncate">{{ stat.title }}</p>
          <p class="text-2xl font-semibold text-primary">
            {{ stat.expected }}
          </p>
          <p class="text-sm font-normal text-gray-900 truncate">{{ stat.subtitle }}</p>
          <div class="flex items-baseline">
            <p class="text-2xl font-semibold text-primary">
              {{ stat.todate }}
            </p>
            <span class="ml-2 text-sm font-medium text-gray-500"> of {{ stat.totaltodate }},</span>
            <p v-if="stat.overtime" class="text-green-600 ml-2 flex items-baseline text-sm font-semibold">
              overtime of {{ stat.overtime }}
            </p>
            <p v-if="stat.missing" class="text-red-600 ml-2 flex items-baseline text-sm font-semibold">
              missing {{ stat.missing }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>


</template>

<script>
import { ArrowSmDownIcon, ArrowSmUpIcon } from '@heroicons/vue/solid'

export default {
    components: {
        ArrowSmDownIcon,
        ArrowSmUpIcon,
    },
    setup() {
        return {
            stats: [
                {
                    category: 'All projects',
                    title: 'Monthly expected hours',
                    expected: '160h',
                    subtitle: 'Monthly worked to date',
                    todate: '12h 30m',
                    totaltodate: '16h',
                    overtime: '',
                    missing: '1h',
                },
                {
                    category: 'BairesDev New Time Tracker',
                    title: 'Monthly expected hours',
                    expected: '80h',
                    subtitle: 'Monthly worked to date',
                    todate: '4h 30m',
                    totaltodate: '8h',
                    overtime: '',
                    missing: '1h',
                },
                {
                    category: 'Another Project to Change the World',
                    title: 'Monthly expected hours',
                    expected: '80h',
                    subtitle: 'Monthly worked to date',
                    todate: '4h 30m',
                    totaltodate: '8h',
                    overtime: '1h',
                    missing: '',
                },
            ],
            title: 'Monthly expected hours to date',
            value: '132h 30m',
            expected: '136h',
            behind: '3h 30m',
            change: '122',
            changeType: 'increase',
            items: [{ id: 1 }, { id: 2 }],
        }
    },
}
</script>
