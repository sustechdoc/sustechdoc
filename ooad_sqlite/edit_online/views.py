# -*-coding:utf-8 -*-
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm,RegisterForm
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
def index(request):
    if request.method == 'POST':
        flag = int(request.POST['flag'])
        if(flag == 0):
            print(flag)
            creat_file(request)
        if(flag == 1):
            save_file(request)

    pass
    return render(request, 'login/index.html')

succeed = True
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
                    return redirect('/index/')
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

                new_user = models.Users.objects.create(user_id = userid , user_phone = phone , user_password = hash_code(password1))
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
        return redirect("/index/")

    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def creat_file(request):
    file_name = request.POST['name']
    print(file_name)
    file = open('D:\\Study\\OOAD\\SUSTECH_DOC\\new_files\\'+ file_name + '.txt','w')
    file.write('this is your txt')
    return render(request, 'login/index.html')

def save_file(request):
    printPDF(request)
    file_content = request.POST['file_con']
    file = open('./test1/test1.tex' , 'w')
    file.write(file_content)
    file.close()
    # compile the txt to latex
    test_project = LatexPdf('xelatex', 'test1', 'test1.tex')
    print('tex file list:')
    print(test_project.get_tex_files_list())
    print('file and folder list:')
    print(test_project.get_files_and_folders())
    test_project.build_pdf()
    compile_state, output_path, log_str = test_project.get_response()
    #succeed=compile_state
    # markdown
    #test_project = Markdown2html('test_md', 'test.md')
    #md_html = test_project.get_html()
   # print(test_project.get_html())
   # return render(request, 'login/index.html',{'b':json.dumps({ 'flag':156, 'file_con': 456 ,})})
    return HttpResponse(json.dumps({ 'if':compile_state,'err':log_str,}))
def downPDF(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf',charset = 'utf-8')
    response['Content-Disposition'] = 'attachment; filename=../test1.pdf'
    return response

def printPDF(request):
    if succeed:
        response = FileResponse(open('./test1/test1.pdf', 'rb'), content_type='application/pdf')
        return response
