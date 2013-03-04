from django.core.management.base import NoArgsCommand

from user_info.views import delete_info


class Command(NoArgsCommand):
    help_text = ''' Delete vimeo user info from the database '''

    def handle_noargs(self, **options):
        delete_info()
