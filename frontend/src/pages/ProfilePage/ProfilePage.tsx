import './ProfilePage.scss';
import {BreadCrumbs, Description, SubHeader} from 'components';
import {Grid} from 'layout';

export function ProfilePage() {
  return (
    <div className="entire-user-profile">
      <BreadCrumbs />
      <h1 className="user-profile-header">User Profile</h1>
      <SubHeader />
      <Grid>
        <div className="row">
          <div className="col-12">
            <Description />
          </div>
        </div>
      </Grid>
    </div>
  );
}
