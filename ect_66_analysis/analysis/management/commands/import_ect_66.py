import environ
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine

from ect_66_analysis.analysis.models import (
    Province, Constituency, Party, CandidateConstituency, CandidatePartyList,
    CandidatePM, ResultConstituenciesPartyListConst, ResultConstituenciesStatus, ResultConstituenciesCandidateConst,
    ResultSummary
)


class Command(BaseCommand):
    help = "import data to database"

    def handle(self, *args, **options):
        data_file = str(settings.BASE_DIR / "data" / "ECT_report_66.xlsx")
        env = environ.Env()
        engine = create_engine(env.str('DATABASE_URL'))

        ResultSummary.objects.all().delete()
        ResultConstituenciesStatus.objects.all().delete()
        ResultConstituenciesCandidateConst.objects.all().delete()
        ResultConstituenciesPartyListConst.objects.all().delete()
        CandidatePM.objects.all().delete()
        CandidatePartyList.objects.all().delete()
        CandidateConstituency.objects.all().delete()
        Party.objects.all().delete()
        Constituency.objects.all().delete()
        Province.objects.all().delete()

        with engine.connect() as conn:
            # info_province
            df = pd.read_excel(data_file, sheet_name='info_province').set_index('prov_id')
            df.to_sql('analysis_province', conn, if_exists='append')

            # info_constituency
            df = pd.read_excel(data_file, sheet_name='info_constituency').groupby(
                ['cons_id', 'cons_no', 'prov_id', 'registered_vote', 'total_vote_stations']
            ).sum()
            df.to_sql('analysis_constituency', conn, if_exists='append')

            # info_party_overview
            df = pd.read_excel(data_file, sheet_name='info_party_overview').set_index('id')
            df.to_sql('analysis_party', conn, if_exists='append')

            # Candidate_Constituency
            df = pd.read_excel(data_file, sheet_name='Candidate_Constituency').set_index('mp_app_id')
            df.to_sql('analysis_candidateconstituency', conn, if_exists='append')

            # Candidate_PartyList
            df = pd.read_excel(data_file, sheet_name='Candidate_PartyList')
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_candidatepartylist', conn, if_exists='append')

            # Candidate_PM
            df = pd.read_excel(data_file, sheet_name='Candidate_PM')
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_candidatepm', conn, if_exists='append')

            # result_constituencies_PartyList
            df = pd.read_excel(data_file, sheet_name='result_constituencies_PartyList')
            df = df.drop(['party_list_vote_percent'], axis=1)
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_resultconstituenciespartylistconst',
                      conn, if_exists='append')

            # result_constituencies_Candidate
            df = pd.read_excel(data_file, sheet_name='result_constituencies_Candidate')
            df = df.drop(['mp_app_vote_percent'], axis=1)
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_resultconstituenciescandidateconst',
                      conn, if_exists='append')

            # result_constituencies_status
            df = pd.read_excel(data_file, sheet_name='result_constituencies_status')
            df = df.drop(['counted_vote_stations', 'percent_count', 'pause_report'],
                         axis=1)
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_resultconstituenciesstatus',
                      conn, if_exists='append')

            # ref: https://www.bbc.com/thai/articles/c3g79jd8qj1o
            result_summary_data = (
                (726, 112, 39),
                (705, 112, 29),
                (709, 68, 3),
                (743, 39, 1),
                (763, 23, 13),
                (701, 22, 3),
                (707, 9, 1),
                (740, 7, 2),
                (762, 5, 1),
                (773, 2, 0),
                (706, 1, 1),
                (719, 0, 1),
                (712, 0 ,1),
                (778, 0, 1),
                (776, 0, 1),
                (747, 0, 1),
                (761, 0, 1),
                (714, 0, 1),
            )
            df = pd.DataFrame(result_summary_data, columns=['party_id', 'constituencies_count', 'party_list_count'])
            df.index += 1
            df.index.name = 'id'
            df.to_sql('analysis_resultsummary', conn, if_exists='append')
