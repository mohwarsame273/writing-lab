import React, { useMemo } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { EditorView, Decoration } from '@codemirror/view';
import { StateField, StateEffect } from '@codemirror/state';

export default function DiagnosticEditor({ value, on_change, diagnostics, placeholder, className, style }) {
  const diagnosticTheme = useMemo(() => {
    return EditorView.theme({
      ".cm-diagnostic-high": { textDecoration: "underline wavy red" },
      ".cm-diagnostic-medium": { textDecoration: "underline wavy orange" },
      ".cm-diagnostic-low": { textDecoration: "underline wavy #d97706" } // yellow-600
    });
  }, []);

  const diagnosticExtension = useMemo(() => {
    if (!diagnostics || diagnostics.length === 0) {
      return [];
    }

    const marks = diagnostics.map(d => {
      let markClass = "cm-diagnostic-low";
      if (d.severity === "high") markClass = "cm-diagnostic-high";
      if (d.severity === "medium") markClass = "cm-diagnostic-medium";

      return Decoration.mark({ class: markClass }).range(d.start, d.end);
    });

    marks.sort((a, b) => a.from - b.from);

    const diagnosticField = StateField.define({
      create() {
        return Decoration.set(marks);
      },
      update(decorations, tr) {
        return Decoration.set(marks);
      },
      provide: f => EditorView.decorations.from(f)
    });

    return [diagnosticField, diagnosticTheme];
  }, [diagnostics, diagnosticTheme]);

  return (
    <div style={style} className={className}>
      <CodeMirror
        value={value}
        onChange={on_change}
        extensions={[diagnosticExtension]}
        placeholder={placeholder}
        basicSetup={{
          lineNumbers: false,
          foldGutter: false,
          highlightActiveLine: false,
          autocompletion: false,
        }}
        theme="light"
      />
    </div>
  );
}
