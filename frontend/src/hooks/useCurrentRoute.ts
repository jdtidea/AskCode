import {useLocation} from 'react-router-dom';

export function useCurrentRoute() {
  const {pathname: route} = useLocation();

  return route;
}
