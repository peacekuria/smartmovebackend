def get_pagination_meta(paginated_obj):
    return {
        "total": paginated_obj.total,
        "pages": paginated_obj.pages,
        "current_page": paginated_obj.page,
        "per_page": paginated_obj.per_page,
        "has_next": paginated_obj.has_next,
        "has_prev": paginated_obj.has_prev
    }