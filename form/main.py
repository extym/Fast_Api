# Import the following modules
# sudo apt install -y wkhtmltopdf
import datetime

from captcha.image import ImageCaptcha
import pdfkit
# import wkhtmltopdf
import templates
import uuid
import json
from flask import Flask, request, render_template
# from cred import user_id, user_secret
# from trap import access_token
import requests
# from cred import organization
from gevent.pywsgi import WSGIServer

# Create an image instance of the given size
image = ImageCaptcha(width=280, height=90)

# Image captcha text
captcha_text = 'FORMS'

# generate the image of the given text
data = image.generate(captcha_text)

# write the image on the given file and save it
image.write(captcha_text, 'CAPTCHA.png')

# create   the Flask app
app = Flask(__name__,
            # static_url_path='',
            static_folder='templates/c_files',
            template_folder='templates'
            )


@app.route('/', methods=['GET', 'POST'])
def example():
    date = datetime.date
    return render_template('index.html', date=date)


@app.route('/list', methods=['GET', 'POST'])
def get_list():
    date = datetime.date
    return render_template('list.html', date=date)

# @app.route('/list7', methods=['GET', 'POST'])
# def get_list7():
#     date = datetime.date
#     return render_template('list-info7.html', date=date)


@app.route('/blanks', methods=['GET', 'POST'])
def get_blanks():
    date = datetime.date
    return render_template('blanks.html', date=date)


@app.route('/phones', methods=['GET', 'POST'])
def phones():
    date = datetime.date
    return render_template('phones.html', date=date)


@app.route('/info', methods=['GET', 'POST'])
def info():
    date = datetime.date
    return render_template('info.html', date=date)


@app.route('/add-info', methods=['GET', 'POST'])
def add_info():
    date = datetime.date
    return render_template('add-info.html', date=date)


@app.route('/form2', methods=['GET', 'POST'])
def add_page():
    date = datetime.date
    return render_template('last.html', date=date)


@app.route('/form-2', methods=['GET', 'POST'])
def add_page_2():
    date = datetime.date
    return render_template('form-2.html', date=date)


@app.route('/form', methods=['GET', 'POST'])
def form_example():
    date = datetime.date
    return render_template('form-old.html', date=date)


# @app.route('/popup-list9', methods=['GET', 'POST'])
# def popup_list9():
#     date = datetime.date
#     return render_template('list-info9.html', date=date)
#
#
# @app.route('/popup-list8', methods=['GET', 'POST'])
# def popup_list8():
#     date = datetime.date
#     return render_template('list-info8.html', date=date)


