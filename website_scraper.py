def display_results(results):
    for result in results:
        url = result.get('url')
        description = result.get('description')
        # Check if description is not None before slicing
        if description is not None:
            description = description[:100]  # Limit to 100 characters
        print(f'URL: {url}, Description: {description}')