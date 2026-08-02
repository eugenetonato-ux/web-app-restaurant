# apps/menu/models.py
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    ordre_affichage = models.PositiveIntegerField(default=0)
    icone = models.CharField(max_length=50, default="fa-utensils", help_text="Nom de classe FontAwesome ou emoji")
    couleur_card = models.CharField(max_length=30, default="linear-gradient(135deg, #8E5CF7, #A881FC)", help_text="Dégradé CSS pour la carte publique")
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre_affichage", "nom"]
        verbose_name_plural = "Catégories"

    def save(self, *args, **kwargs):
        # Génère le slug automatiquement à partir du nom s'il n'a pas été renseigné,
        # et garantit son unicité (ex: "Jus" -> "jus", "jus-2" en cas de doublon).
        if not self.slug:
            base_slug = slugify(self.nom)
            slug_candidat = base_slug
            compteur = 1
            while Category.objects.filter(slug=slug_candidat).exclude(pk=self.pk).exists():
                compteur += 1
                slug_candidat = f"{base_slug}-{compteur}"
            self.slug = slug_candidat
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class MenuItem(models.Model):
    categorie = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0)  # FCFA
    prix_promo = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    photo = models.ImageField(upload_to="menu/", blank=True, null=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL externe d'image haute qualité si pas d'upload")
    disponible = models.BooleanField(default=True)
    est_populaire = models.BooleanField(default=False)
    est_promo = models.BooleanField(default=False)
    badge = models.CharField(max_length=30, blank=True, help_text="ex: HOT, NEW, -15%")
    note_etoiles = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)

    class Meta:
        ordering = ["-est_populaire", "nom"]
        verbose_name_plural = "Articles du Menu"

    def get_prix_effectif(self):
        if self.est_promo and self.prix_promo and self.prix_promo > 0:
            return self.prix_promo
        return self.prix

    def get_image_display(self):
        if self.photo:
            return self.photo.url
        if self.photo_url:
            return self.photo_url
        return "/static/images/default_food.png"

    def __str__(self):
        return f"{self.nom} — {self.get_prix_effectif()} FCFA"