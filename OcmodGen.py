import sublime
import sublime_plugin

class CreateOcmodFileModifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        full_path = view.file_name()

        if not full_path:
            return

        # 1. Переворачиваем слеши
        path = full_path.replace('\\', '/')

        # 2. Отрезаем всё до admin/ или catalog/
        # Проверяем оба варианта и оставляем хвост
        if 'admin/' in path:
            path = 'admin/' + path.split('admin/', 1)[1]
        elif 'catalog/' in path:
            path = 'catalog/' + path.split('catalog/', 1)[1]
        else:
            # Если это системный файл или другой, берем как есть, 
            # но слеши уже исправлены выше
            pass

        # 3. Берем текст (выделенный или всю строку)
        sel = view.sel()[0]
        if sel.empty():
            line_region = view.line(sel)
        else:
            line_region = sel
            
        search_text = view.substr(line_region).strip()

        # 4. Формируем XML OCMOD
        ocmod_template = (
            f'<file path="{path}">\n'
            f'    <operation>\n'
            f'        <search><![CDATA[{search_text}]]></search>\n'
            f'        <add position="after"><![CDATA[\n'
            f'            \n'
            f'        ]]></add>\n'
            f'    </operation>\n'
            f'</file>'
        )

        sublime.set_clipboard(ocmod_template)