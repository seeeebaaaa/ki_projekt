// contains logic for reviews

const get_changes_from_server = async path => {
    const response = await fetch(URLS.get_changes(), {
        method: 'GET',
        headers: {
            Accept: 'application/json'
        },
        body: {
            path: path
        }
    })
    return await response.json()
}
