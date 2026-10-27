# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Atleta(models.Model):
    id_atleta = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    id_esporte = models.ForeignKey('Esporte', models.DO_NOTHING, db_column='id_esporte')

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'atleta'


class DesempenhoBasquete(models.Model):
    id_desempenho = models.AutoField(primary_key=True)
    id_atleta = models.ForeignKey(Atleta, models.DO_NOTHING, db_column='id_atleta')
    id_torneio = models.ForeignKey('Torneio', models.DO_NOTHING, db_column='id_torneio')
    jogos = models.IntegerField(blank=True, null=True)
    assistencias = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    faltas_cometidas = models.IntegerField(blank=True, null=True)
    pontos = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rebotes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    roubos_de_bola = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tocos_bloqueios = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    turnovers = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cestas_3_pontos = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    minutos_jogados = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'desempenho_basquete'
        unique_together = (('id_atleta', 'id_torneio'),)


class DesempenhoFutebol(models.Model):
    id_desempenho = models.AutoField(primary_key=True)
    id_atleta = models.ForeignKey(Atleta, models.DO_NOTHING, db_column='id_atleta')
    id_torneio = models.ForeignKey('Torneio', models.DO_NOTHING, db_column='id_torneio')
    jogos = models.IntegerField(blank=True, null=True)
    gols = models.IntegerField(blank=True, null=True)
    assistencias = models.IntegerField(blank=True, null=True)
    cartoes_amarelos = models.IntegerField(blank=True, null=True)
    cartoes_vermelhos = models.IntegerField(blank=True, null=True)
    finalizacoes = models.IntegerField(blank=True, null=True)
    passes_certos = models.IntegerField(blank=True, null=True)
    desarmes = models.IntegerField(blank=True, null=True)
    faltas_cometidas = models.IntegerField(blank=True, null=True)
    minutos_jogados = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'desempenho_futebol'
        unique_together = (('id_atleta', 'id_torneio'),)


class DesempenhoVolei(models.Model):
    id_desempenho = models.AutoField(primary_key=True)
    id_atleta = models.ForeignKey(Atleta, models.DO_NOTHING, db_column='id_atleta')
    id_torneio = models.ForeignKey('Torneio', models.DO_NOTHING, db_column='id_torneio')
    jogos = models.IntegerField(blank=True, null=True)
    assistencias = models.IntegerField(blank=True, null=True)
    faltas = models.IntegerField(blank=True, null=True)
    ataques_pontos = models.IntegerField(blank=True, null=True)
    bloqueios = models.IntegerField(blank=True, null=True)
    saques_aces = models.IntegerField(blank=True, null=True)
    recepcoes = models.IntegerField(blank=True, null=True)
    erros_saque = models.IntegerField(blank=True, null=True)
    erros_ataque = models.IntegerField(blank=True, null=True)
    pontos_totais = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'desempenho_volei'
        unique_together = (('id_atleta', 'id_torneio'),)


class Esporte(models.Model):
    id_esporte = models.AutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'esporte'


class Torneio(models.Model):
    id_torneio = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    id_esporte = models.ForeignKey(Esporte, models.DO_NOTHING, db_column='id_esporte')

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'torneio'
