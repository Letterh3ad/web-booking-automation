const proxyConfig = {
  mode: 'fixed_servers',
  rules: {
    proxyForHttp: {
      scheme: 'http',
      host: 'geo.iproyal.com',
      port: parseInt('12321', 10)
    },
    proxyForHttps: {
      scheme: 'https',
      host: 'geo.iproyal.com',
      port: parseInt('12321', 10)
    },
    bypassList: ['<local>']
  }
};

const credentials = {
  username: 'zVO94b9ZpCtswL7K',
  password: 'Zb3Mp8F8rpsMNIXI_session-8Qetgtt9_lifetime-59m_streaming-1'
};

chrome.proxy.settings.set(
  { value: proxyConfig, scope: 'regular' },
  function() {
    console.log('Proxy settings applied.');
  }
);

chrome.webRequest.onAuthRequired.addListener(
  function(details) {
    return {
      authCredentials: {
        username: credentials.username,
        password: credentials.password
      }
    };
  },
  { urls: ['<all_urls>'] },
  ['blocking']
);
