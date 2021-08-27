import {
  useAppInsightsContext,
  useTrackEvent,
} from '@microsoft/applicationinsights-react-js';

export function useAnalytics(eventName: string) {
  const insights = useAppInsightsContext();
  const trackEvent = useTrackEvent(insights, eventName, {});

  return trackEvent;
}
