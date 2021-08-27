import {
  ApplicationInsights,
  DistributedTracingModes,
} from '@microsoft/applicationinsights-web';
import {ReactPlugin} from '@microsoft/applicationinsights-react-js';
import {history} from 'helpers';
import {config} from 'config';

const reactPlugin = new ReactPlugin();
const appInsights = new ApplicationInsights({
  config: {
    instrumentationKey: config.appInsightsKey,
    extensions: [reactPlugin],
    extensionConfig: {
      [reactPlugin.identifier]: {history: history},
    },
    disableFetchTracking: false,
    enableRequestHeaderTracking: true,
    enableResponseHeaderTracking: true,
    distributedTracingMode: DistributedTracingModes.AI_AND_W3C,
  },
});
appInsights.loadAppInsights();
export {reactPlugin, appInsights};
