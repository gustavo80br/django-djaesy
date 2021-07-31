<template>
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
            <div class="shadow border-b border-gray-200 sm:rounded-lg bg-white dark:bg-primary border dark:border-sky-600 ">
                <div class="p-4">
                    <time-period-filter ref="time-period-filter"></time-period-filter>
                </div>
                <table class="min-w-full divide-y divide-gray-200 dark:divide-sky-600">
                    <thead class="bg-sky-50 dark:bg-sky-900">
                        <tr>
                            <th class="pl-4">
                                <div class="flex items-center h-5">
                                    <input
                                        v-model="selectAll"
                                        @change="toggleSelectAll"
                                        id="select-all"
                                        name="select-all"
                                        type="checkbox"
                                        class="focus:ring-teal-500 h-4 w-4 text-teal-600 border-gray-300 rounded"
                                    />
                                </div>
                            </th>
                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-right text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                "
                            >
                                Date
                            </th>
                            <th
                                scope="col"
                                class="
                                    py-3
                                    text-right text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                    w-1
                                "
                            >
                                <el-tooltip
                                    class="item"
                                    effect="dark"
                                    content="Overtime hours"
                                    placement="top-start"
                                >
                                    <span>Hours</span>
                                </el-tooltip>
                            </th>
                            <th v-if="!selectedProject" class="
                                    px-6
                                    py-3
                                    text-left text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                ">Project</th>
                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-left text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                "
                            >
                                Category
                            </th>
                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-left text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                "
                            >
                                Comments
                            </th>
                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-left text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                "
                            >
                                Focal Point
                            </th>
                            <th
                                class="
                                    pr-6
                                    py-3
                                    text-right text-xs
                                    font-medium
                                    text-gray-500 dark:text-gray-50
                                    uppercase
                                    tracking-wider
                                "
                            />
                        </tr>
                    </thead>
                    <transition-group tag="tbody" class="bg-white divide-y divide-gray-200 dark:bg-gray-600 dark:divide-gray-500"
                        enter-active-class="transition ease-out duration-700"
                        enter-from-class="transform opacity-0 scale-y-0"
                        enter-to-class="transform opacity-100 scale-y-100"
                        leave-active-class="transition ease-in duration-700"
                        leave-from-class="transform opacity-100 scale-y-100"
                        leave-to-class="transform opacity-0 scale-y-0"
                        move-class="transition ease-out duration-500"
                    >
                        <tr v-if="tasks.length == 0">
                            <td colspan="7" class="px-4 py-5">
                                <div class="text-center w-full text-gray-500 dark:text-gray-50 text-sm">
                                    <img src="../../assets/empty.svg" alt="No records found" class="h-72 mx-auto opacity-50">
                                    <span class="text-teal-500"> Sorry! No records where found.</span> <br> Try changing some filters.
                                </div>

                            </td>
                        </tr>
                        <tr v-else
                            v-for="(task, index) in tasks"
                            :key="task.id"
                            :class="[
                                task.selected ? 'bg-teal-50 dark:bg-teal-800' : '',
                                'cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900',
                            ]"
                        >
                            <td
                                @click="task.selected = !task.selected"
                                class="pl-4"
                            >
                                <div class="flex items-center h-5">
                                    <input
                                        :id="'task[' + index + ']'"
                                        :name="'task[' + index + ']'"
                                        type="checkbox"
                                        class="
                                            focus:ring-teal-500
                                            h-4
                                            w-4
                                            text-teal-600
                                            border-gray-300
                                            rounded
                                        "
                                        :checked="task.selected"
                                    />
                                </div>
                            </td>
                            <td
                                @click="task.selected = !task.selected"
                                class="px-6 py-2 whitespace-nowrap"
                            >
                                <div class="text-right">
                                    <div
                                        class="
                                            text-sm
                                            font-medium
                                            text-gray-400 dark:text-gray-100
                                        "
                                    >
                                        {{ task.date.toLocaleDateString() }}
                                    </div>
                                </div>
                            </td>
                            <td
                                @click="task.selected = !task.selected"
                                class="py-2 whitespace-nowrap text-right"
                            >
                                <div class="text-primary dark:text-sky-100 text-sm font-bold">
                                    <el-tooltip
                                        v-if="task.overtime || task.date.toLocaleDateString() == '7/5/2021'"
                                        class="item"
                                        effect="dark"
                                        content="Overtime"
                                        placement="top"
                                    >
                                        <span v-if="task.date.toLocaleDateString() == '7/5/2021'" class="text-purple-600 dark:text-purple-200 mr-2">HOL</span>
                                        <span v-else class="text-yellow-600 dark:text-yellow-200 mr-2">OT</span>
                                    </el-tooltip>
                                    {{ task.hours }}
                                </div>
                            </td>
                            <td v-if="!selectedProject" class="px-6 py-2 text-sm text-gray-900 dark:text-gray-100">
                                {{ projects.filter((item)=>item.id ==task.project.id )[0].name }}
                            </td>
                            <td
                                @click="task.selected = !task.selected"
                                class="px-6 py-2 whitespace-nowrap"
                            >
                                <div class="text-sm text-gray-900 dark:text-gray-100">
                                    {{
                                        getTaskCategoryByDescription(
                                            task.taskDescription
                                        )
                                    }}
                                </div>
                                <div class="text-sm text-gray-500 dark:text-gray-300">
                                    {{ task.taskDescription }}
                                </div>
                            </td>
                            <td
                                @click="task.selected = !task.selected"
                                class="px-6 py-4 whitespace-nowrap"
                            >
                                <div class="text-sm text-gray-500 dark:text-gray-100">
                                    {{ task.comments }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <a href="#" class="flex-shrink-0 group block">
    <div class="flex items-center">
      <div>
        <img class="inline-block h-8 w-8 rounded-full" :src="task.focalPoint.avatar" :alt="task.focalPoint.name" />
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-gray-900">
          {{ task.focalPoint.name }}
        </p>
      </div>
    </div>
  </a>

                            </td>
                            <td class="pr-6">
                                <Menu
                                    as="div"
                                    class="
                                        relative
                                        flex
                                        justify-end
                                        items-center
                                    "
                                >
                                    <MenuButton
                                        class="
                                            w-8
                                            h-8
                                            bg-white dark:bg-gray-700
                                            inline-flex
                                            items-center
                                            justify-center
                                            text-gray-400
                                            rounded-full
                                            hover:text-gray-500
                                            focus:outline-none
                                            focus:ring-2
                                            focus:ring-offset-2
                                            focus:ring-teal-500
                                        "
                                    >
                                        <span class="sr-only"
                                            >Open options</span
                                        >
                                        <DotsVerticalIcon
                                            class="w-5 h-5"
                                            aria-hidden="true"
                                        />
                                    </MenuButton>
                                    <transition
                                        enter-active-class="transition ease-out duration-100"
                                        enter-from-class="transform opacity-0 scale-95"
                                        enter-to-class="transform opacity-100 scale-100"
                                        leave-active-class="transition ease-in duration-75"
                                        leave-from-class="transform opacity-100 scale-100"
                                        leave-to-class="transform opacity-0 scale-95"
                                    >
                                        <MenuItems
                                            class="
                                                mx-3
                                                origin-top-right
                                                absolute
                                                right-7
                                                top-0
                                                w-48
                                                mt-1
                                                rounded-md
                                                shadow-lg
                                                z-10
                                                bg-white
                                                ring-1 ring-black ring-opacity-5
                                                divide-y divide-gray-200
                                                focus:outline-none
                                            "
                                        >
                                            <div class="py-1">
                                                <MenuItem v-slot="{ active }">
                                                    <a
                                                        href="#"
                                                        @click="
                                                            onEditClick(task)
                                                        "
                                                        :class="[
                                                            active
                                                                ? 'bg-gray-100 text-gray-900'
                                                                : 'text-gray-700',
                                                            'group flex items-center px-4 py-2 text-sm',
                                                        ]"
                                                    >
                                                        <PencilAltIcon
                                                            class="
                                                                mr-3
                                                                h-5
                                                                w-5
                                                                text-gray-400
                                                                group-hover:text-gray-500
                                                            "
                                                            aria-hidden="true"
                                                        />
                                                        Edit
                                                    </a>
                                                </MenuItem>
                                                <MenuItem v-slot="{ active }">
                                                    <a
                                                        href="#"
                                                        @click="showDuplicate(task)"
                                                        :class="[
                                                            active
                                                                ? 'bg-gray-100 text-gray-900'
                                                                : 'text-gray-700',
                                                            'group flex items-center px-4 py-2 text-sm',
                                                        ]"
                                                    >
                                                        <DuplicateIcon
                                                            class="
                                                                mr-3
                                                                h-5
                                                                w-5
                                                                text-gray-400
                                                                group-hover:text-gray-500
                                                            "
                                                            aria-hidden="true"
                                                        />
                                                        Duplicate
                                                    </a>
                                                </MenuItem>
                                            </div>
                                            <div class="py-1">
                                                <MenuItem v-slot="{ active }">
                                                    <a
                                                        href="#"
                                                        @click="
                                                            removeRecord(
                                                                task.id
                                                            )
                                                        "
                                                        :class="[
                                                            active
                                                                ? 'bg-gray-100 text-gray-900'
                                                                : 'text-gray-700',
                                                            'group flex items-center px-4 py-2 text-sm',
                                                        ]"
                                                    >
                                                        <i
                                                            class="
                                                                fad
                                                                fa-trash-alt
                                                                mr-2
                                                            "
                                                        ></i>
                                                        Delete
                                                    </a>
                                                </MenuItem>
                                            </div>
                                        </MenuItems>
                                    </transition>
                                </Menu>
                            </td>
                        </tr>
                    </transition-group>
                    <tfoot class="bg-gray-50 dark:bg-sky-900">
                        <tr>
                            <td
                                colspan="7"
                                class="px-6 py-3 text-gray-500 dark:text-gray-50 rounded-b-lg  text-sm"
                            >
                                <div class="flex items-center justify-between">
                                    <div>
                                        Displaying
                                        <span class="font-bold text-primary dark:text-sky-200">{{
                                            tasks.length
                                        }}</span>
                                        records
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </tfoot>
                </table>
                <div
                    v-if="selected.length"
                    class="
                        fixed
                        bottom-0
                        bg-gray-50
                        px-6
                        py-3
                        w-[970px]
                        flex
                        items-center
                        border-t border-primary
                    "
                >
                    <div class="mr-2">
                        <span class="font-bold text-primary">{{
                            selected.length
                        }}</span>
                        records selected
                    </div>
                    <button
                        type="button"
                        class="
                            mr-2
                            inline-flex
                            items-center
                            px-3
                            py-2
                            border border-transparent
                            shadow-sm
                            text-sm
                            leading-4
                            font-medium
                            rounded-md
                            text-white
                            bg-red-600
                            hover:bg-red-700
                            focus:outline-none
                            focus:ring-2
                            focus:ring-offset-2
                            focus:ring-red-500
                        "
                    >
                        <i class="fad fa-trash-alt mr-2"></i>
                        Delete
                    </button>
                    <button
                        type="button"
                        class="
                            inline-flex
                            items-center
                            px-3
                            py-2
                            border border-transparent
                            shadow-sm
                            text-sm
                            leading-4
                            font-medium
                            rounded-md
                            text-white
                            bg-teal-600
                            hover:bg-teal-700
                            focus:outline-none
                            focus:ring-2
                            focus:ring-offset-2
                            focus:ring-teal-500
                        "
                    >
                        <i class="fad fa-clone mr-2"></i>
                        Duplicate
                    </button>
                </div>
            </div>
        </div>
    </div>
    <duplicate-modal
        v-model:isOpen="isDuplicateModalOpen"
        v-model:duplicateTo="duplicateTo"
        :onConfirm="duplicate"
    ></duplicate-modal>
