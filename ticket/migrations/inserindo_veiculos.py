from django.db import migrations, models

class Migration(migrations.Migration):


    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="INSERT INTO ticket_veiculo(descricao) VALUES ('Carro'), ('Moto')",
            hints={"target_db": "default"}

        )
    ]