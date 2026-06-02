from math import ceil


def paginate(total: int, page: int, limit: int) -> dict:
    pages = max(1, ceil(total / limit))
    return {"total": total, "page": page, "limit": limit, "pages": pages}
