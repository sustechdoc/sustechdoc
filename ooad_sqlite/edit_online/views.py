# -*-coding:utf-8 -*-
import codecs
import shutil
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm
import hashlib
from xhtml2pdf import pisa
from latex_pdf_compiler import LatexPdf
from markdown2html import Markdown2html
from django.template.loader import render_to_string
from django.http import HttpResponse
import urllib
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import json
from directory_utils import Directory
from os import listdir, mkdir
from os.path import isfile, splitext


def initial(request):
    try:
        if (request.session['is_login'] != None):
            cur_user = request.session['user_id']
            # try:
            # user_pro = models.Project.objects.all().values_list('creator_id', 'project_name', 'project_id')
            user_pro = models.Project.objects.filter(creator_id=cur_user)
            print(user_pro)
            all_pro = []
            for up in user_pro:
                all_pro.append((up.project_name, up.project_id))

            user_pro2 = models.Authorize.objects.filter(user_id=cur_user)
            all_pro2 = []
            for up in user_pro2:
                temp_pro = up.project_id
                temp_name = models.Project.objects.get(project_id=temp_pro)
                temp_name = temp_name.project_name
                all_pro2.append((temp_name, temp_pro))

            # all_pro = []
            # for i in range(0, len(user_pro)):
            #     all_pro.append((user_pro[i][1], user_pro[i][2]))

            # except:
            #     print("2222")
            return render(request, 'login/initial.html', {'pro_names': all_pro, 'pro_names2': all_pro2})
        else:
            return render(request, 'login/initial.html')
    except KeyError:
        return render(request, 'login/initial.html')


