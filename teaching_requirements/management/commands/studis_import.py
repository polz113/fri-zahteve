import logging
from collections import defaultdict
from django.core.management.base import BaseCommand

from teaching_requirements.studis import Najave, Osebe, Studij
from teaching_requirements.models import Subject, Activity, Teacher
from .add_user import create_single_user

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

def make_short_name(name):
    """
    Create short_name from the long one.
    """
    ignore = ['IN', 'V', 'Z', 'S']
    return ''.join([s[0] for s in filter(lambda s: s not in ignore, name.upper().split())])


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
        ucitelji = dict()
        ucitelji_po_id = dict()
        for ucitelj in Osebe().get_osebe():
            ucitelji[ucitelj['sifra_predavatelja']] = ucitelj
            ucitelji_po_id[ucitelj['id']] = ucitelj
        studis_najave = Najave(year)
        predmeti = dict()
        for predmet in Studij(year).get_predmeti():
            predmeti[predmet['sifra']] = predmet
        predmeti_cikli = studis_najave.get_predmeti_cikli()
        izvajanja_ids = studis_najave.get_izvajanja_ids()
        odgovorni = defaultdict(set)
        ucitelji_po_upn = dict()
        subjects = dict()
        for predmet_cikli in predmeti_cikli:
            for cikel in predmet_cikli['izvajalci']:
                tip_izv_zahteve = tip_izv_map[cikel['tip_izvajanja']['id']][0]
                subject_code = predmet_cikli['predmet_sifra']
                predmet = predmeti[subject_code]
                subject_name = predmet['naslov'].get('sl', list(predmet['naslov'].values())[0]) 
                short_name = make_short_name(subject_name)
                subject, created = Subject.objects.get_or_create(
                    code = subject_code,
                    defaults = {'name': subject_name, 'short_name': short_name})
                if not created:
                    subject.name = subject_name
                    subject.short_name = short_name
                    for activity in subject.activity_set.all():
                        activity.teachers.clear()
                subject.save()
                subjects[subject_code] = subject.id
                teacher_code = cikel['delavec_sifra']
                ucitelj = ucitelji.get(teacher_code, ucitelji_po_id[cikel['delavec_id']])
                cycles = cikel['cikli_stevilo']
                upn = ucitelj['upn']
                if upn is not None:
                    odgovorni[ucitelj['upn']].add((subject_code, tip_izv_zahteve))
                    ucitelji_po_upn[upn] = ucitelj
        for upn, codes in odgovorni.items():
            teacher_code = ucitelji_po_upn[upn]['sifra_predavatelja']
            create_single_user(
                uid=upn, write_to_db=True, 
                teacher_code=teacher_code)
            print(upn, teacher_code)
            teacher = Teacher.objects.get(code=teacher_code)
            for code, lecture_type in codes:
                activity, created = Activity.objects.get_or_create(
                    subject_id = subjects[code], lecture_type = lecture_type)
                activity.teachers.add(teacher)
                
