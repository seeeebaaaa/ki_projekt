import $ from 'jquery'
// export for others scripts to use
window.$ = $
// window.jQuery = jQuery;

async function fetchTaskResult () {
  const taskId = $('#taskIdText').text()
  if (!taskId || taskId === 'No Task ID') {
    document.getElementById('taskResultText').textContent = 'Invalid Task ID'
    return
  }

  const pollTaskResult = async () => {
    try {
      console.log('before request to', URLS.task_result(taskId))

      const response = await fetch(URLS.task_result(taskId), {
        method: 'GET',
        headers: {
          Accept: 'application/json' // Ensures Turbo handles the response
        }
      })
      const re = await response.json()
      // set output cause why not
      $('#progress-text').text(JSON.stringify(re))
      // set progress bar
      if (re.progress) {
        $('#progress-bar').css('width', re.progress * 5 + 'em')
      } else $('#progress-bar').css('width', '0 em')
      if (re.ready) {
        clearInterval(intervalId)
      }
    } catch (error) {
      $('#progress-text').text('Error occurred')
      console.log(error)

      clearInterval(intervalId)
    }
  }

  const intervalId = setInterval(pollTaskResult, 200)
}

async function startSampleProcess () {
  try {
    const response = await fetch(URLS.startsampleprocess(), {
      method: 'GET',
      headers: {
        Accept: 'application/json'
      }
    })
    const data = await response.json()
    if (data.task_id) {
      document.getElementById('taskIdText').textContent = data.task_id
    } else {
      document.getElementById('taskIdText').textContent = 'No Task ID returned'
    }
  } catch (error) {
    document.getElementById('taskIdText').textContent = 'Error occurred'
  }
}
async function sendRequest () {
  const userInput = document.getElementById('userInput').value
  try {
    const response = await fetch('/getLower', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code: userInput })
    })
    const data = await response.json()
    document.getElementById('responseText').textContent =
      data.result || 'No response'
  } catch (error) {
    document.getElementById('responseText').textContent = 'Error occurred'
  }
}

// see https://jsfiddle.net/daslicht/eh1paqzy/
;(function ($) {
  var parentOffset,
    item,
    overRight = false,
    newWidth,
    dragged = false

  $.fn.dlResizeable = function (options) {
    /* var settings = $.extend({
           
            color: "#556b2f",
            backgroundColor: "white"
        }, options );*/

    item = this

    $(document).mousedown(function (e) {
      newWidth = parentOffset.relX - item.outerWidth()
      if (overRight) {
        dragged = true
      }
    })

    $(document).mouseup(function (e) {
      dragged = false
    })

    $(document).mousemove(function (e) {
      parentOffset = item.offset()
      var relX = e.pageX - parentOffset.left
      var relY = e.pageY - parentOffset.top
      var widthToAdd = 0

      /* check if mouse is above right border */
      if (relX >= item.outerWidth() - 4 && relX <= item.outerWidth()) {
        item.css('cursor', 'col-resize')
        overRight = true
      } else {
        item.css('cursor', 'default')
        overRight = false
      }
      if (dragged) {
        newWidth = relX - item.outerWidth()
        // item.css("min-width",item.outerWidth() + newWidth);
        item.width(item.outerWidth() + newWidth)
      }
    })

    return this
  }
})($)

import { basicSetup } from 'codemirror'
import { EditorView } from '@codemirror/view'

$(_ => {
  $('.main>.content>.files').dlResizeable()
  const view = new EditorView({
    doc: 'Start document',
    parent: $('.main>.content>.editor')[0],
    extensions: [basicSetup]
  })
})
