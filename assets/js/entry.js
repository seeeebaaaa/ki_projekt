import * as util from './utility'
/*
 * This Script contains all entry relreted scripts
 *
 *
 *
 */
const entry_start = _ => {
    // fade out entry screen
    $('.entry').fadeOut({
        duration: 400,
        easing: 'easeOutQuad',
        complete: _ => {
            $('.main').hide().removeClass('hidden').fadeIn(400)
            $('.nav>.center').hide().removeClass('hidden').fadeIn(400)
            $('.nav>.center>.git-link>.input').text($('.entry>.input-container>.input>input').val())
        }
    })
    // fade in entry screen
}

const entry_input = e => {
    const input_field = $(e.currentTarget).find('input') // cause we always set the focus on the element above
    const button = $('.entry>.input-container>button')
    button.prop('disabled', !util.isValidURL(input_field.val()))
}

$(_ => {
    // add on input to enable button
    $('.entry>.input-container>.input').on('input', entry_input)
    // simualte button press on enter
    $('.entry>.input-container>.input').on('keypress', e => {
        const button = $('.entry>.input-container>button')
        if (e.which == 13) {
            if (!button.prop('disabled'))
               button.trigger("click")
        }
    })

    // add script to button
    $('.entry>.input-container>button').on('click', entry_start)
    // when clicking on the outline of the input field also set focus to input field
    $('.entry>.input-container>.input').on('click', _ => {
        $('.entry>.input-container>.input>input').trigger('focus')
    })
})
