/**
 * Get config with authorization token to make Webcandy API calls.
 * @returns {{headers: {Authorization: string}}}
 */
function getAuthConfig() {
    const token = sessionStorage.getItem("token");
    return {
        headers: {
            Authorization: "Bearer " + token,
        }
    }
}

export {
    getAuthConfig
};
