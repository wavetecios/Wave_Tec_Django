from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def _usuario_permitido(user, perfis):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    tecnico = getattr(user, 'tecnico', None)
    return tecnico is not None and tecnico.ativo and tecnico.perfil in perfis


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return user_passes_test(
                lambda u: u.is_authenticated,
                login_url='login',
            )(view_func)(request, *args, **kwargs)

        if not _usuario_permitido(request.user, ['ADMIN']):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def tecnico_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return user_passes_test(
                lambda u: u.is_authenticated,
                login_url='login',
            )(view_func)(request, *args, **kwargs)

        if not _usuario_permitido(request.user, ['ADMIN', 'TECNICO']):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
