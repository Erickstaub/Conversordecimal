from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Conversao, Desafio
import random


# ========================
# 🔧 CONVERSOR
# ========================

def converter_valor(valor, origem, destino):
    bases = {
        'bin': 2,
        'dec': 10,
        'hex': 16,
        'oct': 8
    }

    try:
        decimal = int(valor, bases[origem])

        if destino == 'bin':
            return bin(decimal)[2:]
        elif destino == 'hex':
            return hex(decimal)[2:]
        elif destino == 'oct':
            return oct(decimal)[2:]
        else:
            return str(decimal)

    except ValueError:
        return None


# ========================
# 🎯 GERAR DESAFIO
# ========================

def gerar_desafio():
    bases = ['dec', 'bin', 'hex', 'oct']

    valor_decimal = random.randint(1, 255)

    origem = random.choice(bases)
    destino = random.choice(bases)

    while origem == destino:
        destino = random.choice(bases)

    valor_convertido = converter_valor(str(valor_decimal), 'dec', origem)

    return {
        'valor': valor_convertido,
        'origem': origem,
        'destino': destino
    }


# ========================
# 🏠 HOME (CONVERSOR)
# ========================

@login_required
def home(request):
    resultado = None
    erro = None

    if request.method == 'POST':
        valor = request.POST.get('valor')
        origem = request.POST.get('origem')
        destino = request.POST.get('destino')

        resultado = converter_valor(valor, origem, destino)

        if resultado is None:
            erro = "Valor inválido para a base selecionada"
        else:
            Conversao.objects.create(
                usuario=request.user,
                valor_entrada=valor,
                base_origem=origem,
                base_destino=destino,
                resultado=resultado
            )

            # 🔥 evita duplicação no F5
            return redirect('home')

    historico = Conversao.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')[:20]

    return render(request, 'core/home.html', {
        'resultado': resultado,
        'erro': erro,
        'historico': historico
    })


# ========================
# 🎮 DESAFIO
# ========================

@login_required
def desafio(request):
    if 'desafio' not in request.session:
        request.session['desafio'] = gerar_desafio()

    desafio_atual = request.session['desafio']
    feedback = None

    if request.method == 'POST':
        resposta = request.POST.get('resposta', '').strip().lower()

        correto = converter_valor(
            desafio_atual['valor'],
            desafio_atual['origem'],
            desafio_atual['destino']
        )

        acertou = resposta == (correto or "").lower()

        # salva no banco
        Desafio.objects.create(
            usuario=request.user,
            valor=desafio_atual['valor'],
            base_origem=desafio_atual['origem'],
            base_destino=desafio_atual['destino'],
            resposta_usuario=resposta,
            resposta_correta=correto,
            acertou=acertou
        )

        feedback = {
            'acertou': acertou,
            'correto': correto
        }

        # ✅ SÓ GERA NOVO SE ACERTAR
        if acertou:
            request.session['desafio'] = gerar_desafio()

        desafio_atual = request.session['desafio']

    historico = Desafio.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')[:20]

    return render(request, 'core/desafio.html', {
        'desafio': desafio_atual,
        'feedback': feedback,
        'historico': historico
    })


# ========================
# 👤 REGISTER
# ========================

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)  # 🔥 já loga direto
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {
        'form': form
    })