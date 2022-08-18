import os

INSTALLED_APPS = [
    ...
    'rest_framework',
    'haystack',
    'customers'
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATK': os.path.join(os.path.join()),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'