import $ from 'jquery'
import "./utility"
import "./entry"
import "./tree"
import "./progress"
import "./jquery-ui"



$(_ => {
  window.jQuery = $
  $('.main>.content>.files').resizable({
    containment: "parent", // cant let it get bigger than the parent
    handles: "e", // only allow resizing on the right side of the box,
    minWidth: $('.main>.content>.files').css("min-height")
  })

  $('.main>.content>.files>.select>select').selectmenu()  
})
