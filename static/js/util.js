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

export {
    getAuthConfig,
    getMatchingObject,
    getMatchingIndex
};
