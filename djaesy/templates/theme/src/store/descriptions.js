const options = [
    {
        value: 'absence',
        label: 'Absence',
        children: [
            {
                value: 'Personal Reasons',
                label: 'Personal Reasons',
            },
            {
                value: 'National Holiday',
                label: 'National Holiday',
            },
            {
                value: 'Compensation day',
                label: 'Compensation day',
            },
            {
                value: 'Vacations',
                label: 'Vacations',
            },
            {
                value: 'Sick leave',
                label: 'Sick leave',
            },
            {
                value: 'Paid Time Off',
                label: 'Paid Time Off',
            },
            {
                value: 'Unpaid Time Off',
                label: 'Unpaid Time Off',
            },
            {
                value: 'Other - Absence',
                label: 'Other - Absence',
            },
        ],
    },
    {
        value: 'development',
        label: 'Development',
        children: [
            {
                value: 'Architecture definition',
                label: 'Architecture definition',
            },
            {
                value: 'Code review',
                label: 'Code review',
            },
            {
                value: 'Demo preparation',
                label: 'Demo preparation',
            },
            {
                value: 'Deployment',
                label: 'Deployment',
            },
            {
                value: 'Environment setup',
                label: 'Environment setup',
            },
            {
                value: 'Features development',
                label: 'Features development',
            },
            {
                value: 'Test cases development',
                label: 'Test cases development',
            },
            {
                value: 'Research / Analysis',
                label: 'Research / Analysis',
            },
            {
                value: 'Spike',
                label: 'Spike',
            },
            {
                value: 'Bug Fixing',
                label: 'Bug Fixing',
            },
            {
                value: 'Design',
                label: 'Design',
            },
            {
                value: 'Writing User Stories',
                label: 'Writing User Stories',
            },
            {
                value: 'Requirements analysis',
                label: 'Requirements analysis',
            },
            {
                value: 'Peer review',
                label: 'Peer review',
            },
            {
                value: 'DB Automation',
                label: 'DB Automation',
            },
            {
                value: 'DB Maintenance',
                label: 'DB Maintenance',
            },
            {
                value: 'Research and Learning',
                label: 'Research and Learning',
            },
            {
                value: 'Configuration',
                label: 'Configuration',
            },
            {
                value: 'Library Upgrade',
                label: 'Library Upgrade',
            },
            {
                value: 'Refactor',
                label: 'Refactor',
            },
            {
                value: 'Support',
                label: 'Support',
            },
            {
                value: 'Integration',
                label: 'Integration',
            },
            {
                value: 'Debug',
                label: 'Debug',
            },
            {
                value: 'On call',
                label: 'On call',
            },
            {
                value: 'Mockups Design',
                label: 'Mockups Design',
            },
            {
                value: 'Graphic Design',
                label: 'Graphic Design',
            },
            {
                value: 'Wireframes Design',
                label: 'Wireframes Design',
            },
            {
                value: 'UI definition',
                label: 'UI definition',
            },
            {
                value: 'Other - Development',
                label: 'Other - Development',
            },
        ],
    },
    {
        value: 'administrative',
        label: 'Administrative',
        children: [
            {
                value: 'Email revision/answering',
                label: 'Email revision/answering',
            },
            {
                value: 'Daily Progress Report',
                label: 'Daily Progress Report',
            },
            {
                value: 'Weekly Progress Report',
                label: 'Weekly Progress Report',
            },
            {
                value: 'Other - Administrative',
                label: 'Other - Administrative',
            },
        ],
    },
    {
        value: 'documentation',
        label: 'Documentation',
        children: [
            {
                value: 'Technical Writing',
                label: 'Technical Writing',
            },
            {
                value: 'Diagrams drawing',
                label: 'Diagrams drawing',
            },
            {
                value: 'Documentation reading',
                label: 'Documentation reading',
            },
            {
                value: 'Documentation writing',
                label: 'Documentation writing',
            },
            {
                value: 'Research',
                label: 'Research',
            },
            {
                value: 'Other - Documentation',
                label: 'Other - Documentation',
            },
        ],
    },
    {
        value: 'idle_time',
        label: 'Idle time',
        children: [
            {
                value: 'Travel',
                label: 'Travel',
            },
            {
                value: 'Partial Assigment',
                label: 'Partial Assigment',
            },
            {
                value: 'Internet issues',
                label: 'Internet issues',
            },
            {
                value: 'No assigned tasks',
                label: 'No assigned tasks',
            },
            {
                value: 'Other - Idle time',
                label: 'Other - Idle time',
            },
        ],
    },
    {
        value: 'internal_process',
        label: 'Internal Process',
        children: [
            {
                value: 'Technical Screenings',
                label: 'Technical Screenings',
            },
            {
                value: 'Staffing Technical Interview',
                label: 'Staffing Technical Interview',
            },
            {
                value: 'Coding challenges review',
                label: 'Coding challenges review',
            },
            {
                value: 'Reviewing exams',
                label: 'Reviewing exams',
            },
            {
                value: 'Other - Internal Process',
                label: 'Other - Internal Process',
            },
        ],
    },
    {
        value: 'meetings_client',
        label: 'Meetings (Client)',
        children: [
            {
                value: '1-1 with client focal point',
                label: '1-1 with client focal point',
            },
            {
                value: 'Backlog refinement meeting',
                label: 'Backlog refinement meeting',
            },
            {
                value: 'Blocker removal meeting',
                label: 'Blocker removal meeting',
            },
            {
                value: 'Client side training',
                label: 'Client side training',
            },
            {
                value: 'Sprint Planning',
                label: 'Sprint Planning',
            },
            {
                value: 'Sprint Retrospective',
                label: 'Sprint Retrospective',
            },
            {
                value: 'Sprint Review / Demo',
                label: 'Sprint Review / Demo',
            },
            {
                value: 'Client Meeting',
                label: 'Client Meeting',
            },
            {
                value: 'Daily Meeting',
                label: 'Daily Meeting',
            },
            {
                value: 'KickOff Meeting',
                label: 'KickOff Meeting',
            },
            {
                value: 'Other - Meetings (Client)',
                label: 'Other - Meetings (Client)',
            },
        ],
    },
    {
        value: 'meetings_internal',
        label: 'Meetings (Internal)',
        children: [
            {
                value: '1:1 meeting with HRBP',
                label: '1:1 meeting with HRBP',
            },
            {
                value: '1:1 meeting with Manager',
                label: '1:1 meeting with Manager',
            },
            {
                value: 'Team building meeting',
                label: 'Team building meeting',
            },
            {
                value: 'Other - Meetings (Internal)',
                label: 'Other - Meetings (Internal)',
            },
        ],
    },
    {
        value: 'other',
        label: 'Other',
        children: [
            {
                value: 'Other',
                label: 'Other',
            },
        ],
    },
    {
        value: 'testing',
        label: 'Testing',
        children: [
            {
                value: 'Exploratory',
                label: 'Exploratory',
            },
            {
                value: 'Production Verification',
                label: 'Production Verification',
            },
            {
                value: 'Test Creation/design',
                label: 'Test Creation/design',
            },
            {
                value: 'Smoke testing',
                label: 'Smoke testing',
            },
            {
                value: 'Environment configuration',
                label: 'Environment configuration',
            },
            {
                value: 'Functional Testing',
                label: 'Functional Testing',
            },
            {
                value: 'Regression testing',
                label: 'Regression testing',
            },
            {
                value: 'Testathon / UAT',
                label: 'Testathon / UAT',
            },
            {
                value: 'Coding',
                label: 'Coding',
            },
            {
                value: 'Manual testing',
                label: 'Manual testing',
            },
            {
                value: 'Test case execution',
                label: 'Test case execution',
            },
        ],
    },
    {
        value: 'training',
        label: 'Training (Trainee)',
        children: [
            {
                value: 'Receiving mentoring support',
                label: 'Receiving mentoring support',
            },
            {
                value: 'Online course',
                label: 'Online course',
            },
            {
                value: 'Project Onboarding (Trainee)',
                label: 'Project Onboarding (Trainee)',
            },
            {
                value: 'Reading Documentation',
                label: 'Reading Documentation',
            },
            {
                value: 'Internal course',
                label: 'Internal course',
            },
            {
                value: 'Self training',
                label: 'Self training',
            },
            {
                value: 'Other - Training (Trainee)',
                label: 'Other - Training (Trainee)',
            },
            {
                value: 'Providing mentoring support',
                label: 'Providing mentoring support',
            },
            {
                value: 'Project Onboarding (Trainer)',
                label: 'Project Onboarding (Trainer)',
            },
        ],
    },
]

export const getTaskCategoryByDescription = (taskDescription) => {
    for (const category of options) {
        for (const description of category.children) {
            if (description.value === taskDescription) return category.label
        }
    }
    return null
}

export default options
