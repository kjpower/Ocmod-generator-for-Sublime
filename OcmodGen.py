import sublime
import sublime_plugin
import os

class CreateOcmodFileModifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()
        if not file_path:
            sublime.error_message("Ошибка: Сначала сохраните файл!")
            return

        # Определяем относительный путь файла
        relative_path = file_path
        folders = self.view.window().folders()
        for folder in folders:
            if file_path.startswith(folder):
                relative_path = os.path.relpath(file_path, folder)
                break
        
        # Очистка пути от префиксов (например, для OpenCart 3/4)
        prefixes_to_strip = ["upload/", "src/"]
        for prefix in prefixes_to_strip:
            if relative_path.startswith(prefix):
                relative_path = relative_path[len(prefix):]

        for region in self.view.sel():
            if not region.empty():
                selected_text = self.view.substr(region)
                
                # Формируем структуру OCMOD
                ocmod_block = (
                    f'<file path="{relative_path}">\n'
                    '    <operation>\n'
                    f'        <search><![CDATA[{selected_text}]]></search>\n'
                    f'        <add position="replace"><![CDATA[{selected_text}]]></add>\n'
                    '    </operation>\n'
                    '</file>'
                )
                self.view.replace(edit, region, ocmod_block)

    # Пункт меню будет активен только если выделен текст
    def is_enabled(self):
        return any(not r.empty() for r in self.view.sel())
