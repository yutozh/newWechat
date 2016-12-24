# coding=utf-8
from app import app
from flask import request, render_template, make_response, redirect
from redisControl import SetRedis,GetRedis
import json
@app.route('/bind', methods=["GET","POST"])
def bind():
    if request.method == "GET":
        username = request.args.get("user", "")
        timestamp = request.args.get("timestamp", "")
        if (username ):
            response = make_response(render_template("Bind.html"))
            response.set_cookie('username',username)
            return response
        else:
            return render_template("Timeout.html")
    username = request.cookies.get("username","")
    stuNum = request.form.get("stuNum","")
    libPsd = request.form.get("libPsd","")
    eduPsd = request.form.get("eduPsd","")
    cardPsd = request.form.get("cardPsd","")

    if username and stuNum:
        SetRedis("User:"+username, "Account", stuNum)
        SetRedis("User:"+username, "Pass_lib", libPsd)
        SetRedis("User:"+username, "Pass_edu", eduPsd)
        SetRedis("User:"+username, "Pass_card", cardPsd)
        return json.dumps({"status":True})
    else:
        return json.dumps({"status":False})

# @app.route('/lib',methods=["GET"])
# def libIndex():
#     return render_template("libIndex.html")


@app.route('/lib/<path:target>', methods=["GET", "POST"])
def libIndex(target):
    # 续借页面
    if target=='xj':
        from MatchClass.Library import getLib
        if request.method == "GET":
            username = request.args.get("user", "")
            if not username:
                return redirect("lib/index")
            return render_template("libXj.html")
        else:
            username = request.form.get("user","")
            user_id = GetRedis("User:"+username, "Account")
            password = GetRedis("User:"+username, "Pass_lib")
            status = request.form.get("aim","")
            if not (user_id and password and status):
                return json.dumps({"error":'-1'})
            # 初始化页面的Ajax请求.返回书籍信息
            if status == 'book':
                books, append =  getLib(user_id, password)
                 # 密码错误
                if len(append) >0 and append[0] == "-1":
                    return json.dumps({"error": '-2'})
                return json.dumps(books)
            # 续借请求,返回结果
            elif status == 'xj':
                bookItems = json.loads(request.form.get("books",""))
                books, append = getLib(user_id, password, bookItems)
                return json.dumps(append)
            # 其他请求
            else:
                return redirect('lib/index')
    # 图书馆主页
    elif target=='index':

        return render_template("libIndex.html")
    else:
        return render_template("libIndex.html")
#
# @app.route('/lib',methods=["GET"])
# def libIndex():
#     return render_template("libIndex.html")