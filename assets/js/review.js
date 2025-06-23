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

export let finished_file_contents = {} // path -> file value

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
    // console.log(file_content)
    const ev = create_editor_content(
        file_content.original,
        file_content.changes
    )
    // attach to parent/clear others
    const $parent = $('.main>.content>.editor')
    const $container = $parent.find(">.container")
    $container.empty()
    $container.append(ev.dom)
    // replace filename in tab
    const $tab = $(".main>.content>.editor>.top>.file-name")
    console.log($tab);
    console.log(path.split("/").at(-1));
 
    $tab.text(path.split("/").at(-1));
    $tab.data("file_handle",item);
    $tab.data("ev",ev);
    // see if review panel is still visible
    const $reviewPanel = $('.main > .content > .review')
    if ($reviewPanel.is(':visible'))
        $reviewPanel.hide()
    // see if editor still hidden
    if ($parent.is(':hidden'))
        $parent.removeClass("hidden")

}

export const on_mark_done_click = el => {
    const $tab = $(".main>.content>.editor>.top>.file-name")
    let $file_handle = $tab.data("file_handle")
    // deactivate file on click
    $file_handle.find(".symbol").prop("onclick", null).off("click");
    $file_handle.find(".name").prop("onclick", null).off("click");
    // Get the contents of the CodeMirror editor inside .main>.content>.editor>.container
    // do this before marking as done, so taht data is present
    const ev = $tab.data("ev")
    let path = $file_handle.attr('path').slice(1)
    finished_file_contents[path] = ev.state.doc.toString()
    
    // mark as done
    $file_handle.find(".checkbox > .attention").trigger("simulate_click")

    
}