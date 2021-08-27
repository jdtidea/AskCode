import './index.css';
import '@uitk/react/polyfills';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {Toolkit} from '@uitk/react';
import {ThemeProvider} from '@material-ui/core/styles';
import {MsalProvider} from '@azure/msal-react';
import {AppInsightsContext} from '@microsoft/applicationinsights-react-js';
import {reactPlugin} from 'analytics';
import {msalInstance} from 'auth';
import {QueryCache, QueryClient, QueryClientProvider} from 'react-query';
import {muiTheme} from 'styles';

const queryCache = new QueryCache();
const queryClient = new QueryClient({
  queryCache,
  defaultOptions: {
    queries: {
      useErrorBoundary: true,
      retry: 1,
    },
    mutations: {
      useErrorBoundary: true,
    },
  },
});

ReactDOM.render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <QueryClientProvider client={queryClient}>
        <AppInsightsContext.Provider value={reactPlugin}>
          <Toolkit spacing grid>
            <ThemeProvider theme={muiTheme}>
              <App />
            </ThemeProvider>
          </Toolkit>
        </AppInsightsContext.Provider>
      </QueryClientProvider>
    </MsalProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
