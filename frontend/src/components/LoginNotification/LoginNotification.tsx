import './LoginNotification.scss';
import {useMsal, useIsAuthenticated} from '@azure/msal-react';
import {Notification} from '@uitk/react';
import styled from 'styled-components';
import {theme} from 'styles';
import {HealthDataExchange as Icon1} from '@uitk/react-icons';
import {MemberLink} from 'components';
import {useUser} from 'auth';
import {HelperText, Label, TextInput, Button} from '@uitk/react';

const HealthDataExchange = styled(Icon1)`
  height: ${theme.spacingM};
  width: ${theme.spacingM};
`;

export function LoginNotification() {
  const {isAuthenticated, memberId} = useUser();
  const {instance} = useMsal();
  const activeAccount: any = instance.getActiveAccount();
  if (!activeAccount?.idTokenClaims?.extension_MemberID) {
    if (isAuthenticated) {
      return (
        <>
          <Notification
            className="mv-m after-login-notification"
            variant={'success'}
            id={'notification-info'}
            dismissable="true"
            buttonText="Dismiss"
            icon={<HealthDataExchange />}>
            <MemberLink />
          </Notification>
        </>
      );
    } else {
      return isAuthenticated ? null : (
        <Notification
          className="mv-m"
          variant={'info'}
          id="notification-info"
          dismissable="true"
          buttonText="X">
          <span>
            Not what you were looking for? <b>Login with MSID</b> for better
            answers!
            <Button
              onPress={() => instance.loginRedirect()}
              className="login-btn">
              <span>Login</span>
            </Button>
          </span>
        </Notification>
      );
    }
  } else {
    return null;
  }
}
