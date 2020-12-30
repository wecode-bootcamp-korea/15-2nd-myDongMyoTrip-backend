def message(domain, uidb64, access_token):
    return f'아래 링크를 클릭해서 회원가입을 완료해주세요. \n\n회원가입 링크: http://{domain}/user/activate/{uidb64}/{access_token}\n\n쌩유베리머치!'
