"""
Pagination helpers
- Used for feeds, comments, notifications
"""

def get_pagination_params(request, default_limit=10, max_limit=50):
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", default_limit))
    except ValueError:
        page = 1
        limit = default_limit

    page = max(page, 1)
    limit = min(max(limit, 1), max_limit)

    skip = (page - 1) * limit

    return page, limit, skip
