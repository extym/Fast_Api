finland_url_reg = 'https://finlandvisa.fi/register'
email, code = '', ''
finland_url_reg_confirm = f'https://finlandvisa.fi/register/confirm?email={email}&code={code}'

form_email_xpath = '/html/body/div/div[2]/div[1]/div/div/form/div[1]/input'
form_pass_xpath = '/html/body/div/div[2]/div[1]/div/div/form/div[2]/input'
form_confirm_xpath = '/html/body/div/div[2]/div[1]/div/div/form/div[3]/input'
box_acc_for_trevel_company = '/html/body/div/div[2]/div[1]/div/div/form/div[4]/fieldset/div/div/input'
box_agree = '/html/body/div/div[2]/div[1]/div/div/form/div[5]/div[1]/fieldset/div/div/input'  #/html/body/div/div[2]/div[1]/div/div/form/div[5]/div[1]/fieldset/div/div/div/svg/path
box_agree_two = '/html/body/div/div[2]/div[1]/div/div/form/div[6]/div/div/fieldset/div/div/input'
bottom_xpath = '/html/body/div/div[2]/div[1]/div/div/form/button'
bottom_confirm_register_xpath = '/html/body/div/div[2]/div[1]/div/div/form/button'