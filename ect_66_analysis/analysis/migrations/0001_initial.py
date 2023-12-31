# Generated by Django 4.2.4 on 2023-08-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CandidateConstituency",
            fields=[
                ("mp_app_id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("mp_app_name", models.CharField(max_length=200)),
                ("mp_app_no", models.IntegerField()),
                ("image_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Constituency",
            fields=[
                ("cons_id", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("cons_no", models.IntegerField()),
                ("registered_vote", models.IntegerField()),
                ("total_vote_stations", models.IntegerField()),
                ("zone", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Party",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("party_no", models.IntegerField(null=True, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("abbr", models.CharField(max_length=20)),
                ("color", models.CharField(max_length=10)),
                ("logo_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Province",
            fields=[
                ("province_id", models.IntegerField(db_index=True)),
                ("prov_id", models.CharField(max_length=6, primary_key=True, serialize=False)),
                ("province", models.CharField(max_length=200)),
                ("eng", models.CharField(max_length=200)),
                ("abbre_thai", models.CharField(max_length=10)),
                ("total_registered_vote", models.IntegerField()),
                ("total_vote_stations", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ResultConstituenciesStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("turn_out", models.IntegerField()),
                ("percent_turn_out", models.FloatField()),
                ("cons", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.constituency")),
                ("prov", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.province")),
            ],
        ),
        migrations.CreateModel(
            name="ResultConstituenciesPartyListConst",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("party_list_vote", models.IntegerField()),
                ("cons", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.constituency")),
                ("party", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.party")),
            ],
        ),
        migrations.CreateModel(
            name="ResultConstituenciesCandidateConst",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mp_app_rank", models.IntegerField()),
                ("mp_app_vote", models.IntegerField()),
                ("cons", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.constituency")),
                (
                    "mp_app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="analysis.candidateconstituency"
                    ),
                ),
                ("party", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.party")),
            ],
        ),
        migrations.AddField(
            model_name="constituency",
            name="prov",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.province"),
        ),
        migrations.CreateModel(
            name="CandidatePM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("image_url", models.URLField()),
                (
                    "party",
                    models.ForeignKey(
                        db_column="party_no",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="analysis.party",
                        to_field="party_no",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CandidatePartyList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("list_no", models.IntegerField()),
                ("name", models.CharField(max_length=200)),
                ("image_url", models.URLField()),
                (
                    "party",
                    models.ForeignKey(
                        db_column="party_no",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="analysis.party",
                        to_field="party_no",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="candidateconstituency",
            name="mp_app_party",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="analysis.party"),
        ),
    ]
