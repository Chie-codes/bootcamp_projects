"""Note model definition."""

from django.db import models


class Note(models.Model):
    """Model representing a sticky note."""

    title = models.CharField(max_length=200, help_text="Enter note title")
    content = models.TextField(help_text="Enter note content")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Time note was created"
    )

    def __str__(self):
        """String representation of the note."""
        return self.title