def index(request, project_id):
    # print("come index")
    user_pro = models.Project.objects.get(project_id=project_id)
    request.session["cur_type"] = user_pro.type
    cur_pro_name = user_pro.project_name
    real_pro_name = str(user_pro.creator_id) + '_' + cur_pro_name
    request.session['cur_project'] = project_id
    cur_dir = Directory('./Projects/' + real_pro_name + '/')
    request.session["cur_base"] = './Projects/' + real_pro_name + '/'
    # cur_dir.create_folder('test1')
    all_url = [(0, "root")]
    files_list = cur_dir.get_files_and_folders()
    return render(request, 'login/index.html', {'file_names': files_list, "url": all_url})


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            userid = login_form.cleaned_data['userid']
            password = login_form.cleaned_data['password']

            try:

                user = models.Users.objects.get(user_id=userid)

                if user.user_password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.user_id
                    request.session['user_name'] = user.user_name
                    return redirect('/initial/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            userid = register_form.cleaned_data['userid']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.Users.objects.filter(user_id=userid)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.Users.objects.filter(user_email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())
                same_phone_user = models.Users.objects.filter(user_phone=phone)
                if same_phone_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.Users.objects.create(user_id=userid, user_phone=phone,
                                                       user_password=hash_code(password1))
                new_user.user_id = userid
                new_user.user_name = username

                new_user.user_phone = phone
                new_user.user_email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        print('here1')
        # 如果本来就未登录，也就没有登出一说
        return redirect("/initial")

    request.session.flush()

    ''' request.session['is_login'] = False
    request.session['user_id'] = None
    request.session['user_name'] = None
    request.session['cur_project'] = None'''
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/initial")


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def creat_file(request):
    try:
        if_exist = models.Project.objects.get(creator_id=request.session["user_id"],
                                              project_id=request.session["cur_project"])
        cur_url = request.POST["position"]
        print(cur_url)
        cur_url = cur_url[4:]
        file_name = request.POST['name']
        if (file_name == ''):
            return HttpResponse(json.dumps({"is_ok": True}))
        print(file_name)
        # temp = models.Project.objects.get(project_id=request.session["cur_project"])
        base_url = request.session['cur_base'] + cur_url + "/"

        if (request.session["cur_type"] == "md"):
            file = open(base_url + file_name + '.md', 'w')
            file.write('this is your txt')
            file.close()
        else:
            mode_type = "main" + request.POST["mode"] + ".tex"
            temp_con = ""
            print('modetype {}'.format(mode_type))
            file = open("./tex_mode/" + mode_type, 'r')
            temp_con = file.read()
            file.close()
            file = open(base_url + file_name + '.tex', 'w')
            file.write(temp_con)
            file.close()
        print(base_url)
        print('creat_file succeed')
        return HttpResponse(json.dumps({"is_ok": True}))
    except KeyError:
        file = open(base_url + file_name)
        # file.write(temp_con)
        file.close()
        print('creat_file succeed')
        return HttpResponse(json.dumps({"is_ok": True}))
    except models.Project.DoesNotExist:
        if_exist = models.Authorize.objects.get(user_id=request.session["user_id"],
                                                project_id=request.session["cur_project"])
        if (if_exist.can_write == 0):
            return HttpResponse(json.dumps({"is_ok": False}))
        cur_url = request.POST["position"]
        print(cur_url)
        cur_url = cur_url[4:]
        file_name = request.POST['name']
        if (file_name == ''):
            return HttpResponse(json.dumps({"is_ok": True}))
        print(file_name)
        # temp = models.Project.objects.get(project_id=request.session["cur_project"])
        base_url = request.session['cur_base'] + cur_url + "/"

        if (request.session["cur_type"] == "md"):
            file = open(base_url + file_name + '.md', 'w')
            file.write('this is your txt')
            file.close()
        else:
            mode_type = "main" + request.POST["mode"] + ".tex"
            temp_con = ""
            file = open("./tex_mode/" + mode_type, 'r')
            temp_con = file.read()
            file.close()
            file = open(base_url + file_name + '.tex', 'w')
            file.write(temp_con)
            file.close()
        print(base_url)
        print('creat_file succeed')
        return HttpResponse(json.dumps({"is_ok": True}))


def creat_fold(request):
    try:
        if_exist = models.Project.objects.get(creator_id= request.session["user_id"] , project_id= request.session["cur_project"])
        cur_url = request.POST["position"]
        print(cur_url)
        cur_url = cur_url.strip('root/')
        file_name = request.POST['name']
        if (file_name == ''):
            return HttpResponse(json.dumps({"is_ok": True}))
        print(file_name)
        now_pro = models.Project.objects.get(project_id=request.session["cur_project"])
        base_url = request.session['cur_base'] + cur_url + "/"
        cur_dir = Directory(base_url)
        print(base_url)
        cur_dir.create_folder(file_name)

        print('creat_fold succeed')
        return HttpResponse(json.dumps({"is_ok": True}))
    except models.Project.DoesNotExist:
        if_exist = models.Authorize.objects.get(user_id=request.session["user_id"],
                                                project_id=request.session["cur_project"])
        if (if_exist.can_write == 0):
            return HttpResponse(json.dumps({"is_ok": False}))
        cur_url = request.POST["position"]
        print(cur_url)
        cur_url = cur_url.strip('root/')
        file_name = request.POST['name']
        if (file_name == ''):
            return HttpResponse(json.dumps({"is_ok": True}))
        print(file_name)
        now_pro = models.Project.objects.get(project_id=request.session["cur_project"])
        base_url = request.session['cur_base'] + cur_url + "/"
        cur_dir = Directory(base_url)
        print(base_url)
        cur_dir.create_folder(file_name)

        print('creat_fold succeed')
        return HttpResponse(json.dumps({"is_ok": True}))


def save_file(request):
    try:
        if_exist = models.Project.objects.get(project_id= request.session["cur_project"])
        # assert if_exist.creator_id==request.session["user_id"]
        file_content = request.POST['file_con']
        if request.session["cur_type"] == "tex":
            # write to the temp tex file
            file = open('./test1/test1.tex', 'w')
            file.write(file_content)
            file.close()
            #
            file = open(request.session["cur_file"], 'w')
            file.write(file_content)
            file.close()
            # copy file and folders
            # request.session["cur_base"] = './Projects/' + real_pro_name + '/'

            cur_base = request.session["cur_file"]
            print('cur_base')
            print(cur_base)
            file_name = cur_base.split('/')[-1]
            dir_path = '/home/ubuntu/ooad_sqlite/'+cur_base.strip(file_name).strip('/')
            test_project = LatexPdf('xelatex', dir_path, file_name)
            print('tex file list:')
            print(test_project.get_tex_files_list())
            print('file and folder list:')
            print(test_project.get_files_and_folders())
            test_project.build_pdf()
            compile_state, output_path, log_str = test_project.get_response()
            printPDF(request)
            import os
            files = os.listdir(dir_path)
            del_suffix = ['fdb_latexmk','lof','lot','blg','fls','toc', 'vrb', 'aux', 'nav', 'out', 'snm', 'synctex.gz']
            for file in files:
                for suffix in del_suffix:
                    if file.endswith(suffix):
                        os.remove(dir_path+'/'+file)
            pdf_rel_dir = request.session["cur_file"].strip('tex')+'pdf'
            print('pdfrel{}'.format(pdf_rel_dir))
            return HttpResponse(json.dumps({"is_ok":True,"which_type": "tex", 'if': compile_state, 'err': log_str, 'pdf_dir':pdf_rel_dir}))
        else:
            print(file_content)
            file = open(request.session["cur_file"], 'w')
            file.write(file_content)
            file.close()
            return HttpResponse(json.dumps({"is_ok":True,"which_type": "md"}))
    except models.Project.DoesNotExist:
        print('user_id {} proj_id {}'.format(request.session["user_id"], request.session["cur_project"]))
        if_exist = models.Authorize.objects.get(user_id=request.session["user_id"],
                                                project_id=request.session["cur_project"])
        if (if_exist.can_write == 0):
            return HttpResponse(json.dumps({"is_ok":False}))
        printPDF(request)
        file_content = request.POST['file_con']
        if request.session["cur_type"] == "tex":
            # write to the temp tex file
            file = open('./test1/test1.tex', 'w')
            file.write(file_content)
            file.close()
            #
            file = open(request.session["cur_file"], 'w')
            file.write(file_content)
            file.close()
            # copy file and folders
            # request.session["cur_base"] = './Projects/' + real_pro_name + '/'

            cur_base = request.session["cur_file"]
            print('cur_base')
            print(cur_base)
            file_name = cur_base.split('/')[-1]
            dir_path = '/home/ubuntu/ooad_sqlite/' + cur_base.strip(file_name).strip('/')
            test_project = LatexPdf('xelatex', dir_path, file_name)
            print('tex file list:')
            print(test_project.get_tex_files_list())
            print('file and folder list:')
            print(test_project.get_files_and_folders())
            test_project.build_pdf()
            compile_state, output_path, log_str = test_project.get_response()
            printPDF(request)
            import os
            files = os.listdir(dir_path)
            del_suffix = ['fdb_latexmk', 'lof', 'lot', 'blg', 'fls', 'toc', 'vrb', 'aux', 'nav', 'out', 'snm',
                          'synctex.gz']
            for file in files:
                for suffix in del_suffix:
                    if file.endswith(suffix):
                        os.remove(dir_path + '/' + file)
            pdf_rel_dir = request.session["cur_file"].strip('tex') + 'pdf'
            print('pdfrel{}'.format(pdf_rel_dir))
            return HttpResponse(json.dumps(
                {"is_ok": True, "which_type": "tex", 'if': compile_state, 'err': log_str, 'pdf_dir': pdf_rel_dir}))
        else:
            print(file_content)
            file = open(request.session["cur_file"], 'w')
            file.write(file_content)
            file.close()
            return HttpResponse(json.dumps({"is_ok":True,"which_type": "md"}))
    # succeed=compile_state
    # markdown
    # test_project = Markdown2html('test_md', 'test.md')
    # md_html = test_project.get_html()
    # print(test_project.get_html())
    # return render(request, 'login/index.html',{'b':json.dumps({ 'flag':156, 'file_con': 456 ,})})


def downPDF(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf', charset='utf-8')
    response['Content-Disposition'] = 'attachment; filename=../test1.pdf'
    return response


def printPDF(request):
    now_file_pdf = request.session["cur_file"].strip('tex')+'pdf'
    response = FileResponse(open(now_file_pdf, 'rb'), content_type='application/pdf')
    return response


def update_md(request):
    md_data = request.POST["md_data"]
    print(md_data)

    with codecs.open('./test_md/test.md', 'w', encoding='utf-8') as file:
        file.write(md_data)
        file.close()
    test_project = Markdown2html('test_md', 'test.md')
    md_html = test_project.get_html()
    return HttpResponse(md_html)


def creat_project(request):
    cur_dir = Directory("./Projects/")
    creator_id = request.session['user_id']
    project_name = request.POST['name']
    if (project_name == ''):
        return render(request, 'login/initial.html', locals())
    type = request.POST['type']

    new_pro = models.Project.objects.create(project_name=project_name, creator_id=creator_id, type=type)
    proname = str(creator_id) + '_' + project_name
    cur_dir.create_folder(proname)
    return render(request, 'login/initial.html', locals())


# return render(request, 'login/register.html', locals())

# def open_fold(request):
#     temp_path = request.POST['fold_dir']
#     print(temp_path)
#     cur_base = './Projects/' + str(request.session["user_id"]) + "_" + request.session["cur_project"] + "/"
#     request.session['cur_base'] = cur_base
#     print(cur_base)
#     cur_url = cur_base + temp_path
#     cur_dir = Directory(cur_url)
#     # cur_dir.create_folder('test1')
#     files_list = cur_dir.get_files_and_folders()
#     print(files_list)
#     return HttpResponse(json.dumps({'data': files_list, }))


def open_cur_pro_fold(request):
    dir_path = request.POST['url_list']
    dir_list = dir_path.split('/')
    print(dir_list)
    dir_list.pop(0)
    dir_list.pop(0)
    if len(dir_list) != 0:
        dir_list[-1] = dir_list[-1].split(' ')[-1]
    print(dir_list)
    # dir_path = dir_path[7:]
    cur_base = request.session['cur_base']
    list2path = cur_base
    for i in dir_list:
        list2path += i + '/'

    list2path = list2path[:-1]
    print(list2path)
    if not isfile(list2path):
        return_url_list = [(0, 'root')]
        i = 1
        for dl in dir_list:
            return_url_list.append((i, dl))
            i += 1
        diro = Directory(list2path + "/")
        return_ff_list = diro.get_files_and_folders()
        #  return render(request, 'login/index.html', {'is_file': False, 'url': return_url_list, 'file_names': return_ff_list, 'content': None})
        # return render(request, 'login/index.html', {'file_names': files_list, "url": all_url})
        return HttpResponse(
            json.dumps({'is_file': False, 'url': return_url_list, 'file_names': return_ff_list, 'content': None}))
    else:
        request.session["cur_file"] = list2path
        with codecs.open(list2path, "r", encoding='utf-8') as f:
            file = f.read()
        print(file)
        request.session["cur_edit_file"] = list2path
        return HttpResponse(json.dumps({"is_file": True, 'content': file}))
    # cur_diro = Directory(cur_base)

    # return HttpResponse(142)


def upload(request):
    '''
    :param request: dir_path example: test/file.zip or test1/test2/file.tex; bit_stream;
    :return: nothing
    '''
    try:
        if_exist = models.Project.objects.get(creator_id= request.session["user_id"] , project_id= request.session["cur_project"])
        cur_base = request.session['cur_base']
        dir_path = request.POST.get("position")
        dir_path = dir_path.replace('root/', '')
        print(dir_path)
        bit_stream = request.FILES.get('upload_file')
        file_name = dir_path + request.POST.get("file_name")
        print("upload file name:" + file_name)
        # file_name = dir_path.split('/')[-1]
        post_fix = splitext(file_name)[-1]
        no_file_dir = cur_base + dir_path.strip(file_name)
        print(no_file_dir)
        diro = Directory(no_file_dir)
        # print(post_fix)
        if post_fix == '.zip':
            zip_path = './Temp/zips/'
            with open(zip_path + file_name, 'wb') as zip_file:

                for chunk in bit_stream.chunks():
                    zip_file.write(chunk)
            diro.unzip(file_name, no_file_dir)
        else:
            print((no_file_dir + file_name))
            with open((no_file_dir + file_name), 'wb') as common_file:
                for chunk in bit_stream.chunks():
                    common_file.write(chunk)
        print('success')
        return HttpResponse(json.dumps({"is_ok":True}))
    except:
        if_exist = models.Authorize.objects.get(user_id= request.session["user_id"] , project_id=request.session["cur_project"])
        if(if_exist.can_write == 0):
            return HttpResponse(json.dumps({"is_ok": False}))
        cur_base = request.session['cur_base']
        dir_path = request.POST.get("position")
        dir_path = dir_path.replace('root/', '')
        print(dir_path)
        bit_stream = request.FILES.get('upload_file')
        file_name = dir_path + request.POST.get("file_name")
        print("upload file name:" + file_name)
        # file_name = dir_path.split('/')[-1]
        post_fix = splitext(file_name)[-1]
        no_file_dir = cur_base + dir_path.strip(file_name)
        print(no_file_dir)
        diro = Directory(no_file_dir)
        # print(post_fix)
        if post_fix == '.zip':
            zip_path = './Temp/zips/'
            with open(zip_path + file_name, 'wb') as zip_file:

                for chunk in bit_stream.chunks():
                    zip_file.write(chunk)
            diro.unzip(file_name, no_file_dir)
        else:
            print((no_file_dir + file_name))
            with open((no_file_dir + file_name), 'wb') as common_file:
                for chunk in bit_stream.chunks():
                    common_file.write(chunk)
        print('success')
        return HttpResponse(json.dumps({"is_ok": True}))





def delete(request):
    # ./Project/11713021_test/
    cur_base = request.session['cur_base']
    # root/test1/test2/
    dir_path = request.POST.get("position")
    dir_path = dir_path.replace('root/', '')
    print(dir_path)
    ff_name = dir_path + request.POST.get("ff_name")
    post_fix = splitext(ff_name)[-1]
    no_file_dir = cur_base + dir_path.strip(ff_name)
    print(no_file_dir)
    diro = Directory(no_file_dir)
    if isfile(no_file_dir + ff_name):
        diro.delete_file(ff_name)
    else:
        diro.delete_folder(ff_name)
    return HttpResponse("sfsdf")


def invite(request):
    try:
        if_exist = models.Project.objects.get(creator_id=request.session["user_id"],
                                              project_id=request.session["cur_project"])
        invited = int(request.POST["invited"])
        right = int(request.POST["right"])
        try:
            print("cunzai")
            user_pro = models.Users.objects.get(user_id=invited)
          #  pro_info = models.Project.objects.get(project_id=request.session['cur_project'])
            print("cun")
           # pro_id = pro_info.project_id
          #  print(pro_id)
            try:
                new_pro = models.Authorize.objects.create(project_id=request.session["cur_project"], user_id=user_pro.user_id, can_write = right)
                return HttpResponse(json.dumps({"is_oo":True,"is_ok": 0}))
            except:
                return HttpResponse(json.dumps({"is_oo":True,"is_ok": 1}))

        except:
            return HttpResponse(json.dumps({"is_oo":True,"is_ok": 2}))
    except:
        return HttpResponse(json.dumps({"is_oo":False}))



