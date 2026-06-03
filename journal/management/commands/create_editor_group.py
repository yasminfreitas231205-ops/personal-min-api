from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from journal.models import JournalEntry


class Command(BaseCommand):
    help = 'Cria o grupo "Editor" com permissões de leitura para todas as entradas'

    def handle(self, *args, **options):
        # Criar ou obter o grupo 'Editor'
        group, created = Group.objects.get_or_create(name='Editor')
        
        # Obter o tipo de conteúdo para JournalEntry
        content_type = ContentType.objects.get_for_model(JournalEntry)
        
        # Obter ou criar as permissões (as permissões padrão já devem existir)
        # Permissões padrão: view_journalentry, add_journalentry, change_journalentry, delete_journalentry
        try:
            view_permission = Permission.objects.get(
                content_type=content_type,
                codename='view_journalentry'
            )
            group.permissions.add(view_permission)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.WARNING('Permissão view_journalentry não encontrada'))
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Editor" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Editor" já existe.')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Permissão de leitura (view_journalentry) adicionada ao grupo "Editor".')
        )
