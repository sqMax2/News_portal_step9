from django.core.management.base import BaseCommand, CommandError
from newsapp.models import Post, Category


class Command(BaseCommand):

    help = 'Wipes all posts in category after confirm at console'  # "python manage.py <command> --help"
    requires_migrations_checks = True  # reminds of migrations

    def add_arguments(self, parser):
        # parser.add_argument('argument', nargs='+', type=int)
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):

        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all posts at {options["category"]}? yes/no')  # confirmation request
        answer = input()  # reads confirmation

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))
            return

        try:
            category = Category.objects.get(name=options["category"])
            category.posts.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))

        # if answer == 'yes':
        #     Category.objects.get(name='').posts.all().delete()
        #     # Post.objects.all().delete()
        #     self.stdout.write(self.style.SUCCESS('Successfully wiped posts!'))
        #     return
        #
        # self.stdout.write(
        #     self.style.ERROR('Access denied'))
