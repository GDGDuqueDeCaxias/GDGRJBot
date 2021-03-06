import argparse
import datetime
import functools
import logging
import os
import re
import threading


class HandlerHelper:
    def __init__(self):
        self.functions = {}

    def __call__(self, *names):
        """Decorator para marcar funções como comandos do bot"""
        def decorator(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs)
            for name in names:
                self.functions[name] = func
            return wrapped
        return decorator

    def handle(self, name, *args, raises=False, **kwargs):
        """Executa a função associada ao comando passado

        :except: Exceções são relançadas se `raises` é `True`, do contrário, são enviadas ao log.
        :return: `True` ou `False` indicando que o comando foi executado
        """
        function = self.functions.get(name)
        if function:
            try:
                function(*args, **kwargs)
            except Exception as e:
                raise e if raises else logging.exception(e)
            return True
        return False


def match_command(text):
    """Verifica se o texto passado representa um comando

    :return: um objeto regex match ou `None`
    """
    return re.match(r'(/[^\s]+ ?[^\s]+(?:\s+[^\s]+)*)', text)


def extract_command(text):
    """Extrai o nome do comando, incluindo a barra '/'

    :return: nome do comando ou `None`
    """
    match = match_command(text)
    if match:
        return match.group(1).split()[0].split('@')[0]


class TimeZone:
    class TZ(datetime.tzinfo):
        ZERO = datetime.timedelta(0)

        def __init__(self, hours):
            self._utcoffset = datetime.timedelta(hours=hours)
            self._tzname = 'GMT%d' % hours

        def utcoffset(self, dt):
            return self._utcoffset

        def tzname(self, dt):
            return self._tzname

        def dst(self, dt):
            return self.ZERO

    # cache de fusos horários
    timezones = {}

    @classmethod
    def gmt(cls, hours):
        if hours not in cls.timezones:
            cls.timezones[hours] = cls.TZ(hours)
        return cls.timezones[hours]

# aliases úteis
AJU_TZ = TimeZone.gmt(-3)


class Atomic:
    def __init__(self, value=None):
        self._value = value
        self._lock = threading.RLock()

    def set(self, value, on_diff=False):
        with self._lock:
            if on_diff:
                if value == self._value:
                    return False
            self._value = value
            return True

    def get(self, on_none_f=None):
        with self._lock:
            if self._value is None:
                self.set(on_none_f())
            return self._value


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._required_actions = []

    def add_argument(self, *args, **kwargs):
        action = super().add_argument(*args, **kwargs)
        if action.required:
            action.required = False
            self._required_actions += [action]

    def parse_args(self, *args, **kwargs):
        namespace = super().parse_args(*args, **kwargs)

        # Mounting config
        config = {k: v or os.environ.get(k.upper(), '')
                  for k, v in vars(namespace).items()}

        # Verifying required arguments
        missing_args = [argparse._get_action_name(a)
                        for a in self._required_actions if not config[a.dest]]
        if missing_args:
            self.error("missing arguments: " + ", ".join(missing_args))

        return config