@app.route('/form1', methods=['GET', 'POST'])
def form_ex():
    return '''<form method="POST">
    <!DOCTYPE  html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>АО-1</title>
        <meta name="generator" content="pdf2htmlEX"/>
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
<style type="text/css">
/*!
 * Base CSS for pdf2htmlEX
 * Copyright 2012,2013 Lu Wang <coolwanglu@gmail.com>
 * https://github.com/pdf2htmlEX/pdf2htmlEX/blob/master/share/LICENSE
 */#sidebar{position:absolute;top:0;left:0;bottom:0;width:250px;padding:0;margin:0;overflow:auto}#page-container{position:absolute;top:0;left:0;margin:0;padding:0;border:0}@media screen{#sidebar.opened+#page-container{left:250px}#page-container{bottom:0;right:0;overflow:auto}.loading-indicator{display:none}.loading-indicator.active{display:block;position:absolute;width:64px;height:64px;top:50%;left:50%;margin-top:-32px;margin-left:-32px}.loading-indicator img{position:absolute;top:0;left:0;bottom:0;right:0}}@media print{@page{margin:0}html{margin:0}body{margin:0;-webkit-print-color-adjust:exact}#sidebar{display:none}#page-container{width:auto;height:auto;overflow:visible;background-color:transparent}.d{display:none}}.pf{position:relative;background-color:white;overflow:hidden;margin:0;border:0}.pc{position:absolute;border:0;padding:0;margin:0;top:0;left:0;width:100%;height:100%;overflow:hidden;display:block;transform-origin:0 0;-ms-transform-origin:0 0;-webkit-transform-origin:0 0}.pc.opened{display:block}.bf{position:absolute;border:0;margin:0;top:0;bottom:0;width:100%;height:100%;-ms-user-select:none;-moz-user-select:none;-webkit-user-select:none;user-select:none}.bi{position:absolute;border:0;margin:0;-ms-user-select:none;-moz-user-select:none;-webkit-user-select:none;user-select:none}@media print{.pf{margin:0;box-shadow:none;page-break-after:always;page-break-inside:avoid}@-moz-document url-prefix(){.pf{overflow:visible;border:1px solid #fff}.pc{overflow:visible}}}.c{position:absolute;border:0;padding:0;margin:0;overflow:hidden;display:block}.t{position:absolute;white-space:pre;font-size:1px;transform-origin:0 100%;-ms-transform-origin:0 100%;-webkit-transform-origin:0 100%;unicode-bidi:bidi-override;-moz-font-feature-settings:"liga" 0}.t:after{content:''}.t:before{content:'';display:inline-block}.t span{position:relative;unicode-bidi:bidi-override}._{display:inline-block;color:transparent;z-index:-1}::selection{background:rgba(127,255,255,0.4)}::-moz-selection{background:rgba(127,255,255,0.4)}.pi{display:none}.d{position:absolute;transform-origin:0 100%;-ms-transform-origin:0 100%;-webkit-transform-origin:0 100%}.it{border:0;background-color:rgba(255,255,255,0.0)}.ir:hover{cursor:pointer}</style>
<style type="text/css">
/*!
 * Fancy styles for pdf2htmlEX
 * Copyright 2012,2013 Lu Wang <coolwanglu@gmail.com>
 * https://github.com/pdf2htmlEX/pdf2htmlEX/blob/master/share/LICENSE
 */@keyframes fadein{from{opacity:0}to{opacity:1}}@-webkit-keyframes fadein{from{opacity:0}to{opacity:1}}@keyframes swing{0{transform:rotate(0)}10%{transform:rotate(0)}90%{transform:rotate(720deg)}100%{transform:rotate(720deg)}}@-webkit-keyframes swing{0{-webkit-transform:rotate(0)}10%{-webkit-transform:rotate(0)}90%{-webkit-transform:rotate(720deg)}100%{-webkit-transform:rotate(720deg)}}@media screen{#sidebar{background-color:#2f3236;background-image:url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjNDAzYzNmIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDBMNCA0Wk00IDBMMCA0WiIgc3Ryb2tlLXdpZHRoPSIxIiBzdHJva2U9IiMxZTI5MmQiPjwvcGF0aD4KPC9zdmc+")}#outline{font-family:Georgia,Times,"Times New Roman",serif;font-size:13px;margin:2em 1em}#outline ul{padding:0}#outline li{list-style-type:none;margin:1em 0}#outline li>ul{margin-left:1em}#outline a,#outline a:visited,#outline a:hover,#outline a:active{line-height:1.2;color:#e8e8e8;text-overflow:ellipsis;white-space:nowrap;text-decoration:none;display:block;overflow:hidden;outline:0}#outline a:hover{color:#0cf}#page-container{background-color:#9e9e9e;background-image:url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjOWU5ZTllIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDVMNSAwWk02IDRMNCA2Wk0tMSAxTDEgLTFaIiBzdHJva2U9IiM4ODgiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=");-webkit-transition:left 500ms;transition:left 500ms}.pf{margin:13px auto;box-shadow:1px 1px 3px 1px #333;border-collapse:separate}.pc.opened{-webkit-animation:fadein 100ms;animation:fadein 100ms}.loading-indicator.active{-webkit-animation:swing 1.5s ease-in-out .01s infinite alternate none;animation:swing 1.5s ease-in-out .01s infinite alternate none}.checked{background:no-repeat url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3goQDSYgDiGofgAAAslJREFUOMvtlM9LFGEYx7/vvOPM6ywuuyPFihWFBUsdNnA6KLIh+QPx4KWExULdHQ/9A9EfUodYmATDYg/iRewQzklFWxcEBcGgEplDkDtI6sw4PzrIbrOuedBb9MALD7zv+3m+z4/3Bf7bZS2bzQIAcrmcMDExcTeXy10DAFVVAQDksgFUVZ1ljD3yfd+0LOuFpmnvVVW9GHhkZAQcxwkNDQ2FSCQyRMgJxnVdy7KstKZpn7nwha6urqqfTqfPBAJAuVymlNLXoigOhfd5nmeiKL5TVTV+lmIKwAOA7u5u6Lped2BsbOwjY6yf4zgQQkAIAcedaPR9H67r3uYBQFEUFItFtLe332lpaVkUBOHK3t5eRtf1DwAwODiIubk5DA8PM8bYW1EU+wEgCIJqsCAIQAiB7/u253k2BQDDMJBKpa4mEon5eDx+UxAESJL0uK2t7XosFlvSdf0QAEmlUnlRFJ9Waho2Qghc1/U9z3uWz+eX+Wr+lL6SZfleEAQIggA8z6OpqSknimIvYyybSCReMsZ6TislhCAIAti2Dc/zejVNWwCAavN8339j27YbTg0AGGM3WltbP4WhlRWq6Q/btrs1TVsYHx+vNgqKoqBUKn2NRqPFxsbGJzzP05puUlpt0ukyOI6z7zjOwNTU1OLo6CgmJyf/gA3DgKIoWF1d/cIY24/FYgOU0pp0z/Ityzo8Pj5OTk9PbwHA+vp6zWghDC+VSiuRSOQgGo32UErJ38CO42wdHR09LBQK3zKZDDY2NupmFmF4R0cHVlZWlmRZ/iVJUn9FeWWcCCE4ODjYtG27Z2Zm5juAOmgdGAB2d3cBADs7O8uSJN2SZfl+WKlpmpumaT6Yn58vn/fs6XmbhmHMNjc3tzDGFI7jYJrm5vb29sDa2trPC/9aiqJUy5pOp4f6+vqeJ5PJBAB0dnZe/t8NBajx/z37Df5OGX8d13xzAAAAAElFTkSuQmCC)}}</style>
<style type="text/css">
.ff0{font-family:sans-serif;visibility:hidden;}
@font-face{font-family:ff1;src:url('data:application/font-woff;base64,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')format("woff");}.ff1{font-family:ff1;line-height:0.931641;font-style:normal;font-weight:normal;visibility:visible;}
@font-face{font-family:ff2;src:url('data:application/font-woff;base64,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')format("woff");}.ff2{font-family:ff2;line-height:0.861328;font-style:normal;font-weight:normal;visibility:visible;}
.m0{transform:matrix(0.375000,0.000000,0.000000,0.375000,0,0);-ms-transform:matrix(0.375000,0.000000,0.000000,0.375000,0,0);-webkit-transform:matrix(0.375000,0.000000,0.000000,0.375000,0,0);}
.v0{vertical-align:0.000000px;}
.ls0{letter-spacing:0.000000px;}
.sc_{text-shadow:none;}
.sc0{text-shadow:-0.015em 0 transparent,0 0.015em transparent,0.015em 0 transparent,0 -0.015em  transparent;}
@media screen and (-webkit-min-device-pixel-ratio:0){
.sc_{-webkit-text-stroke:0px transparent;}
.sc0{-webkit-text-stroke:0.015em transparent;text-shadow:none;}
}
.ws0{word-spacing:0.000000px;}
._1d{margin-left:-1.076868px;}
._0{width:1.031936px;}
._c{width:18.437400px;}
._8{width:53.478096px;}
._19{width:60.504000px;}
._a{width:63.978176px;}
._7{width:64.991040px;}
._6{width:68.808000px;}
._13{width:74.708040px;}
._12{width:81.098744px;}
._1b{width:90.840000px;}
._4{width:94.684000px;}
._17{width:96.376608px;}
._2{width:120.035552px;}
._21{width:150.360832px;}
._d{width:163.783688px;}
._1{width:169.019328px;}
._20{width:192.255328px;}
._3{width:195.465064px;}
._15{width:199.575840px;}
._22{width:206.090848px;}
._14{width:227.371232px;}
._23{width:271.225696px;}
._18{width:272.604000px;}
._b{width:302.442240px;}
._5{width:369.816000px;}
._1c{width:381.013064px;}
._10{width:461.960616px;}
._11{width:469.228360px;}
._e{width:507.925944px;}
._9{width:513.570872px;}
._1f{width:596.992960px;}
._1e{width:608.734400px;}
._f{width:690.896280px;}
._16{width:725.401064px;}
._1a{width:1211.341600px;}
.fc0{color:rgb(0,0,0);}
.fs2{font-size:27.612000px;}
.fs4{font-size:31.656000px;}
.fs0{font-size:35.584000px;}
.fs1{font-size:39.624000px;}
.fs3{font-size:47.596000px;}
.fs5{font-size:63.196000px;}
.y0{bottom:-0.750000px;}
.y2c{bottom:5.725500px;}
.y2{bottom:5.766000px;}
.y5{bottom:5.809500px;}
.y4a{bottom:7.954500px;}
.y3f{bottom:7.996500px;}
.y38{bottom:92.103000px;}
.ya{bottom:129.565500px;}
.y3c{bottom:151.203000px;}
.y3b{bottom:169.050000px;}
.y3a{bottom:184.794000px;}
.y32{bottom:199.233000px;}
.y39{bottom:202.768500px;}
.y37{bottom:221.668500px;}
.y36{bottom:237.454500px;}
.y35{bottom:262.794000px;}
.y34{bottom:280.642500px;}
.y33{bottom:308.088000px;}
.y31{bottom:328.798500px;}
.y30{bottom:352.035000px;}
.y2f{bottom:369.883500px;}
.y2e{bottom:389.077500px;}
.y2d{bottom:406.926000px;}
.y2b{bottom:438.244500px;}
.y2a{bottom:455.671500px;}
.y29{bottom:473.520000px;}
.y28{bottom:511.320000px;}
.y27{bottom:535.483500px;}
.y26{bottom:554.383500px;}
.y25{bottom:573.283500px;}
.y24{bottom:592.183500px;}
.y48{bottom:595.510500px;}
.y23{bottom:629.691000px;}
.y46{bottom:630.028500px;}
.y22{bottom:648.885000px;}
.y21{bottom:667.786500px;}
.y44{bottom:676.837500px;}
.y20{bottom:686.686500px;}
.y1e{bottom:696.115500px;}
.y1f{bottom:705.586500px;}
.y42{bottom:706.809000px;}
.y43{bottom:708.787500px;}
.y49{bottom:719.058000px;}
.y1d{bottom:728.401500px;}
.y1c{bottom:759.594000px;}
.y47{bottom:761.530500px;}
.y1b{bottom:788.218500px;}
.y3d{bottom:791.418000px;}
.y1a{bottom:805.771500px;}
.y19{bottom:806.403000px;}
.y45{bottom:808.339500px;}
.y18{bottom:835.785000px;}
.y17{bottom:836.374500px;}
.y16{bottom:866.977500px;}
.y40{bottom:889.792500px;}
.y41{bottom:891.729000px;}
.y3e{bottom:914.923500px;}
.y15{bottom:920.689500px;}
.y14{bottom:943.168500px;}
.yb{bottom:957.018000px;}
.y12{bottom:963.289500px;}
.y13{bottom:971.245500px;}
.y11{bottom:989.220000px;}
.y10{bottom:991.618500px;}
.yf{bottom:1014.729000px;}
.ye{bottom:1033.629000px;}
.yd{bottom:1052.529000px;}
.yc{bottom:1070.841000px;}
.y9{bottom:1086.583500px;}
.y8{bottom:1103.674500px;}
.y7{bottom:1105.485000px;}
.y6{bottom:1124.385000px;}
.y4{bottom:1149.178500px;}
.y3{bottom:1165.848000px;}
.y1{bottom:1182.517500px;}
.h9{height:14.733000px;}
.h2{height:16.626000px;}
.h6{height:19.765230px;}
.h8{height:22.660008px;}
.h3{height:25.471750px;}
.ha{height:25.551000px;}
.hc{height:26.686500px;}
.h4{height:28.363664px;}
.h7{height:40.530969px;}
.hb{height:45.236980px;}
.h5{height:1069.578000px;}
.h0{height:1262.834646px;}
.h1{height:1263.750000px;}
.w4{width:27.949500px;}
.w5{width:56.322000px;}
.w3{width:70.002000px;}
.w7{width:490.527000px;}
.w2{width:817.558500px;}
.w6{width:822.694500px;}
.w0{width:892.955906px;}
.w1{width:894.000000px;}
.x0{left:0.000000px;}
.xa{left:2.316000px;}
.x1{left:63.688500px;}
.x14{left:66.594000px;}
.x25{left:74.718000px;}
.x1b{left:80.695500px;}
.x18{left:113.403000px;}
.x27{left:125.568000px;}
.xf{left:136.638000px;}
.x29{left:152.761500px;}
.x28{left:157.138500px;}
.x2a{left:160.042500px;}
.x1a{left:211.945500px;}
.x2b{left:213.544500px;}
.x8{left:217.039500px;}
.x19{left:221.248500px;}
.x26{left:227.857500px;}
.xb{left:264.606000px;}
.x17{left:274.035000px;}
.x21{left:331.198500px;}
.xe{left:361.507500px;}
.x22{left:407.559000px;}
.x3{left:484.129500px;}
.x1d{left:499.240500px;}
.x1c{left:537.000000px;}
.xc{left:558.468000px;}
.x2{left:575.305500px;}
.x12{left:582.882000px;}
.x11{left:588.144000px;}
.x6{left:592.480500px;}
.x1f{left:620.893500px;}
.x23{left:622.071000px;}
.x9{left:636.088500px;}
.x1e{left:650.106000px;}
.x4{left:662.146500px;}
.x24{left:681.130500px;}
.x15{left:691.654500px;}
.x16{left:714.469500px;}
.x10{left:716.995500px;}
.xd{left:720.742500px;}
.x13{left:722.551500px;}
.x7{left:730.213500px;}
.x20{left:740.148000px;}
.x5{left:744.019500px;}
@media print{
.v0{vertical-align:0.000000pt;}
.ls0{letter-spacing:0.000000pt;}
.ws0{word-spacing:0.000000pt;}
._1d{margin-left:-0.957216pt;}
._0{width:0.917276pt;}
._c{width:16.388800pt;}
._8{width:47.536085pt;}
._19{width:53.781333pt;}
._a{width:56.869490pt;}
._7{width:57.769813pt;}
._6{width:61.162667pt;}
._13{width:66.407147pt;}
._12{width:72.087772pt;}
._1b{width:80.746667pt;}
._4{width:84.163556pt;}
._17{width:85.668096pt;}
._2{width:106.698268pt;}
._21{width:133.654073pt;}
._d{width:145.585500pt;}
._1{width:150.239403pt;}
._20{width:170.893625pt;}
._3{width:173.746724pt;}
._15{width:177.400747pt;}
._22{width:183.191865pt;}
._14{width:202.107762pt;}
._23{width:241.089508pt;}
._18{width:242.314667pt;}
._b{width:268.837547pt;}
._5{width:328.725333pt;}
._1c{width:338.678279pt;}
._10{width:410.631659pt;}
._11{width:417.091876pt;}
._e{width:451.489728pt;}
._9{width:456.507442pt;}
._1f{width:530.660409pt;}
._1e{width:541.097244pt;}
._f{width:614.130027pt;}
._16{width:644.800946pt;}
._1a{width:1076.748089pt;}
.fs2{font-size:24.544000pt;}
.fs4{font-size:28.138667pt;}
.fs0{font-size:31.630222pt;}
.fs1{font-size:35.221333pt;}
.fs3{font-size:42.307556pt;}
.fs5{font-size:56.174222pt;}
.y0{bottom:-0.666667pt;}
.y2c{bottom:5.089333pt;}
.y2{bottom:5.125333pt;}
.y5{bottom:5.164000pt;}
.y4a{bottom:7.070667pt;}
.y3f{bottom:7.108000pt;}
.y38{bottom:81.869333pt;}
.ya{bottom:115.169333pt;}
.y3c{bottom:134.402667pt;}
.y3b{bottom:150.266667pt;}
.y3a{bottom:164.261333pt;}
.y32{bottom:177.096000pt;}
.y39{bottom:180.238667pt;}
.y37{bottom:197.038667pt;}
.y36{bottom:211.070667pt;}
.y35{bottom:233.594667pt;}
.y34{bottom:249.460000pt;}
.y33{bottom:273.856000pt;}
.y31{bottom:292.265333pt;}
.y30{bottom:312.920000pt;}
.y2f{bottom:328.785333pt;}
.y2e{bottom:345.846667pt;}
.y2d{bottom:361.712000pt;}
.y2b{bottom:389.550667pt;}
.y2a{bottom:405.041333pt;}
.y29{bottom:420.906667pt;}
.y28{bottom:454.506667pt;}
.y27{bottom:475.985333pt;}
.y26{bottom:492.785333pt;}
.y25{bottom:509.585333pt;}
.y24{bottom:526.385333pt;}
.y48{bottom:529.342667pt;}
.y23{bottom:559.725333pt;}
.y46{bottom:560.025333pt;}
.y22{bottom:576.786667pt;}
.y21{bottom:593.588000pt;}
.y44{bottom:601.633333pt;}
.y20{bottom:610.388000pt;}
.y1e{bottom:618.769333pt;}
.y1f{bottom:627.188000pt;}
.y42{bottom:628.274667pt;}
.y43{bottom:630.033333pt;}
.y49{bottom:639.162667pt;}
.y1d{bottom:647.468000pt;}
.y1c{bottom:675.194667pt;}
.y47{bottom:676.916000pt;}
.y1b{bottom:700.638667pt;}
.y3d{bottom:703.482667pt;}
.y1a{bottom:716.241333pt;}
.y19{bottom:716.802667pt;}
.y45{bottom:718.524000pt;}
.y18{bottom:742.920000pt;}
.y17{bottom:743.444000pt;}
.y16{bottom:770.646667pt;}
.y40{bottom:790.926667pt;}
.y41{bottom:792.648000pt;}
.y3e{bottom:813.265333pt;}
.y15{bottom:818.390667pt;}
.y14{bottom:838.372000pt;}
.yb{bottom:850.682667pt;}
.y12{bottom:856.257333pt;}
.y13{bottom:863.329333pt;}
.y11{bottom:879.306667pt;}
.y10{bottom:881.438667pt;}
.yf{bottom:901.981333pt;}
.ye{bottom:918.781333pt;}
.yd{bottom:935.581333pt;}
.yc{bottom:951.858667pt;}
.y9{bottom:965.852000pt;}
.y8{bottom:981.044000pt;}
.y7{bottom:982.653333pt;}
.y6{bottom:999.453333pt;}
.y4{bottom:1021.492000pt;}
.y3{bottom:1036.309333pt;}
.y1{bottom:1051.126667pt;}
.h9{height:13.096000pt;}
.h2{height:14.778667pt;}
.h6{height:17.569094pt;}
.h8{height:20.142229pt;}
.h3{height:22.641556pt;}
.ha{height:22.712000pt;}
.hc{height:23.721333pt;}
.h4{height:25.212146pt;}
.h7{height:36.027528pt;}
.hb{height:40.210649pt;}
.h5{height:950.736000pt;}
.h0{height:1122.519685pt;}
.h1{height:1123.333333pt;}
.w4{width:24.844000pt;}
.w5{width:50.064000pt;}
.w3{width:62.224000pt;}
.w7{width:436.024000pt;}
.w2{width:726.718667pt;}
.w6{width:731.284000pt;}
.w0{width:793.738583pt;}
.w1{width:794.666667pt;}
.x0{left:0.000000pt;}
.xa{left:2.058667pt;}
.x1{left:56.612000pt;}
.x14{left:59.194667pt;}
.x25{left:66.416000pt;}
.x1b{left:71.729333pt;}
.x18{left:100.802667pt;}
.x27{left:111.616000pt;}
.xf{left:121.456000pt;}
.x29{left:135.788000pt;}
.x28{left:139.678667pt;}
.x2a{left:142.260000pt;}
.x1a{left:188.396000pt;}
.x2b{left:189.817333pt;}
.x8{left:192.924000pt;}
.x19{left:196.665333pt;}
.x26{left:202.540000pt;}
.xb{left:235.205333pt;}
.x17{left:243.586667pt;}
.x21{left:294.398667pt;}
.xe{left:321.340000pt;}
.x22{left:362.274667pt;}
.x3{left:430.337333pt;}
.x1d{left:443.769333pt;}
.x1c{left:477.333333pt;}
.xc{left:496.416000pt;}
.x2{left:511.382667pt;}
.x12{left:518.117333pt;}
.x11{left:522.794667pt;}
.x6{left:526.649333pt;}
.x1f{left:551.905333pt;}
.x23{left:552.952000pt;}
.x9{left:565.412000pt;}
.x1e{left:577.872000pt;}
.x4{left:588.574667pt;}
.x24{left:605.449333pt;}
.x15{left:614.804000pt;}
.x16{left:635.084000pt;}
.x10{left:637.329333pt;}
.xd{left:640.660000pt;}
.x13{left:642.268000pt;}
.x7{left:649.078667pt;}
.x20{left:657.909333pt;}
.x5{left:661.350667pt;}
}
</style>
<script>
/*
 Copyright 2012 Mozilla Foundation
 Copyright 2013 Lu Wang <coolwanglu@gmail.com>
 Apachine License Version 2.0
*/
(function(){function b(a,b,e,f){var c=(a.className||"").split(/\s+/g);""===c[0]&&c.shift();var d=c.indexOf(b);0>d&&e&&c.push(b);0<=d&&f&&c.splice(d,1);a.className=c.join(" ");return 0<=d}if(!("classList"in document.createElement("div"))){var e={add:function(a){b(this.element,a,!0,!1)},contains:function(a){return b(this.element,a,!1,!1)},remove:function(a){b(this.element,a,!1,!0)},toggle:function(a){b(this.element,a,!0,!0)}};Object.defineProperty(HTMLElement.prototype,"classList",{get:function(){if(this._classList)return this._classList;
var a=Object.create(e,{element:{value:this,writable:!1,enumerable:!0}});Object.defineProperty(this,"_classList",{value:a,writable:!1,enumerable:!1});return a},enumerable:!0})}})();
</script>
<script>
(function(){/*
 pdf2htmlEX.js: Core UI functions for pdf2htmlEX
 Copyright 2012,2013 Lu Wang <coolwanglu@gmail.com> and other contributors
 https://github.com/pdf2htmlEX/pdf2htmlEX/blob/master/share/LICENSE
*/
var pdf2htmlEX=window.pdf2htmlEX=window.pdf2htmlEX||{},CSS_CLASS_NAMES={page_frame:"pf",page_content_box:"pc",page_data:"pi",background_image:"bi",link:"l",input_radio:"ir",__dummy__:"no comma"},DEFAULT_CONFIG={container_id:"page-container",sidebar_id:"sidebar",outline_id:"outline",loading_indicator_cls:"loading-indicator",preload_pages:3,render_timeout:100,scale_step:0.9,key_handler:!0,hashchange_handler:!0,view_history_handler:!0,__dummy__:"no comma"},EPS=1E-6;
function invert(a){var b=a[0]*a[3]-a[1]*a[2];return[a[3]/b,-a[1]/b,-a[2]/b,a[0]/b,(a[2]*a[5]-a[3]*a[4])/b,(a[1]*a[4]-a[0]*a[5])/b]}function transform(a,b){return[a[0]*b[0]+a[2]*b[1]+a[4],a[1]*b[0]+a[3]*b[1]+a[5]]}function get_page_number(a){return parseInt(a.getAttribute("data-page-no"),16)}function disable_dragstart(a){for(var b=0,c=a.length;b<c;++b)a[b].addEventListener("dragstart",function(){return!1},!1)}
function clone_and_extend_objs(a){for(var b={},c=0,e=arguments.length;c<e;++c){var h=arguments[c],d;for(d in h)h.hasOwnProperty(d)&&(b[d]=h[d])}return b}
function Page(a){if(a){this.shown=this.loaded=!1;this.page=a;this.num=get_page_number(a);this.original_height=a.clientHeight;this.original_width=a.clientWidth;var b=a.getElementsByClassName(CSS_CLASS_NAMES.page_content_box)[0];b&&(this.content_box=b,this.original_scale=this.cur_scale=this.original_height/b.clientHeight,this.page_data=JSON.parse(a.getElementsByClassName(CSS_CLASS_NAMES.page_data)[0].getAttribute("data-data")),this.ctm=this.page_data.ctm,this.ictm=invert(this.ctm),this.loaded=!0)}}
Page.prototype={hide:function(){this.loaded&&this.shown&&(this.content_box.classList.remove("opened"),this.shown=!1)},show:function(){this.loaded&&!this.shown&&(this.content_box.classList.add("opened"),this.shown=!0)},rescale:function(a){this.cur_scale=0===a?this.original_scale:a;this.loaded&&(a=this.content_box.style,a.msTransform=a.webkitTransform=a.transform="scale("+this.cur_scale.toFixed(3)+")");a=this.page.style;a.height=this.original_height*this.cur_scale+"px";a.width=this.original_width*this.cur_scale+
"px"},view_position:function(){var a=this.page,b=a.parentNode;return[b.scrollLeft-a.offsetLeft-a.clientLeft,b.scrollTop-a.offsetTop-a.clientTop]},height:function(){return this.page.clientHeight},width:function(){return this.page.clientWidth}};function Viewer(a){this.config=clone_and_extend_objs(DEFAULT_CONFIG,0<arguments.length?a:{});this.pages_loading=[];this.init_before_loading_content();var b=this;document.addEventListener("DOMContentLoaded",function(){b.init_after_loading_content()},!1)}
Viewer.prototype={scale:1,cur_page_idx:0,first_page_idx:0,init_before_loading_content:function(){this.pre_hide_pages()},initialize_radio_button:function(){for(var a=document.getElementsByClassName(CSS_CLASS_NAMES.input_radio),b=0;b<a.length;b++)a[b].addEventListener("click",function(){this.classList.toggle("checked")})},init_after_loading_content:function(){this.sidebar=document.getElementById(this.config.sidebar_id);this.outline=document.getElementById(this.config.outline_id);this.container=document.getElementById(this.config.container_id);
this.loading_indicator=document.getElementsByClassName(this.config.loading_indicator_cls)[0];for(var a=!0,b=this.outline.childNodes,c=0,e=b.length;c<e;++c)if("ul"===b[c].nodeName.toLowerCase()){a=!1;break}a||this.sidebar.classList.add("opened");this.find_pages();if(0!=this.pages.length){disable_dragstart(document.getElementsByClassName(CSS_CLASS_NAMES.background_image));this.config.key_handler&&this.register_key_handler();var h=this;this.config.hashchange_handler&&window.addEventListener("hashchange",
function(a){h.navigate_to_dest(document.location.hash.substring(1))},!1);this.config.view_history_handler&&window.addEventListener("popstate",function(a){a.state&&h.navigate_to_dest(a.state)},!1);this.container.addEventListener("scroll",function(){h.update_page_idx();h.schedule_render(!0)},!1);[this.container,this.outline].forEach(function(a){a.addEventListener("click",h.link_handler.bind(h),!1)});this.initialize_radio_button();this.render()}},find_pages:function(){for(var a=[],b={},c=this.container.childNodes,
e=0,h=c.length;e<h;++e){var d=c[e];d.nodeType===Node.ELEMENT_NODE&&d.classList.contains(CSS_CLASS_NAMES.page_frame)&&(d=new Page(d),a.push(d),b[d.num]=a.length-1)}this.pages=a;this.page_map=b},load_page:function(a,b,c){var e=this.pages;if(!(a>=e.length||(e=e[a],e.loaded||this.pages_loading[a]))){var e=e.page,h=e.getAttribute("data-page-url");if(h){this.pages_loading[a]=!0;var d=e.getElementsByClassName(this.config.loading_indicator_cls)[0];"undefined"===typeof d&&(d=this.loading_indicator.cloneNode(!0),
d.classList.add("active"),e.appendChild(d));var f=this,g=new XMLHttpRequest;g.open("GET",h,!0);g.onload=function(){if(200===g.status||0===g.status){var b=document.createElement("div");b.innerHTML=g.responseText;for(var d=null,b=b.childNodes,e=0,h=b.length;e<h;++e){var p=b[e];if(p.nodeType===Node.ELEMENT_NODE&&p.classList.contains(CSS_CLASS_NAMES.page_frame)){d=p;break}}b=f.pages[a];f.container.replaceChild(d,b.page);b=new Page(d);f.pages[a]=b;b.hide();b.rescale(f.scale);disable_dragstart(d.getElementsByClassName(CSS_CLASS_NAMES.background_image));
f.schedule_render(!1);c&&c(b)}delete f.pages_loading[a]};g.send(null)}void 0===b&&(b=this.config.preload_pages);0<--b&&(f=this,setTimeout(function(){f.load_page(a+1,b)},0))}},pre_hide_pages:function(){var a="@media screen{."+CSS_CLASS_NAMES.page_content_box+"{display:none;}}",b=document.createElement("style");b.styleSheet?b.styleSheet.cssText=a:b.appendChild(document.createTextNode(a));document.head.appendChild(b)},render:function(){for(var a=this.container,b=a.scrollTop,c=a.clientHeight,a=b-c,b=
b+c+c,c=this.pages,e=0,h=c.length;e<h;++e){var d=c[e],f=d.page,g=f.offsetTop+f.clientTop,f=g+f.clientHeight;g<=b&&f>=a?d.loaded?d.show():this.load_page(e):d.hide()}},update_page_idx:function(){var a=this.pages,b=a.length;if(!(2>b)){for(var c=this.container,e=c.scrollTop,c=e+c.clientHeight,h=-1,d=b,f=d-h;1<f;){var g=h+Math.floor(f/2),f=a[g].page;f.offsetTop+f.clientTop+f.clientHeight>=e?d=g:h=g;f=d-h}this.first_page_idx=d;for(var g=h=this.cur_page_idx,k=0;d<b;++d){var f=a[d].page,l=f.offsetTop+f.clientTop,
f=f.clientHeight;if(l>c)break;f=(Math.min(c,l+f)-Math.max(e,l))/f;if(d===h&&Math.abs(f-1)<=EPS){g=h;break}f>k&&(k=f,g=d)}this.cur_page_idx=g}},schedule_render:function(a){if(void 0!==this.render_timer){if(!a)return;clearTimeout(this.render_timer)}var b=this;this.render_timer=setTimeout(function(){delete b.render_timer;b.render()},this.config.render_timeout)},register_key_handler:function(){var a=this;window.addEventListener("DOMMouseScroll",function(b){if(b.ctrlKey){b.preventDefault();var c=a.container,
e=c.getBoundingClientRect(),c=[b.clientX-e.left-c.clientLeft,b.clientY-e.top-c.clientTop];a.rescale(Math.pow(a.config.scale_step,b.detail),!0,c)}},!1);window.addEventListener("keydown",function(b){var c=!1,e=b.ctrlKey||b.metaKey,h=b.altKey;switch(b.keyCode){case 61:case 107:case 187:e&&(a.rescale(1/a.config.scale_step,!0),c=!0);break;case 173:case 109:case 189:e&&(a.rescale(a.config.scale_step,!0),c=!0);break;case 48:e&&(a.rescale(0,!1),c=!0);break;case 33:h?a.scroll_to(a.cur_page_idx-1):a.container.scrollTop-=
a.container.clientHeight;c=!0;break;case 34:h?a.scroll_to(a.cur_page_idx+1):a.container.scrollTop+=a.container.clientHeight;c=!0;break;case 35:a.container.scrollTop=a.container.scrollHeight;c=!0;break;case 36:a.container.scrollTop=0,c=!0}c&&b.preventDefault()},!1)},rescale:function(a,b,c){var e=this.scale;this.scale=a=0===a?1:b?e*a:a;c||(c=[0,0]);b=this.container;c[0]+=b.scrollLeft;c[1]+=b.scrollTop;for(var h=this.pages,d=h.length,f=this.first_page_idx;f<d;++f){var g=h[f].page;if(g.offsetTop+g.clientTop>=
c[1])break}g=f-1;0>g&&(g=0);var g=h[g].page,k=g.clientWidth,f=g.clientHeight,l=g.offsetLeft+g.clientLeft,m=c[0]-l;0>m?m=0:m>k&&(m=k);k=g.offsetTop+g.clientTop;c=c[1]-k;0>c?c=0:c>f&&(c=f);for(f=0;f<d;++f)h[f].rescale(a);b.scrollLeft+=m/e*a+g.offsetLeft+g.clientLeft-m-l;b.scrollTop+=c/e*a+g.offsetTop+g.clientTop-c-k;this.schedule_render(!0)},fit_width:function(){var a=this.cur_page_idx;this.rescale(this.container.clientWidth/this.pages[a].width(),!0);this.scroll_to(a)},fit_height:function(){var a=this.cur_page_idx;
this.rescale(this.container.clientHeight/this.pages[a].height(),!0);this.scroll_to(a)},get_containing_page:function(a){for(;a;){if(a.nodeType===Node.ELEMENT_NODE&&a.classList.contains(CSS_CLASS_NAMES.page_frame)){a=get_page_number(a);var b=this.page_map;return a in b?this.pages[b[a]]:null}a=a.parentNode}return null},link_handler:function(a){var b=a.target,c=b.getAttribute("data-dest-detail");if(c){if(this.config.view_history_handler)try{var e=this.get_current_view_hash();window.history.replaceState(e,
"","#"+e);window.history.pushState(c,"","#"+c)}catch(h){}this.navigate_to_dest(c,this.get_containing_page(b));a.preventDefault()}},navigate_to_dest:function(a,b){try{var c=JSON.parse(a)}catch(e){return}if(c instanceof Array){var h=c[0],d=this.page_map;if(h in d){for(var f=d[h],h=this.pages[f],d=2,g=c.length;d<g;++d){var k=c[d];if(null!==k&&"number"!==typeof k)return}for(;6>c.length;)c.push(null);var g=b||this.pages[this.cur_page_idx],d=g.view_position(),d=transform(g.ictm,[d[0],g.height()-d[1]]),
g=this.scale,l=[0,0],m=!0,k=!1,n=this.scale;switch(c[1]){case "XYZ":l=[null===c[2]?d[0]:c[2]*n,null===c[3]?d[1]:c[3]*n];g=c[4];if(null===g||0===g)g=this.scale;k=!0;break;case "Fit":case "FitB":l=[0,0];k=!0;break;case "FitH":case "FitBH":l=[0,null===c[2]?d[1]:c[2]*n];k=!0;break;case "FitV":case "FitBV":l=[null===c[2]?d[0]:c[2]*n,0];k=!0;break;case "FitR":l=[c[2]*n,c[5]*n],m=!1,k=!0}if(k){this.rescale(g,!1);var p=this,c=function(a){l=transform(a.ctm,l);m&&(l[1]=a.height()-l[1]);p.scroll_to(f,l)};h.loaded?
c(h):(this.load_page(f,void 0,c),this.scroll_to(f))}}}},scroll_to:function(a,b){var c=this.pages;if(!(0>a||a>=c.length)){c=c[a].view_position();void 0===b&&(b=[0,0]);var e=this.container;e.scrollLeft+=b[0]-c[0];e.scrollTop+=b[1]-c[1]}},get_current_view_hash:function(){var a=[],b=this.pages[this.cur_page_idx];a.push(b.num);a.push("XYZ");var c=b.view_position(),c=transform(b.ictm,[c[0],b.height()-c[1]]);a.push(c[0]/this.scale);a.push(c[1]/this.scale);a.push(this.scale);return JSON.stringify(a)}};
pdf2htmlEX.Viewer=Viewer;})();
</script>
<script>
try{
pdf2htmlEX.defaultViewer = new pdf2htmlEX.Viewer({});
}catch(e){}
</script>
<title></title>
</head>
<body>
<div id="sidebar">
<div id="outline">
</div>
</div>
<div id="page-container">
<div id="pf1" class="pf w0 h0" data-page-no="1"><div class="pc pc1 w0 h0">
<img class="bi x0 y0 w1 h1" alt="" src="data:image/png;base64,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"/>
<div class="c x1 y1 w2 h2"><div class="t m0 x2 h3 y2 ff1 fs0 fc0 sc0 ls0 ws0">Унифициро<span class="_ _0"></span>ванная форма<span class="_ _0"></span> № АО-1</div></div>
<div class="c x1 y3 w2 h2"><div class="t m0 x3 h3 y2 ff1 fs0 fc0 sc0 ls0 ws0">Утверждена Постано<span class="_ _0"></span>влением Госкомстата<span class="_ _0"></span> России</div></div>
<div class="c x1 y4 w2 h2"><div class="t m0 x4 h3 y5 ff1 fs0 fc0 sc0 ls0 ws0">от 01.08.200<span class="_ _0"></span>1 № 55</div></div><div class="t m0 x5 h4 y6 ff1 fs1 fc0 sc0 ls0 ws0">Код</div>
<div class="t m0 x6 h4 y7 ff1 fs1 fc0 sc0 ls0 ws0">Форма по ОКУД </div><div class="t m0 x7 h4 y8 ff1 fs1 fc0 sc0 ls0 ws0">0302001</div>
<div class="t m0 x8 h4 y9 ff1 fs1 fc0 sc0 ls0 ws0">ООО &quot; переработка&quot; ЗПКТ</div><div class="c x9 ya w3 h5"><div class="t m0 xa h4 yb ff1 fs1 fc0 sc0 ls0 ws0">по ОКПО </div></div>
<div class="t m0 xb h6 yc ff1 fs2 fc0 sc0 ls0 ws0">(наименование о<span class="_ _0"></span>рганизации)</div><div class="t m0 xc h3 yd ff1 fs0 fc0 sc0 ls0 ws0">УТВЕРЖДАЮ</div><div class="t m0 xc h3 ye ff1 fs0 fc0 sc0 ls0 ws0">Отчет в сумме</div>
<div class="t m0 xd h3 yf ff1 fs0 fc0 sc0 ls0 ws0">руб.<span class="_ _1"> </span>коп.</div>
<div class="t m0 xe h3 y10 ff1 fs0 fc0 sc0 ls0 ws0">Номер<span class="_ _2"> </span>Дата</div>
<div class="t m0 xc h3 y11 ff1 fs0 fc0 sc0 ls0 ws0">Руководитель</div><div class="t m0 xf h7 y12 ff2 fs3 fc0 sc0 ls0 ws0">АВАНСОВЫЙ ОТЧЕТ</div>
<div class="t m0 x10 h6 y13 ff1 fs2 fc0 sc0 ls0 ws0">(должность)</div><div class="t m0 x11 h6 y14 ff1 fs2 fc0 sc0 ls0 ws0">(подпись)<span class="_ _3"> </span>(расшифровк<span class="_ _0"></span>а подписи)</div>
<div class="t m0 x12 h3 y15 ff1 fs0 fc0 sc0 ls0 ws0">«<span class="_ _4"> </span>»<span class="_ _5"> </span>20<span class="_ _6"> </span>г.</div><div class="t m0 x13 h8 y16 ff1 fs4 fc0 sc0 ls0 ws0">Код</div>
<div class="t m0 x14 h4 y17 ff1 fs1 fc0 sc0 ls0 ws0">Структурное подразделение<span class="_ _7"> </span>АУП, бухгалтерия</div>
<div class="t m0 x15 h8 y18 ff1 fs4 fc0 sc0 ls0 ws0">8-888-888-88<span class="_ _0"></span>-88</div><div class="t m0 x14 h4 y19 ff1 fs1 fc0 sc0 ls0 ws0">Подотчетное лицо<span class="_ _8"> </span>Иванов Иван Иванович<span class="_ _9"> </span>Табельный номер</div><div class="t m0 x16 h8 y1a ff1 fs4 fc0 sc0 ls0 ws0">111111</div><div class="t m0 x17 h6 y1b ff1 fs2 fc0 sc0 ls0 ws0">(фамилия, инициалы)</div><div class="t m0 x14 h4 y1c ff1 fs1 fc0 sc0 ls0 ws0">Профессия (должность)<span class="_ _a"> </span>бухгалтер<span class="_ _b"> </span>Назначение аванса<span class="_ _c"> </span>проезд в отпуск</div><div class="t m0 x18 h8 y1d ff1 fs4 fc0 sc0 ls0 ws0">Наименование показателя<span class="_ _d"> </span>Сумма, руб.коп.<span class="_ _e"> </span>Бухгалтерская запись</div><div class="t m0 x14 h8 y1e ff1 fs4 fc0 sc0 ls0 ws0"> Предыдущий аванс</div><div class="t m0 x19 h8 y1f ff1 fs4 fc0 sc0 ls0 ws0">остаток<span class="_ _f"> </span>дебет<span class="_ _10"> </span>кредит</div><div class="t m0 x1a h8 y20 ff1 fs4 fc0 sc0 ls0 ws0">перерасход<span class="_ _11"> </span>счет, субсчет<span class="_ _12"> </span>сумма, руб.коп.<span class="_ _4"> </span>счет,<span class="_ _0"></span> субсчет<span class="_ _13"> </span>сумма, руб.коп.</div><div class="t m0 x14 h8 y21 ff1 fs4 fc0 sc0 ls0 ws0"> Получен аванс 1. из кассы</div><div class="t m0 x14 h8 y22 ff1 fs4 fc0 sc0 ls0 ws0"> 1а. в валюте (справочно)</div><div class="t m0 x14 h6 y23 ff1 fs2 fc0 sc0 ls0 ws0"> 2.</div><div class="t m0 x14 h8 y24 ff1 fs4 fc0 sc0 ls0 ws0"> Итого получено</div><div class="t m0 x14 h8 y25 ff1 fs4 fc0 sc0 ls0 ws0"> Израсходовано</div><div class="t m0 x1b h8 y26 ff1 fs4 fc0 sc0 ls0 ws0">Остаток</div><div class="t m0 x1b h8 y27 ff1 fs4 fc0 sc0 ls0 ws0">Перерасход</div><div class="t m0 x14 h3 y28 ff1 fs0 fc0 sc0 ls0 ws0">Приложение<span class="_ _14"> </span>документов на<span class="_ _15"> </span>листах</div><div class="t m0 x14 h3 y29 ff1 fs0 fc0 sc0 ls0 ws0">Отчет провере<span class="_ _0"></span>н. К утверждению в сумме</div><div class="t m0 x1c h6 y2a ff1 fs2 fc0 sc0 ls0 ws0">(сумма пропис<span class="_ _0"></span>ью)</div><div class="c x1 y2b w2 h9"><div class="t m0 x1d h3 y2c ff1 fs0 fc0 sc0 ls0 ws0">руб.</div></div><div class="c x1e y2b w4 h9"><div class="t m0 xa h3 y2c ff1 fs0 fc0 sc0 ls0 ws0">коп.</div></div><div class="c x1 y2b w2 h9"><div class="t m0 x1f h3 y2c ff1 fs0 fc0 sc0 ls0 ws0">(</div></div><div class="c x5 y2b w4 h9"><div class="t m0 xa h3 y2c ff1 fs0 fc0 sc0 ls0 ws0">руб.</div></div><div class="c x1 y2b w2 h9"><div class="t m0 x20 h3 y2c ff1 fs0 fc0 sc0 ls0 ws0">коп.)</div></div><div class="t m0 x14 h3 y2d ff1 fs0 fc0 sc0 ls0 ws0">Главный бухгалтер</div><div class="t m0 xb h6 y2e ff1 fs2 fc0 sc0 ls0 ws0">(подпись)<span class="_ _16"> </span>(расшифровк<span class="_ _0"></span>а подписи)</div><div class="t m0 x14 h3 y2f ff1 fs0 fc0 sc0 ls0 ws0">Бухгалтер</div><div class="t m0 xb h6 y30 ff1 fs2 fc0 sc0 ls0 ws0">(подпись)<span class="_ _16"> </span>(расшифровк<span class="_ _0"></span>а подписи)</div><div class="t m0 x14 h3 y31 ff1 fs0 fc0 sc0 ls0 ws0">Остаток внесен<span class="_ _17"> </span>в сумме</div><div class="c x21 ya w4 h5"><div class="t m0 xa h3 y32 ff1 fs0 fc0 sc0 ls0 ws0">руб.</div></div><div class="t m0 x22 h3 y31 ff1 fs0 fc0 sc0 ls0 ws0">коп. по кассовому<span class="_ _0"></span> ордеру  №</div><div class="c x23 ya w4 h5"><div class="t m0 xa h3 y32 ff1 fs0 fc0 sc0 ls0 ws0">от «</div></div><div class="t m0 x24 h3 y31 ff1 fs0 fc0 sc0 ls0 ws0">»<span class="_ _18"> </span>20<span class="_ _19"> </span>г.</div><div class="t m0 x14 h3 y33 ff1 fs0 fc0 sc0 ls0 ws0">Перерасх<span class="_ _0"></span>од выдан</div><div class="t m0 x25 h3 y34 ff1 fs0 fc0 sc0 ls0 ws0">Бухгалтер (кас<span class="_ _0"></span>сир)<span class="_ _1a"> </span> «<span class="_ _1b"> </span>»<span class="_ _18"> </span>20<span class="_ _19"> </span>г.</div><div class="t m0 xb h6 y35 ff1 fs2 fc0 sc0 ls0 ws0">(подпись)<span class="_ _1c"> </span>(расшифровк<span class="_ _0"></span>а подписи)</div><div class="t m0 x22 h6 y36 ff1 fs2 fc0 sc0 ls0 ws0">л и н и я   о т р е з <span class="_ _1d"></span>а</div><div class="t m0 x14 h3 y37 ff1 fs0 fc0 sc0 ls0 ws0">Расписка. Принят к прове<span class="_ _0"></span>рке от<span class="_ _1e"> </span>авансовый о<span class="_ _0"></span>тчет №</div><div class="c x23 ya w4 h5"><div class="t m0 xa h3 y38 ff1 fs0 fc0 sc0 ls0 ws0">от «</div></div><div class="t m0 x24 h3 y37 ff1 fs0 fc0 sc0 ls0 ws0">»<span class="_ _18"> </span>20<span class="_ _19"> </span>г.</div><div class="t m0 x25 h3 y39 ff1 fs0 fc0 sc0 ls0 ws0">на сумму <span class="_ _1f"> </span>руб.<span class="_ _20"> </span>коп., количество документо<span class="_ _0"></span>в<span class="_ _21"> </span>на<span class="_ _22"> </span>листах</div><div class="t m0 x26 h6 y3a ff1 fs2 fc0 sc0 ls0 ws0">(прописью)</div><div class="t m0 x27 h3 y3b ff1 fs0 fc0 sc0 ls0 ws0">Бухгалтер<span class="_ _1a"> </span> «<span class="_ _1b"> </span>»<span class="_ _23"> </span>20<span class="_ _19"> </span>г.</div><div class="t m0 xb h6 y3c ff1 fs2 fc0 sc0 ls0 ws0">(подпись)<span class="_ _1c"> </span>(расшифровк<span class="_ _0"></span>а подписи)</div></div><div class="pi" data-data='{"ctm":[1.500000,0.000000,0.000000,1.500000,0.000000,0.000000]}'></div></div>
<div id="pf2" class="pf w0 h0" data-page-no="2">
<div class="pc pc2 w0 h0"><div class="pi" data-data='{"ctm":[1.500000,0.000000,0.000000,1.500000,0.000000,0.000000]}'></div>
         <form>
              <p><button action="/topdf">Кнопка с текстом</button></p>
         </form>
        <form action="/topdf" method="POST">
    <!-- скрытый параметр -->
    <input type="hidden" name="index" value="2">
    <input type="submit" class="btn btn-dark" value="Нажать 2">
</form>
</div>
</div>


               
            </div>
        </div>

    </body>
</html>

    </form>'''


@app.route('/topdf', methods=['POST'])
def topdf():
    index = request.form['index']
    pdfkit.from_url('http://forma-avansa.tk:8000/form', 'out.pdf')
    return 'OK'


if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()

# while True:
#     run_pending()
#     time.sleep(1)
