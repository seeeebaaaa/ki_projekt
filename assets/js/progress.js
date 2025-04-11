import $ from 'jquery'
import { load_tree } from './tree'

// possible, stati: inactive, current, done
const states = [
    'start',
    'select',
    'ai',
    'review',
    'bundle',
    'sphinx',
    'download'
]

export const start_step = step => {
    // Sets the previous connector to done
    // sets the ball and following connector to current
    const index = states.indexOf(step)
    const ball_index = index * 2 + 1
    const connector_index = index * 2
    const ball = $(`.p-bar-container .step:nth-child(${ball_index})`)
    const previous_connector = $(`.p-bar-container .connector:nth-child(${connector_index})`)
    if (previous_connector.length) {
        previous_connector.find('.text span').text('')
        previous_connector.find('.status').text('')
        previous_connector.removeClass('current').addClass('done')
    }
    const next_connector = $(`.p-bar-container .connector:nth-child(${connector_index+2})`)
    if (next_connector.length) {
        next_connector.find('.text span').text('')
        next_connector.find('.status').text('')
        next_connector.removeClass('done').addClass('current')
    }
    ball.removeClass('done').addClass('current')
}

const is_started = step => {
    const index = states.indexOf(step)
    const ball_index = index * 2 + 1
    const ball = $(`.p-bar-container .step:nth-child(${ball_index})`)
    return ball.hasClass("current")
}


export const stop_step = step => {
    // sets the ball and following connector to current
    const index = states.indexOf(step)
    const ball_index = index * 2 + 1
    const connector_index = index * 2
    const ball = $(`.p-bar-container .step:nth-child(${ball_index})`)
    const next_connector = $(`.p-bar-container .connector:nth-child(${connector_index+2})`)
    if (next_connector.length) {
        next_connector.find('.text span').text('')
        next_connector.find('.status').text('')
        next_connector.removeClass('current').addClass('done')
    }
    ball.removeClass('current').addClass('done')
}

export const update_progress = (step, text = "", status = "") => {
    // if the step is not started, start it
    if (!is_started(step))
        start_step(step)
    // Assigns the connector after the step the given text and status
    const index = states.indexOf(step)*2+1
    const connector_index = index -1
    const next_connector = $(`.p-bar-container .connector:nth-child(${connector_index + 2})`)
    if (next_connector.length) {
        if (text)
            next_connector.find('.text span').text(text)
        if (status)
            next_connector.find('.status').text(status)
    }
}

const get_progress = async _ => {
    const response = await fetch(URLS.progress(), {
        method: 'GET',
        headers: {
          Accept: 'application/json'
        }
    })
    return await response.json()
    
}


let poll = null
// should use a websocket instead of this, but thats sth for the future
export const poll_progress = (cb_loop,cb_end,interval = 200) => {
    let old_state = ""
    const polling_function = async _ => {
        try {
            // get current progress
            const re = await get_progress()
            console.log(re);
            // quit if done or sth
            if (re.task_state && re.task_state == "done") {
                cb_end(re,old_state)
                stop_step(old_state)
                clearInterval(poll)
            }
            // apply progress
            cb_loop(re)
            old_state = re.state
        } catch (e) {
            console.log(e);
            
            clearInterval(poll)
        }
    }
    poll = setInterval(polling_function,interval)
}


export const git_clone_cb_loop = re => {
    update_progress(re.state, re.state_text, re.state_status)
}
export const git_clone_cb_end = (re,old_state) => {
    stop_step(old_state)
    // show file tree
    load_tree(re.data.files)
    // hide loading screen
    $(".main>.content>.loading").hide()
    $(".main>.content>.selection").removeClass("hidden")
    // show select screen
}
// window.start_step = start_step
// window.update_progress = update_progress
$(_ => {})
