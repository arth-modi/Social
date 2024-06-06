from rest_framework import filters, serializers

class HasImageFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        hasimg = request.query_params.get('hasimg')
        if hasimg is not None:
            if hasimg.lower() == "true":
                queryset=queryset.exclude(image="")
                
            elif hasimg.lower()=="false":
                queryset=queryset.filter(image="")
                # print(queryset)
            else:
                raise serializers.ValidationError("Expected true or false")
        return queryset