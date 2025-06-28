from django.db import models


class ServiceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BeautyService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()

    def __str__(self):
        return self.name


class Salon(models.Model):
    name = models.CharField(max_length=100, default="Beauty City")
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='salon_images/')
    work_start_at = models.TimeField()
    work_end_time = models.TimeField()
    services = models.ManyToManyField(BeautyService, related_name='salons')

    def __str__(self):
        return self.address


class Review(models.Model):
    phone_number = models.BigIntegerField()
    description = models.TextField()
    name = models.CharField(max_length=100)


class Specialist(models.Model):
    experience = models.CharField(max_length=100)
    spec = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='specialist_images/')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    skills = models.ManyToManyField(BeautyService, related_name='specialists')

    def __str__(self):
        return f'{self.spec} ({self.experience})'


class Promo(models.Model):
    is_active = models.BooleanField(default=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    date = models.DateField()
    slot = models.TimeField()
    duration_min = models.IntegerField()
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField()
    is_paid = models.BooleanField(default=False)
    service = models.ForeignKey(BeautyService, on_delete=models.CASCADE)
    Promo = models.ForeignKey(Promo, null=True, blank=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} — {self.date} {self.slot}'


class ClientReview(models.Model):
    RATING_CHOICES = [
        ('1', '★☆☆☆☆'),
        ('2', '★★☆☆☆'),
        ('3', '★★★☆☆'),
        ('4', '★★★★☆'),
        ('5', '★★★★★'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField()
    review = models.TextField()
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
