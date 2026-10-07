'use strict';

{
    const navSidebar = document.getElementById('nav-sidebar');
    const storageKey = 'assetverse.admin.navSidebarScrollTop';

    if (navSidebar) {
        const savedScrollTop = sessionStorage.getItem(storageKey);
        if (savedScrollTop !== null) {
            navSidebar.scrollTop = Number(savedScrollTop);
        }

        const saveScrollPosition = () => {
            sessionStorage.setItem(storageKey, String(navSidebar.scrollTop));
        };
        navSidebar.addEventListener('scroll', saveScrollPosition, {passive: true});
        window.addEventListener('pagehide', saveScrollPosition);
    }
}
