from django import forms # Djangoが準備しているforms
from .models import Customer # モデルの部分で定義したDBのテーブル

class InputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    # DBの内容のメタ情報を記載しています
    class Meta:
        model = Customer
        exclude = ['id', 'result', 'proba', 'comment', 'registered_date']