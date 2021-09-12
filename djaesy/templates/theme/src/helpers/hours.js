export const hourStringToMinutes = (hourString) => {
    const [h, m] = hourString.split(':')
    return parseInt(h) * 60 + parseInt(m)
}
