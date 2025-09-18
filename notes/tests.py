"""Unit tests for Sticky Notes app."""

from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTests(TestCase):
    """Tests for Note model."""

    def test_note_creation(self):
        """Test that a note can be created and saved."""
        note = Note.objects.create(title="Test Note", content="This is a test note.")
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note.")
        self.assertIsNotNone(note.created_at)


class NoteViewTests(TestCase):
    """Tests for Note views (CRUD)."""

    def setUp(self):
        """Create a test note for use in view tests."""
        self.note = Note.objects.create(title="Sample Note", content="Sample content.")

    def test_note_list_view(self):
        """Test that the note list view returns 200 and contains the note."""
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Note")

    def test_add_note_view(self):
        """Test creating a new note through the add view."""
        response = self.client.post(
            reverse("add_note"),
            {"title": "New Note", "content": "New content"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Note")
        self.assertEqual(Note.objects.count(), 2)

    def test_edit_note_view(self):
        """Test editing an existing note."""
        response = self.client.post(
            reverse("edit_note", args=[self.note.pk]),
            {"title": "Updated Note", "content": "Updated content"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")
        self.assertEqual(self.note.content, "Updated content")

    def test_delete_note_view(self):
        """Test deleting a note."""
        response = self.client.post(
            reverse("delete_note", args=[self.note.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)


class NoteTemplateTests(TestCase):
    """Tests for note templates and HTML rendering."""

    def setUp(self):
        """Create a sample note for template tests."""
        self.note = Note.objects.create(
            title="Template Test", content="Check template HTML."
        )

    def test_note_list_template_used(self):
        """Test that note_list.html is used and displays the note."""
        response = self.client.get(reverse("note_list"))
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertContains(response, "Template Test")
        # Check that the yellow card class is present
        self.assertContains(response, "note-card")
        # Check for Edit and Delete buttons
        self.assertContains(response, "Edit")
        self.assertContains(response, "Delete")

    def test_add_note_template_used(self):
        """Test that add_note.html is used."""
        response = self.client.get(reverse("add_note"))
        self.assertTemplateUsed(response, "notes/add_note.html")
        self.assertContains(response, "Add New Note")
        self.assertContains(response, "<form", html=True)

    def test_edit_note_template_used(self):
        """Test that edit_note.html is used."""
        response = self.client.get(reverse("edit_note", args=[self.note.pk]))
        self.assertTemplateUsed(response, "notes/edit_note.html")
        self.assertContains(response, "Edit Note")
        self.assertContains(response, "<form", html=True)

    def test_delete_note_template_used(self):
        """Test that delete_note.html is used."""
        response = self.client.get(reverse("delete_note", args=[self.note.pk]))
        self.assertTemplateUsed(response, "notes/delete_note.html")
        self.assertContains(response, "Delete Note")
        self.assertContains(response, "<form", html=True)
