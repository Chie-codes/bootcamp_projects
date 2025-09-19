from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders
from .models import Note

class NoteModelTest(TestCase):
    def test_create_note(self):
        note = Note.objects.create(title="Test Note", content="This is a test.")
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test.")

class NoteViewTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Sample Note", content="Sample content")

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Note")
        self.assertTemplateUsed(response, "notes/note_list.html")

    def test_add_note_view(self):
        response = self.client.post(reverse("add_note"), {
            "title": "New Note",
            "content": "New content"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_edit_note_view(self):
        response = self.client.post(reverse("edit_note", args=[self.note.id]), {
            "title": "Updated Note",
            "content": "Updated content"
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")

    def test_delete_note_view(self):
        response = self.client.post(reverse("delete_note", args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

class TemplateTests(TestCase):
    def test_base_template_has_bootstrap(self):
        response = self.client.get(reverse("note_list"))
        self.assertContains(response, "cdn.jsdelivr.net/npm/bootstrap")

    def test_note_list_has_sticky_note_styles(self):
        Note.objects.create(title="Styled Note", content="Styled content")
        response = self.client.get(reverse("note_list"))
        self.assertContains(response, "note-card")
        self.assertContains(response, "bg-light-blue")

class StaticFilesTests(TestCase):
    def test_style_css_exists(self):
        path = finders.find("notes/css/style.css")
        self.assertIsNotNone(path, "style.css was not found in static files!")
