from django.shortcuts import render, redirect
from .forms import InputForm
import joblib
import numpy as np
from .models import Customer

# モデルの読み込み
loaded_model = joblib.load('model/ml_model.pkl')


def index(request):
    return render(request, 'mlapp/index.html')


def input_form(request):
# 下記の様に編集
    if request.method == "POST": # Formの入力があった時、
        form = InputForm(request.POST) # 入力データを取得する。
        if form.is_valid(): # Formの記載の検証を行い、
            form.save() # 問題なければ、入力データを保存
            return redirect('result') # 保存後遷移するページの指定
    else:
        form = InputForm()
        return render(request, 'mlapp/input_form.html', {'form':form})


def result(request):
    # 最新の登録者のデータを取得
    data = Customer.objects.order_by('id').reverse().values_list('limit_balance', 'education', 'marriage', 'age') # 学習させたカラムの順番

    # 推論の実行
    x = np.array([data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    y_proba = y_proba * 100
    y, y_proba = y[0], y_proba[0] 

    # 推論結果を保存
    customer = Customer.objects.order_by('id').reverse()[0] # Customerの切り出し
    customer.proba = y_proba[y]
    customer.result = y
    customer.save()

    return render(request, 'mlapp/result.html', {'y':y, 'y_proba':y_proba}) # 推論結果をHTMLに渡す