</template>

<script>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import {
    DotsVerticalIcon,
    DuplicateIcon,
    PencilAltIcon,
} from '@heroicons/vue/solid'

import TimePeriodFilter from '../filters/TimePeriodFilter.vue'
import { mapState, mapActions } from 'vuex'
import { getTaskCategoryByDescription } from '../../store/descriptions'
import DuplicateModal from '../forms/modals/DuplicateModal.vue'

export default {
    components: {
        Menu,
        MenuButton,
        MenuItem,
        MenuItems,
        DotsVerticalIcon,
        DuplicateIcon,
        PencilAltIcon,
        TimePeriodFilter,
        DuplicateModal,
    },
    props: ['onEditClick'],
    data(){
        return {
            selectAll: false,
            isDuplicateModalOpen: false,
            duplicateTo: new Date(),
            duplicateTask:null,
        }
    },
    computed: {
        ...mapState({
             tasks: (state) => state.filteredRecords,
             selectedProject: (state) => state.filters.project,
             projects: (state) => state.projects,
             }),
        selected() {
            return this.tasks.filter((item) => item.selected)
        },
    },
    methods: {
        getTaskCategoryByDescription,
        toggleSelectAll(){
            if(this.selectAll){
                this.tasks.forEach((item) => item.selected = true)
            } else {
                this.tasks.forEach((item) => item.selected = false)
            }

        },
        showDuplicate(task){
            this.duplicateTask = task
            this.isDuplicateModalOpen = true

        },
        duplicate(){
            this.duplicateTask.date = this.duplicateTo,
            this.duplicateTask.id = null,
            this.saveRecord(this.duplicateTask)
            this.isDuplicateModalOpen = false
            this.$notify({
                    title: 'Record saved!',
                    message: 'Your record has been duplicated to the selected month',
                    type: 'success',
                })
        },
        ...mapActions(['saveRecord','removeRecord', 'search']),
    },
    mounted() {
        this.search()
    },
}
</script>
