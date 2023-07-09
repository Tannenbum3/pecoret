from django.db import migrations, models
import django.db.models.deletion


def migrate_asset_to_component(apps, schema_editor):
    Finding = apps.get_model('backend', 'Finding')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    for finding in Finding.objects.all():
        for asset in ["web_application", "host", "service", "mobile_application"]:
            if getattr(finding, asset):
                finding_asset = getattr(finding, asset)
                break
        finding.component = finding_asset
        finding.component_object_id = finding_asset.pk
        finding.component_content_type = ContentType.objects.get_for_model(finding_asset)
        finding.save()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("backend", "0006_alter_advisory_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="finding",
            name="component_content_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(("app_label", "backend"), ("model", "webapplication")),
                    models.Q(("app_label", "backend"), ("model", "service")),
                    models.Q(("app_label", "backend"), ("model", "host")),
                    models.Q(("app_label", "backend"), ("model", "mobileapplication")),
                    _connector="OR",
                ),
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="component_object_id",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddIndex(
            model_name="finding",
            index=models.Index(
                fields=["component_content_type", "component_object_id"],
                name="backend_fin_compone_af25d2_idx",
            ),
        ),
        migrations.RunPython(migrate_asset_to_component)
    ]
