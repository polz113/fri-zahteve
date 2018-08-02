import logging

from django.core.management.base import BaseCommand

from frinajave.models import TeacherSubjectCycles
from friprosveta.models import LectureType, Subject
from friprosveta.studis import Najave
from timetable.models import TimetableSet

logger = logging.getLogger(__name__)

tip_izv_map = {
    1: 'P',
    2: 'AV',
    3: 'LV',
    4: 'LV',
    5: 'LV',
    6: 'LV',
    7: 'P',
    8: 'LV',
}


class Command(BaseCommand):
    """
    Get najave from studis.
    """
    args = 'studis_import year'
    help = '''Usage:
studis_import year

Year is the first part in the study year:
2015/2016 -> 2015
'''

    def add_arguments(self, parser):
        parser.add_argument('year', nargs=1, type=str)

    def handle(self, *args, **options):
        logger.info("Entering handle")
        logger.debug("Args: {}".format(args))
        logger.debug("Options: {}".format(options))
        year = options['year'][0]
        "Semester can be 1 (zimski), 2(poletni), 3(celoletni) or 4(blocni)."

        studis_najave = Najave(year)
        predmeti_cikli = studis_najave.get_predmeti_cikli()
        izvajanja_ids = studis_najave.get_izvajanja_ids()

        for predmet_cikli in predmeti_cikli:
            for cikel in predmet_cikli['izvajalci']:
                tip_izv_zahteve = tip_izv_map[cikel['tip_izvajanja']['id']][0]
                subject_code = predmet_cikli['predmet_sifra']
                teacher_code = cikel['delavec_sifra']
                cycles = cikel['cikli_stevilo']
                
