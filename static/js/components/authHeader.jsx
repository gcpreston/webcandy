import React from 'react';

export default function authHeader() {
    const token = JSON.parse(sessionStorage.getItem('token'));

    if (token) {
        return { "Authorization": "Bearer " + token };
    } else {
        return {};
    }
}
