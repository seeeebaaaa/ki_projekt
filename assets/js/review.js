// contains logic for reviews

import { create_editor_content } from './editor'
import $ from 'jquery'

const get_changes_from_server = async path => {
    const response = await fetch(URLS.get_changes(), {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            path: path
        })
    })
    let res = await response.json()
    console.log(res)
    return res
}

const loaded_files = {}

let currently_loaded = ""

// on file click, get changes and file from server
export const on_file_click = async el => {

    // TODO: check if other file is already open and not finished

    const item = $(el.currentTarget).closest('.leaf.item')
    const path = item.attr('path').slice(1) // remove starting slash
    if (currently_loaded == path)
        return
    else
        currently_loaded=path

    let file_content = null
    if (loaded_files[path]) {
        file_content = loaded_files[path]
    } else {
        file_content = await get_changes_from_server(path)
        loaded_files[path] = file_content
    }
    console.log(file_content)
    const ev = create_editor_content(
        file_content.original,
        file_content.changes
    )
    // attach to parent/clear others
    const $parent = $('.main>.content>.editor')
    const $container = $parent.find(">.container")
    $container.empty()
    $container.append(ev.dom)
    // see if review panel is still visible
    const $reviewPanel = $('.main > .content > .review')
    if ($reviewPanel.is(':visible'))
        $reviewPanel.hide()
    // see if editor still hidden
    if ($parent.is(':hidden'))
        $parent.removeClass("hidden")
}
