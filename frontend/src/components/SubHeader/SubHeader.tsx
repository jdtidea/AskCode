import './SubHeader.scss';
import {useCallback} from 'react';
import {useUser} from 'auth';
import {Button} from '@uitk/react';

export function SubHeader() {
  const {instance, activeAccount} = useUser();
  const handleSignOut = useCallback(() => {
    instance.logout();
  }, [instance]);

  return (
    <div className="sub-header">
      <div className="left-container">
        <div className="round-icon">EI</div>
        <div>
          <h3 style={{margin: '0', textAlign: 'initial'}}>
            {activeAccount?.name}
          </h3>
        </div>
      </div>
      <div className="right-container">
        <Button variant="ghost-alternative" onClick={handleSignOut}>
          Sign Out
        </Button>
      </div>
    </div>
  );
}
