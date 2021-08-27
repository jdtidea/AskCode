import {useMemo} from 'react';
import {
  Header as UITKHeader,
  NavigationConfig,
  getNativeProps,
  anchorProperties,
} from '@uitk/react';
import {Logo} from './Logo';
import {Link} from 'react-router-dom';
import {useUser} from 'auth';
import {useCurrentRoute} from 'hooks';
import {createGlobalStyle} from 'styled-components';

const HeaderStyle = createGlobalStyle`
  .header {
    display: flex;
    align-items: center;
  }
`;

// define our custom link so client side routing works
const Route = (item: Record<string, any>) => {
  const {children, url} = item;

  // get the native anchor attributes of the link item so we can prop spread
  const anchorProps = getNativeProps(item, anchorProperties);

  return (
    <Link to={url} {...anchorProps}>
      {children}
    </Link>
  );
};

export function Header() {
  const {instance, isAuthenticated, displayName} = useUser();

  const globalNavigation: NavigationConfig = useMemo(() => {
    return isAuthenticated
      ? {
          linkAs: Route,
          links: [
            {
              label: displayName,
              links: [
                {label: 'Home', url: '/'},
                {label: 'Profile', url: '/profile'},
                {
                  label: 'Sign Out',
                  onClick: () => instance.logout(),
                },
              ],
            },
          ],
        }
      : {
          links: [
            {
              label: 'Login',
              onClick: async () => await instance.loginRedirect(),
            },
          ],
        };
  }, [displayName, instance, isAuthenticated]);

  return (
    <>
      <HeaderStyle />
      <UITKHeader
        logoContent={<Logo />}
        globalNavigation={globalNavigation}
        useLocation={useCurrentRoute}
        skipLink={{id: 'main'}}
        className="header"
      />
    </>
  );
}
