import $ from 'jquery'
import {
    poll_progress,
    process_files_cb_loop,
    process_files_cb_end,
    submit_review_cb_loop,
    submit_review_cb_end,
    stop_step
} from './progress'

import {on_file_click, finished_file_contents} from "./review"

async function buildTree (paths, review = false) {
    const root = {}

    // Step 1: Build nested object structure
    // sort paths for correct order
    paths.sort()
    paths.forEach(path => {
        const parts = path.split('/')
        let current = root
        parts.forEach((part, i) => {
            if (!current[part]) {
                current[part] = i === parts.length - 1 ? null : {}
            }
            current = current[part]
        })
    })

    async function cT (tree, $root, path_til_now) {
        for (const key in tree) {
            if (tree[key] === null) {
                // key is a file, so add leaf to root
                const $checker = review
                    ? await buildHighlgiht(path_til_now, key)
                    : await buildCheckbox(path_til_now, key)
                $root.append(
                    $('<div></div>')
                        .addClass('leaf item')

                        .attr('path', path_til_now + '/' + key)
                        .prop('title', path_til_now + '/' + key)
                        .append(
                            $('<div></div>')
                                .addClass('symbol')
                                .html(await getSVG('page.svg'))
                                .on('click', on_file_click)
                        )
                        .append(
                            $('<div></div>')
                                .addClass('name')
                                .text(key)
                                .on('click', on_file_click)
                        )
                        .append($checker)
                )
            } else {
                // key is a folder, so start new section adn append that to the root
                const $section = $('<div></div>').addClass('section')
                const $head = $('<div></div>')
                    .addClass('head item')
                    .attr('path', path_til_now + '/' + key)
                    .prop('title', path_til_now + '/' + key)
                    .append(
                        $('<div></div>')
                            .addClass('action')
                            .html(await getSVG('plus.svg'))
                            .on('click', unfold_section)
                    )
                    .append(
                        $('<div></div>')
                            .addClass('symbol')
                            .html(await getSVG('folder.svg'))
                            .on('click', unfold_section)
                    )
                    .append(
                        $('<div></div>')
                            .addClass('name')
                            .text(key)
                            .on('click', unfold_section)
                    )
                const $checker = review
                    ? await buildHighlgiht(path_til_now, key)
                    : await buildCheckbox(path_til_now, key)
                const $group = $('<div></div>')
                    .addClass('group')
                    .append('<div class="line"><div></div></div>')
                const $items = $('<div></div>').addClass('items')

                $section.append($head)
                $head.append($checker)
                $group.append($items)
                $section.append($group)
                await cT(tree[key], $items, path_til_now + '/' + key)
                $root.append($section)
            }
        }
        return $root
    }

    return await cT(root, $('<div></div>').addClass('tree'), '')
}

const buildCheckbox = async _ => {
    const $checkbox = $('<div></div>')
        .addClass('star checkbox')
        .append(
            $(`<input type="checkbox" name=""></input>`)
                .hide()
                .on('prop_change_up', prop_change_up)
                .on('prop_change_down', prop_change_down)
        )
        .append(
            $(`<div></div>`)
                .html(await getSVG('star.svg'))
                .on('click', check_item)
        )
    return $checkbox
}

// the highlight for the reviewing process.
// can be Attention or Done
const buildHighlgiht = async _ => {
    const $hightlight = $('<div></div>')
        .addClass('highlight checkbox')
        .append(
            $(`<input type="checkbox" name=""></input>`)
                .hide()
                .on('prop_change_up', prop_change_up)
                .on('prop_change_down', prop_change_down)
        )
        .append(
            $(`<div></div>`)
                .addClass('check')
                .html(await getSVG('check.svg'))
                .on('simulate_click', check_item_highlight)
        )
        .append(
            $(`<div></div>`)
                .addClass('attention')
                .html(await getSVG('sparks-solid.svg'))
                .on('simulate_click', check_item_highlight)
        )
    return $hightlight
}

const stored_images = {}

