# import unittest
from latex_pdf_compiler import LatexPdf
from markdown2html import Markdown2html
from directory_utils import Directory

"""
实例化LatexPdf时即会创建对应路径
TODO 创建对应文档
"""
# TODO if no this file?
test_project = LatexPdf('xelatex', 'test1', 'test1.tex')
print('tex file list:')
print(test_project.get_tex_files_list())
print('file and folder list:')
print(test_project.get_files_and_folders())
test_project.build_pdf()
compile_state, output_path, log_str = test_project.get_response()
if compile_state:
    print('pdf directory is {}'.format(output_path))
else:
    print('compile failed')
    print('compile log is {}'.format(log_str))

# class TestCompiler(unittest.TestCase):
#     def test_latex(self):
#         """
#         实例化LatexPdf时即会创建对应路径
#         TODO 创建对应文档
#         """
#         # TODO if no this file?
#         test_project = LatexPdf('xelatex', 'test_bib', 'lab_report_1.tex')
#         print('tex file list:')
#         print(test_project.get_tex_files_list())
#         print('file and folder list:')
#         print(test_project.get_files_and_folders())
#         test_project.build_pdf()
#         compile_state, output_path, log_str = test_project.get_response()
#         if compile_state:
#             print('pdf directory is {}'.format(output_path))
#         else:
#             print('compile failed')
#             print('compile log is {}'.format(log_str))

    # def test_markdown(self):
    #     # markdown
    #     test_project = Markdown2html('test_md', 'test.md')
    #     print(test_project.get_html())

    # def test_directory(self):
    #
    #     # test delete and create
    #     cur_dir = Directory('./')
    #     cur_dir.delete_folder('no')
    #     # cur_dir.delete_folder('yes')
    #     cur_dir.create_folder('yes')
    #
    #     cur_dir.rename_ff('yes', 'no')
    #     # cur_dir.rename_ff('asd1', 'asd')
    #     # cur_dir.copy_file('db.sqlite3')
    #     # cur_dir.copy_folder('test_md')
    #     # cur_dir.delete_file('asdas')
    #     # cur_dir.delete_folder('yes')




# if __name__ == '__main__':
#     unittest.main()
