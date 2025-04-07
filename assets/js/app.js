import $ from 'jquery'
import "./tree"
import "./utility"

import { basicSetup } from 'codemirror'
import { EditorView } from '@codemirror/view'
import { python } from "@codemirror/lang-python"
import { vsCodeDark } from '@fsegurai/codemirror-theme-vscode-dark'

$(_ => {
  $('.main>.content>.files').dlResizeable()

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
