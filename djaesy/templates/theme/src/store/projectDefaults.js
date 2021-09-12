const projectDefaults = new Map([
    [
        1,
        {
            id: 1,
            focalPoint: {
                id: 2,
                name: 'Arlene Mccoy',
                avatar: 'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            },
            description: ['documentation', 'Documentation writing'],
            sortResults: { id: 3, name: 'Comments' },
            timePeriod: {
                name: 'Weekly',
                description:
                    'Display list of tasks for selected week. Defaults to running week.',
            },
        },
    ],
    [
        2,
        {
            id: 2,
            focalPoint: {
                id: 5,
                name: 'Tanya Fox',
                avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            },
            description: ['documentation', 'Documentation writing'],
            sortResults: { id: 1, name: 'Most recent first' },
            timePeriod: {
                name: 'Weekly',
                description:
                    'Display list of tasks for selected week. Defaults to running week.',
            },
        },
    ],
])

export default projectDefaults
