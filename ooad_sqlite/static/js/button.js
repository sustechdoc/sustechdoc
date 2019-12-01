function onClickAddRegis() {

    let id = document.querySelector('form input[name="user_id"]').value;
    let name = document.querySelector('form input[name="user_name"]').value;
    let password = document.querySelector('form input[name = "user_password"').value;
    let phone = document.querySelector('form input[name="user_phone"]').value;
    let email = document.querySelector('form input[name="user_email"]').value;

    if (validInput(id , name ,password, phone , email)){
        //注册成功
        alert("成功注册！")
        //返回登录页面
        back()
    }
}

function back(){

}

function validInput(id, name , password,phone, email){
    let id_form = new RegExp (/^[1-9]{8,8}$/)
    let phone_form = new RegExp(/^1[3456789]\d{9}$/)
    let email_form = new RegExp(/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/);
    if (! id_form.test(id)){
        alert("The id format is wrong!")
        return false
    }

    if ( name == null){
        alert("Your name is need to input!")
        return false
    }
    if ( password == null ){
        alert("Your password is need to input!")
        return false
    }
    if ( password.length < 6){
        alert("Your password should be at least six char")
        return false
    }
    if( ! phone_form.test(phone)){
        alert("The phone format is wrong!")
        return false
    }
    if(! email_form.test(email)){
        alert("The email format is wrong!")
        return false
    }
    return true
}

function back(){

}