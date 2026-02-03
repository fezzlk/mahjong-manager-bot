from wtforms import Form, StringField, SubmitField, validators


class RegisterWebUserForm(Form):
    name = StringField(
        label="名前*",
        validators=[validators.DataRequired(message="名前は必須です")],
        render_kw={"readonly": ""},
    )
    email = StringField(
        label="メールアドレス*",
        validators=[validators.DataRequired(message="メールアドレスは必須です")],
        render_kw={"readonly": ""},
    )
    submit = SubmitField("登録")
