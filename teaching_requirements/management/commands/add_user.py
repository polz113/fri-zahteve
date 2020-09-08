import logging
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django_auth_ldap.backend import LDAPBackend
# from ldap3 import Server, Connection, ALL
import ldap

from teaching_requirements.models import Teacher
from django.contrib.auth.models import User


def create_single_user(first_name=None, last_name=None,
                       uid=None, code=None, teacher_code=None,
                       write_to_db=False, out_stream=sys.stdout,
                       name_encoding='utf-8'):
    """
    Add a new user, create a Teacher object.
    """
    logger = logging.getLogger(__name__)
    logger.info("Creating single user")
    logger.debug("FN: {0}, LN: {1}, UID: {2}, code: {3}, tc: {4}, wdb: {5}, os: {6}".format(
        first_name, last_name, uid, code, teacher_code, write_to_db, out_stream
    ))
    try:
        logger.debug("Creating LDAP backend")
        ldap_backend = LDAPBackend()
    except:
        logger.exception()
        ldap_backend = None

    logger.debug("LDAP connecting to {0}".format(settings.AUTH_LDAP_SERVER_URI))
    attributes = ['userprincipalname', 'givenname', 'sn', 'objectclass']
    conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    conn.simple_bind_s(settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)
    # Connection(server, settings.AUTH_LDAP_BIND_DN,
    #                  settings.AUTH_LDAP_BIND_PASSWORD, auto_bind=True)
    logger.debug("LDAP BIND with username {0}".format(settings.AUTH_LDAP_BIND_DN))
    s = settings.AUTH_LDAP_USER_SEARCH
    if uid is None and (first_name is not None and last_name is not None):
        logger.debug("UID is none, trying name based search")
        k = (first_name, last_name)
        filterstr = '(&(givenName={0})(sn={1}))'.format(first_name.encode(name_encoding),
                                                        last_name.encode(name_encoding))
        logger.debug("Filterstring: {0}".format(filterstr))
        try:
            results = conn.search_s(s.base_dn, filterstr)
        except Exception:
            logger.debug("Error during LDAP search")
        logger.debug("Got results: {0}".format(results))
        if len(results) == 0:
            logger.debug("No results found")
            return False
        res1 = results[0]
        v = res1.userprincipalname.value
    else:
        logger.debug("UID is not none, perform UID search")
        k = None
        v = uid
        filterstr = "(userprincipalname={0})".format(v)
        logger.debug("Filterstring: {0}".format(filterstr))
        try:
            results = conn.search_s(s.base_dn, ldap.SCOPE_SUBTREE, filterstr, attributes)
        except Exception:
            logger.exception("Error during LDAP search")
        logger.debug("Got results: {0}".format(results))
        if len(results) == 0:
            logger.debug("No results found")
            return False
        res1 = results[0][1]
        k = (res1['givenName'][0], res1['sn'][0])
        if first_name is None:
            first_name = k[0].decode(name_encoding)
            logger.debug("Set first name to {0}".format(first_name))
        if last_name is None:
            last_name = k[1].decode(name_encoding)
            # last_name = k[1].upper()
            logger.debug("Set last name to {0}".format(first_name))

    logger.debug("Found {} {}: {}".format(
        first_name, last_name, v))

    if ldap_backend is not None:
        try:
            logger.debug("Populating user")
            u = ldap_backend.populate_user(v)
            if u is None:
                raise Exception("user " + v + " not found in ldap!")
            else:
                logger.debug("Populated user: {0}".format(u))
                u.save()
            u = User.objects.get(username__iexact=v)
            u.first_name = first_name
            u.last_name = last_name
            logger.debug("Setting first nad last name: {}; {}".format(first_name, last_name))
            if write_to_db:
                logger.debug("Saving user to DB")
                u.save()
            try:
                if teacher_code is not None:
                    logger.debug("Creating corresponding teacher")
                    if hasattr(u, "teacher"):
                        t = u.teacher
                        t.code = teacher_code
                    else:
                        t, created = Teacher.objects.get_or_create(
                            code=teacher_code, defaults={'user_id': u.id})
                    logger.debug("{}".format(t))
                    old_user = t.user
                    t.user = u
                    logger.debug("Changing user on teacher to {0}".format(u))
                    if write_to_db:
                        if old_user is not None and old_user.id != u.id:
                            logger.debug("Deleting old user {}".format(old_user))
                            old_user.delete()
                        logger.debug("Saving teacher")
                        t.save()
                    else:
                        logger.debug("Teacher not saved: {}".format(t))
            except Exception as e:
                print(e)
                logger.exception("Error creating teacher")
            return u
        except:
            logger.exception("Error during teacher creation")
    else:
        logger.error("No LDAP backend found")


class Command(BaseCommand):
    WRITE_TO_DB = True

    help = """Populate user from uni-lj.si LDAP"""

    def add_arguments(self, parser):
        parser.add_argument('--username', nargs=1, help="import user by username")
        parser.add_argument('--name', nargs=2, help="import user by first_name, last_name")

    def handle(self, *args, **options):
        username = options['username']
        name = options['name']
        if username:
            create_single_user(uid=username[0], write_to_db=self.WRITE_TO_DB)
        elif name:
            create_single_user(first_name=name[0].upper(),
                               last_name=name[1].upper(),
                               write_to_db=self.WRITE_TO_DB, out_stream=self.stdout)
