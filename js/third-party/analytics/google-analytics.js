/* global CONFIG, dataLayer, gtag */

if (!CONFIG.google_analytics.only_pageview) {
  if (CONFIG.hostname === location.hostname) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function() {
      dataLayer.push(arguments);
    };
    gtag('js', new Date());
    gtag('config', CONFIG.google_analytics.tracking_id);

    document.addEventListener('pjax:success', () => {
      gtag('event', 'page_view', {
        page_location: location.href,
        page_path    : location.pathname,
        page_title   : document.title
      });
    });
  }
} else {
  const sendPageView = () => {
    if (!CONFIG.google_analytics || !CONFIG.google_analytics.tracking_id || typeof gtag !== 'function') {
      return;
    }
    if (CONFIG.hostname !== location.hostname) return;
    gtag('config', CONFIG.google_analytics.tracking_id, {
      page_path: location.pathname + location.search + location.hash,
      page_title: document.title
    });
  };
  document.addEventListener('pjax:complete', sendPageView);
}
