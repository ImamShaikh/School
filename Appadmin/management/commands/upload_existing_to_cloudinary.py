"""
Management command: upload_existing_to_cloudinary

Uploads existing local media files to Cloudinary and updates the
corresponding database records so they point to the new Cloudinary URLs.

Usage:
    python manage.py upload_existing_to_cloudinary
    python manage.py upload_existing_to_cloudinary --dry-run   # preview only

IMPORTANT:
  - Run this AFTER setting CLOUDINARY_URL in your .env / Render env vars.
  - Run this ONCE. Running it again will create duplicate uploads.
  - Back up your database before running in production.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = (
        "One-time migration: uploads existing local media files to Cloudinary "
        "and updates database references."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which files would be uploaded without actually uploading.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Verify Cloudinary is configured
        cloudinary_url = os.environ.get('CLOUDINARY_URL', '')
        if not cloudinary_url:
            self.stderr.write(
                self.style.ERROR(
                    "CLOUDINARY_URL is not set. Set it in your .env file or "
                    "Render environment variables before running this command."
                )
            )
            return

        import cloudinary
        import cloudinary.uploader

        self.stdout.write(self.style.SUCCESS("=== Cloudinary Migration ==="))
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN mode — no files will be uploaded.\n"))

        # Import all models that have image/file fields
        from Appadmin.models import (
            Teacher, SchoolInfo, Event, News,
            GalleryImage, ManagementMember, Facility
        )

        # Define (model, field_name, cloudinary_folder) tuples
        model_fields = [
            (Teacher,          'image',          'teachers'),
            (SchoolInfo,       'logo',           'school'),
            (SchoolInfo,       'principal_photo','school'),
            (Event,            'image',          'events'),
            (News,             'image',          'news'),
            (GalleryImage,     'image',          'gallery'),
            (ManagementMember, 'photo',          'management'),
            (Facility,         'image',          'facilities'),
        ]

        total_uploaded = 0
        total_skipped  = 0
        total_errors   = 0

        for Model, field_name, folder in model_fields:
            model_name = Model.__name__
            self.stdout.write(f"\n[{model_name}.{field_name}]")

            for obj in Model.objects.all():
                field_value = getattr(obj, field_name)

                if not field_value:
                    self.stdout.write(f"  id={obj.pk}: no image — skipping")
                    total_skipped += 1
                    continue

                # Build the local file path
                field_name_str = str(field_value.name)

                # Already a Cloudinary URL? Skip.
                if field_name_str.startswith('http://') or field_name_str.startswith('https://'):
                    self.stdout.write(f"  id={obj.pk}: already a URL ({field_name_str[:60]}…) — skipping")
                    total_skipped += 1
                    continue

                local_path = os.path.join(settings.MEDIA_ROOT, field_name_str)

                if not os.path.isfile(local_path):
                    self.stdout.write(
                        self.style.WARNING(f"  id={obj.pk}: local file not found: {local_path}")
                    )
                    total_skipped += 1
                    continue

                file_basename = os.path.basename(field_name_str)
                public_id = f"{folder}/{os.path.splitext(file_basename)[0]}"

                self.stdout.write(f"  id={obj.pk}: {local_path} → cloudinary:{public_id}")

                if dry_run:
                    total_uploaded += 1
                    continue

                try:
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder=folder,
                        public_id=os.path.splitext(file_basename)[0],
                        overwrite=False,       # Don't overwrite existing
                        resource_type='image',
                        tags=['govind-ashramshala', 'migrated'],
                    )
                    # Update the DB field to store the Cloudinary public_id
                    # django-cloudinary-storage stores the public_id as the field value
                    setattr(obj, field_name, result['public_id'])
                    obj.save(update_fields=[field_name])
                    self.stdout.write(
                        self.style.SUCCESS(f"    ✓ Uploaded: {result['secure_url'][:70]}…")
                    )
                    total_uploaded += 1
                except Exception as exc:
                    self.stderr.write(
                        self.style.ERROR(f"    ✗ Upload failed for id={obj.pk}: {exc}")
                    )
                    total_errors += 1

        # Summary
        self.stdout.write("\n" + "=" * 50)
        action = "Would upload" if dry_run else "Uploaded"
        self.stdout.write(self.style.SUCCESS(f"  {action}: {total_uploaded} file(s)"))
        self.stdout.write(f"  Skipped:  {total_skipped} file(s)")
        if total_errors:
            self.stdout.write(self.style.ERROR(f"  Errors:   {total_errors} file(s)"))
        else:
            self.stdout.write(f"  Errors:   {total_errors}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nRe-run without --dry-run to perform the actual upload.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("\nMigration complete!"))
