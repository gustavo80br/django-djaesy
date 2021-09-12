<template>
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
            <div class="bg-white px-4 py-5 border-b border-gray-200 sm:px-6">
                <div
                    class="
                        -ml-4
                        -mt-4
                        flex
                        justify-between
                        items-center
                        flex-wrap
                        sm:flex-nowrap
                    "
                >
                    <div class="ml-4 mt-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900">
                            Monthly report
                        </h3>
                        <p class="mt-1 text-sm text-gray-500">
                            This is the details of worked hours reported by the
                            user.
                        </p>
                        <p v-if="report.status == 'submitted'">
                            <a
                                href="/BairesDev_TimeTracker_Report.pdf"
                                target="_blank"
                                class="text-teal-500 text-sm"
                                ><i class="fad fa-file-pdf mr-2"></i> Download
                                as PDF</a
                            >
                        </p>
                    </div>
                    <div class="ml-4 mt-4 flex-shrink-0 items-center">
                        <submit-button
                            @click="approveReport"
                            v-if="report.status == 'submitted'"
                            ><i class="far fa-check mr-2"></i
                            >Approve</submit-button
                        >
                        <submit-button
                            @click="rejectReport"
                            v-if="report.status == 'submitted'"
                            type="danger"
                            ><i class="far fa-times mr-2"></i>
                            Reject</submit-button
                        >
                        <span
                            v-if="report.status == 'approved'"
                            class="
                                inline-flex
                                items-center
                                px-2.5
                                py-0.5
                                rounded-full
                                text-xs
                                font-medium
                                bg-green-100
                                text-green-800
                            "
                        >
                            Approved
                        </span>
                        <span
                            v-if="report.status == 'rejected'"
                            class="
                                inline-flex
                                items-center
                                px-2.5
                                py-0.5
                                rounded-full
                                text-xs
                                font-medium
                                bg-red-100
                                text-red-800
                            "
                        >
                            Rejected
                        </span>
                        <span
                            v-if="report.status == 'working'"
                            class="
                                inline-flex
                                items-center
                                px-2.5
                                py-0.5
                                rounded-full
                                text-xs
                                font-medium
                                bg-sky-100
                                text-sky-800
                            "
                        >
                            Working on
                        </span>
                    </div>
                </div>
            </div>
            <div class="shadow border-b border-gray-200 sm:rounded-lg bg-white">
                <table
                    v-if="report && report.tasks.length"
                    class="min-w-full divide-y divide-gray-200"
                >
                    <thead class="bg-sky-50">
                        <tr>
                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-right text-xs
                                    font-medium
                                    text-gray-500
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
                                    text-gray-500
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

                            <th
                                scope="col"
                                class="
                                    px-6
                                    py-3
                                    text-left text-xs
                                    font-medium
                                    text-gray-500
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
                                    text-gray-500
                                    uppercase
                                    tracking-wider
                                "
                            >
                                Comments
                            </th>
                        </tr>
                    </thead>
                    <tbody
                        v-if="report.tasks.length"
                        class="bg-white divide-y divide-gray-200"
                    >
                        <tr
                            v-for="(task, index) in report.tasks"
                            :key="index"
                            class="hover:bg-gray-50"
                        >
                            <td class="px-6 py-2 whitespace-nowrap">
                                <div class="text-right">
                                    <div
                                        class="
                                            text-sm
                                            font-medium
                                            text-gray-400
                                        "
                                    >
                                        {{ task.date.toLocaleDateString() }}
                                    </div>
                                </div>
                            </td>
                            <td class="py-2 whitespace-nowrap text-right">
                                <div class="text-primary text-sm font-bold">
                                    <el-tooltip
                                        v-if="task.overtime"
                                        class="item"
                                        effect="dark"
                                        content="Overtime"
                                        placement="top"
                                    >
                                        <span class="text-yellow-600 mr-2"
                                            >OT</span
                                        >
                                    </el-tooltip>
                                    {{ task.hours }}
                                </div>
                            </td>
                            <td class="px-6 py-2 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{
                                        getTaskCategoryByDescription(
                                            task.taskDescription
                                        )
                                    }}
                                </div>
                                <div class="text-sm text-gray-500">
                                    {{ task.taskDescription }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-500">
                                    {{ task.comments }}
                                </div>
                            </td>
                        </tr>
                    </tbody>
                    <tfoot class="bg-gray-50">
                        <tr>
                            <td
                                colspan="6"
                                class="px-6 py-3 text-gray-500 text-sm"
                            >
                                <div class="flex items-center justify-between">
                                    <div>
                                        Displaying
                                        <span class="font-bold text-primary">{{
                                            report.tasks.length
                                        }}</span>
                                        records
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import { getTaskCategoryByDescription } from '../../store/descriptions'
import SubmitButton from '../forms/SubmitButton.vue'

export default {
    components: {
        SubmitButton,
    },
    props: ['report'],

    methods: {
        getTaskCategoryByDescription,
        approveReport() {
            this.$store.commit('setReportStatus', {
                report: this.report,
                status: 'approved',
            })
        },
        rejectReport() {
            this.$store.commit('setReportStatus', {
                report: this.report,
                status: 'rejected',
            })
        },
    },
}
</script>
