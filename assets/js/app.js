import $ from 'jquery'
// export for others scripts to use
window.$ = $
import "./tree"

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
