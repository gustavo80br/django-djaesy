<template>
    <div>
        <label
            for="description"
            class="block text-sm font-medium text-gray-700"
        >
            Task Description
        </label>
        <div class="mt-1">
            <el-cascader
                :model-value="modelValue"
                @change="update"
                class="w-full"
                placeholder="Select task category and description"
                :options="descriptions"
                :props="{ expandTrigger: 'hover' }"
                clearable
                filterable
            ></el-cascader>
        </div>
    </div>
</template>

<script>

import { mapState } from 'vuex'
export default {
    props: ['modelValue'],
    emits: ['update:modelValue'],
    data() {
        return {
        }
    },
    computed: {
        ...mapState({
            descriptions: (state) => state.descriptions,
        }),
    },
    methods:{
        update(val){
            this.$emit('update:modelValue', val)
        }
    }
}
</script>
