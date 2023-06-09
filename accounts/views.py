from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from .models import FormContato

# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        return render(request, 'Usuario ou senha inválido')
    else:
        auth.login(request, user)
        messages.success(request, 'logado com sucesso')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    #messages.success(request, 'cadastrado')
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/cadastro.html')
    
    if len(senha) < 6 :
        messages.error(request, ' O campo senha não pode ter menos de 6 catacter')
        return render(request, 'accounts/cadastro.html')
    
    if senha != senha2:
        messages.error(request,'as senhas não conferem')
        return render(request, 'accounts/cadastro.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario já existe')
        return render(request, 'accounts/cadastro.html')
    
    if User.objects.filter(username=email).exists():
        messages.error(request, 'E-mail ja existe')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso!')

    #Salvando form do usuario e redirecionando
    user = User.objects.create_user(
        username=usuario, 
        email=email, 
        password=senha, 
        first_name=nome, 
        last_name=sobrenome)
    user.save()

    return redirect('login')

    
@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form':form})
    
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'existem campos invalidos')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form':form})
    
    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais de 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato{request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')