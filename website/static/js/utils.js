function getDateString(date) {
    return (
        date.toLocaleDateString([], { year:'numeric', month:'short', day:'numeric' }) +
        " at " +
        date.toLocaleTimeString([], {timeStyle: 'short'})
    )
}

/**
 * Produces a function with a built in delay for debouncing
 * @param {Function} callback - Function to execute
 * @param {Number} delay - (in milliseconds)
 * @returns A function that executes the callback after the delay using the provided args
 */
 function getDebouncer(callback, delay) {
    let timeout = null;
    return (...args) => {
        if (timeout) clearTimeout(timeout);
        timeout = setTimeout(() => {
            timeout = null;
            callback(...args);
        }, delay);
    }
}