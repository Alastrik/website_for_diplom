from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Role, User, Employer, EmploymentStatus, Graduate, Employment, Document, Feedback, Report, \
    RegistrationRequest

admin.site.site_header = "Информационная система учета трудоустройства выпускников"
admin.site.site_title = "ИСУТВ МУИВ"
admin.site.index_title = "Главная"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_count')
    search_fields = ('name',)
    ordering = ('name',)

    def user_count(self, obj):
        """Количество пользователей с этой ролью"""
        count = obj.user_set.count()
        return format_html(
            '<span style="background: #940101; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            count
        )

    user_count.short_description = 'Пользователей'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name_display', 'role_badge', 'status_badge', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    date_hierarchy = 'date_joined'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Личная информация'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Права доступа'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def full_name_display(self, obj):
        """ФИО"""
        if hasattr(obj, 'graduate_profile') and obj.graduate_profile.full_name:
            name = obj.graduate_profile.full_name.strip()
            if name:
                return name

        # Для всех остальных — Фамилия Имя
        full_name = f"{obj.last_name} {obj.first_name}".strip()
        return full_name if full_name else obj.username if obj.username else '—'

    full_name_display.short_description = 'ФИО'

    def role_badge(self, obj):
        """Роль с цветным бейджем"""
        if obj.role:
            colors = {
                'admin': '#dc3545',
                'manager': '#28a745',
                'graduate': '#007bff',
            }
            color = colors.get(obj.role.name.lower(), '#6c757d')
            return format_html(
                '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
                color, obj.role.name.upper()
            )
        return '—'

    role_badge.short_description = 'Роль'

    def status_badge(self, obj):
        """Статус активности"""
        if obj.is_active:
            return mark_safe('<span style="color: #28a745;">● Активен</span>')
        return mark_safe('<span style="color: #dc3545;">● Неактивен</span>')

    status_badge.short_description = 'Статус'


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'contact_info', 'employees_count')
    list_filter = ('industry',)
    search_fields = ('name', 'industry', 'contact_person', 'email')
    ordering = ('name',)
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'industry')
        }),
        ('Контактные данные', {
            'fields': ('contact_person', 'email', 'phone')
        }),
    )

    def contact_info(self, obj):
        """Контактная информация"""
        parts = []
        if obj.contact_person:
            parts.append(f'<strong>{obj.contact_person}</strong>')
        if obj.email:
            parts.append(f'<a href="mailto:{obj.email}">{obj.email}</a>')
        if obj.phone:
            parts.append(f'📞 {obj.phone}')
        return mark_safe('<br>'.join(parts)) if parts else '—'

    contact_info.short_description = 'Контакты'

    def employees_count(self, obj):
        """Количество сотрудников (выпускников)"""
        count = obj.employment_set.count()
        if count > 0:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{}</span>',
                count
            )
        return '0'

    employees_count.short_description = 'Выпускников'


@admin.register(EmploymentStatus)
class EmploymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'employment_count')
    search_fields = ('name',)
    ordering = ('name',)

    def employment_count(self, obj):
        """Количество выпускников с этим статусом"""
        count = obj.employment_set.count()
        return format_html(
            '<span style="background: #940101; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            count
        )

    employment_count.short_description = 'Использований'


