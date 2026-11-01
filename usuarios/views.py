from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_required
from .models import Tecnico

User = get_user_model()


@login_required
def lista_tecnicos(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'tecnico') and request.user.tecnico and request.user.tecnico.perfil == 'ADMIN')):
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('home')

    tecnicos = Tecnico.objects.select_related('user').all()
    usuarios = User.objects.all().order_by('username')
    return render(
        request,
        'usuarios/lista_tecnicos.html',
        {'tecnicos': tecnicos, 'usuarios': usuarios}
    )


@login_required
@admin_required
def novo_tecnico(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        nome = request.POST.get('nome', '').strip()
        especialidade = request.POST.get('especialidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        perfil = request.POST.get('perfil', 'TECNICO')

        if not username or not password or not nome:
            messages.error(request, 'Usuário, senha e nome do técnico são obrigatórios.')
            return render(request, 'usuarios/novo_tecnico.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Já existe um usuário com este nome.')
            return render(request, 'usuarios/novo_tecnico.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        Tecnico.objects.create(
            user=user,
            nome=nome,
            especialidade=especialidade,
            telefone=telefone,
            perfil=perfil,
        )

        messages.success(request, 'Usuário e técnico cadastrados com sucesso.')
        return redirect('lista_tecnicos')

    return render(request, 'usuarios/novo_tecnico.html')


@login_required
@admin_required
def editar_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        especialidade = request.POST.get('especialidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        ativo = 'ativo' in request.POST
        perfil = request.POST.get('perfil', tecnico.perfil)

        tecnico.nome = nome
        tecnico.especialidade = especialidade
        tecnico.telefone = telefone
        tecnico.ativo = ativo
        tecnico.perfil = perfil
        tecnico.save()

        if tecnico.user:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            if username:
                tecnico.user.username = username
            if email:
                tecnico.user.email = email
            tecnico.user.save()

        messages.success(request, 'Técnico atualizado com sucesso.')
        return redirect('lista_tecnicos')

    return render(request, 'usuarios/editar_tecnico.html', {'tecnico': tecnico})


@login_required
@admin_required
def excluir_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)

    if request.method == 'POST':
        if tecnico.user:
            tecnico.user.delete()
        tecnico.delete()
        messages.success(request, 'Técnico excluído com sucesso.')
        return redirect('lista_tecnicos')

    return render(request, 'usuarios/excluir_tecnico.html', {'tecnico': tecnico})
