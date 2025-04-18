import $ from 'jquery'

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
            Accept: 'application/json'
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
        console.log(error);
      document.getElementById('taskIdText').textContent = 'Error occurred'
    }
  }
async function sendRequest() {
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
      document.getElementById('responseText').textContent = 'Error occurredded'
    }
  }
  

$(_ => {
    $("#submit_lower").on("click", _ => {
          sendRequest()
    })
    $("#startSampleProcess").on("click", _ => {
        startSampleProcess()
    })
    $("#fetchTaskResult").on("click", _ => {
        fetchTaskResult()
    })
  })