# ✅ ЕДИНСТВЕННЫЙ GraduateAdmin — исправленный
@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'graduation_year', 'faculty', 'specialization', 'contact_info', 'employment_status_badge')
    list_filter = ('graduation_year', 'faculty', 'specialization')
    search_fields = ('full_name', 'faculty', 'specialization', 'email', 'phone')
    ordering = ('-graduation_year', 'full_name')
    list_per_page = 25
    # УБРАНО: readonly_fields = ('user',)

    fieldsets = (
        ('Связанный пользователь', {
            'fields': ('user',)
        }),
        ('Личная информация', {
            'fields': ('full_name', 'graduation_year')
        }),
        ('Образование', {
            'fields': ('faculty', 'specialization')
        }),
        ('Контактные данные', {
            'fields': ('email', 'phone')
        }),
    )

    def contact_info(self, obj):
        """Контактная информация"""
        parts = []
        if obj.email:
            parts.append(f'<a href="mailto:{obj.email}">✉ {obj.email}</a>')
        if obj.phone:
            parts.append(f'📞 {obj.phone}')
        return mark_safe('<br>'.join(parts)) if parts else '—'

    contact_info.short_description = 'Контакты'

    def employment_status_badge(self, obj):
        """Статус трудоустройства"""
        try:
            employment = obj.employment
            if employment and employment.status:
                return format_html(
                    '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
                    employment.status.name
                )
        except Employment.DoesNotExist:
            pass
        return mark_safe(
            '<span style="background: #6c757d; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">НЕ УКАЗАН</span>'
        )

    employment_status_badge.short_description = 'Трудоустройство'


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'graduate_link', 'status_badge', 'employer_link', 'job_title', 'salary_display', 'start_date',
                    'days_employed', 'updated_at')
    list_filter = ('status', 'start_date', 'updated_at')
    search_fields = ('graduate__full_name', 'job_title', 'employer__name')
    ordering = ('-updated_at',)
    date_hierarchy = 'start_date'
    list_per_page = 25

    fieldsets = (
        ('Выпускник', {
            'fields': ('graduate',)
        }),
        ('Работа', {
            'fields': ('status', 'employer', 'job_title', 'salary', 'start_date')
        }),
        ('Системная информация', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('updated_at',)

    def graduate_link(self, obj):
        """Ссылка на выпускника"""
        url = reverse('admin:muiv_graduation_system_graduate_change', args=[obj.graduate.id])
        return format_html('<a href="{}">{}</a>', url, obj.graduate.full_name)

    graduate_link.short_description = 'Выпускник'

    def employer_link(self, obj):
        """Ссылка на работодателя"""
        if obj.employer:
            url = reverse('admin:muiv_graduation_system_employer_change', args=[obj.employer.id])
            return format_html('<a href="{}">{}</a>', url, obj.employer.name)
        return '—'

    employer_link.short_description = 'Работодатель'

    def status_badge(self, obj):
        """Статус с бейджем"""
        if obj.status:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
                obj.status.name
            )
        return '—'

    status_badge.short_description = 'Статус'

    def salary_display(self, obj):
        if obj.salary:
            # Форматируем число с пробелами как разделитель тысяч (по ГОСТ)
            formatted_salary = f"{obj.salary:,}".replace(",", " ")
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{} ₽</span>',
                formatted_salary
            )
        return '—'

    salary_display.short_description = 'Зарплата'

    def days_employed(self, obj):
        """Дней на работе"""
        if obj.start_date:
            from datetime import date
            days = (date.today() - obj.start_date).days
            if days > 0:
                return f'{days} дн.'
        return '—'

    days_employed.short_description = 'Стаж'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'graduate_link', 'doc_type_badge', 'uploaded_at')
    list_filter = ('doc_type', 'uploaded_at')
    search_fields = ('filename', 'graduate__full_name')
    ordering = ('-uploaded_at',)
    date_hierarchy = 'uploaded_at'
    list_per_page = 25

    readonly_fields = ('uploaded_at',)

    fieldsets = (
        ('Выпускник', {
            'fields': ('graduate',)
        }),
        ('Файл', {
            'fields': ('filename', 'filepath', 'doc_type')
        }),
        ('Системная информация', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )

    def graduate_link(self, obj):
        """Ссылка на выпускника"""
        url = reverse('admin:muiv_graduation_system_graduate_change', args=[obj.graduate.id])
        return format_html('<a href="{}">{}</a>', url, obj.graduate.full_name)

    graduate_link.short_description = 'Выпускник'

    def doc_type_badge(self, obj):
        """Тип документа"""
        if obj.doc_type:
            colors = {
                'resume': '#007bff',
                'certificate': '#28a745',
                'diploma': '#dc3545',
            }
            color = colors.get(obj.doc_type.lower(), '#6c757d')
            return format_html(
                '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
                color, obj.doc_type.upper()
            )
        return '—'

    doc_type_badge.short_description = 'Тип'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'subject', 'message_preview', 'created_at', 'is_read_badge')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'subject', 'message')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['mark_as_read', 'mark_as_unread']

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Отправитель', {
            'fields': ('user',)
        }),
        ('Сообщение', {
            'fields': ('subject', 'message')
        }),
        ('Статус', {
            'fields': ('is_read', 'created_at')
        }),
    )

    def user_link(self, obj):
        """Ссылка на пользователя"""
        url = reverse('admin:muiv_graduation_system_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = 'Отправитель'

    def message_preview(self, obj):
        """Превью сообщения"""
        preview = obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return preview

    message_preview.short_description = 'Сообщение'

    def is_read_badge(self, obj):
        """Статус прочтения"""
        if obj.is_read:
            return mark_safe('<span style="color: #6c757d;">✓ Прочитано</span>')
        return mark_safe('<span style="color: #940101; font-weight: bold;">✉ Новое</span>')

    is_read_badge.short_description = 'Статус'

    def mark_as_read(self, request, queryset):
        """Отметить как прочитанное"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} сообщений отмечено как прочитанные')

    mark_as_read.short_description = '✓ Отметить как прочитанное'

    def mark_as_unread(self, request, queryset):
        """Отметить как непрочитанное"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} сообщений отмечено как непрочитанные')

    mark_as_unread.short_description = '✉ Отметить как непрочитанное'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'generated_by_link', 'format_badge', 'generated_at')
    list_filter = ('format', 'generated_at')
    search_fields = ('title', 'generated_by__username')
    ordering = ('-generated_at',)
    date_hierarchy = 'generated_at'
    list_per_page = 25

    readonly_fields = ('generated_at',)

    fieldsets = (
        ('Отчет', {
            'fields': ('title', 'format', 'filepath')
        }),
        ('Системная информация', {
            'fields': ('generated_by', 'generated_at')
        }),
    )

    def generated_by_link(self, obj):
        """Ссылка на пользователя"""
        url = reverse('admin:muiv_graduation_system_user_change', args=[obj.generated_by.id])
        return format_html('<a href="{}">{}</a>', url, obj.generated_by.username)

    generated_by_link.short_description = 'Создал'

    def format_badge(self, obj):
        """Формат файла"""
        colors = {
            'docx': '#2b5797',
            'xlsx': '#217346',
            'pdf': '#d93025',
        }
        color = colors.get(obj.format.lower(), '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.format.upper()
        )

    format_badge.short_description = 'Формат'


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'full_name', 'created_at', 'status_badge', 'approved_by_link')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['approve_selected_requests', 'reject_selected_requests']

    readonly_fields = ('created_at', 'password_hash')

    fieldsets = (
        ('Данные пользователя', {
            'fields': ('username', 'email', 'full_name', 'password_hash')
        }),
        ('Статус заявки', {
            'fields': ('is_approved', 'approved_by', 'created_at')
        }),
    )

    def status_badge(self, obj):
        """Статус заявки"""
        if obj.is_approved:
            return mark_safe(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Одобрено</span>'
            )
        return mark_safe(
            '<span style="background: #ffc107; color: #000; padding: 3px 8px; border-radius: 3px;">⏳ Ожидает</span>'
        )

    status_badge.short_description = 'Статус'

    def approved_by_link(self, obj):
        """Кто одобрил"""
        if obj.approved_by:
            url = reverse('admin:muiv_graduation_system_user_change', args=[obj.approved_by.id])
            return format_html('<a href="{}">{}</a>', url, obj.approved_by.username)
        return '—'

    approved_by_link.short_description = 'Одобрил'

    def approve_selected_requests(self, request, queryset):
        """Одобрить заявки и создать пользователей"""
        from django.contrib.auth.hashers import make_password
        from .models import User, Role

        count = 0
        for obj in queryset.filter(is_approved=False):
            # Получаем роль "Manager"
            manager_role = Role.objects.filter(name__iexact='manager').first()
            if not manager_role:
                self.message_user(request, 'Ошибка: роль "Manager" не найдена', level='ERROR')
                continue

            # Разбираем full_name на части (Фамилия Имя Отчество)
            name_parts = obj.full_name.split() if obj.full_name else []
            last_name = name_parts[0] if len(name_parts) > 0 else ''
            first_name = name_parts[1] if len(name_parts) > 1 else ''

            # Создаем пользователя
            user = User.objects.create(
                username=obj.username,
                email=obj.email,
                first_name=first_name,
                last_name=last_name,
                password=obj.password_hash,  # Используем как есть, если это хеш
                role=manager_role,
                is_active=True,
                is_staff=False,
            )

            # Отмечаем и удаляем заявку
            obj.is_approved = True
            obj.approved_by = request.user
            obj.save()
            obj.delete()
            count += 1

        self.message_user(request, f'Успешно создано пользователей: {count}')

    approve_selected_requests.short_description = '✓ Одобрить выбранные заявки'

    def reject_selected_requests(self, request, queryset):
        """Отклонить заявки"""
        count = queryset.filter(is_approved=False).delete()[0]
        self.message_user(request, f'Отклонено заявок: {count}')

    reject_selected_requests.short_description = '✗ Отклонить выбранные заявки'