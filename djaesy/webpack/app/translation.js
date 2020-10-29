
// Adiciona a ação de troca de idioma aos links .language-toggler
// Estes links ficam no dropdown de idiomas do arquivo base.html
// Ao clicar, realiza POST para a url de troca de idioma do Django
// https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#django.views.i18n.set_language

;(function() {
    $(document).ready(function() {
        $('.language-toggler').on('click', function(e) {
            let el = $(this);
            let language = el.data('language');
            let post_url = SET_LANGUAGE_URL;
            let post = {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                'language': language,
                'next': ''
            };
            $.post(post_url, post, function(data) {
                window.location.reload(true);
            });
            e.preventDefault();
        });
    });
}.call(this));
