from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Роль пользователя'
    )
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Employer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название компании')
    industry = models.CharField(max_length=100, blank=True, verbose_name='Отрасль')
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Контактное лицо')
    email = models.EmailField(blank=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'


class EmploymentStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Статус трудоустройства')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус трудоустройства'
        verbose_name_plural = 'Статусы трудоустройства'


class Graduate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='graduate_profile',
        verbose_name='Пользователь'
    )
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    graduation_year = models.IntegerField(verbose_name='Год выпуска')
    faculty = models.CharField(max_length=100, blank=True, verbose_name='Факультет')
    specialization = models.CharField(max_length=100, blank=True, verbose_name='Специализация')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Выпускник'
        verbose_name_plural = 'Выпускники'


class Employment(models.Model):
    graduate = models.OneToOneField(
        Graduate,
        on_delete=models.CASCADE,
        related_name='employment',
        verbose_name='Выпускник'
    )
    employer = models.ForeignKey(
        Employer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Работодатель'
    )
    status = models.ForeignKey(
        EmploymentStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Статус'
    )
    job_title = models.CharField(max_length=150, blank=True, verbose_name='Должность')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала работы')
    salary = models.IntegerField(null=True, blank=True, verbose_name='Зарплата')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.graduate.full_name} — {self.status}"

    class Meta:
        verbose_name = 'Трудоустройство'
        verbose_name_plural = 'Трудоустройства'


class Document(models.Model):
    graduate = models.ForeignKey(
        Graduate,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Выпускник'
    )
    filename = models.CharField(max_length=255, verbose_name='Имя файла')
    filepath = models.CharField(max_length=500, verbose_name='Путь к файлу')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    doc_type = models.CharField(max_length=50, blank=True, verbose_name='Тип документа')

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Feedback(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Пользователь'
    )
    subject = models.CharField(max_length=100, blank=True, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    def __str__(self):
        return f"Feedback from {self.user.username}"

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'


class Report(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название отчета')
    generated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Создан пользователем'
    )
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации')
    format = models.CharField(max_length=10, verbose_name='Формат')
    filepath = models.CharField(max_length=500, verbose_name='Путь к файлу')

    def __str__(self):
        return f"{self.title}.{self.format}"

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class RegistrationRequest(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    password_hash = models.CharField(max_length=128, verbose_name='Хеш пароля')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Полное имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_approved = models.BooleanField(default=False, verbose_name='Подтверждено')
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Подтверждено пользователем'
    )

    def __str__(self):
        return f"Request: {self.username}"

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрацию'