# Python program showing
# use of __call__() method

class crud_combo:

    def __init__(self, function):
        self.function = function

    def __call__(self):
        # We can add some code
        # before function call

        self.function()

        # We can also add some code
        # after function call.


def dec(klass):

    from django.conf import settings
    urls_module = settings.ROOT_URLCONF
    urls = __import__(urls_module)

    x = 1
    
    return klass