async function getSVG (svgName) {
    // check if already loaded for performance
    if (stored_images[svgName]) return stored_images[svgName]

    const r = await fetch('svg/' + svgName)
    const text = await r.text()
    stored_images[svgName] = text
    return text
}

export async function load_tree (paths, review = false) {
    const tree = await buildTree(paths, review)
    $('.main>.content>.files>.none').hide()
    $('.main>.content>.files>.tree').remove()
    $('.main>.content>.files').append(tree)
}

window.load_tree = load_tree

// tree functions

const unfold_section = e => {
    const head_item = $(e.currentTarget).closest('.head.item')
    head_item.siblings().toggleClass('open')
}

// const open_file = e => {
//     const item = $(e.currentTarget).closest('.leaf.item')
//     console.log(`Request file from server.. (${item.attr('path')})`)
// }

const check_item = e => {
    const item_checkbox = $(e.currentTarget).siblings()
    item_checkbox
        .prop('checked', (_, prop) => !prop)
        .prop('indeterminate', false)
        .trigger('prop_change_down')
        .trigger('prop_change_up')
    toggle_process_button()
}

const check_item_highlight = e => {
    const item_checkbox = $(e.currentTarget).siblings()
    item_checkbox
        .prop('checked', (_, prop) => !prop)
        .prop('indeterminate', false)
        .trigger('prop_change_down')
        .trigger('prop_change_up')
    toggle_review_button()
}

const prop_change_up = e => {
    const current_item = $($(e.currentTarget).parents()[1]).hasClass('leaf')
        ? $($(e.currentTarget).parents()[1])
        : $($(e.currentTarget).parents()[2])
    // reflect changes upwards, introduce indeterminate state, unless were already at top
    if (!current_item.parent().hasClass('tree')) {
        // sum up all checks of siblings, to see what should happen
        let sum_fully_checked = +(
            current_item.find('.checkbox>input').prop('checked') &&
            !current_item.find('.checkbox>input').prop('indeterminate')
        )
        let sum_not_checked = +!current_item
            .find('.checkbox>input')
            .prop('checked')
        for (const item of current_item.siblings()) {
            // if leaf

            if ($(item).hasClass('leaf')) {
                console.log(
                    $(item).find('.checkbox>input').prop('checked'),
                    $(item).find('.checkbox>input').prop('indeterminate')
                )

                sum_fully_checked += +(
                    $(item).find('.checkbox>input').prop('checked') &&
                    !$(item).find('.checkbox>input').prop('indeterminate')
                )
                sum_not_checked += +!$(item)
                    .find('.checkbox>input')
                    .prop('checked')
            } else {
                console.log('calc sum for section')

                // is section
                sum_fully_checked += +(
                    $(item).find('>.head>.checkbox>input').prop('checked') &&
                    !$(item)
                        .find('>.head>.checkbox>input')
                        .prop('indeterminate')
                )
                sum_not_checked += +!$(item)
                    .find('>.head>.checkbox>input')
                    .prop('checked')
            }
        }
        // console.log(
        //     'sums:\n',
        //     'fully checked:',
        //     sum_fully_checked,
        //     '\nnot checked',
        //     sum_not_checked
        // )
        const num_of_boxes = current_item.siblings().length + 1
        if (num_of_boxes == sum_fully_checked)
            // all childs are fully checked, so also fully check
            $(current_item.parents()[2])
                .find('>.head.item>.checkbox>input')
                .prop('checked', true)
                .prop('indeterminate', false)
        else if (num_of_boxes == sum_not_checked)
            // no childs are selected
            $(current_item.parents()[2])
                .find('>.head.item>.checkbox>input')
                .prop('checked', false)
                .prop('indeterminate', false)
        // some childs are selected
        else
            $(current_item.parents()[2])
                .find('>.head.item>.checkbox>input')
                .prop('checked', true)
                .prop('indeterminate', true)

        console.log(
            'Triggering parent',
            $(current_item.parents()[2]),
            'from',
            current_item
        )
        $(current_item.parents()[2])
            .find('>.head>.checkbox>input')
            .trigger('prop_change_up')
    }
}

