document.addEventListener("DOMContentLoaded", () => {
  // Initialize home map
  const homeMap = document.getElementById("home-map");
  if (homeMap) {
    homeMap.innerHTML = companyMapHtml("map-embed map-embed--large");
  }

  // Initialize company details
  const homeCompanyDetails = document.getElementById("home-company-details");
  if (homeCompanyDetails) {
    homeCompanyDetails.innerHTML = companyDetailsHtml();
  }
});
