class UrlHelper {
    static changeGetParam(url, param, value) {
        // Convert to URL object
        url = new URL(url);

        // Get search params from url
        let searchParams = url.searchParams;

        // Set new value
        searchParams.set(param, value);

        // Set search params
        url.search = searchParams.toString();

        return url.toString();
    }
}