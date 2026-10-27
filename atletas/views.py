import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from .models import Atleta, Torneio, DesempenhoFutebol, DesempenhoVolei, DesempenhoBasquete

def normalizar(texto):
    # tira acento e deixa minúsculo: "Vôlei" vira "volei"
    texto = unicodedata.normalize('NFKD', texto)
    return texto.encode('ascii', 'ignore').decode('ascii').lower()


def tabela_do_esporte(nome_esporte):
    nome = normalizar(nome_esporte)
    if 'futebol' in nome:
        return DesempenhoFutebol
    if 'volei' in nome:
        return DesempenhoVolei
    if 'basquete' in nome:
        return DesempenhoBasquete
    return None


def lista_atletas(request):
    atletas = Atleta.objects.select_related('id_esporte').all()
    return render(request, 'atletas/lista.html', {'atletas': atletas})


def detalhe_atleta(request, id_atleta):
    atleta = get_object_or_404(Atleta.objects.select_related('id_esporte'), pk=id_atleta)

    modelo = tabela_do_esporte(atleta.id_esporte.nome)
    desempenho = None
    if modelo:
        desempenho = modelo.objects.filter(id_atleta=atleta).select_related('id_torneio').first()

    # monta uma lista de (nome interno, nome bonito, valor), pulando id e chaves estrangeiras
    estatisticas = []
    if desempenho:
        for campo in desempenho._meta.fields:
            if campo.primary_key or campo.is_relation:
                continue
            valor = getattr(desempenho, campo.name)
            estatisticas.append((campo.name, campo.verbose_name.capitalize(), valor))

    return render(request, 'atletas/detalhe.html', {
        'atleta': atleta,
        'desempenho': desempenho,
        'estatisticas': estatisticas,
        'torneio': Torneio.objects.filter(id_esporte=atleta.id_esporte).first(),
    })

def editar_estatisticas(request, id_atleta):
    atleta = get_object_or_404(Atleta.objects.select_related('id_esporte'), pk=id_atleta)

    modelo = tabela_do_esporte(atleta.id_esporte.nome)
    if modelo is None:
        return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)

    desempenho = modelo.objects.filter(id_atleta=atleta).first()
    if desempenho is None:
        return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)

    # formulário gerado automaticamente, sem os campos de atleta e torneio
    Formulario = modelform_factory(modelo, exclude=['id_atleta', 'id_torneio'])

    if request.method == 'POST':
        form = Formulario(request.POST, instance=desempenho)
        if form.is_valid():
            form.save()
            return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)
    else:
        form = Formulario(instance=desempenho)

    return render(request, 'atletas/editar.html', {'atleta': atleta, 'form': form})

def ajustar_estatistica(request, id_atleta):
    if request.method != 'POST':
        return redirect('detalhe_atleta', id_atleta=id_atleta)

    atleta = get_object_or_404(Atleta.objects.select_related('id_esporte'), pk=id_atleta)
    modelo = tabela_do_esporte(atleta.id_esporte.nome)

    if modelo:
        desempenho = modelo.objects.filter(id_atleta=atleta).first()
        campo = request.POST.get('campo')
        acao = request.POST.get('acao')

        # só aceita campos de estatística de verdade (nada de id ou chave estrangeira)
        campos_validos = [c.name for c in modelo._meta.fields
                          if not c.primary_key and not c.is_relation]

        if desempenho and campo in campos_validos:
            valor = getattr(desempenho, campo) or 0
            if acao == 'mais':
                valor = valor + 1
            elif acao == 'menos':
                valor = max(valor - 1, 0)
            setattr(desempenho, campo, valor)
            desempenho.save(update_fields=[campo])

    return redirect('detalhe_atleta', id_atleta=id_atleta)

def cadastrar_atleta(request):
    FormularioAtleta = modelform_factory(
        Atleta,
        fields=['nome', 'id_esporte'],
        labels={'nome': 'Nome', 'id_esporte': 'Esporte'},
    )

    if request.method == 'POST':
        form = FormularioAtleta(request.POST)
        if form.is_valid():
            atleta = form.save()

            # cria a linha de estatísticas zerada no torneio do esporte
            modelo = tabela_do_esporte(atleta.id_esporte.nome)
            torneio = Torneio.objects.filter(id_esporte=atleta.id_esporte).first()
            if modelo and torneio:
                zeros = {c.name: 0 for c in modelo._meta.fields
                         if not c.primary_key and not c.is_relation}
                modelo.objects.create(id_atleta=atleta, id_torneio=torneio, **zeros)

            return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)
    else:
        form = FormularioAtleta()

    return render(request, 'atletas/cadastrar.html', {'form': form})


def excluir_atleta(request, id_atleta):
    atleta = get_object_or_404(Atleta, pk=id_atleta)

    if request.method == 'POST':
        for modelo in (DesempenhoFutebol, DesempenhoVolei, DesempenhoBasquete):
            modelo.objects.filter(id_atleta=atleta).delete()
        atleta.delete()
        return redirect('lista_atletas')

    return render(request, 'atletas/excluir.html', {'atleta': atleta})

def editar_atleta(request, id_atleta):
    atleta = get_object_or_404(Atleta, pk=id_atleta)
    FormularioAtleta = modelform_factory(Atleta, fields=['nome'], labels={'nome': 'Nome'})

    if request.method == 'POST':
        form = FormularioAtleta(request.POST, instance=atleta)
        if form.is_valid():
            form.save()
            return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)
    else:
        form = FormularioAtleta(instance=atleta)

    return render(request, 'atletas/editar_atleta.html', {'atleta': atleta, 'form': form})

def criar_desempenho_zerado(atleta):
    modelo = tabela_do_esporte(atleta.id_esporte.nome)
    torneio = Torneio.objects.filter(id_esporte=atleta.id_esporte).first()
    if modelo is None or torneio is None:
        return None

    existente = modelo.objects.filter(id_atleta=atleta, id_torneio=torneio).first()
    if existente:
        return existente

    zeros = {c.name: 0 for c in modelo._meta.fields
             if not c.primary_key and not c.is_relation}
    return modelo.objects.create(id_atleta=atleta, id_torneio=torneio, **zeros)


def criar_estatisticas(request, id_atleta):
    atleta = get_object_or_404(Atleta.objects.select_related('id_esporte'), pk=id_atleta)
    if request.method == 'POST':
        criar_desempenho_zerado(atleta)
    return redirect('detalhe_atleta', id_atleta=atleta.id_atleta)