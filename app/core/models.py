import uuid

from core.fields import CountryField
from core.utils import JANUARY, MONTH_CHOICES, current_year, year_choices
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Period(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    year = models.PositiveSmallIntegerField("year", choices=year_choices(), default=current_year)
    month = models.PositiveSmallIntegerField("month", choices=MONTH_CHOICES, default=JANUARY)

    class Meta:
        ordering = ["-year", "-month"]
        indexes = [
            models.Index(fields=["year"], name="period_year_idx"),
            models.Index(fields=["month"], name="period_month_idx"),
            models.Index(fields=["year", "month"], name="period_year_month_idx"),
        ]
        unique_together = ["year", "month"]

    def __str__(self):
        return f"{self.year}-{self.month:02d}"


class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "name"], name="genre_id_name_idx"),
        ]

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField("year", choices=year_choices(), default=current_year())
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="movies")
    language = models.CharField(max_length=2)
    overview = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=50, validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True
    )

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ("-year", "title")
        indexes = [
            models.Index(fields=["id", "title"], name="movie_id_title_idx"),
            models.Index(fields=["id", "genre"], name="movie_id_genre_idx"),
        ]

    def __str__(self):
        return self.title


class Network(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    name = models.CharField(max_length=32)
    country = CountryField()
    start_period = models.ForeignKey(Period, on_delete=models.DO_NOTHING, related_name="network_start_period")
    end_period = models.ForeignKey(Period, on_delete=models.DO_NOTHING, related_name="network_end_period")

    class Meta:
        ordering = ["-end_period__year", "-start_period__year"]

    def __str__(self):
        return f"{self.name}: {self.start_period} ~ {self.end_period}"
