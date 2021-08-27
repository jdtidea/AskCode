import {BrowserAuthOptions} from '@azure/msal-browser';
interface Config {
  appInsightsKey: string;
  auth: BrowserAuthOptions;
  scopes: Array<string>;
  domainThreshold: number;
  b2cExtensionsClientId: string;
}

interface EnvConfig {
  dev: Config;
  prod: Config;
}

const domainThreshold = 0.5;

const envConfig: EnvConfig = {
  dev: {
    appInsightsKey: 'aaf262a0-71a8-41ac-84ad-2c6cdbfc606d',
    auth: {
      clientId: 'dcbb629f-c429-44ae-84a9-f78584b37f00',
      authority:
        'https://optumatcdev.b2clogin.com/optumatcdev.onmicrosoft.com/B2C_1_askoptumsignup',
      knownAuthorities: [
        'optumatcdev.b2clogin.com',
        'https://dev.ask.optum.ai',
        'authgateway3-dev.entiam.uhg.com',
      ],
      redirectUri: '/auth',
    },
    scopes: ['https://optumatcdev.onmicrosoft.com/askoptum-api-dev/Search'],
    b2cExtensionsClientId: 'f3fb518578a34f3fb90c54fd4c3eee46',
    domainThreshold,
  },
  prod: {
    appInsightsKey: 'de8556e9-0a34-41fa-a303-d16676045d84',
    auth: {
      clientId: 'c300481a-bf08-4f6b-925b-8a3609a9aa16',
      authority:
        'https://optumatcprod.b2clogin.com/optumatcprod.onmicrosoft.com/B2C_1_askoptumsignup',
      knownAuthorities: ['optumatcprod.b2clogin.com'],
      redirectUri: '/auth',
    },
    scopes: ['https://optumatcprod.onmicrosoft.com/askoptum-api-prod/Search'],
    b2cExtensionsClientId: 'd5f60563697c4c5c891036f7776a1d11',
    domainThreshold,
  },
};

const config = envConfig[(process.env as any).REACT_APP_AO_ENV || 'dev'];
export {config};
