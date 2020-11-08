from crispy_forms.layout import Layout, Fieldset, Div

USER_CREATE_EDIT_LAYOUT = Layout(
    Div(
        Div('email', css_class="col col-12"),
        Div('password1', css_class="col col-12"),
        Div('password2', css_class="col col-12"),
        css_class='col col-12 col-sm-12 col-md-4'
    ),
    Div(
        Div('name', css_class="col col-12"),
        Div('user_type', css_class="col col-12"),
        Div('role', css_class="col col-12"),
        css_class='col col-12 col-sm-12 col-md-4',
    ),
    Div(
        Div('is_active', css_class="col col-12"),
        Div('must_change_password', css_class="col col-12"),
        css_class='col col-12 col-sm-12 col-md-4',
    )
)
