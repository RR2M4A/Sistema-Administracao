from django.db import migrations

def create_default_departments(apps, schema_editor):

    Department = apps.get_model('core', 'Department')

    defaults = [
        {'name': 'Coordenação de Administração Geral', 'acronym': 'COAG'},
        {'name': 'Gerência de Administração', 'acronym': 'GEAD'},
        {'name': 'Núcleo de Informática', 'acronym': 'NUINF'},
        {'name': 'Núcleo de Material e Patrimônio', 'acronym': 'NUMAP'},
        {'name': 'Gerência de Orçamento e Finanças', 'acronym': 'GEOFIN'},
        {'name': 'Gerência de Pessoas', 'acronym': 'GEPES'},
        {'name': 'Coordenação de Desenvolvimento', 'acronym': 'CODES'},
        {'name': 'Diretoria de Desenvolvimento e Territorial', 'acronym': 'DIDOT'},
        {'name': 'Gerência de Gestão do Território e Desevolvimento Econômico', 'acronym': 'GETEDEC'},
        {'name': 'Diretoria de Articulação', 'acronym': 'DIART'},
        {'name': 'Gerência de Políticas Sociais, Cultura, Esporte e Lazer', 'acronym': 'GEPSCEL'},
        {'name': 'Coordenação de Licenciamento, Obras e Manutenção', 'acronym': 'COLOM'},
        {'name': 'Diretoria de Aprovação e Licenciamento', 'acronym': 'DIALIC'},
        {'name': 'Gerência de Licenciamento de Obras e Atividades Econômicas', 'acronym': 'GELOAE'},
        {'name': 'Gerência de Elaboração e Aprovação de Projetos', 'acronym': 'GEAPRO'},
        {'name': 'Diretoria de Obras', 'acronym': 'DIROB'},
        {'name': 'Gerência de Obras', 'acronym': 'GEOB'},
        {'name': 'Gerência de Manutenção e Conservação', 'acronym': 'GEMAC'},
        {'name': 'Assessoria de comunicação', 'acronym': 'ASCOM'},
        {'name': 'Assessoria Técnica', 'acronym': 'ASTEC'},
        {'name': 'Assessoria de Planejamento', 'acronym': 'ASPLAN'},
        {'name': 'Gabinete', 'acronym': 'GAB'},
        {'name': 'Ouvidoria', 'acronym': 'OUV'},
        {'name': 'Junta de Serviço Militar', 'acronym': 'JSM'},
    ]

    for dept in defaults:
        Department.objects.create(name=dept['name'], acronym=dept['acronym'])

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_departments),
    ]