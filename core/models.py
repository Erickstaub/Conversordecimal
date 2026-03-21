from django.db import models

# Create your models he
from django.db import models
from django.contrib.auth.models import User

class Conversao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_entrada = models.CharField(max_length=100)
    base_origem = models.CharField(max_length=10)
    base_destino = models.CharField(max_length=10)
    resultado = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valor_entrada} ({self.base_origem} → {self.base_destino})"

class Desafio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.CharField(max_length=100)
    base_origem = models.CharField(max_length=10)
    base_destino = models.CharField(max_length=10)
    resposta_usuario = models.CharField(max_length=100)
    resposta_correta = models.CharField(max_length=100)
    acertou = models.BooleanField()
    criado_em = models.DateTimeField(auto_now_add=True)


class Pontuacao(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    desafios_respondidos = models.IntegerField(default=0)
    desafios_corretos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.pontos} pts"