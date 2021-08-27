// This hook is no longer currently used
import {useCallback, useMemo} from 'react';
import {
  SelfCare,
  Provider,
  Claim,
  Pharmacy,
  DollarSignHollow,
  InfoFilled,
  Guidelines,
} from '@uitk/react-icons';
import {Domains} from 'types';
import {theme} from 'styles';
import {IconWrapper, Button} from 'components';
import {useAnalytics, TrackingEventsEnum} from 'analytics';

const iconProps = {
  customSize: '2rem',
  fill: theme.colorBackgroundBrand,
};

export function useDomain(domain: Domains | undefined) {
  const trackClick = useAnalytics(TrackingEventsEnum.CONTENT_CLICK);

  const Icon = useMemo(() => {
    let SelectedIcon = InfoFilled;
    switch (domain) {
      case Domains.benefits:
        SelectedIcon = SelfCare;
        break;
      case Domains.claims:
        SelectedIcon = Claim;
        break;
      case Domains.provider:
        SelectedIcon = Provider;
        break;
      case Domains.pharmacy:
        SelectedIcon = Pharmacy;
        break;
      case Domains.financial:
        SelectedIcon = DollarSignHollow;
        break;
      case Domains.healthLibrary:
        SelectedIcon = Guidelines;
        break;
    }

    return (
      <IconWrapper>
        <SelectedIcon {...iconProps} />
      </IconWrapper>
    );
  }, [domain]);

  const clickHandler = useCallback(
    (domain: Domains | undefined, external: boolean, e: any) => {
      e.preventDefault();
      trackClick({
        domain,
      });
      window.open(e.currentTarget.href, external ? '_blank' : '_self');
    },
    [trackClick],
  );

  const markdownComponents = useMemo(() => {
    switch (domain) {
      case Domains.healthLibrary:
        return {
          a: ({...props}) => (
            <Button.Link
              bold
              onClick={(e) => {
                clickHandler(domain, props.external, e);
              }}
              {...props}
            />
          ),
        };
      default:
        return {
          a: ({...props}) => (
            <Button.Link
              onClick={(e) => {
                clickHandler(domain, props.external, e);
              }}
              {...props}
            />
          ),
        };
    }
  }, [domain, clickHandler]);

  return {Icon, markdownComponents};
}
