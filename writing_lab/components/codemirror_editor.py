import reflex as rx

class CodeMirrorEditor(rx.NoSSRComponent):
    library = "$/public/DiagnosticEditor.jsx"
    tag = "DiagnosticEditor"
    is_default = True
    
    lib_dependencies: list[str] = [
        "@uiw/react-codemirror",
        "@codemirror/view",
        "@codemirror/state",
        "@codemirror/language"
    ]

    value: rx.Var[str]
    diagnostics: rx.Var[list[dict]]
    placeholder: rx.Var[str]
    on_change: rx.EventHandler[lambda text: [text]]

cm_editor = CodeMirrorEditor.create
