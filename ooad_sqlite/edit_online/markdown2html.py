import markdown
import codecs
from directory_utils import Directory
class Markdown2html:
    project_name = 'test_md' # TODO 处理空格
    main_document = 'test.md'
    __project_path = './'+project_name+'/'
    __document_path = __project_path + main_document
    def __init__(self,project_name, main_document):
        self.project_name= project_name
        self.main_document= main_document
        self.__directory = Directory(self.__project_path)

    def get_html(self):
        input_file = codecs.open(self.__document_path, mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)
        return html