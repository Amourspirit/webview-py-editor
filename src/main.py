import sys
import webview
import jedi
import json
from menu_sample import menu_items
from pathlib import Path


# https://pywebview.flowrl.com/guide/api.html#webview-settings

webview.settings = {
    "ALLOW_DOWNLOADS": False,
    "ALLOW_FILE_URLS": True,
    "OPEN_EXTERNAL_LINKS_IN_BROWSER": True,
    "OPEN_DEVTOOLS_IN_DEBUG": False,
}


class Api:
    def __init__(self):
        self._window = None

    def set_window(self, window: webview.Window):
        self._window = window

    def destroy(self):
        if self._window:
            self._window.destroy()
        self._window = None
        sys.exit()

    def log(self, value):
        code = self._window.evaluate_js("getCode()")
        print("Code:\n{}".format(code))

    def get_autocomplete(self, code, line, column):
        try:
            code = self._window.evaluate_js("getCode()")
            print("code:\n", code)
            script = jedi.Script(code, path="")
            print("script:\n", script)
            completions = script.complete(line, column)
            suggestions = [completion.name for completion in completions]
            print()
            print("Suggestions:\n", suggestions)
            return json.dumps(suggestions)
        except Exception:
            return json.dumps([])


def find_src_dir():
    current_path = Path.cwd()
    while current_path != current_path.root:
        if (current_path / "src").exists():
            return current_path / "src"
        current_path = current_path.parent
    return None


def set_code(window: webview.Window):
    code = "# Write your code here! \n# \\'"
    escaped_code = json.dumps(code)  # Escape the string for JavaScript
    print(escaped_code)
    window.evaluate_js(f"setCode({escaped_code})")


def main():
    api = Api()
    window = webview.create_window(
        title="Python Editor",
        url=Path(find_src_dir() / "html/index.html").as_uri(),
        js_api=api,
    )
    api.set_window(window)
    webview.start(set_code, (window,), gui="qt", menu=menu_items)
    print("Ended Webview")


if __name__ == "__main__":
    main()
