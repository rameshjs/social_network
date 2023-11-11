from django.db.models import Q
import django_filters
from users.models import User


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        email_query = Q(email__iexact=value) | Q(email__icontains=value)
        name_query = Q(name__icontains=value)

        combined_query = email_query | name_query

        return queryset.filter(combined_query)

    class Meta:
        model = User
        fields = ["search"]
