/**
 * Get config with authorization token to make Webcandy API calls.
 * @return {{headers: {Authorization: string}}}
 */
function getAuthConfig() {
    const token = sessionStorage.getItem("token");
    return {
        headers: {
            Authorization: "Bearer " + token,
        }
    }
}

/**
 * Find the first member of arr with the given key-value pair.
 */
function getMatchingObject(arr, key, value) {
    for (const obj of arr) {
        if (obj[key] === value)
            return obj;
    }
    return null;
}

/**
 * Find the index of the first member of arr with the given key-value pair.
 */
function getMatchingIndex(arr, key, value) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i][key] === value)
            return i;
    }
    return null;
}

/**
 * Check if two arrays have matching contents.
 */
function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    for (let i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}

/**
 * Check if a 2D array includes another given array.
 * @param arr - The 2D array to use
 * @param e - The inner array to check for
 */
function array2dIncludes(arr, e) {
    for (let i = 0; i < arr.length; i++) {
        if (arraysEqual(arr[i], e))
            return true;
    }
    return false;
}

export {
    getAuthConfig,
    getMatchingObject,
    getMatchingIndex,
    arraysEqual,
    array2dIncludes
};
