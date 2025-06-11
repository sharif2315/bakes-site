def get_breadcrumbs(page):
    root_page = page.get_site().root_page
    parent_page = page.get_parent()
    breadcrumbs = []

    # Always add root
    breadcrumbs.append({'title': root_page.title, 'url': root_page.url})

    # Only add parent if it's not the root
    if parent_page.id != root_page.id:
        breadcrumbs.append({'title': parent_page.title, 'url': parent_page.url})

    # Add current page (no URL)
    breadcrumbs.append({'title': page.title})

    return breadcrumbs
