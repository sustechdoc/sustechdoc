from my_latex import latex
from my_latex.latex.exc import LatexBuildError
from directory_utils import Directory
class LatexPdf:
    compiler = 'xelatex' # default compiler
    project_name = 'test1' # TODO 处理空格
    main_document = 'test.tex'
    __compiler_list = ['xelatex','lualatex','pdflatex','latex']
    __project_path = './'+project_name+'/'
    __latex_path = __project_path + main_document
    __output_path = ''
    __compile_state = True
    __logs = ''
    def __init__(self, compiler, project_name, main_document):
        try:
            assert compiler in self.__compiler_list
        except AssertionError:
            print('Compiler is not support!')
        self.compiler = compiler
        self.project_name = project_name
        self.main_document = main_document
        self.__project_path = self.project_name
        self.__latex_path = self.__project_path+'/'
        self.__output_path = self.__project_path+'{}.pdf'.format(main_document)
        self.__directory = Directory(self.__project_path)

        # self.__compile_state = True
        # self.__logs = ''
        # self.__log_path = './'+project_name+'/'+'{}.log'.format(project_name)

    def get_tex_files_list(self):
        return self.__directory.get_tex_files_list()

    def get_files_and_folders(self):
        return self.__directory.get_files_and_folders()

    def build_pdf(self):
        builder = latex.build.LatexMkBuilder(pdflatex=self.compiler)
        try:
            pdf = builder.build_pdf(self.__latex_path, self.main_document)
            pdf.save_to(self.__output_path)
        except LatexBuildError as e:
            print('compile failed')
            self.__compile_state = False
            for err in e.get_errors():
                err_str = ''
                location = 'Error in {0[filename]}, line {0[line]}: {0[error]}\r\n'.format(err)
                content = '    {}\r\n'.format(err['context'][1])
                err_str+=location
                err_str+=content
                self.__logs+=err_str
            print(len(self.__logs))
            print(self.__logs)

    def __get_log(self):
    #     log = open(self.__log_path,'r')
    #     log_text = log.read()
    #     log.close()
        return self.__logs

    def get_response(self):
        return self.__compile_state,self.__output_path,self.__get_log()
