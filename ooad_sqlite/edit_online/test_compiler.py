from latex_pdf_compiler import LatexPdf
from markdown2html import Markdown2html
'''这是使用样例'''
'''
实例化LatexPdf时即会创建对应路径
TODO 创建对应文档
'''
# latex
# TODO if no this file?
test_project = LatexPdf('xelatex','test1','test1.tex')
print('tex file list:')
print(test_project.get_tex_files_list())
print('file and folder list:')
print(test_project.get_files_and_folders())
test_project.build_pdf()
compile_state,output_path,log_str=test_project.get_response()
if compile_state:
    print('pdf directory is {}'.format(output_path))
else:
    print('compile failed')
    print('compile log is {}'.format(log_str))


# markdown
test_project = Markdown2html('test_md','test.md')
print(test_project.get_html())