const projects = [
    {
        id: 1,
        name: 'BairesDev New Time Tracker',
        description: 'This is just a dummy description of a great project.',
        hours: '68h',
        expectedDailyMinutes: 4 * 60,
        status: 'ok',
        focal: {
            id: 9,
            name: 'Juliana Ponzio',
            email: 'juliana.ponzio@bairesdev.com',
            avatar: 'https://ca.slack-edge.com/T9U2U104U-U01CTG078RG-30f636af9db9-512',
        },
    },
    {
        id: 2,
        name: 'Another Project to Change the World',
        description: 'And this is another description without meaning.',
        hours: '64h 30m',
        status: 'behind',
        expectedDailyMinutes: 4 * 60,
        focal: {
            id: 4,
            name: 'Tom Cook',
            email: 'tom@cook.com',
            avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        },
    },
]

export default projects
