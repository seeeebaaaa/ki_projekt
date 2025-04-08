import $ from 'jquery'

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
    ball.removeClass('done').addClass('current')
}

export const update_progress = (step, text="", status="") => {
    // Assigns the connector after the step the given text and status
    const index = states.indexOf(step)
    const connector_index = index * 2
    const next_connector = $(`.p-bar-container .connector:nth-child(${connector_index + 2})`)
    if (next_connector.length) {
        if (text)
            next_connector.find('.text span').text(text)
        if (status)
            next_connector.find('.status').text(status)
    }
}

// window.start_step = start_step
// window.update_progress = update_progress
$(_ => {})
