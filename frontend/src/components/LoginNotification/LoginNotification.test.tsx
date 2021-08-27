import {render} from 'test';
import {LoginNotification} from './LoginNotification';

describe(LoginNotification.name, () => {
  it('Should render', () => {
    const {getByText} = render(<LoginNotification />);
    expect(getByText('Login')).toBeTruthy();
  });
});
