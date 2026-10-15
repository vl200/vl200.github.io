/* Existing Google Analytics property. Local previews never send traffic. */
(() => {
  "use strict";
  const settings = {
  "measurement_id": "G-M758ZKREW1",
  "production_hosts": [
    "volkerlaux.github.io"
  ]
};
  const host = window.location.hostname;
  const isPreview = new URLSearchParams(window.location.search).has("preview");
  if (window.location.protocol !== "https:" || isPreview ||
      !settings.production_hosts.includes(host) ||
      !/^G-[A-Z0-9]+$/.test(settings.measurement_id)) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", settings.measurement_id);
  const tag = document.createElement("script");
  tag.async = true;
  tag.src = "https://www.googletagmanager.com/gtag/js?id=" + settings.measurement_id;
  document.head.appendChild(tag);
})();
