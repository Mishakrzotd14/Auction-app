from rest_framework import filters


class AuctionTypeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        auction_type = request.query_params.get('auction')
        if auction_type == 'english':
            queryset = queryset.filter(auction__englishauction__isnull=False)
        elif auction_type == 'dutch':
            queryset = queryset.filter(auction__dutchauction__isnull=False)
        return queryset
