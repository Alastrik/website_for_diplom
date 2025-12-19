from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from muiv_graduation_system.models import Employer

User = get_user_model()


@receiver(post_save, sender=User)
def set_admin_permissions(sender, instance, created, **kwargs):
    if created and instance.role:
        if instance.role.name == 'admin':
            instance.is_superuser = True
            instance.is_staff = True
            instance.save(update_fields=['is_superuser', 'is_staff'])


@receiver(post_migrate)
def init_demo_data(sender, **kwargs):
    if sender.name != 'muiv_graduation_system':
        return

    from .models import Role, User, EmploymentStatus, Graduate
    from django.contrib.auth.hashers import make_password

    # === Роли ===
    if Role.objects.count() == 0:
        roles = ['admin', 'manager', 'graduate']
        for name in roles:
            Role.objects.create(name=name)

    # === Статусы ===
    if EmploymentStatus.objects.count() == 0:
        statuses = ["трудоустроен", "в поиске", "не трудоустроен"]
        for name in statuses:
            EmploymentStatus.objects.create(name=name)

    # === Пользователи ===
    if User.objects.count() == 0:
        demo_users = [
            {'username': 'admin', 'email': 'admin@muiv.ru', 'password': 'admin123', 'role': 'admin'},
            {'username': 'manager', 'email': 'manager@muiv.ru', 'password': 'manager123', 'role': 'manager'},
            {'username': 'graduate', 'email': 'graduate@muiv.ru', 'password': 'grad123', 'role': 'graduate'},
        ]
        for u in demo_users:
            role = Role.objects.get(name=u['role'])
            User.objects.create(
                username=u['username'],
                email=u['email'],
                password=make_password(u['password']),
                role=role
            )

    # === Выпускник ===
    if Graduate.objects.count() == 0:
        grad_user = User.objects.get(username='graduate')
        Graduate.objects.create(
            user=grad_user,
            full_name="Иванов Иван Иванович",
            graduation_year=2024,
            faculty="Факультет информационных технологий",
            specialization="Бизнес-информатика",
            phone="+79001234567",
            email="graduate@muiv.ru"
        )

    if Employer.objects.count() == 0:
        employers = [
            {
                "name": "Яндекс",
                "industry": "IT / Интернет",
                "contact_person": "Иванова Анна Сергеевна",
                "email": "hr@yandex.ru",
                "phone": "+7 (495) 739-70-00"
            },
            {
                "name": "Сбербанк",
                "industry": "Банковская сфера",
                "contact_person": "Петров Михаил Александрович",
                "email": "recruitment@sberbank.ru",
                "phone": "+7 (495) 500-55-50"
            },
            {
                "name": "Газпром",
                "industry": "Нефтегазовая промышленность",
                "contact_person": "Смирнова Елена Владимировна",
                "email": "hr@gazprom.ru",
                "phone": "+7 (495) 719-30-01"
            },
            {
                "name": "Tinkoff",
                "industry": "Финтех",
                "contact_person": "Козлов Дмитрий Игоревич",
                "email": "jobs@tinkoff.ru",
                "phone": "+7 (495) 648-10-10"
            },
            {
                "name": "VK",
                "industry": "IT / Социальные сети",
                "contact_person": "Соколова Мария Петровна",
                "email": "hr@vk.com",
                "phone": "+7 (812) 640-20-20"
            },
            {
                "name": "Ростелеком",
                "industry": "Телекоммуникации",
                "contact_person": "Новиков Алексей Викторович",
                "email": "career@rt.ru",
                "phone": "+7 (495) 727-45-45"
            },
            {
                "name": "Ozon",
                "industry": "E-commerce",
                "contact_person": "Морозова Ольга Николаевна",
                "email": "hr@ozon.ru",
                "phone": "+7 (495) 730-67-67"
            },
            {
                "name": "Лаборатория Касперского",
                "industry": "Информационная безопасность",
                "contact_person": "Васильев Сергей Андреевич",
                "email": "jobs@kaspersky.com",
                "phone": "+7 (495) 797-87-00"
            },
            {
                "name": "Альфа-Банк",
                "industry": "Банковская сфера",
                "contact_person": "Федорова Татьяна Олеговна",
                "email": "hr@alfabank.ru",
                "phone": "+7 (495) 788-88-78"
            },
            {
                "name": "МТС",
                "industry": "Телекоммуникации",
                "contact_person": "Кузнецов Андрей Павлович",
                "email": "recruitment@mts.ru",
                "phone": "+7 (495) 766-01-66"
            }
        ]

        for employer_data in employers:
            Employer.objects.create(**employer_data)

    print("✅ Демо-данные успешно созданы")
