import { basicSetup } from 'codemirror'
import { EditorView} from '@codemirror/view'
import { python } from '@codemirror/lang-python'
import { vsCodeDark } from '@fsegurai/codemirror-theme-vscode-dark'
import { unifiedMergeView } from '@codemirror/merge'

const fullHeightEditor = EditorView.theme({
    '&': { height: '100%' },
    '.cm-scroller': { height: '100%' }
})

$(_ => {
    // const view = new EditorView({
    //     doc: `#blablabla`,
    //     parent: $('.main>.content>.editor')[0],
    //     extensions: [
    //         basicSetup,
    //         fullHeightEditor,
    //         python(),
    //         vsCodeDark,
    //         unifiedMergeView({ original: '#bleblabla' })
    //     ]
    // })
})

export const create_editor_content = (originalContent, changedContent) => {
        const ev = new EditorView({
            doc: changedContent,
            extensions: [
                basicSetup,
                fullHeightEditor,
                python(),
                vsCodeDark,
                unifiedMergeView({ original: originalContent })
            ]
        });
    return ev
};
