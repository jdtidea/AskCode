import {useEffect} from 'react';
import {useMsal, useIsAuthenticated} from '@azure/msal-react';

export function useUser() {
  const {inProgress, instance} = useMsal();
  const accounts = instance.getAllAccounts();
  const isAuthenticated = useIsAuthenticated();
  const activeAccount = instance.getActiveAccount();
  const claims = activeAccount?.idTokenClaims ?? {};
  const displayName = activeAccount?.name ?? activeAccount?.username ?? '';
  const userId = claims['sub'];
  const dob = claims['extension_DateofBirth'];
  const memberId = claims['extension_MemberID'];
  const groupNumber = claims['extension_GroupNumber'];

  useEffect(() => {
    if (!activeAccount && accounts.length > 0) {
      instance.setActiveAccount(accounts[0]);
    }
  }, [activeAccount, accounts, instance]);

  return {
    instance,
    userId,
    inProgress,
    isAuthenticated,
    activeAccount,
    displayName,
    dob,
    memberId,
    groupNumber,
  };
}
