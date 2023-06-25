
export const changeFavicon = (favicon: "./favicon_pro.ico" | "./favicon.ico") => {
    var link:HTMLLinkElement | null = document.querySelector("link[rel~='icon']");
    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.head.appendChild(link);
    }
    link.href = favicon;
}
