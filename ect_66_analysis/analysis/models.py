from django.db import models


class Province(models.Model):
    province_id = models.IntegerField(db_index=True)
    prov_id = models.CharField(max_length=6, primary_key=True)
    province = models.CharField(max_length=200)
    eng = models.CharField(max_length=200)
    abbre_thai = models.CharField(max_length=10)
    total_registered_vote = models.IntegerField()
    total_vote_stations = models.IntegerField()

    def __str__(self):
        return f'[{self.prov_id}] {self.province}'


class Constituency(models.Model):
    cons_id = models.CharField(primary_key=True, max_length=10)
    cons_no = models.IntegerField()
    prov = models.ForeignKey(Province, models.PROTECT)
    registered_vote = models.IntegerField()
    total_vote_stations = models.IntegerField()
    zone = models.TextField()

    def __str__(self):
        return f'{self.cons_id}'


class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    party_no = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=200)
    abbr = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    logo_url = models.URLField()

    def __str__(self):
        return f'[{self.party_no}] {self.name}'


class CandidateConstituency(models.Model):
    mp_app_id = models.CharField(max_length=20, primary_key=True)
    mp_app_name = models.CharField(max_length=200)
    mp_app_no = models.IntegerField()
    mp_app_party = models.ForeignKey(Party, models.PROTECT, to_field='id')
    image_url = models.URLField()

    def __str__(self):
        return f'{self.mp_app_party} - {self.mp_app_name}'


class CandidatePartyList(models.Model):
    party = models.ForeignKey(Party, models.PROTECT,
                              to_field='party_no', db_column='party_no')
    list_no = models.IntegerField()
    name = models.CharField(max_length=200)
    image_url = models.URLField()

    def __str__(self):
        return f'{self.party} - {self.name}'


class CandidatePM(models.Model):
    party = models.ForeignKey(Party, models.PROTECT,
                              to_field='party_no', db_column='party_no')
    name = models.CharField(max_length=200)
    image_url = models.URLField()

    def __str__(self):
        return f'{self.party} - {self.name}'


class ResultConstituenciesPartyListConst(models.Model):
    cons = models.ForeignKey(Constituency, models.PROTECT, to_field='cons_id')
    party = models.ForeignKey(Party, models.PROTECT)
    party_list_vote = models.IntegerField()

    def __str__(self):
        return f'{self.cons} - {self.party} - {self.party_list_vote}'


class ResultConstituenciesCandidateConst(models.Model):
    cons = models.ForeignKey(Constituency, models.PROTECT)
    mp_app = models.ForeignKey(CandidateConstituency, models.PROTECT)
    mp_app_rank = models.IntegerField()
    mp_app_vote = models.IntegerField()
    party = models.ForeignKey(Party, models.PROTECT)

    def __str__(self):
        return f'{self.cons} - {self.mp_app} - {self.mp_app_vote}'


class ResultConstituenciesStatus(models.Model):
    prov = models.ForeignKey(Province, models.PROTECT)
    cons = models.ForeignKey(Constituency, models.PROTECT)
    turn_out = models.IntegerField()
    percent_turn_out = models.FloatField()

    def __str__(self):
        return f'{self.cons} - {self.prov} - {self.percent_turn_out}%'
