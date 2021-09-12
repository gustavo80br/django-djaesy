import { v4 } from 'uuid'
const today = new Date()
const reports = [
    {
        month: '2021-06',
        project: 1,
        status: 'working',
        hours: 20,
        overtime: 0,
        tasks:[]
    },
    {
        month: '2021-06',
        project: 2,
        status: 'submitted',
        hours: 170,
        overtime: 10,
        tasks:[
            {
                id: v4(),
                date: new Date(today.getFullYear(), today.getMonth()-1, 15),
                project: {
                    id: 2,
                },
                hours: '160:00',
                taskDescription: 'No assigned tasks',
                comments: 'Ticket #234, solve the problem',
                overtime: false,
            },
            {
                id: v4(),
                date: new Date(today.getFullYear(), today.getMonth()-1, 11),
                project: {
                    id: 2,
                },
                hours: '10:00',
                taskDescription: 'Other',
                comments: 'Overtime description',
                overtime: true,
            },
        ]
    },
    {
        month: '2021-05',
        project: 1,
        status: 'rejected',
        hours: 2,
        overtime: 0,
        tasks:[
            {
                id: v4(),
                date: new Date(today.getFullYear(), today.getMonth()-2, 15),
                project: {
                    id: 1,
                },
                hours: '2:00',
                taskDescription: 'No assigned tasks',
                comments: 'Ticket #234, solve the problem',
                overtime: true,
            },
        ]
    },
    {
        month: '2021-05',
        project: 2,
        status: 'approved',
        hours: 3,
        overtime: 0,
        tasks:[
            {
                id: v4(),
                date: new Date(today.getFullYear(), today.getMonth()-2, 15),
                project: {
                    id: 2,
                },
                hours: '3:00',
                taskDescription: 'Other',
                comments: 'Some description of an old task',
                overtime: false,
            },
        ]
    }
]

export default reports
