chrome.webRequest.onAuthRequired.addListener(
  function (details) {
    return {
      authCredentials: {
        username: 'zVO94b9ZpCtswL7K',
        password: 'Zb3Mp8F8rpsMNIXI_country-pt_streaming-1'
      }
    };
  },
  { urls: ['<all_urls>'] },
  ['blocking']
);
