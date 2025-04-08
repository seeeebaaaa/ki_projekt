import $ from 'jquery'
import "./utility"
import "./entry"
import "./tree"
import "./progress"
import "./jquery-ui"

import { basicSetup } from 'codemirror'
import { EditorView } from '@codemirror/view'
import { python } from "@codemirror/lang-python"
import { vsCodeDark } from '@fsegurai/codemirror-theme-vscode-dark'

$(_ => {
  window.jQuery = $
  $('.main>.content>.files').resizable({
    containment: "parent", // cant let it get bigger than the parent
    handles: "e", // only allow resizing on the right side of the box,
    minWidth: $('.main>.content>.files').css("min-height")
  })

  $('.main>.content>.files>.select>select').selectmenu()

  const fullHeightEditor = EditorView.theme({
    '&': { height: '100%' },
    '.cm-scroller': { height: '100%' }
  })

  const view = new EditorView({
    doc: `#blablbla`,
    parent: $('.main>.content>.editor')[0],
    extensions: [
      basicSetup,
      fullHeightEditor,
      python(),
      vsCodeDark,
    ]
  })
  
})