const prop_change_down = e => {
    // reflext change downwards, if we are a head item (aka, have items under us)
    if ($($(e.currentTarget).parents()[1]).hasClass('head item')) {
        // section head:
        const section = $($(e.currentTarget).parents()[1]).parent()
        const items = section.find('>.group>.items')
        const checked = $(e.currentTarget).prop('checked')

        for (const item of items.children()) {
            if ($(item).hasClass('leaf'))
                $(item)
                    .find('>.checkbox>input')
                    .prop('checked', checked)
                    .prop('indeterminate', false)
                    .trigger('prop_change_down')
            else
                $(item)
                    .find('>.head.item>.checkbox>input')
                    .prop('checked', checked)
                    .prop('indeterminate', false)
                    .trigger('prop_change_down')
        }
    }
}

const get_list_of_selected_paths = _ => {
    const tree = $('.main>.content>.files>.tree')
    const path_list = []
    for (const item of tree.find('.item')) {
        if ($(item).find('.checkbox>input').prop('checked'))
            path_list.push($(item).attr('path'))
    }
    return path_list
}

const get_list_of_accepted_paths = _ => {
    const path_list = get_list_of_selected_paths()
    return path_list.filter(path => path.endsWith('.py'))
}

const toggle_process_button = _ => {
    const button = $('.main>.content>.selection button')

    // remove all entries of list that don't end with .py
    const filteredPaths = get_list_of_accepted_paths()
    button.prop('disabled', filteredPaths.length == 0)

    if (filteredPaths.length != 0) {
        // display all files that will be processed
        const $list = $('.main>.content>.selection>.files-to-process>.list')
        const content = filteredPaths.join('<br>')
        $list.html(content)
        $('.main>.content>.selection>.files-to-process *').show()
    } else $('.main>.content>.selection>.files-to-process *').hide()
}

// will finish the review once everything is done
const toggle_review_button = _ => {
    // send all files to server to be put into actual files and then bundled

    // collect all selected files (for review, we want all checked files)

    // prepare file_changes dict (could be just a list of paths, or you may want to send more info)

    // send to /submit_review as file_changes dict
    console.log("FFC:", finished_file_contents);
    
    // check if all files are accepted
    const tree = $('.main>.content>.files>.tree')
    for (const item of tree.find('.item')) {
        if (!$(item).find('.checkbox>input').prop('checked'))
            return
    }
    // now every file is checked aka marked as done
    
    fetch('/submit_review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
        },
        body: JSON.stringify({"file_changes":finished_file_contents})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Review submission error:', data.error);
            return;
        }
        // then call poll_progress again
        // close previous state
        stop_step('review')
        $(".main>.content>.loading").show()
        $(".main>.content>.review").hide()
        $(".main>.content>.editor").hide()
        poll_progress(submit_review_cb_loop, submit_review_cb_end, 100);
    })
    .catch(err => {
        console.error('Network error during review submission:', err);
        // Optionally show error to user
    });
}

$(_ => {
    $('.main>.content>.selection>.files-to-process *').hide()
})

// send request when process button is pressed

const start_file_processing = async _ => {
    // start process in backend
    const valid_paths = get_list_of_accepted_paths()
    const re = await (
        await fetch(URLS.process(), {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                files: valid_paths
            })
        })
    ).json()
    if (re.error) {
        // handle error from backend
        console.log(re.error)
    } else {
        // close previous state
        stop_step('select')
        //  disable state button
        $('.main > .content > .selection > .container > button').prop(
            'disabled',
            true
        )
        $('.main>.content>.loading').show()
        $('.main>.content>.selection').hide()
        // otherwise, start polling for progress updatess
        poll_progress(process_files_cb_loop, process_files_cb_end, 100)
    }
}

// attach to button
$(_ => {
    $('.main > .content > .selection > .container > button').on(
        'click',
        start_file_processing
    )
})
