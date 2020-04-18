from dal import autocomplete

from .models import Place


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Place.objects.none()
        qs = Place.objects.all()
        print(qs)
        if self.q:
            qs = qs.filter(city__istartswith=self.q)
        print(qs)
        return qs
